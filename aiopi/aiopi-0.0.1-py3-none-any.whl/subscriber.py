import asyncio
import logging
from collections.abc import AsyncIterable
from datetime import datetime
from typing import Dict, Set

from dints.abc import AbstractManager, AbstractSubscriber
from pydantic import ValidationError

from aiopi.models import PISubscriberItem, PISubscriberMessage, PISubscription



_LOGGER = logging.getLogger(__name__)


class PISubscriber(AbstractSubscriber):
    def __init__(
        self,
        subscriptions: Set[PISubscription],
        manager: AbstractManager,
        maxlen: int,
        loop: asyncio.AbstractEventLoop
    ) -> None:
        super().__init__(subscriptions, manager, maxlen, loop)
        self._chronological: Dict[str, datetime] = {
            subscription.web_id: None for subscription in subscriptions
        }
        self._data_waiter: asyncio.Future = None

    def publish(self, data: str) -> None:
        """Publish data to the subscriber. This method should only be called by
        the manager.
        """
        try:
            data = PISubscriberMessage.parse_raw(data)
        except ValidationError:
            _LOGGER.error("Message validation failed", exc_info=True, extra={"raw": data})

        super().publish(data)
        
        waiter = self._data_waiter
        self._data_waiter = None
        if waiter is not None and not waiter.done():
            waiter.set_result(None)

        _LOGGER.debug("Message published to subscriber")
    
    async def __aiter__(self) -> AsyncIterable[PISubscriberItem]:
        """Async iterable for streaming real time PI data.
        
        This method is intended to be used in event sourcing and websocket contexts.
        The generator will stream data indefinitely until shutdown by the caller
        or stopped by the stream manager due to a subscription issue in the underlying
        client.

        Yields:
            data: A dictionary containing all the data updates for a single WebId.
                This data structure can be sent directly to a client in both an event
                sourcing and websocket framework
        """
        stop = self._stop_waiter
        # If `False`, `stop` called before caller could begin iterating
        if stop is not None and not stop.done():
            # Loop forever until `stop` is called by stream manager
            while not stop.done():
                if not self._data_queue:
                    waiter = self._loop.create_future()
                    self._data_waiter = waiter

                    await asyncio.wait([waiter, stop], return_when=asyncio.FIRST_COMPLETED)
                    if not waiter.done(): # `stop` called waiting for data
                        _LOGGER.debug("Subscriber stopped while waiting for data")
                        waiter.cancel()
                        self._data_waiter = None
                        break

                # Pop messages from the data queue until there are no messages
                # left
                while True:
                    try:
                        msg: PISubscriberMessage = self._data_queue.popleft()
                    except IndexError:
                        # Empty queue
                        break
                    # Each item represents all data points for a single WebId. We
                    # only yield data for a single WebId at a time
                    for item in msg.items:
                        web_id = item.web_id
                        timestamp = item.items[-1].timestamp # Most recent timestamp
                        if web_id in self.subscriptions:
                            # Only yield the data if it is the next chronological
                            # item for that WebId. This ensures no duplicate data
                            # is sent
                            last_timestamp = self._chronological.get(web_id)
                            if last_timestamp is None or last_timestamp < timestamp:
                                yield item
                            self._chronological[web_id] = timestamp