import sys
from ctypes import *
from libp2p.utils import *


lib = load_library()


class PeerStore(SimpleFreeMixin):
    lib.peerStore_delete.argtypes = [c_size_t, ]
    _FREE = lib.peerStore_delete
    lib.peerStore_addAddrs.argtypes = [c_size_t, GoString, MsgpackArg, ]
    lib.peerStore_addAddrs.restype = MsgpackBody
    _ADD_ADDRS = lib.peerStore_addAddrs
    lib.peerStore_setAddrs.argtypes = [c_size_t, GoString, MsgpackArg, ]
    lib.peerStore_setAddrs.restype = MsgpackBody
    _SET_ADDRS = lib.peerStore_setAddrs
    lib.peerStore_updateAddrs.argtypes = [c_size_t, GoString, c_size_t, c_size_t, ]
    lib.peerStore_updateAddrs.restype = MsgpackBody
    _UPDATE_ADDRS = lib.peerStore_updateAddrs
    lib.peerStore_addrs.argtypes = [c_size_t, GoString, ]
    lib.peerStore_addrs.restype = MsgpackBody
    _ADDRS = lib.peerStore_addrs
    lib.peerStore_clearAddrs.argtypes = [c_size_t, GoString, ]
    lib.peerStore_clearAddrs.restype = MsgpackBody
    _CLEAR_ADDRS = lib.peerStore_clearAddrs
    lib.peerStore_peersWithAddrs.argtypes = [c_size_t, ]
    lib.peerStore_peersWithAddrs.restype = MsgpackBody
    _PEERS_WITH_ADDRS = lib.peerStore_peersWithAddrs
    PermanentAddrTTL = sys.maxsize
    ConnectedAddrTTL = sys.maxsize - 1

    def __init__(self, handle):
        self.handle = handle

    def add_addr(self, peer_id: str, multi_addr: str, ttl: int):
        self.add_addrs(peer_id=peer_id, multi_addr=[multi_addr, ], ttl=ttl)

    def add_addrs(self, peer_id: str, multi_addr: list[str], ttl: int):
        args = {
            'Strings': [str(addr) for addr in multi_addr],
            'Integers': [ttl, ],
        }
        arg = MsgpackArg.from_dict(args)
        result: MsgpackBody = self._ADD_ADDRS(self.handle, GoString.new(peer_id), arg)
        result.raise_error()

    def set_addrs(self, peer_id: str, multi_addr: str, ttl: int):
        args = {
            'Strings': [str(addr) for addr in multi_addr],
            'Integers': [ttl, ],
        }
        arg = MsgpackArg.from_dict(args)
        result: MsgpackBody = self._SET_ADDRS(self.handle, GoString.new(peer_id), arg)
        result.raise_error()

    def update_addrs(self, peer_id: str, old_ttl: int, new_ttl: int):
        result: MsgpackBody = self._SET_ADDRS(self.handle, GoString.new(peer_id), old_ttl, new_ttl)
        result.raise_error()

    def addrs(self, peer_id: str) -> list[str]:
        result: MsgpackBody = self._ADDRS(self.handle, GoString.new(peer_id))
        result.raise_error()
        return result.strings

    def peer_with_addrs(self) -> list[str]:
        result: MsgpackBody = self._PEERS_WITH_ADDRS(self.handle)
        result.raise_error()
        return result.strings


__all__ = ['PeerStore', ]
