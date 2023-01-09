from datetime import datetime, timedelta
from typing import AsyncIterable, Sequence

from dints.abc import AbstractTimeseriesCollection
from dints.models import BaseSubscription
from dints.timeseries.api.core import TimeseriesCollection
from dints.types import TimeseriesRow



class LocalTimeseriesCollection(AbstractTimeseriesCollection):
    """Timeseries collection using the local backend API.
    
    All data is stored in memory and this class just implements the standard
    interface for a timeseries collection.

    Args:
        subscriptions: A sequence of the subscriptions to stream data for. The
            data will be streamed in sorted order of the subscriptions (using
            the hash of the subscription).
        delta: A timedelta for the stream period.
        collection: The backend timeseries collection to iterate from
    """
    def __init__(
        self,
        subscriptions: Sequence[BaseSubscription],
        delta: timedelta,
        collection: TimeseriesCollection
    ) -> None:
        super().__init__(subscriptions, delta)
        self._collection = collection

    async def __aiter__(self) -> AsyncIterable[TimeseriesRow]:
        start = datetime.now() - self._delta
        view = self._collection.filter_by_subscription(self.subscriptions)
        async for timestamp, row in view.iter_range(start):
            yield timestamp, row