from ctypes import *
from libp2p.dht import DHT
from libp2p.peer import AddrInfoChan
from libp2p.utils import *

lib = load_library()


class RoutingDiscovery(SimpleFreeMixin):
    lib.routingDiscovery_new.argtypes = [c_size_t, ]
    lib.routingDiscovery_new.restype = c_size_t
    _INIT = lib.routingDiscovery_new
    lib.routingDiscovery_delete.argtypes = [c_size_t, ]
    _FREE = lib.routingDiscovery_delete
    lib.routingDiscovery_findPeers.argtypes = [c_size_t, GoString, ]
    lib.routingDiscovery_findPeers.restype = MsgpackBody
    _FIND_PEERS = lib.routingDiscovery_findPeers
    lib.routingDiscovery_advertise.argtypes = [c_size_t, GoString, ]
    _ADVERTISE = lib.routingDiscovery_advertise

    def __init__(self, dht: DHT):
        self.handle = self._INIT(dht.handle)
        self.loop = dht.loop

    def find_peers(self, rendezvous: str):
        result: MsgpackBody = self._FIND_PEERS(self.handle, GoString.new(rendezvous))
        result.raise_error()
        return AddrInfoChan(handle=result.handles.first(), loop=self.loop)

    def advertise(self, rendezvous: str):
        self._ADVERTISE(self.handle, GoString.new(rendezvous))


__all__ = ['RoutingDiscovery']
