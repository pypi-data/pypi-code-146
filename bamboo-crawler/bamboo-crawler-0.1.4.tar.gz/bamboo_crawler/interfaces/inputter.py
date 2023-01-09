from typing import Protocol, TypeVar

from .context import Context

T = TypeVar("T")


class Inputter(Protocol[T]):
    def read(self) -> Context[T]:
        ...

    def done(self) -> None:
        ...
