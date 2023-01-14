from reactivex import Observable, compose, operators
from reactivex.operators import flat_map, with_latest_from
from ..models import (
    Order,
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
)
from ..connection.request_response import wait_for_response
from ..events import MethodName
from ..rest.user_open_orders import get_user_open_orders
from returns.curry import curry
from expression import curry_flip

from .subscribe import subscribe_to_channel
from ccxt import cryptocom

exchange = cryptocom()

OpenOrdersData = list[Order]


def _subscribe_open_orders(
    messages: Observable[CryptodotcomResponseMessage], instrument: str = ""
):
    instrument = instrument.replace("/", "_")
    channel = "user.order" + "" if not instrument else f".{instrument}"
    return subscribe_to_channel(messages, channel)


def to_open_orders_entries(message: CryptodotcomResponseMessage):
    return exchange.parse_orders(message.result["data"])


def subscribe_open_orders_reload(
    messages: Observable[CryptodotcomResponseMessage],
    socket,
    instrument: str = "",
):
    def reload(x) -> Observable:
        return get_user_open_orders(messages, socket.value, instrument)

    return compose(
        _subscribe_open_orders(messages),
        flat_map(reload),
        operators.map(to_open_orders_entries),
    )


def subscribe_open_orders(
    messages: Observable[CryptodotcomResponseMessage], instrument: str = ""
):
    return _subscribe_open_orders(messages, instrument).pipe(
        operators.map(to_open_orders_entries),
    )


__all__ = [
    "subscribe_open_orders",
]
