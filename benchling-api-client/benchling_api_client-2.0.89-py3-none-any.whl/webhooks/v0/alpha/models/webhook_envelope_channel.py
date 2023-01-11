from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class WebhookEnvelopeChannel(Enums.KnownString):
    APP_SIGNALS = "app_signals"
    EVENTS = "events"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "WebhookEnvelopeChannel":
        if not isinstance(val, str):
            raise ValueError(f"Value of WebhookEnvelopeChannel must be a string (encountered: {val})")
        newcls = Enum("WebhookEnvelopeChannel", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(WebhookEnvelopeChannel, getattr(newcls, "_UNKNOWN"))
