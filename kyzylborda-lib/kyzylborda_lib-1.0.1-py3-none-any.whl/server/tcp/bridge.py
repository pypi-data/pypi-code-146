import asyncio
import contextlib
import errno
import os
import socket
import traceback

from .connection import Connection
from ... import libc


__all__ = ("Bridge", "bridge_connections_unidirectional", "bridge_connections")


class Bridge:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer

        self._reader_fd = reader._transport._sock_fd
        self._writer_fd = writer._transport._sock_fd

        self._listening_for_read_socket = True
        self._listening_for_write_pipe = True
        self._listening_for_write_socket = True

        self._can_read_socket = False
        self._can_write_pipe = True
        self._can_write_socket = True
        self._current_pipe_size = 0
        self._at_eof = False
        self._done = False

        self._fut = None

        self._r_pipe_fd, self._w_pipe_fd = os.pipe2(os.O_NONBLOCK)


    def close(self):
        os.close(self._r_pipe_fd)
        os.close(self._w_pipe_fd)


    def _on_can_read_socket(self):
        self._can_read_socket = True
        self._update_state()

    def _on_can_write_pipe(self):
        self._can_write_pipe = True
        self._update_state()

    def _on_can_write_socket(self):
        self._can_write_socket = True
        self._update_state()


    def _splice(self, r_fd: int, w_fd: int) -> int:
        while True:
            n_read = libc.libc.splice(r_fd, None, w_fd, None, 1024 * 1024, libc.SPLICE_F_NONBLOCK)
            if n_read > 0:
                return n_read
            if n_read == 0:
                raise EOFError()
            err = libc.get_errno()
            if err == errno.EAGAIN:
                raise BlockingIOError()
            if err == errno.EINTR:
                continue
            raise OSError(err, libc.strerror(err), "splice failed")


    def _update_state(self):
        if self._done:
            return

        if not self._at_eof and self._can_read_socket and self._can_write_pipe:
            try:
                self._current_pipe_size += self._splice(self._reader_fd, self._w_pipe_fd)
                self._can_read_socket = False
                self._can_write_pipe = False
            except (EOFError, ConnectionResetError):
                self._at_eof = True

        try:
            while self._current_pipe_size > 0 and self._can_write_socket:
                self._current_pipe_size -= self._splice(self._r_pipe_fd, self._writer_fd)
        except (BrokenPipeError, ConnectionResetError):
            try:
                self._reader._transport._sock.shutdown(socket.SHUT_RD)
            except IOError:
                pass
            self._done = True
        except BlockingIOError:
            self._can_write_socket = False

        if self._at_eof and self._current_pipe_size == 0:
            self._done = True

        if self._done:
            self._fut.set_result(None)

        self._update_listeners()


    def _update_listeners(self):
        loop = asyncio.get_running_loop()

        if self._can_read_socket == self._listening_for_read_socket:
            if self._can_read_socket:
                loop._remove_reader(self._reader_fd)
            else:
                loop._add_reader(self._reader_fd, self._on_can_read_socket)
        self._listening_for_read_socket = not self._can_read_socket

        if self._can_write_pipe == self._listening_for_write_pipe:
            if self._can_write_pipe:
                loop._remove_writer(self._w_pipe_fd)
            else:
                loop._add_writer(self._w_pipe_fd, self._on_can_write_pipe)
        self._listening_for_write_pipe = not self._can_write_pipe

        if self._can_write_socket == self._listening_for_write_socket:
            if self._can_write_socket:
                loop._remove_writer(self._writer_fd)
            else:
                loop._add_writer(self._writer_fd, self._on_can_write_socket)
        self._listening_for_write_socket = not self._can_write_socket


    async def run(self):
        loop = asyncio.get_running_loop()

        # An internal sendall() method must be used instead of _writer.write() because write() is
        # unavailable when the socket is inhibited, and doing write() before inhibition risks a
        # TOCTOU problem when data becomes available between flushing and inhibition (a case that
        # actually happened for me).
        if self._reader._buffer:
            try:
                # This admittedly depends on implementation details of StreamWriter and StreamReader
                self._writer._transport._sock.sendall(self._reader._buffer)
            except (BrokenPipeError, ConnectionResetError):
                try:
                    self._reader._transport._sock.shutdown(socket.SHUT_RD)
                except IOError:
                    pass
                return

        if not self._reader._eof:
            self._fut = loop.create_future()

            # XXX: This chunk is about as wrong as things get without breaking down completely. I am
            # so damn sorry.
            #
            # At this moment, transports are still attached to the sockets, and we do not want to
            # detach them: if bridge_connections_unidirectional bridges A to B, we still want to
            # allow writing to A and reading from B. However, socket transports are all or none: we
            # can't split then into read-only and write-only parts, disabling one and leaving the
            # other active. So we can't remove the transport in a supported way, but still want to
            # add the readers/writers. The "solution"? Use the private _add*/_remove* methods
            # instead of their public counterparts so that the checks are bypassed.
            #
            # I have not seen problems with this hack so far, though it might break if writes to B
            # are attempted after bridge_connections_unidirectional() notices A EOF'ed and returns.
            loop._add_reader(self._reader_fd, self._on_can_read_socket)
            loop._add_writer(self._w_pipe_fd, self._on_can_write_pipe)
            loop._add_writer(self._writer_fd, self._on_can_write_socket)

            await self._fut

            if self._listening_for_read_socket:
                loop._remove_reader(self._reader_fd)
            if self._listening_for_write_pipe:
                loop._remove_writer(self._w_pipe_fd)
            if self._listening_for_write_socket:
                loop._remove_writer(self._writer_fd)

        try:
            self._writer._transport._sock.shutdown(socket.SHUT_WR)
        except IOError:
            pass


async def bridge_connections_unidirectional(a: Connection, b: Connection):
    with contextlib.closing(Bridge(a.reader, b.writer)) as bridge:
        await bridge.run()


async def bridge_connections(a: Connection, b: Connection):
    await asyncio.gather(bridge_connections_unidirectional(a, b), bridge_connections_unidirectional(b, a))
