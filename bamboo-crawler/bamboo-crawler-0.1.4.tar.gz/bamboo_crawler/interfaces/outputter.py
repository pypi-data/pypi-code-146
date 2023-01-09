from typing import Optional, Protocol, TypeVar

from .context import Context

T = TypeVar("T")


class Outputter(Protocol[T]):
    def write(self, value: T, *, context: Optional[Context[T]] = None) -> None:
        ...
