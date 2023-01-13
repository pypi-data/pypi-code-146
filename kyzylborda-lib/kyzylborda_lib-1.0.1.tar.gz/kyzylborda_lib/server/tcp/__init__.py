from __future__ import annotations

from typing import Awaitable, Callable, TYPE_CHECKING

from .. import handlers
from .bridge import bridge_connections_unidirectional, bridge_connections
from .connection import Connection, connect, parse_address


__all__ = ("HandlerType", "listen", "bridge_connections_unidirectional", "bridge_connections", "parse_address", "Connection", "connect")


if TYPE_CHECKING:
    HandlerType = Callable[[Connection], Awaitable[Connection | str | None]]
else:
    HandlerType = None


def listen(handler: HandlerType):
    if handlers._global_handler is not None:
        raise ValueError("Cannot @*.listen twice")

    async def wrapped(address: str):
        from .reverse_proxy import ReverseProxy
        await ReverseProxy(handler).listen(address)

    handlers._global_handler = wrapped

    return handler
