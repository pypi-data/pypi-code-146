from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SessionStatus(Enums.KnownString):
    COMPLETED_WITH_WARNINGS = "COMPLETED_WITH_WARNINGS"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    TIMEOUT = "TIMEOUT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SessionStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of SessionStatus must be a string (encountered: {val})")
        newcls = Enum("SessionStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SessionStatus, getattr(newcls, "_UNKNOWN"))
