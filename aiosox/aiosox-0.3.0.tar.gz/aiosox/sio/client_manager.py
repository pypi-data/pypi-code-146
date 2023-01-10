import asyncio
import typing
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    Dict,
    Self,
)

from aiokafka.errors import KafkaConnectionError
from async_generator import asynccontextmanager
from socketio.asyncio_pubsub_manager import AsyncPubSubManager

from ..kafka.utils import get_kafka_consumer, get_kafka_producer


class Unsubscribed(Exception):
    pass


class KafkaEvent:
    def __init__(self, channel: str, message: str) -> None:
        self.channel = channel
        self.message = message

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, KafkaEvent)
            and self.channel == other.channel
            and self.message == other.message
        )

    def __repr__(self) -> str:
        return f"Event(channel={self.channel!r}, message={self.message!r})"


class Subscriber:
    def __init__(self, queue: asyncio.Queue) -> None:
        self._queue = queue

    async def __aiter__(self) -> AsyncGenerator:
        try:
            while True:
                yield await self.get()
        except Unsubscribed:
            pass

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        ...

    async def get(self) -> KafkaEvent:
        item = await self._queue.get()
        if item is None:
            raise Unsubscribed()
        return item


class KafkaBackend:
    def __init__(self, url: str, group_id: str | None = None):
        self._servers = url
        self._consumer_channels: typing.Set = set()
        self.group_id = group_id

    async def connect(self) -> None:
        self._producer = get_kafka_producer(bootstrap_servers=self._servers)
        self._consumer = get_kafka_consumer(bootstrap_servers=self._servers, group_id=self.group_id)

        await self._producer.start()
        await self._consumer.start()

    async def disconnect(self) -> None:
        await self._producer.stop()
        await self._consumer.stop()

    async def subscribe(self, channel: str) -> None:
        self._consumer_channels.add(channel)
        self._consumer.subscribe(topics=self._consumer_channels)

    async def unsubscribe(self, channel: str) -> None:
        self._consumer.unsubscribe()

    async def publish(self, channel: str, message: typing.Any) -> None:
        await self._producer.send_and_wait(channel, message)

    async def next_published(self) -> KafkaEvent:
        message = await self._consumer.getone()
        return KafkaEvent(channel=message.topic, message=message.value)


class SocketIoClientManager(AsyncPubSubManager):
    def __init__(
        self,
        kafka_backend: KafkaBackend,
        channel="socketio",
        write_only=False,
        logger=None,
    ):
        super().__init__(channel, write_only, logger)
        self.kafka_backend: KafkaBackend = kafka_backend
        self._subscribers: Dict[str, Any] = {}
        self._backend = kafka_backend

    async def __aenter__(self) -> Self:
        await self.on_start()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self.on_shutdown()

    async def _listener(self) -> None:

        while True:
            event = await self._backend.next_published()

            for queue in list(self._subscribers.get(event.channel, [])):
                await queue.put(event)

    async def on_start(self) -> None:
        try:
            await self._backend.connect()
        except KafkaConnectionError as e:
            await self.kafka_backend.disconnect()
            raise RuntimeError("unable to connect to kafka")
        self._listener_task = asyncio.create_task(self._listener())

    async def on_shutdown(self) -> None:
        if self._listener_task.done():
            self._listener_task.result()
        else:
            self._listener_task.cancel()
        await self._backend.disconnect()

    @asynccontextmanager
    async def subscribe(self, channel: str) -> AsyncIterator["Subscriber"]:
        queue: asyncio.Queue = asyncio.Queue()

        try:
            if not self._subscribers.get(channel):
                await self._backend.subscribe(channel)
                self._subscribers[channel] = set([queue])
            else:
                self._subscribers[channel].add(queue)

            yield Subscriber(queue)

            self._subscribers[channel].remove(queue)
            if not self._subscribers.get(channel):
                del self._subscribers[channel]
                await self._backend.unsubscribe(channel)
        finally:
            await queue.put(None)

    async def _publish(self, message: Any):
        await self._backend.publish(self.channel, message)

    async def _listen(self):
        async with self.subscribe(channel=self.channel) as subscriber:  # type:ignore
            async for event in subscriber:
                yield event.message
