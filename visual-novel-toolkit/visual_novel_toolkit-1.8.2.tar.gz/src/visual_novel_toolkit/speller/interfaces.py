from typing import Protocol


class Words(Protocol):
    def get(self) -> list[str]:
        raise RuntimeError

    def set(self, value: list[str]) -> None:
        raise RuntimeError
