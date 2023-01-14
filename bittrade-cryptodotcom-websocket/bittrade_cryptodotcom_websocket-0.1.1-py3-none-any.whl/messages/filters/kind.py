from reactivex import operators
from typing import TYPE_CHECKING, Callable
from reactivex import Observable
from ...models import CryptodotcomResponseMessage


def _is_channel_message(channel: str):
    def channel_message_filter(x: CryptodotcomResponseMessage):
        # We use a startswith because channels like user.order (without instrument) actually send as user.order.ETH_USDT
        return x.method == "subscribe" and x.result.get("subscription", "").startswith(
            channel
        )

    return channel_message_filter


def keep_channel_messages(
    channel: str,
) -> Callable[
    [Observable[CryptodotcomResponseMessage]], Observable[CryptodotcomResponseMessage]
]:
    return operators.filter(_is_channel_message(channel))
