from ctypes import *
from libp2p import Host
from libp2p.peer import AddrInfo
from libp2p.utils import *


lib = load_library()


lib.client_reserve.argtypes = [c_longlong, c_longlong, ]
lib.client_reserve.restype = MsgpackBody
_CLIENT_RESERVE = lib.client_reserve


async def reserve(host: Host, addr_info: AddrInfo):
    fut = c_wrap(host.io_loop, _CLIENT_RESERVE, host.handle, addr_info.handle)
    result: MsgpackBody = await fut
    result.raise_error()


__all__ = ['reserve', ]
