from ctypes import *
from libp2p import Host
from libp2p.utils import *


lib = load_library()


class Relay(SimpleFreeMixin):
    lib.relay_new.argtypes = [c_size_t, MsgpackArg, ]
    lib.relay_new.restype = MsgpackBody
    _INIT = lib.relay_new
    lib.relay_delete.argtypes = [c_size_t, ]
    _FREE = lib.relay_delete

    def __init__(self, host: Host):
        result: MsgpackBody = self._INIT(host.handle, MsgpackArg.from_dict(dict()))
        result.raise_error()
        self.handle = result.handles.first()
        super(Relay, self).__init__()


__all__ = ['Relay', ]
