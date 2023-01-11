from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class GetDatasetContentFormat(Enums.KnownString):
    CSV = "csv"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "GetDatasetContentFormat":
        if not isinstance(val, str):
            raise ValueError(f"Value of GetDatasetContentFormat must be a string (encountered: {val})")
        newcls = Enum("GetDatasetContentFormat", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(GetDatasetContentFormat, getattr(newcls, "_UNKNOWN"))
