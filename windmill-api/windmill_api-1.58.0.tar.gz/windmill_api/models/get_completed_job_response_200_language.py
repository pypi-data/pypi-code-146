from enum import Enum


class GetCompletedJobResponse200Language(str, Enum):
    PYTHON3 = "python3"
    DENO = "deno"
    GO = "go"
    BASH = "bash"

    def __str__(self) -> str:
        return str(self.value)
