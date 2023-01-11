from enum import Enum


class GetAppByVersionResponse200ExecutionMode(str, Enum):
    VIEWER = "viewer"
    PUBLISHER = "publisher"
    ANONYMOUS = "anonymous"

    def __str__(self) -> str:
        return str(self.value)
