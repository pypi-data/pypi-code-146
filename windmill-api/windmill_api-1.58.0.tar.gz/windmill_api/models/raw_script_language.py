from enum import Enum


class RawScriptLanguage(str, Enum):
    DENO = "deno"
    PYTHON3 = "python3"
    GO = "go"
    BASH = "bash"

    def __str__(self) -> str:
        return str(self.value)
