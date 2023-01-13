from __future__ import annotations

from functools import partial
import re
import traceback
from typing import Awaitable, Callable, Optional, TYPE_CHECKING

from .connection import request, read_http_header
from .pre_handler import pre_handler
from .protocol_commons import MalformedHeaderError
from .request import Request, RequestHeader
from .response import Response, ResponseHeader, respond
from ...sandbox import Box, stop_box
from .. import tcp


__all__ = (
    "HandlerType",
    "listen",
    "MalformedHeaderError",
    "Request", "RequestHeader",
    "Response", "ResponseHeader", "respond",
    "request"
)


if TYPE_CHECKING:
    HandlerType = Callable[[Request], Awaitable[Response | tcp.Connection | str | None]]
else:
    HandlerType = None


def listen(handler: Optional[HandlerType]=None, *, allow_keep_alive: bool=False):
    if handler is None:
        return partial(listen, allow_keep_alive=allow_keep_alive)

    async def wrapped(connection: tcp.Connection) -> tcp.Connection | str | None:
        try:
            raw_header = await read_http_header(connection)
        except MalformedHeaderError:
            return None

        req = Request(RequestHeader(raw_header), connection)

        if not allow_keep_alive:
            del req.headers["Connection"]
            req.headers["Connection"] = "close"

        try:
            ret = await pre_handler(req)
            if ret is None:
                ret = await handler(req)
        except Exception:
            traceback.print_exc()
            ret = respond(500)

        if ret is None:
            return None

        if isinstance(ret, Box):
            box = ret
            with box.borrow():  # don't let the box be deleted while we are using it
                address = box.get_socket_address()
                if address is None:
                    raise ValueError(f"Box {box} does not bind to a socket--check kyzylborda-box.yml.")
                ret = await request(req, address)
                ret.data.keep_object_alive(box.borrow())

        if isinstance(ret, str):
            ret = await request(req, ret)

        if isinstance(ret, Response):
            if not allow_keep_alive:
                del ret.headers["Connection"]
                ret.headers["Connection"] = "close"
            await connection.writeall(ret.raw_header)
            if isinstance(ret.data, bytes):
                connection.write(ret.data)
                return None
            ret = ret.data

        return ret

    tcp.listen(wrapped)
