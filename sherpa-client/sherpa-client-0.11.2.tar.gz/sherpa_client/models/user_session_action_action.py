from enum import Enum


class UserSessionActionAction(str, Enum):
    CREATE = "create"
    OPEN = "open"
    START = "start"
    PAUSE = "pause"
    STOP = "stop"
    CLOSE = "close"
    ADD_EXTRA_TIME = "add_extra_time"

    def __str__(self) -> str:
        return str(self.value)
