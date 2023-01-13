import asyncio
import re

from .protocol_commons import MalformedHeaderError
from .request import Request, RequestHeader
from .response import Response, ResponseHeader
from .. import tcp


__all__ = ("request",)


bg_tasks = set()


async def read_http_header(connection: tcp.Connection) -> bytes:
    MAX_HEADER_SIZE = 16384

    raw_header = bytearray()
    while len(raw_header) < MAX_HEADER_SIZE:
        checked_prefix = max(0, len(raw_header) - 3)
        block = await connection.read(MAX_HEADER_SIZE - len(raw_header))
        if block == b"":
            raise MalformedHeaderError("Connection terminated too early")
        raw_header += block
        match = re.search(rb"\r?\n\r?\n", raw_header[checked_prefix:])
        if match:
            idx = match.end() + checked_prefix
            connection.unread(raw_header[idx:])
            return raw_header[:idx]

    raise MalformedHeaderError("The header is too long")


async def request(request: Request, address: str) -> Response:
    connection = await tcp.connect(address)
    await connection.writeall(request.raw_header)

    if isinstance(request.data, tcp.Connection):
        task = asyncio.create_task(tcp.bridge_connections_unidirectional(request.data, connection))
    elif request.data:
        task = asyncio.create_task(connection.writeall(request.data))

    bg_tasks.add(task)
    task.add_done_callback(lambda t: bg_tasks.remove(task))

    raw_header = await read_http_header(connection)
    return Response(ResponseHeader(raw_header), connection)
