import asyncio
from ctypes import *
import dataclasses
from libp2p.utils import *


lib = load_library()


@dataclasses.dataclass
class AddrInfo(SimpleFreeMixin):
    lib.addrInfo_delete.argtypes = [c_size_t, ]
    _FREE = lib.addrInfo_delete
    lib.addrInfo_new.argtypes = [GoString, MsgpackArg, ]
    lib.addrInfo_new.restype = MsgpackBody
    _INIT = lib.addrInfo_new
    lib.addrInfo_addrs.argtypes = [c_size_t, ]
    lib.addrInfo_addrs.restype = MsgpackBody
    _ADDRS = lib.addrInfo_addrs
    lib.addrInfo_id.argtypes = [c_size_t, ]
    lib.addrInfo_id.restype = MsgpackBody
    _ID = lib.addrInfo_id

    id: str = dataclasses.field()
    addrs: list[str] = dataclasses.field(default_factory=list, repr=False)

    def __init__(self, peer_id: str = None, addrs: list[str] = None, handle: int = None):
        if handle is None:
            args = {
                'Strings': [str(addr) for addr in addrs],
            }
            arg = MsgpackArg.from_dict(args)
            result: MsgpackBody = self._INIT(GoString.new(peer_id), arg)
            result.raise_error()
            handle = result.handles.first()
        self.handle = handle
        if peer_id:
            self.id = peer_id
        else:
            self.id = self._id()
        if addrs is not None:
            self.addrs = addrs
        else:
            self.addrs = self._addrs()

    def _addrs(self) -> list[str]:
        result: MsgpackBody = self._ADDRS(self.handle)
        result.raise_error()
        addrs = [s for s in result.strings]
        return addrs

    def _id(self) -> str:
        result: MsgpackBody = self._ID(self.handle)
        result.raise_error()
        return result.strings.first()


class AddrInfoChan(SimpleFreeMixin):
    lib.addrInfoChan_delete.argtypes = [c_size_t, ]
    _FREE = lib.addrInfoChan_delete
    lib.addrInfoChan_pop.argtypes = [c_size_t, ]
    lib.addrInfoChan_pop.restype = c_size_t
    _POP = lib.addrInfoChan_pop

    def __init__(self, handle: int, loop: asyncio.AbstractEventLoop):
        self.handle = handle
        self.loop = loop

    def __aiter__(self):
        return self

    async def __anext__(self) -> AddrInfo:
        fut = c_wrap(self.loop, self._POP, self.handle)
        handle = await fut
        if not handle:
            raise StopAsyncIteration
        addr = AddrInfo(handle=handle)
        return addr


lib.peer_addrInfoFromP2pAddr.argtypes = [GoString, ]
lib.peer_addrInfoFromP2pAddr.restype = MsgpackBody
_ADDR_INFO_FROM_P2P_ADDR = lib.peer_addrInfoFromP2pAddr


def addr_info_from_p2p_addr(multi_addr_string: str):
    result: MsgpackBody = _ADDR_INFO_FROM_P2P_ADDR(GoString.new(multi_addr_string))
    result.raise_error()
    handle = result.handles.first()
    return AddrInfo(handle=handle)


__all__ = [
    'AddrInfo',
    'AddrInfoChan',
    'addr_info_from_p2p_addr',
]
