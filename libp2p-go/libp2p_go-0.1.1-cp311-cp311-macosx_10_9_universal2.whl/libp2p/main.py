import asyncio
from ctypes import *
from typing import Type
from functools import cached_property
from libp2p.conn_mgr import ConnMgr
from libp2p.peer import AddrInfo
from libp2p.utils import *
from libp2p.crypto import PrivKey
from libp2p.peer_store import PeerStore


lib = load_library()


class DisableRelay(Option):
    lib.option_disableRelay.argtypes = []
    lib.option_disableRelay.restype = c_size_t
    _INIT = lib.option_disableRelay

    def __init__(self) -> None:
        handle = self._INIT()
        super(DisableRelay, self).__init__(handle)


class ListenAddrStrings(Option):
    lib.option_listenAddrStrings.argtypes = [MsgpackArg, ]
    lib.option_listenAddrStrings.restype = c_size_t
    _INIT = lib.option_listenAddrStrings

    def __init__(self, *addrs: str) -> None:
        args = {
            'Strings': list(addrs),
        }
        arg = MsgpackArg.from_dict(args)
        handle = self._INIT(arg)
        super(ListenAddrStrings, self).__init__(handle)


class Identity(Option):
    lib.option_identity.argtypes = [c_size_t, ]
    lib.option_identity.restype = c_size_t
    _INIT = lib.option_identity

    def __init__(self, priv: PrivKey) -> None:
        handle = self._INIT(priv.handle)
        super(Identity, self).__init__(handle)


class NoSecurity(Option):
    lib.option_noSecurity.argtypes = []
    lib.option_noSecurity.restype = c_size_t
    _INIT = lib.option_noSecurity

    def __init__(self) -> None:
        handle = self._INIT()
        super(NoSecurity, self).__init__(handle)


class SecurityTls(Option):
    lib.option_security_tls.argtypes = []
    lib.option_security_tls.restype = c_size_t
    _INIT = lib.option_security_tls

    def __init__(self) -> None:
        handle = self._INIT()
        super(SecurityTls, self).__init__(handle)


class SecurityNoise(Option):
    lib.option_security_noise.argtypes = []
    lib.option_security_noise.restype = c_size_t
    _INIT = lib.option_security_noise

    def __init__(self) -> None:
        handle = self._INIT()
        super(SecurityNoise, self).__init__(handle)


class DefaultTransports(Option):
    lib.option_defaultTransports.argtypes = []
    lib.option_defaultTransports.restype = c_size_t
    _INIT = lib.option_defaultTransports

    def __init__(self) -> None:
        handle = self._INIT()
        super(DefaultTransports, self).__init__(handle)


class ConnectionManager(Option):
    lib.option_connectionManager.argtypes = [c_size_t, ]
    lib.option_connectionManager.restype = c_size_t
    _INIT = lib.option_connectionManager

    def __init__(self, mgr: ConnMgr) -> None:
        handle = self._INIT(mgr.handle)
        super(ConnectionManager, self).__init__(handle)


class NATPortMap(Option):
    lib.option_natPortMap.argtypes = []
    lib.option_natPortMap.restype = c_size_t
    _INIT = lib.option_natPortMap

    def __init__(self) -> None:
        handle = self._INIT()
        super(NATPortMap, self).__init__(handle)


class Routing(Option):
    lib.option_routing.argtypes = []
    lib.option_routing.restype = c_size_t
    _INIT = lib.option_routing

    def __init__(self) -> None:
        handle = self._INIT()
        super(Routing, self).__init__(handle)


class EnableNATService(Option):
    lib.option_enableNATService.argtypes = []
    lib.option_enableNATService.restype = c_size_t
    _INIT = lib.option_enableNATService

    def __init__(self) -> None:
        handle = self._INIT()
        super(EnableNATService, self).__init__(handle)


class NoListenAddrs(Option):
    lib.option_noListenAddrs.argtypes = []
    lib.option_noListenAddrs.restype = c_size_t
    _INIT = lib.option_noListenAddrs

    def __init__(self) -> None:
        handle = self._INIT()
        super(NoListenAddrs, self).__init__(handle)


class EnableRelay(Option):
    lib.option_enableRelay.argtypes = []
    lib.option_enableRelay.restype = c_size_t
    _INIT = lib.option_enableRelay

    def __init__(self) -> None:
        handle = self._INIT()
        super(EnableRelay, self).__init__(handle)


class EnableAutoRelay(Option):
    lib.option_autoRelay.argtypes = [MsgpackArg, ]
    lib.option_autoRelay.restype = c_size_t
    _INIT = lib.option_autoRelay

    def __init__(self) -> None:
        args = {
            "Handles": [],
        }
        handle = self._INIT(MsgpackArg.from_dict(args))
        super(EnableAutoRelay, self).__init__(handle)


class Ping(Option):
    lib.option_ping.argtypes = [c_bool, ]
    lib.option_ping.restype = c_size_t
    _INIT = lib.option_ping

    def __init__(self, enable=True) -> None:
        handle = self._INIT(enable)
        super(Ping, self).__init__(handle)


class SetPeerStore(Option):
    lib.option_peerStore.argtypes = [c_size_t, ]
    lib.option_peerStore.restype = c_size_t
    _INIT = lib.option_peerStore

    def __init__(self, peer_store: PeerStore) -> None:
        handle = self._INIT(peer_store.handle)
        super(SetPeerStore, self).__init__(handle)


class PrivateNetwork(Option):
    lib.option_privateNetwork.argtypes = [c_size_t, POINTER(c_ubyte), c_bool, ]
    lib.option_privateNetwork.restype = c_size_t
    _INIT = lib.option_privateNetwork

    def __init__(self, psk: bytes, force_private_network=False) -> None:
        assert len(psk) == 32
        buffer = (c_ubyte * len(psk)).from_buffer(bytearray(psk))
        handle = self._INIT(len(psk), buffer, force_private_network)
        super(PrivateNetwork, self).__init__(handle)


class MuxerYamux(Option):
    lib.option_muxerYamux.argtypes = [GoString, ]
    lib.option_muxerYamux.restype = c_size_t
    _INIT = lib.option_muxerYamux

    def __init__(self, protocol_id: str) -> None:
        handle = self._INIT(protocol_id)
        super(MuxerYamux, self).__init__(handle)


class DefaultMuxers(Option):
    lib.option_defaultMuxers.restype = c_size_t
    _INIT = lib.option_defaultMuxers

    def __init__(self):
        handle = self._INIT()
        super(DefaultMuxers, self).__init__(handle)


class DefaultSecurity(Option):
    lib.option_defaultSecurity.restype = c_size_t
    _INIT = lib.option_defaultSecurity

    def __init__(self):
        handle = self._INIT()
        super(DefaultSecurity, self).__init__(handle)


class TransportWebsocket(Option):
    lib.option_transport_ws.restype = c_size_t
    _INIT = lib.option_transport_ws

    def __init__(self):
        handle = self._INIT()
        super(TransportWebsocket, self).__init__(handle)


class Stream(SimpleFreeMixin):
    lib.stream_delete.argtypes = [c_size_t, ]
    _FREE = lib.stream_delete
    lib.stream_reset.argtypes = [c_size_t, ]
    _RESET = lib.stream_reset
    lib.stream_close.argtypes = [c_size_t, ]
    _CLOSE = lib.stream_close
    lib.stream_id.argtypes = [c_size_t, ]
    lib.stream_id.restype = MsgpackBody
    _ID = lib.stream_id
    lib.stream_protocol.argtypes = [c_size_t, ]
    lib.stream_protocol.restype = MsgpackBody
    _PROTOCOL = lib.stream_protocol
    lib.stream_readString.argtypes = [c_size_t, c_char, ]
    lib.stream_readString.restype = MsgpackBody
    _READ_STRING = lib.stream_readString
    lib.stream_readAll.argtypes = [c_size_t, ]
    lib.stream_readAll.restype = MsgpackBody
    _READ_ALL = lib.stream_readAll
    lib.stream_write.argtypes = [c_size_t, c_size_t, POINTER(c_ubyte), ]
    lib.stream_write.restype = MsgpackBody
    _WRITE = lib.stream_write
    lib.stream_read.argtypes = [c_size_t, c_size_t, ]
    lib.stream_read.restype = MsgpackBody
    _READ = lib.stream_read

    def __init__(self, handle, loop: asyncio.AbstractEventLoop) -> None:
        self.handle = handle
        self._loop = loop
        super(Stream, self).__init__()

    async def reset(self):
        fut = c_wrap(self._loop, self._RESET, self.handle)
        await fut

    async def close(self):
        fut = c_wrap(self._loop, self._CLOSE, self.handle)
        await fut

    async def write(self, b: bytes):
        buffer = (c_ubyte * len(b)).from_buffer(bytearray(b))
        fut = c_wrap(self._loop, self._WRITE, self.handle, len(b), buffer)
        result: MsgpackBody = await fut
        result.raise_error()

    async def read_bytes(self, n: int) -> tuple[int, bytes]:
        fut = c_wrap(self._loop, self._READ, self.handle, n)
        result: MsgpackBody = await fut
        result.raise_error()
        return result.integers.first(), result.bytes.first()

    async def read_string(self, delim='\n') -> str:
        ch = ord(delim)
        fut = c_wrap(self._loop, self._READ_STRING, self.handle, ch)
        result: MsgpackBody = await fut
        result.raise_error()
        return result.strings.first()

    async def read_all(self) -> bytes:
        fut = c_wrap(self._loop, self._READ_ALL, self.handle)
        result: MsgpackBody = await fut
        result.raise_error()
        return result.bytes.first()

    @cached_property
    def id(self) -> str:
        return self._ID(self.handle)

    @cached_property
    def protocol(self) -> str:
        return self._PROTOCOL(self.handle)


class Network:
    lib.network_listenAddresses.argtypes = [c_size_t, ]
    lib.network_listenAddresses.restype = MsgpackBody
    _LISTEN_ADDRESSES = lib.network_listenAddresses
    lib.network_resetDial.argtypes = [c_size_t, GoString, ]
    lib.network_resetDial.restype = MsgpackBody
    _RESET_DIAL = lib.network_resetDial

    def __init__(self, host_handle):
        self.host_handle = host_handle

    def listen_addresses(self) -> list[str]:
        result: MsgpackBody = self._LISTEN_ADDRESSES(self.host_handle)
        result.raise_error()
        return [s for s in result.strings]

    def reset_dial(self, peer_id: str):
        result: MsgpackBody = self._RESET_DIAL(self.host_handle, GoString.new(peer_id))
        result.raise_error()


class Host(SimpleFreeMixin):
    lib.host_new.argtypes = [MsgpackArg, ]
    lib.host_new.restype = MsgpackBody
    _INIT = lib.host_new
    lib.host_delete.argtypes = [c_size_t, ]
    _FREE = lib.host_delete
    lib.host_addrs.argtypes = [c_size_t, ]
    lib.host_addrs.restype = MsgpackBody
    _ADDRS = lib.host_addrs
    _STREAM_HANDLER_FUNC = CFUNCTYPE(None, c_size_t)
    lib.host_setStreamHandler.argtypes = [c_size_t, GoString, _STREAM_HANDLER_FUNC, ]
    _SET_STREAM_HANDLER = lib.host_setStreamHandler
    lib.host_removeStreamHandler.argtypes = [c_size_t, GoString, ]
    _REMOVE_STREAM_HANDLER = lib.host_removeStreamHandler
    lib.host_newStream.argtypes = [c_size_t, GoString, GoString, ]
    lib.host_newStream.restype = MsgpackBody
    _NEW_STREAM = lib.host_newStream
    lib.host_newStreamWithUseTransient.argtypes = [c_size_t, GoString, GoString, ]
    lib.host_newStreamWithUseTransient.restype = MsgpackBody
    _NEW_STREAM_WITH_USE_TRANSIENT = lib.host_newStreamWithUseTransient
    lib.host_id.argtypes = [c_size_t, ]
    lib.host_id.restype = MsgpackBody
    _ID = lib.host_id
    lib.host_close.argtypes = [c_size_t, ]
    _CLOSE = lib.host_close
    lib.host_connect.argtypes = [c_size_t, c_size_t, ]
    lib.host_connect.restype = MsgpackBody
    _CONNECT = lib.host_connect
    lib.host_peerStore.argtypes = [c_size_t, ]
    lib.host_peerStore.restype = c_size_t
    _PEER_STORE = lib.host_peerStore

    def __init__(self, *options: Option | Type[Option], loop: asyncio.AbstractEventLoop = None, handle: int = None):
        if handle is None:
            options: list[Option] = [
                opt()
                if isinstance(opt, type) and issubclass(opt, Option) else opt
                for opt in options
            ]
            args = {
                'Handles': [opt.handle for opt in options],
            }
            arg = MsgpackArg.from_dict(args)
            result: MsgpackBody = self._INIT(arg)
            result.raise_error()
            handle = result.handles.first()
        self.handle = handle
        # 虚拟C函数指针必须保持被引用，否则被GC掉后再异步Go回调触发函数指针时已经是悬空指针了。
        self._fp_d = dict()
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop

    @property
    def io_loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def id(self) -> str:
        result: MsgpackBody = self._ID(self.handle)
        return result.strings.first()

    def addrs(self) -> list[str]:
        result: MsgpackBody = self._ADDRS(self.handle)
        result.raise_error()
        return [str(s) for s in result.strings]

    def set_stream_handler(self, protocol_id: str, callback):
        def create_task_wrap(handle):
            stream = Stream(handle, loop=self._loop)
            return self._loop.create_task(callback(stream), name=f'libp2pHandler{protocol_id}-{handle}')

        def cb_wrap(handle):
            self._loop.call_soon_threadsafe(
                create_task_wrap,
                handle,
            )

        fp = self._STREAM_HANDLER_FUNC(cb_wrap)
        self._fp_d[protocol_id] = fp
        self._SET_STREAM_HANDLER(self.handle, GoString.new(protocol_id), fp)

    def remove_stream_handler(self, protocol_id: str):
        if protocol_id in self._fp_d:
            del self._fp_d[protocol_id]
        self._REMOVE_STREAM_HANDLER(self.handle, GoString.new(protocol_id))

    async def new_stream(self, peer_id: str, protocol_id: str) -> Stream:
        fut = c_wrap(self._loop, self._NEW_STREAM, self.handle, GoString.new(peer_id), GoString.new(protocol_id))
        result: MsgpackBody = await fut
        result.raise_error()
        stream_handle = result.handles.first()
        return Stream(stream_handle, loop=self._loop)

    async def new_stream_with_use_transient(self, peer_id: str, protocol_id: str) -> Stream:
        fut = c_wrap(
            self._loop,
            self._NEW_STREAM_WITH_USE_TRANSIENT,
            self.handle, GoString.new(peer_id), GoString.new(protocol_id),
        )
        result: MsgpackBody = await fut
        result.raise_error()
        stream_handle = result.handles.first()
        return Stream(stream_handle, loop=self._loop)

    async def close(self):
        fut = c_wrap(self._loop, self._CLOSE, self.handle)
        await fut

    async def connect(self, addr_info: AddrInfo):
        fut = c_wrap(self._loop, self._CONNECT, self.handle, addr_info.handle)
        result: MsgpackBody = await fut
        result.raise_error()

    @cached_property
    def peer_store(self):
        handle = self._PEER_STORE(self.handle)
        return PeerStore(handle)

    @cached_property
    def network(self):
        return Network(self.handle)


__all__ = [
    'DisableRelay',
    'ListenAddrStrings',
    'Identity',
    'NoSecurity',
    'SecurityTls',
    'SecurityNoise',
    'DefaultTransports',
    'ConnectionManager',
    'NATPortMap',
    'Routing',
    'EnableNATService',
    'NoListenAddrs',
    'EnableRelay',
    'EnableAutoRelay',
    'Ping',
    'PrivateNetwork',
    'MuxerYamux',
    'DefaultMuxers',
    'DefaultSecurity',
    'TransportWebsocket',
    'Stream',
    'PeerStore',
    'Network',
    'Host',
]
