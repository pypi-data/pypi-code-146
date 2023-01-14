from decimal import Decimal
from reactivex import Observable, compose, operators

from ..models import CryptodotcomResponseMessage
from .subscribe import subscribe_to_channel
from ccxt import cryptocom

exchange = cryptocom()

TickerData = dict[str, str]


def to_ticker_data(message: CryptodotcomResponseMessage):
    return exchange.parse_tickers(message.result['data'])


def subscribe_ticker(pair: str, messages: Observable[CryptodotcomResponseMessage]):
    instrument = pair.replace("/", "_")  # in case we used common USDT/USD
    channel_name = f"ticker.{instrument}"
    return compose(
        subscribe_to_channel(messages, channel_name),
        operators.map(to_ticker_data),
    )


__all__ = [
    "subscribe_ticker",
]
