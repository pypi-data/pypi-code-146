import asyncio
import socket
import struct
from typing import Any, Awaitable, Callable, Iterable

from ... import libc


__all__ = ("parse_address", "Connection", "connect")


def parse_address(address: str):
    if address.startswith("netns:"):
        # netns:<path>:<address>
        _, path, address = address.split(":", 2)
        return "netns", (path, address)
    elif address.startswith("unix:"):
        # unix:/path/to/socket
        return "unix", (address[5:],)
    else:
        # localhost:80
        host, port = address.split(":")
        return "tcp", (host, int(port))


class Connection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self._objects_to_keep_alive = []

    def keep_object_alive(self, obj):
        self._objects_to_keep_alive.append(obj.__enter__())

    async def __aenter__(self) -> "Connection":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                await self.drain()
                self.write_eof()
                self.close()
            else:
                self.reset()
        except IOError as e:
            pass
        finally:
            for obj in self._objects_to_keep_alive:
                obj.__exit__(exc_type, exc, tb)

    def unread(self, data: bytes | bytearray):
        self.reader._buffer = data + self.reader._buffer

    async def read(self, n: int=-1) -> bytes:
        return await self.reader.read(n)
    async def readline(self) -> bytes:
        return await self.reader.readline()
    async def readexactly(self, n: int) -> bytes:
        return await self.reader.readexactly(n)
    async def readuntil(self, separator: bytes) -> bytes:
        return await self.reader.readuntil(separator)

    def write(self, data: bytes):
        self.writer.write(data)
    def writelines(self, data: Iterable[bytes]):
        self.writer.writelines(data)
    async def drain(self):
        await self.writer.drain()
    def write_eof(self):
        self.writer.write_eof()
    async def writeall(self, data: bytes):
        self.write(data)
        await self.drain()

    def close(self):
        self.writer.close()

    def reset(self):
        self.writer._transport._sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
        self.close()


def _create_socket(address: str) -> tuple[socket.socket, Any, Callable[..., Awaitable[Any]]]:
    proto, addr = parse_address(address)

    if proto == "netns":
        with open("/proc/self/ns/net", "rb") as f_self:
            path, address = addr
            with open(path, "rb") as f_other:
                if libc.libc.setns(f_other.fileno(), 0) == -1:
                    err = libc.get_errno()
                    raise OSError(err, libc.strerror(err), "setns failed")

            try:
                return _create_socket(address)
            finally:
                if libc.libc.setns(f_self.fileno(), 0) == -1:
                    err = libc.get_errno()
                    raise OSError(err, libc.strerror(err), "setns failed")

    if proto == "unix":
        return socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0), addr[0], asyncio.open_unix_connection

    if proto == "tcp":
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0), addr, asyncio.open_connection

    raise ValueError(f"Unsupported protocol {proto}")


async def connect(address: str) -> Connection:
    sock, addr, do_connect = _create_socket(address)

    loop = asyncio.get_running_loop()

    try:
        sock.setblocking(False)
        await loop.sock_connect(sock, addr)
    except Exception:
        sock.close()
        raise

    reader, writer = await do_connect(sock=sock, limit=4 * 1024)
    return Connection(reader, writer)
