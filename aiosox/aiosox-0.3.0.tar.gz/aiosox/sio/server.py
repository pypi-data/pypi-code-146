from types import UnionType
from typing import Dict, List, Type, TypeVar, Union, get_origin

import socketio
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.schema import schema

from aiosox import asyncapi

from ..asyncapi.bindings import (
    WebSocketsOperationBinding,
)
from ..asyncapi.message import ApiMessage
from ..asyncapi.operation import OperationBindings
from ..utils import to_camel, to_no_underscore
from .actors import SIOHandler, SIOJsonEmitter
from .client_manager import KafkaBackend, SocketIoClientManager
from .enums import SioAuth
from .schemas import SioError

T = TypeVar("T", bound=BaseModel)


def resolve_model(
    model: Type[BaseModel] | Union[Type[BaseModel], Type[BaseModel]] | List[Type[BaseModel]]
):
    """method to determine the schema model,type and ref"""
    origin = get_origin(model)
    # standard
    if origin is None:
        return model
    # union
    if origin == Union or origin == UnionType:
        return [resolve_model(m) for m in list(model.__args__)]

    # list
    elif issubclass(origin, list):
        return resolve_model(list(model.__args__)[0])


def resolve_api_message(actor: SIOJsonEmitter | SIOHandler) -> ApiMessage:
    """method to determine api message from a handler/emmit"""

    # handler
    if issubclass(type(actor), SIOHandler):

        name = actor.event
        content_type = actor.media_type
        payload = {}
        # payload model
        if actor.model is not None:
            payload = {"oneOf": []}
            resolved_model = resolve_model(actor.model)
            # union
            if issubclass(type(resolved_model), list):
                payload = {
                    "oneOf": [
                        {"$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{m.__name__}"}
                        for m in resolved_model
                    ]
                }
            else:
                model_origin = None
                model_origin = get_origin(actor.model)
                # list
                if model_origin and issubclass(model_origin, list):
                    payload["oneOf"].append(
                        {
                            "type": "array",
                            "items": {
                                "$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{actor.model.__args__[0].__name__}"
                            },
                        }
                    )
                # single model
                else:
                    payload["oneOf"].append(
                        {"$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{actor.model.__name__}"}
                    )
        # response model
        x_response = {"oneOf": []}
        if actor.response_model is not None:
            resolved_response_model = resolve_model(actor.response_model)
            # union
            if issubclass(type(resolved_response_model), list):
                x_response = {
                    "oneOf": [
                        {"$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{m.__name__}"}
                        for m in resolved_response_model
                    ]
                }
            else:
                model_origin = None
                model_origin = get_origin(actor.response_model)
                # list
                if model_origin and issubclass(model_origin, list):
                    x_response["oneOf"].append(
                        {
                            "type": "array",
                            "items": {
                                "$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{actor.response_model.__args__[0].__name__}"
                            },
                        }
                    )
                # single model
                else:
                    x_response["oneOf"].append(
                        {"$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{actor.response_model.__name__}"}
                    )

        description = actor.message_description
        x_response["oneOf"].append({"$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{SioError.__name__}"})
    # emmiter
    elif issubclass(type(actor), SIOJsonEmitter):
        name = actor._meta.event
        payload = {"oneOf": []}
        description = None
        content_type = actor._meta.media_type
        x_response = None
        if actor._model is not None:
            resolved_response_model = resolve_model(actor._model)

            # union
            if issubclass(type(resolved_response_model), list):
                payload = {
                    "oneOf": [
                        {"$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{m.__name__}"}
                        for m in resolved_response_model
                    ]
                }
            else:
                model_origin = None
                model_origin = get_origin(actor._model)
                # list
                if model_origin and issubclass(model_origin, list):
                    payload["oneOf"].append(
                        {
                            "type": "array",
                            "items": {
                                "$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{actor._model.__args__[0].__name__}"
                            },
                        }
                    )
                # single model
                else:
                    payload["oneOf"].append(
                        {"$ref": f"{asyncapi.SCHEMA_REF_PREFIX}{actor._model.__name__}"}
                    )

        description = actor._meta.message_description

    else:
        raise Exception("message for actor not supported")
    return asyncapi.ApiMessage(  # type:ignore
        name=name,
        contentType=content_type,
        description=description,
        payload=payload,
        x_response=x_response,  # type:ignore
    )


def resolve_api_opperation_binding(auth: SioAuth) -> OperationBindings:
    """method to resolve which auth to be used for the method"""

    if str(auth) == SioAuth.token:
        return OperationBindings(
            socketio=WebSocketsOperationBinding(
                headers={"$ref": "#/components/securitySchemes/apiKey"}
            )
        )

    elif auth == SioAuth.jwt:
        return OperationBindings(
            socketio=WebSocketsOperationBinding(
                headers={"$ref": "#/components/securitySchemes/bearer"}
            )
        )
    else:
        return OperationBindings(socketio=WebSocketsOperationBinding())


class SocketIoServer:
    """socketio server"""

    def __init__(
        self,
        app: FastAPI,
        kafka_url: str,
    ) -> None:

        group_id = app.title.lower() if app.title else "aiosox"
        kafka_backend: KafkaBackend = KafkaBackend(kafka_url, group_id=group_id)
        self.client_manager: SocketIoClientManager = SocketIoClientManager(
            kafka_backend=kafka_backend
        )

        self._sio: socketio.AsyncServer = socketio.AsyncServer(
            async_mode="asgi",
            cors_allowed_origins="*",
            cors_credentials=True,
            SameSite=None,
            monitor_clients=True,
            client_manager=self.client_manager,
        )

        self._asgiapp: socketio.ASGIApp = socketio.ASGIApp(
            socketio_server=self._sio,
        )
        self._app: FastAPI = app
        self.info = asyncapi.ApiInfo(
            title=self._app.title,
            version=self._app.openapi_version,
            description=self._app.description,
        )
        self.servers = {
            "dev": asyncapi.ApiServer(
                url="localhost:8000",
                protocol=asyncapi.ApiServerProtocol.SIO,
                security=[{"apiKey": []}, {"bearer": []}],  # type:ignore
            )
        }

        self.tags = []

        self.asyncapi_schema: asyncapi.AsyncAPI | None = None
        self._app.get(
            "/asyncapi.json",
            include_in_schema=False,
            response_model=asyncapi.AsyncAPI,
            response_model_exclude_none=True,
        )(self._asyncapi)

        self._app.mount("/ws", self._asgiapp)

        self._handlers: List[SIOHandler] = []
        self._emitters: List[SIOJsonEmitter] = []

    def _generate_operation_id_for_method(self, event_name: str, namespace: str) -> str | None:
        """method to generate a unique id for each method event of the namspace"""

        return to_camel(
            f"{namespace[1:].capitalize()}{to_no_underscore(event_name.capitalize()).replace(' ','')}"
        )

    def _asyncapi(self) -> "asyncapi.AsyncAPI":
        if not self.asyncapi_schema:

            models_to_resolve = [SioError]
            for namespace, namespace_handler in self._sio.namespace_handlers.items():

                if namespace_handler._handlers or namespace_handler._emitters:
                    models_to_resolve += (
                        [
                            handler.model
                            for handler in namespace_handler._handlers
                            if namespace_handler._handlers and handler.model is not None
                        ]
                        + [
                            emitter._model
                            for emitter in namespace_handler._emitters
                            if namespace_handler._emitters and emitter._model is not None
                        ]
                        + [
                            handler.response_model
                            for handler in self._handlers
                            if handler.response_model is not None
                        ]
                    )

            resolved_models = []
            for m in models_to_resolve:
                resolved = resolve_model(m)
                if type(resolved) is list and not type(resolved) == Type[BaseModel]:
                    [resolved_models.append(r) for r in resolved]

                else:
                    resolved_models.append(resolved)

            used_models = resolved_models
            components = self.get_components(used_models)
            self.asyncapi_schema = asyncapi.AsyncAPI(
                servers=self.servers,
                tags=self.tags,
                info=self.info,
                components=components,
                id="urn:com:" + "_".join(self._app.title.lower().split(" ")),
                channels=self.get_channels(),
            )

        return self.asyncapi_schema

    def get_components(self, used_models: List[Type[BaseModel]]):
        return asyncapi.ApiComponents(
            schemas=schema(used_models, ref_prefix=asyncapi.SCHEMA_REF_PREFIX)["definitions"],
            security_schemes={
                "apiKey": asyncapi.ApiSecurityScheme(  # type:ignore
                    param_type=asyncapi.ApiSecuritySchemesType.HTTP_API_KEY,  # type:ignore
                    name="token",
                    param_in=asyncapi.ApiSecuritySchemeLocation.header,  # type:ignore
                ),
                "bearer": asyncapi.ApiSecurityScheme(  # type:ignore
                    param_type=asyncapi.ApiSecuritySchemesType.HTTP,  # type:ignore
                    scheme="bearer",
                    bearerFormat="Bearer",
                ),
            },
        )

    def get_channels(
        self,
    ) -> Dict[str, asyncapi.ApiChannel]:

        return {
            f"{handler.namespace}/"
            + handler.event: asyncapi.ApiChannel(  # type:ignore
                publish=asyncapi.ApiOperation(
                    operationId=handler.name,
                    summary=handler.summary,
                    description=handler.description,
                    message=resolve_api_message(handler),
                    bindings=resolve_api_opperation_binding(handler.auth),
                ),
            )
            for handler in self._handlers
        } | {
            f"{emitter._meta.namespace}/"
            + emitter._meta.event: asyncapi.ApiChannel(  # type:ignore
                subscribe=asyncapi.ApiOperation(
                    operationId=self._generate_operation_id_for_method(
                        namespace=emitter._meta.namespace, event_name=emitter._meta.event
                    ),
                    summary=emitter._meta.summary,
                    description=emitter._meta.description,
                    message=resolve_api_message(emitter),
                    bindings=resolve_api_opperation_binding(emitter._meta.auth),
                ),
            )
            for emitter in self._emitters
        }

    async def _register_all_handlers(self):
        """method to loop through all the namespaces and extract handlers"""
        for ns, ns_handler in self._sio.namespace_handlers.items():

            for handler in ns_handler._handlers:
                self._sio.on(event=handler.event, handler=handler.fn, namespace=ns)
                self._handlers.append(handler)
            for emitter in ns_handler._emitters:
                emitter._sio = self._sio
                self._emitters.append(emitter)

    async def start(self):
        """on init"""

        await self._register_all_handlers()
        self.asyncapi_schema = self._asyncapi()
        await self.client_manager.on_start()

    async def shutdown(self):
        """on shutdown"""
        await self.client_manager.on_shutdown()

    def is_asyncio_based(self) -> bool:
        return True

    @property
    def attach(self):
        return self._sio.attach

    @property
    def emit(self):
        return self._sio.emit

    @property
    def send(self):
        return self._sio.send

    @property
    def call(self):
        return self._sio.call

    @property
    def close_room(self):
        return self._sio.close_room

    @property
    def get_session(self):
        return self._sio.get_session

    @property
    def save_session(self):
        return self._sio.save_session

    @property
    def session(self):
        return self._sio.session

    @property
    def disconnect(self):
        return self._sio.disconnect

    @property
    def handle_request(self):
        return self._sio.handle_request

    @property
    def start_background_task(self):
        return self._sio.start_background_task

    @property
    def sleep(self):
        return self._sio.sleep

    @property
    def enter_room(self):
        return self._sio.enter_room

    @property
    def leave_room(self):
        return self._sio.leave_room

    @property
    def register_namespace(self):

        return self._sio.register_namespace
