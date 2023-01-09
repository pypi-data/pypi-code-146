from enum import Enum


class StarJsonBodyFavoriteKind(str, Enum):
    FLOW = "flow"
    APP = "app"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
