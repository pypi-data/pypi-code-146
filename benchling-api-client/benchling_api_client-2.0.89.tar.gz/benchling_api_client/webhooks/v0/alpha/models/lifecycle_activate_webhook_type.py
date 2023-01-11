from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LifecycleActivateWebhookType(Enums.KnownString):
    V0_ALPHAAPPACTIVATEREQUESTED = "v0-alpha.app.activateRequested"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LifecycleActivateWebhookType":
        if not isinstance(val, str):
            raise ValueError(f"Value of LifecycleActivateWebhookType must be a string (encountered: {val})")
        newcls = Enum("LifecycleActivateWebhookType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LifecycleActivateWebhookType, getattr(newcls, "_UNKNOWN"))
