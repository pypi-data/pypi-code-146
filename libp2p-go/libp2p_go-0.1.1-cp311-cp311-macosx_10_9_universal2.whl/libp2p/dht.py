import enum
import asyncio
from ctypes import *
from typing import Self
from libp2p import Host
from libp2p.data_store import MutexDataStore
from libp2p.utils import *

lib = load_library()


class DhtOption(Option):
    load_library().dhtOption_delete.argtypes = [c_size_t, ]
    _FREE = load_library().dhtOption_delete


class DhtModeEnum(AutoInt):
    ModeAuto = enum.auto()
    ModeClient = enum.auto()
    ModeServer = enum.auto()
    ModeAutoServer = enum.auto()


class Mode(DhtOption):
    lib.dhtOption_mode.argtypes = [c_size_t, ]
    lib.dhtOption_mode.restype = c_size_t
    _INIT = lib.dhtOption_mode

    def __init__(self, mode: DhtModeEnum) -> None:
        handle = self._INIT(mode.value)
        super(Mode, self).__init__(handle)


class DataStore(DhtOption):
    lib.dhtOption_datastore.argtypes = [c_size_t, ]
    lib.dhtOption_datastore.restype = c_size_t
    _INIT = lib.dhtOption_datastore

    def __init__(self, ds: MutexDataStore) -> None:
        handle = self._INIT(ds.handle)
        super(DataStore, self).__init__(handle)
        self.ds = ds


class DHT(SimpleFreeMixin):
    lib.dht_new.argtypes = [c_size_t, MsgpackArg, ]
    lib.dht_new.restype = MsgpackBody
    _INIT = lib.dht_new
    lib.dht_newDHT.argtypes = [c_size_t, c_size_t, ]
    lib.dht_newDHT.restype = c_size_t
    _NEW_DHT = lib.dht_newDHT
    lib.dht_delete.argtypes = [c_size_t, ]
    _FREE = lib.dht_delete
    lib.dht_bootstrap.argtypes = [c_size_t, ]
    lib.dht_bootstrap.restype = MsgpackBody
    _BOOTSTRAP = lib.dht_bootstrap
    lib.dht_defaultBootstrapPeers.restype = MsgpackBody
    _DEFAULT_BOOTSTRAP_PEERS = lib.dht_defaultBootstrapPeers
    lib.dht_ping.argtypes = [c_size_t, GoString, ]
    lib.dht_ping.restype = MsgpackBody
    _PING = lib.dht_ping
    lib.dht_putValue.argtypes = [c_size_t, MsgpackArg, ]
    lib.dht_putValue.restype = MsgpackBody
    _PUT_VALUE = lib.dht_putValue
    lib.dht_getValue.argtypes = [c_size_t, MsgpackArg, ]
    lib.dht_getValue.restype = MsgpackBody
    _GET_VALUE = lib.dht_getValue

    def __init__(self, handle: int, loop: asyncio.AbstractEventLoop):
        self.handle = handle
        self.loop: asyncio.AbstractEventLoop = loop

    @classmethod
    def new(cls, host: Host, *opts: DhtOption) -> Self:
        args = {
            'Handles': [opt.handle for opt in opts]
        }
        result: MsgpackBody = cls._INIT(host.handle, MsgpackArg.from_dict(args))
        result.raise_error()
        return DHT(result.handles.first(), host.io_loop)

    @classmethod
    def new_dht(cls, host: Host, mutex_data_store: MutexDataStore) -> Self:
        handle = cls._NEW_DHT(host.handle, mutex_data_store.handle)
        return DHT(handle, host.io_loop)

    def bootstrap(self):
        result: MsgpackBody = self._BOOTSTRAP(self.handle)
        result.raise_error()

    @classmethod
    def default_bootstrap_peers(cls) -> list[str]:
        result: MsgpackBody = cls._DEFAULT_BOOTSTRAP_PEERS()
        result.raise_error()
        return result.strings

    async def ping(self, peer_id: str) -> bool:
        result: MsgpackBody = self._PING(self.handle, GoString.new(peer_id))
        result.raise_error()
        return True

    async def get_value(self, key: str) -> None | bytes:
        args = {
            "Strings": [key, ],
            "Handles": [],
        }
        fut = c_wrap(self.loop, self._GET_VALUE, self.handle, MsgpackArg.from_dict(args))
        result: MsgpackBody = await fut
        try:
            result.raise_error()
        except LibP2PError as e:
            if "routing: not found" in str(e):
                return None
        return result.bytes.first()

    async def put_value(self, key: str, value: bytes):
        args = {
            "Strings": [key, ],
            "Bytes": [value, ],
            "Handles": [],
        }
        fut = c_wrap(self.loop, self._PUT_VALUE, self.handle, MsgpackArg.from_dict(args))
        result: MsgpackBody = await fut
        result.raise_error()


__all__ = [
    'DhtModeEnum',
    'Mode',
    'DataStore',
    'DHT',
]
