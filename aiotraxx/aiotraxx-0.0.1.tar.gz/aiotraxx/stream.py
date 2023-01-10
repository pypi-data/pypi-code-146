import asyncio
import csv
import functools
import io
import logging
import random
from collections.abc import AsyncIterable
from datetime import datetime, timedelta
from typing import Sequence, Set

import pendulum
from aiohttp import ClientResponse, ClientSession
from dints.abc import AbstractClient, AbstractConnection
from dints.models import ErrorMessage
from pydantic import ValidationError

from aiotraxx.exceptions import ExpiredSession
from aiotraxx.http import TraxxClient
from aiotraxx.models import TraxxSensorMessage, TraxxSubscription



_LOGGER = logging.getLogger(__name__)


class TraxxConnection(AbstractConnection):
    def __init__(
        self,
        client: "TraxxStreamClient",
        loop: asyncio.AbstractEventLoop,
        *,
        update_interval: float,
        max_missed_updates: int,
        backoff_factor: float,
        initial_backoff: float,
        timezone: str
    ) -> None:
        super().__init__(client, loop)
        self.update_interval = update_interval
        self.max_missed_updates = max_missed_updates
        self.backoff_factor = backoff_factor
        self.initial_backoff = initial_backoff
        self.timezone = timezone

    @property
    def subscription(self) -> TraxxSubscription:
        return list(self.subscriptions)[0]

    async def start(self, subscription: TraxxSubscription) -> None:
        if self.is_running:
            raise RuntimeError("Attempted to start a running connection.")
        self.subscriptions.add(subscription)
        runner = self._loop.create_task(self.run())
        runner.add_done_callback(self.connection_lost)
        self._runner = runner

    async def run(self) -> None:
        subscription = self.subscription
        asset_id = subscription.asset_id
        sensor_id = subscription.sensor_id
        last_update: datetime = None
        last_timestamp: datetime = None
        attempts = 0
        while True:
            now = datetime.now()
            if last_update is not None:
                # ensure start is sufficiently far back that we get data most
                # of the time
                start_time = min(last_update, now-timedelta(minutes=2))
            else:
                # backfill 15 minutes of data
                start_time = now-timedelta(minutes=15)
            begin = int(pendulum.instance(start_time, self.timezone).float_timestamp * 1000)
            end = int(pendulum.instance(now, self.timezone).float_timestamp * 1000)
            try:
                response: ClientResponse = await self.client.session.sensors.sensor_data(
                    asset_id,
                    sensor_id,
                    begin,
                    end
                )
                response.raise_for_status()
                content = await response.read()
            except Exception:
                _LOGGER.warning("Failed to retrieve sensor data: %r", subscription, exc_info=True)
                if attempts >= self.max_missed_updates:
                    raise
                backoff_delay = (
                    self.initial_backoff * self.backoff_factor ** attempts
                )
                backoff_delay = min(
                    
                    self.update_interval,
                    int(backoff_delay)
                )
                _LOGGER.info(
                    "Attempting next update in %0.2f. Attempt %i of %i",
                    backoff_delay,
                    attempts + 1,
                    self.max_missed_updates
                )
                await asyncio.sleep(backoff_delay)
                attempts += 1
                continue
            else:
                if b"<!DOCTYPE html>" in content:
                    raise ExpiredSession()
                self._last_update = now
                attempts = 0
            
            sleeper = self._loop.create_task(
                asyncio.sleep(self.update_interval + random.randint(-2000, 2000)/1000)
            )
            if not content:
                _LOGGER.debug("No content returned for sensor: %r", subscription)
            else:
                buffer = io.StringIO(content.decode())
                reader = csv.reader(buffer)
                items = [{"timestamp": line[0], "value": line[1]} for line in reader]
                if items and self._online:
                    try:
                        msg = TraxxSensorMessage(
                            sensor=subscription,
                            items=items
                        )
                    except ValidationError:
                        _LOGGER.warning("Message validation failed", exc_info=True, extra={"raw": items})
                    else:
                        if last_timestamp is not None:
                            msg.filter(last_timestamp)
                        if msg.items:
                            last_timestamp = msg.items[-1].timestamp
                            await self.client._data_queue.put(msg.json())
            await sleeper


class TraxxStreamClient(AbstractClient):
    def __init__(
        self,
        session: ClientSession,
        *,
        max_subscriptions: int = 100,
        max_buffered_messages: int = 1000,
        update_interval: float = 30.0,
        max_missed_updates: int = 10,
        backoff_factor: float = 1.618,
        initial_backoff: float = 5.0
    ) -> None:
        super().__init__()
        self.session = TraxxClient(session)
        self.max_subscriptions = max_subscriptions
        self._connection_factory = functools.partial(
            TraxxConnection,
            self,
            self._loop,
            update_interval=update_interval,
            max_missed_updates=max_missed_updates,
            backoff_factor=backoff_factor,
            initial_backoff=initial_backoff
        )

        self._data_queue: asyncio.Queue = asyncio.Queue(maxsize=max_buffered_messages)

    @property
    def capacity(self) -> int:
        return self.max_subscriptions - len(self.subscriptions)

    def connection_lost(self, connection: "TraxxConnection") -> None:
        """Callback for `PIChannelConnection` indicating the connection has been lost."""
        exc = connection.exception
        if exc is not None:
            self._errors_queue.put_nowait(
                ErrorMessage(
                    exc=exc,
                    subscriptions=connection.subscriptions
                )
            )
        if connection in self._connections:
            self._connections.remove(connection)

    async def close(self) -> None:
        for connection in self._connections: connection.stop()
        await self.session.close()

    async def messages(self) -> AsyncIterable[str]:
        """Receive incoming messages for all sensor subscriptions.
        
        Yields:
            message: The result of `TraxxSensorMessage.json()`
        """
        while True:
            msg = await self._data_queue.get()
            yield msg

    async def errors(self) -> AsyncIterable[ErrorMessage]:
        """Receive errors that cause connections to fail.
        
        Yields:
            error: An instance of `ErrorMessage`
        """
        while True:
            err = await self._errors_queue.get()
            yield err

    async def subscribe(self, subscriptions: Sequence[TraxxSubscription]) -> bool:
        """Subscribe the client to a sequence of Traxx sensors.

        Args:
            subscriptions: The sequence of subscriptions to subscribe to

        Returns:
            result: A boolean indicating the success of the operation. `True` means
                that all subscriptions were successfully subscribed to. `False` means
                that none of the subscriptions were subscribed to
        """
        subscriptions: Set[TraxxSubscription] = set(subscriptions)

        if self.capacity >= len(subscriptions):
            subscriptions = subscriptions.difference(self.subscriptions)
            connections = [self._connection_factory() for _ in range(len(subscriptions))]
            for subscription, connection in zip(subscriptions, connections):
                # Connection cant fail to start
                await connection.start(subscription)
                connection.toggle()
            self._connections.extend(connections)
            return True
        return False

    async def unsubscribe(self, subscriptions: Sequence[TraxxSubscription]) -> bool:
        """Unsubscribe the client from a sequence of Traxx sensors.

        Args:
            subscriptions: The sequence of subscriptions to subscribe to

        Returns:
            result: A boolean indicating the success of the operation. `True` means
                that all subscriptions were successfully subscribed to. `False` means
                that none of the subscriptions were subscribed to
        """
        subscriptions: Set[TraxxSubscription] = set(subscriptions)
        dne = subscriptions.difference(self.subscriptions)
        subscriptions = subscriptions.difference(dne)

        if subscriptions:
            for subscription in subscriptions:
                for connection in self._connections:
                    if connection.subscriptions[0] == subscription:
                        connection.stop()
        return True