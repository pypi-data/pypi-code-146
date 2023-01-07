from ctypes import *
from libp2p.utils import *


lib = load_library()


class MapDataStore(SimpleFreeMixin):
    lib.mapDatastore_new.argtypes = []
    lib.mapDatastore_new.restype = c_size_t
    _INIT = lib.mapDatastore_new
    lib.mapDatastore_delete.argtypes = [c_size_t, ]
    _FREE = lib.mapDatastore_delete

    def __init__(self):
        handle = self._INIT()
        self.handle = handle


class MutexDataStore(SimpleFreeMixin):
    lib.mutexDatastore_new.argtypes = [c_size_t, ]
    lib.mutexDatastore_new.restype = c_size_t
    _INIT = lib.mutexDatastore_new
    lib.mutexDatastore_delete.argtypes = [c_size_t, ]
    _FREE = lib.mutexDatastore_delete

    def __init__(self, map_data_store: MapDataStore):
        handle = self._INIT(map_data_store.handle)
        self.handle = handle


__all__ = ['MapDataStore', 'MutexDataStore', ]
