from typing import Any, Callable, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from socketio import AsyncServer

from .enums import SioAuth

from ..utils import BaseModel
from .schemas import SioError

T = TypeVar("T", bound=BaseModel)


class SIOActorMeta(BaseModel):
    event: str
    title: str | None
    summary: str | None
    description: str | None
    model: Type[BaseModel] | Union[Any, Type[BaseModel]] | None = None
    media_type: str
    message_description: str | None
    namespace: str
    auth: SioAuth


class SIOEmitterMeta(SIOActorMeta):

    include: Optional[Any] = None
    exclude: Optional[Any] = None
    by_alias: bool = True
    exclude_unset: bool = False
    exclude_defaults: bool = False
    exclude_none: bool = False


class SIOJsonEmitter(Generic[T]):

    _sio: Optional[AsyncServer] = None

    def __init__(
        self, model: Type[T] | Union[Type[T], Type[T]] | List[Type[T]], meta: SIOEmitterMeta
    ):
        self._meta = meta
        self._model = model

    def get_meta(self):
        return self._meta

    async def emit(self, payload: T, emit_to: List[str], encode_kwargs={}, **kwargs):
        meta_args = self._meta.dict(
            include={
                "include",
                "exclude",
                "by_alias",
                "exclude_unset",
                "exclude_defaults",
                "exclude_none",
            }
        )
        if not self._sio:
            raise RuntimeError("sio not connected to json emmiter")
        await self._sio.emit(
            self._meta.event,
            data=jsonable_encoder(payload, **(meta_args | encode_kwargs)),
            sid=emit_to,
            namespace="/" + self._meta.namespace,
        )


class SIOHandler(SIOActorMeta):
    name: str | None
    response_model: Type[BaseModel] | Union[Any, Type[BaseModel]] | List[
        Type[BaseModel]
    ] | None = None
    fn: Callable
