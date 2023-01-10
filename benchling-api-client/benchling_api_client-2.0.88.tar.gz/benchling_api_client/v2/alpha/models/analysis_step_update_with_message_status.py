from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AnalysisStepUpdateWithMessageStatus(Enums.KnownString):
    FAILED = "FAILED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AnalysisStepUpdateWithMessageStatus":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AnalysisStepUpdateWithMessageStatus must be a string (encountered: {val})"
            )
        newcls = Enum("AnalysisStepUpdateWithMessageStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AnalysisStepUpdateWithMessageStatus, getattr(newcls, "_UNKNOWN"))
