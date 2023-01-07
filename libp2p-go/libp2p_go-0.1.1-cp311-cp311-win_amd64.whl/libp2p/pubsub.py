import struct
import asyncio
import dataclasses
from ctypes import *
from typing import Self
import base58
from libp2p import Host
from libp2p.utils import *


lib = load_library()


@dataclasses.dataclass
class LibP2PMessage:
    topic: str = dataclasses.field()
    from_peer: str = dataclasses.field()
    data: bytes = dataclasses.field()
    seq_no: int = dataclasses.field()
    signature: bytes = dataclasses.field(repr=False)
    key: bytes = dataclasses.field(repr=False)


class Subscription(SimpleFreeMixin):
    lib.subscription_delete.argtypes = [c_size_t, ]
    _FREE = lib.subscription_delete
    lib.subscription_cancel.argtypes = [c_size_t, ]
    _CANCEL = lib.subscription_cancel
    lib.subscription_next.argtypes = [c_size_t, ]
    lib.subscription_next.restype = MsgpackBody
    _NEXT = lib.subscription_next

    def __init__(self, handle: int, loop: asyncio.AbstractEventLoop):
        self.handle = handle
        self._loop = loop

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> LibP2PMessage:
        return await self.next()

    async def cancel(self):
        fut = c_wrap(self._loop, self._CANCEL, self.handle)
        await fut

    async def next(self) -> LibP2PMessage:
        fut = c_wrap(self._loop, self._NEXT, self.handle, MsgpackArg.from_dict(dict()))
        result: MsgpackBody = await fut
        result.raise_error()
        msg = LibP2PMessage(
            topic=result.strings.first(),
            from_peer=base58.b58encode(result.bytes[0]).decode('utf8'),
            data=result.bytes[1],
            seq_no=struct.unpack(">Q", result.bytes[2])[0],
            signature=result.bytes[3],
            key=result.bytes[4],
        )
        return msg


class Topic(SimpleFreeMixin):
    lib.topic_delete.argtypes = [c_size_t, ]
    _FREE = lib.topic_delete
    lib.topic_publish.argtypes = [c_size_t, c_size_t, POINTER(c_ubyte), MsgpackArg, ]
    lib.topic_publish.restype = MsgpackBody
    _PUBLISH = lib.topic_publish
    lib.topic_subscription.argtypes = [c_size_t, GoString, ]
    lib.topic_subscription.restype = MsgpackBody
    _SUBSCRIPTION = lib.topic_subscription
    lib.topic_close.argtypes = [c_size_t, ]
    lib.topic_close.restype = MsgpackBody
    _CLOSE = lib.topic_close

    def __init__(self, handle: int, loop: asyncio.AbstractEventLoop):
        self.handle = handle
        self._loop = loop

    async def subscription(self) -> Subscription:
        fut = c_wrap(self._loop, self._SUBSCRIPTION, self.handle, MsgpackArg.from_dict(dict()))
        result: MsgpackBody = await fut
        result.raise_error()
        return Subscription(result.handles.first(), self._loop)

    async def publish(self, data: bytes):
        buffer = (c_ubyte * len(data)).from_buffer(bytearray(data))
        fut = c_wrap(self._loop, self._PUBLISH, self.handle, len(data), buffer, MsgpackArg.from_dict(dict()))
        result: MsgpackBody = await fut
        result.raise_error()

    async def close(self):
        fut = c_wrap(self._loop, self._CLOSE, self.handle)
        result: MsgpackBody = await fut
        result.raise_error()


class PubSub(SimpleFreeMixin):
    lib.pubsub_delete.argtypes = [c_size_t, ]
    _FREE = lib.pubsub_delete
    lib.pubsub_gossipSubNew.argtypes = [c_size_t, MsgpackArg, ]
    lib.pubsub_gossipSubNew.restype = MsgpackBody
    _GOSSIP_NEW = lib.pubsub_gossipSubNew
    lib.pubsub_floodSubNew.argtypes = [c_size_t, MsgpackArg, ]
    lib.pubsub_floodSubNew.restype = MsgpackBody
    _FLOOD_NEW = lib.pubsub_floodSubNew
    lib.pubsub_join.argtypes = [c_size_t, GoString, MsgpackArg, ]
    lib.pubsub_join.restype = MsgpackBody
    _JOIN = lib.pubsub_join
    lib.pubsub_listPeers.argtypes = [c_size_t, GoString, ]
    lib.pubsub_listPeers.restype = MsgpackBody
    _LIST_PEERS = lib.pubsub_listPeers
    lib.pubsub_getTopics.argtypes = [c_size_t, ]
    lib.pubsub_getTopics.restype = MsgpackBody
    _GET_TOPICS = lib.pubsub_getTopics

    def __init__(self, handle: int, loop: asyncio.AbstractEventLoop):
        self.handle = handle
        self._loop = loop

    @classmethod
    def new_gossip(cls, host: Host) -> Self:
        result: MsgpackBody = cls._GOSSIP_NEW(host.handle, MsgpackArg.from_dict(dict()))
        result.raise_error()
        return PubSub(result.handles.first(), host.io_loop)

    @classmethod
    def new_flood(cls, host: Host) -> Self:
        result: MsgpackBody = cls._FLOOD_NEW(host.handle, MsgpackArg.from_dict(dict()))
        result.raise_error()
        return PubSub(result.handles.first(), host.io_loop)

    async def join(self, topic_name: str) -> Topic:
        fut = c_wrap(self._loop, self._JOIN, self.handle, GoString.new(topic_name), MsgpackArg.from_dict(dict()))
        result: MsgpackBody = await fut
        result.raise_error()
        return Topic(result.handles.first(), self._loop)

    async def list_peers(self, topic_name: str) -> list[str]:
        fut = c_wrap(self._loop, self._LIST_PEERS, self.handle, GoString.new(topic_name))
        result: MsgpackBody = await fut
        result.raise_error()
        return result.strings

    async def get_topics(self) -> list[str]:
        fut = c_wrap(self._loop, self._GET_TOPICS, self.handle)
        result: MsgpackBody = await fut
        result.raise_error()
        return result.strings


__all__ = ['LibP2PMessage', 'Subscription', 'Topic', 'PubSub', ]
