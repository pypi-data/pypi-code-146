from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SessionMessageStyle(Enums.KnownString):
    ERROR = "ERROR"
    INFO = "INFO"
    NONE = "NONE"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SessionMessageStyle":
        if not isinstance(val, str):
            raise ValueError(f"Value of SessionMessageStyle must be a string (encountered: {val})")
        newcls = Enum("SessionMessageStyle", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SessionMessageStyle, getattr(newcls, "_UNKNOWN"))
