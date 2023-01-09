from enum import Enum


class CategoryPatchStatus(str, Enum):
    OK = "OK"
    KO = "KO"

    def __str__(self) -> str:
        return str(self.value)
