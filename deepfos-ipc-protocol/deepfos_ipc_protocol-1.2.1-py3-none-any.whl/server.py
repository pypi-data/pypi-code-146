import asyncio
import typing

from loguru import logger

from dip.proto import Protocol, SetConnectionIdProto, read_uint32


class Stream:
    def __init__(self):
        self._pending = None
        self._ready = []

    def new_segmant(self, buf):
        buf_len = len(buf)
        expect_len = read_uint32(buf[1:5])[0] + 5
        if expect_len == buf_len:
            self._ready.append(buf)
            self._pending = None
        elif expect_len > buf_len:
            self._pending = buf
        else:
            self._ready.append(buf[:expect_len])
            self._pending = buf[expect_len:]

    def amend_pending(self, buf):
        new_buf = self._pending + buf
        self.new_segmant(new_buf)

    def feed_data(self, buf: bytes):
        if not self._pending:
            self.new_segmant(buf)
        else:
            self.amend_pending(buf)

    def iter_data(self):
        while self._ready:
            yield self._ready.pop(0)


# -----------------------------------------------------------------------------
# typing

T = typing.TypeVar('T', bound='DeepfosIPCProtocol')
Callback_T = typing.Callable[
    [T, str, typing.Any],
    typing.Any
]


class DeepfosIPCProtocol(asyncio.Protocol):
    def __init__(self: T, callback: Callback_T = None, **kwargs) -> None:
        self.callback = callback
        self.transport = None
        self.id = None
        self._stream = Stream()

    def abort(self):
        self._stream = Stream()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self._stream.feed_data(data)

        errors = []
        data_processed = False

        for buf in self._stream.iter_data():
            data_processed = True
            try:
                self.process_message(buf)
            except Exception as e:
                self.abort()
                logger.error(e)
                errors.append(repr(e).encode("utf8"))

        if data_processed:
            if errors:
                self.transport.write(b''.join(errors))
            else:
                self.transport.write(b"ok")

    def process_message(self, data):
        mtype = data[0]
        proto = Protocol.dispatch(mtype)
        decoded = proto.decode(data)
        logger.opt(lazy=True).debug("Receive data: {data!r}", data=lambda: decoded)
        if proto is SetConnectionIdProto:
            self.id = decoded
        elif self.callback is not None:
            self.callback(self.id, chr(mtype), decoded)

    def connection_lost(self, error):
        if error:
            logger.error('SERVER ERROR: {}'.format(error))
        else:
            logger.debug('connection closed.')
        super().connection_lost(error)
        self.transport = None


class Server:
    """
    启动Server服务.
    """
    def __init__(
        self,
        sockname: str,
        callback: Callback_T = None,
        loop: asyncio.BaseEventLoop = None,
        **kwrags
    ) -> None:
        self.sockname = sockname
        self.callback = callback
        self.waiter = None
        self.server = None
        self.kwargs = kwrags
        self._loop = loop or asyncio.get_running_loop()

    async def _create_server(self):
        srv = await self._loop.create_unix_server(
            lambda: DeepfosIPCProtocol(self.callback, **self.kwargs),
            self.sockname,
        )
        return srv

    async def start(self):
        self.server = await self._create_server()
        return self.server

    async def serve_forever(self):
        self.waiter = self._loop.create_future()
        srv = await self.start()
        async with srv:
            await srv.start_serving()
            logger.info(f'Start serving at {self.sockname}.')
            await self.waiter
        logger.info('Server stopped.')

    def stop(self):
        if self.waiter is not None:
            self.waiter.set_result(None)
            self.waiter = None
