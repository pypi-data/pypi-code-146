from typing import Optional

from reactivex import ConnectableObservable
from reactivex.operators import publish
from reactivex.abc import SchedulerBase

from .reconnect import retry_with_backoff
from .generic import raw_websocket_connection, WebsocketBundle, MARKET_URL


def public_websocket_connection(
    *, reconnect: bool = True, scheduler: Optional[SchedulerBase] = None
) -> ConnectableObservable[WebsocketBundle]:
    connection = raw_websocket_connection(MARKET_URL, scheduler=scheduler)
    if reconnect:
        connection = connection.pipe(retry_with_backoff())
    return connection.pipe(publish())


__all__ = [
    "public_websocket_connection",
]
