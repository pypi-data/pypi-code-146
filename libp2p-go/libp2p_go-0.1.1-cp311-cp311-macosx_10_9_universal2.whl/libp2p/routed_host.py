from ctypes import *
from libp2p.main import Host, Stream
from libp2p.dht import DHT
from libp2p.peer import AddrInfo
from libp2p.utils import *


lib = load_library()


class RoutedHost(Host):
    lib.routedHost_new.argtypes = [c_size_t, c_size_t, ]
    lib.routedHost_new.restype = c_size_t
    _INIT = lib.routedHost_new
    lib.routedHost_delete.argtypes = [c_size_t, ]
    _FREE = lib.routedHost_delete
    lib.routedHost_connect.argtypes = [c_size_t, c_size_t, ]
    lib.routedHost_connect.restype = MsgpackBody
    _CONNECT = lib.routedHost_connect
    lib.routedHost_newStream.argtypes = [c_size_t, GoString, GoString, ]
    lib.routedHost_newStream.restype = MsgpackBody
    _NEW_STREAM = lib.routedHost_newStream

    def __init__(self, host: Host, dht: DHT):
        routed_host_handle = self._INIT(host.handle, dht.handle)
        self.routed_host_handle = routed_host_handle
        self._host = host
        super().__init__(loop=host.io_loop, handle=host.handle)
        self.del_handle = routed_host_handle

    async def connect(self, addr_info: AddrInfo):
        fut = c_wrap(self._loop, self._CONNECT, self.routed_host_handle, addr_info.handle)
        result: MsgpackBody = await fut
        result.raise_error()

    async def new_stream(self, peer_id: str, protocol_id: str) -> Stream:
        fut = c_wrap(self._loop, self._NEW_STREAM, self.routed_host_handle, GoString.new(peer_id), GoString.new(protocol_id))
        result: MsgpackBody = await fut
        result.raise_error()
        stream_handle = result.handles.first()
        return Stream(stream_handle, loop=self._loop)


__all__ = ['RoutedHost', ]
