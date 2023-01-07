from ctypes import *
from libp2p.utils import *


lib = load_library()


class ConnMgrOption(Option):
    lib.optionConnmgr_delete.argtypes = [c_size_t, ]
    _FREE = lib.optionConnmgr_delete


class WithGracePeriod(ConnMgrOption):
    lib.option_withGracePeriod.argtypes = [c_longlong, ]
    lib.option_withGracePeriod.restype = c_size_t
    _WITH_GRACE_PERIOD = lib.option_withGracePeriod

    def __init__(self, p: int) -> None:
        handle = self._WITH_GRACE_PERIOD(p)
        super(WithGracePeriod, self).__init__(handle)


class ConnMgr(SimpleFreeMixin):
    lib.connMgr_delete.argtypes = [c_size_t, ]
    _FREE = lib.connMgr_delete
    lib.connMgr_new.argtypes = [MsgpackArg, ]
    lib.connMgr_new.restype = MsgpackBody
    _NEW = lib.connMgr_new

    def __init__(self, low: int, high: int, *options: ConnMgrOption):
        args = {
            'Integers': [low, high, ],
            'Handles': [opt.handle for opt in options],
        }
        arg = MsgpackArg.from_dict(args)
        result: MsgpackBody = self._NEW(arg)
        result.raise_error()
        self.handle = result.handles.first()


__all__ = [
    'WithGracePeriod',
    'ConnMgr',
]
