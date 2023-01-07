from ctypes import *
from libp2p import Host
from libp2p.peer import AddrInfo
from libp2p.utils import *

lib = load_library()


class MdnsService(SimpleFreeMixin):
    _NOTIFEE_HANDLER_FUNC = CFUNCTYPE(None, c_size_t)
    lib.mdnsService_new.argtypes = [c_size_t, GoString, _NOTIFEE_HANDLER_FUNC, ]
    lib.mdnsService_new.restype = c_size_t
    _INIT = lib.mdnsService_new
    lib.mdnsService_delete.argtypes = [c_size_t, ]
    _FREE = lib.mdnsService_delete
    lib.mdnsService_start.argtypes = [c_size_t, ]
    lib.mdnsService_start.restype = MsgpackBody
    _START = lib.mdnsService_start
    lib.mdnsService_close.argtypes = [c_size_t, ]
    lib.mdnsService_close.restype = MsgpackBody
    _CLOSE = lib.mdnsService_close

    def __init__(self, host: Host, rendezvous: str, discovery_notifee):
        loop = host.io_loop
        assert loop, rendezvous

        def create_task_wrap(handle):
            addr_info = AddrInfo(handle=handle)
            return loop.create_task(discovery_notifee(addr_info), name=f'libp2pMdnsNotifee{handle}')

        def cb_wrap(handle):
            loop.call_soon_threadsafe(
                create_task_wrap,
                handle,
            )

        self.fp = self._NOTIFEE_HANDLER_FUNC(cb_wrap)
        self.handle = self._INIT(host.handle, GoString.new(rendezvous), self.fp)

    def start(self):
        result: MsgpackBody = self._START(self.handle)
        result.raise_error()

    def stop(self):
        result: MsgpackBody = self._CLOSE(self.handle)
        result.raise_error()


__all__ = ['MdnsService']
