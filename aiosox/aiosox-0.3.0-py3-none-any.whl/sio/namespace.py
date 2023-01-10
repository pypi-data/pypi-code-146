from typing import TYPE_CHECKING, Any, Callable, List, Optional, Type, TypeVar, Union

import socketio
from pydantic import BaseModel

from ..utils import to_camel, to_no_underscore, Func
from .actors import SIOEmitterMeta, SIOHandler, SIOJsonEmitter
from .enums import SioAuth
from importlib import import_module


T = TypeVar("T", bound=BaseModel)

Y = TypeVar("Y", bound=BaseModel)


def load_handler(handler_id: str) -> Callable:
    *module_path_elements, object_name = handler_id.split(".")
    module = import_module(".".join(module_path_elements))

    return getattr(module, object_name)


class RequestValidationError(Exception):
    pass


class ResponseValidationError(Exception):
    pass


def _generate_operation_id_for_method(event_name: str, namespace: str) -> str | None:
    """method to generate a unique id for each method event of the namspace"""

    return to_camel(
        f"{namespace[1:].capitalize()}{to_no_underscore(event_name.capitalize()).replace(' ','')}"
    )


class SioNamespace(socketio.AsyncNamespace):
    def __init__(
        self,
        namespace: str,
    ) -> None:
        self._handlers: List[SIOHandler] = []
        self._emitters: List[SIOJsonEmitter] = []

        self._namespace_name = namespace

        super(socketio.Namespace, self).__init__(namespace=namespace)

    def on(
        self,
        event: str,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
        message_description: str | None = None,
        payload_model: Type[BaseModel] | Union[Type[BaseModel], Any] | None = None,
        response_model: Type[BaseModel]
        | Union[Type[BaseModel], Any]
        | List[Type[BaseModel]]
        | None = None,
        media_type: str = "application/json",
        auth: SioAuth = SioAuth.no_auth,
    ):
        def decorator(
            fn: Func,
        ):

            self._handlers.append(
                SIOHandler(
                    name=_generate_operation_id_for_method(
                        namespace=self._namespace_name, event_name=fn.__name__
                    ),
                    event=event,
                    title=title,
                    summary=summary,
                    description=description,
                    model=payload_model,
                    response_model=response_model,
                    media_type=media_type,
                    message_description=message_description,
                    namespace=self._namespace_name[1:],
                    auth=auth,
                    fn=fn,
                )
            )

        return decorator

    def create_emitter(
        self,
        event: str,
        model: Type[List[T]] | Type[Union[Type[T], Type]] | Type[T],
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
        message_description: str | None = None,
        media_type: str = "application/json",
        include: Optional[Any] = None,
        exclude: Optional[Any] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        auth: SioAuth = SioAuth.no_auth,
    ):

        emitter = SIOJsonEmitter(
            model=model,
            meta=SIOEmitterMeta(
                event=to_camel(event),
                title=title,
                summary=summary,
                description=description,
                model=model,
                media_type=media_type,
                message_description=message_description,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                namespace=self._namespace_name[1:],
                auth=auth,
            ),
        )
        self._emitters.append(emitter)
        return emitter
