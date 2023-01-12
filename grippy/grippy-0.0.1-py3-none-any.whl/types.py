from typing import Callable, ParamSpec, Protocol, TypeVar

from grippy.proto_message import ProtoMessage

T = TypeVar('T')
P = ParamSpec('P')


class RPC(Protocol[P, T]):
    _request_message: ProtoMessage
    _return_message: ProtoMessage

    __call__: Callable[P, T]
