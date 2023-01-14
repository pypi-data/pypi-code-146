from typing import List, Dict, Any

from reactivex import Observable, compose, operators

from .models import CryptodotcomResponseMessage

from .channels import ChannelName
from .models.spread import SpreadPayload
from .payload import to_payload
from .subscribe import subscribe_to_channel


def to_spread_payload(message: CryptodotcomResponseMessage):
    return to_payload(message, SpreadPayload)


def subscribe_spread(pair: str, messages: Observable[Dict | List]):
    return compose(
        subscribe_to_channel(messages, ChannelName.CHANNEL_TICKER),
        operators.map(to_spread_payload),
    )


__all__ = [
    "SpreadPayload",
    "subscribe_spread",
]
