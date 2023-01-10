from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CanvasInitializeWebhookType(Enums.KnownString):
    V0_BETACANVASINITIALIZED = "v0-beta.canvas.initialized"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CanvasInitializeWebhookType":
        if not isinstance(val, str):
            raise ValueError(f"Value of CanvasInitializeWebhookType must be a string (encountered: {val})")
        newcls = Enum("CanvasInitializeWebhookType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CanvasInitializeWebhookType, getattr(newcls, "_UNKNOWN"))
