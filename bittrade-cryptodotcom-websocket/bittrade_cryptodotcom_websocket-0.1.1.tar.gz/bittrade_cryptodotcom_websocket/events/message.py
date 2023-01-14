from typing import TypedDict

from typing import TYPE_CHECKING

from ..models.request import CryptodotcomRequestMessage
from .methods import MethodName


def make_sub_unsub_messages(channel: str):
    return CryptodotcomRequestMessage(
        MethodName.SUBSCRIBE, params={"channels": [channel]}
    ), CryptodotcomRequestMessage(
        MethodName.UNSUBSCRIBE, params={"channels": [channel]}
    )
