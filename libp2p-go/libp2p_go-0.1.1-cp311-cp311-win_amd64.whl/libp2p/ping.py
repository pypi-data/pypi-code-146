import asyncio
import dataclasses
from ctypes import *
from libp2p import Host
from libp2p.utils import *


lib = load_library()


@dataclasses.dataclass
class PingResult:
    rtt: int = dataclasses.field()
    error: str = dataclasses.field(default=None)


class PingChan(SimpleFreeMixin):
    lib.pingChan_delete.argtypes = [c_size_t, ]
    _FREE = lib.pingChan_delete
    lib.pingChan_pop.argtypes = [c_size_t, ]
    lib.pingChan_pop.restype = MsgpackBody
    _POP = lib.pingChan_pop

    def __init__(self, handle: int, loop: asyncio.AbstractEventLoop):
        self.handle = handle
        self.loop = loop

    def __aiter__(self):
        return self

    async def __anext__(self):
        fut = c_wrap(self.loop, self._POP, self.handle)
        result: MsgpackBody = await fut
        if result.integers:
            rtt = result.integers.first()
        else:
            raise StopAsyncIteration
        error = result.strings.first() if result.strings else None
        return PingResult(rtt=rtt, error=error)


class PingService(SimpleFreeMixin):
    lib.ping_new.argtypes = [c_size_t, ]
    lib.ping_new.restype = c_size_t
    _INIT = lib.ping_new
    lib.ping_delete.argtypes = [c_size_t, ]
    _FREE = lib.ping_delete
    lib.ping_ping.argtypes = [c_size_t, GoString, ]
    lib.ping_ping.restype = c_size_t
    _PING = lib.ping_ping

    def __init__(self, host: Host):
        handle = self._INIT(host.handle)
        self.handle = handle
        self.loop = host.io_loop

    def ping(self, peer_id: str) -> PingChan:
        ping_chan = self._PING(self.handle, GoString.new(peer_id))
        return PingChan(ping_chan, loop=self.loop)


__all__ = ['PingService', 'PingChan', 'PingResult', ]
