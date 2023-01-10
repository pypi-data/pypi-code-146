from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LifecycleDeactivateWebhookType(Enums.KnownString):
    V0_ALPHAAPPDEACTIVATED = "v0-alpha.app.deactivated"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LifecycleDeactivateWebhookType":
        if not isinstance(val, str):
            raise ValueError(f"Value of LifecycleDeactivateWebhookType must be a string (encountered: {val})")
        newcls = Enum("LifecycleDeactivateWebhookType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LifecycleDeactivateWebhookType, getattr(newcls, "_UNKNOWN"))
