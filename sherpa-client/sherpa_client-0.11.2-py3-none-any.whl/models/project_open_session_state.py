from enum import Enum


class ProjectOpenSessionState(str, Enum):
    NOT_EXISTS = "NOT_EXISTS"
    NEW = "NEW"
    OPEN = "OPEN"
    STARTED = "STARTED"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    CLOSED = "CLOSED"
    SAME = "SAME"

    def __str__(self) -> str:
        return str(self.value)
