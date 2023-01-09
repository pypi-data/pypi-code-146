from __future__ import annotations

from typing import Any, Iterable, Protocol, TypeVar

from .context import Context

T = TypeVar("T", contravariant=True)
S = TypeVar("S", covariant=True)


class Processor(Protocol[T, S]):
    def process(
        self, value: T, *, context: Context[Any] | None = None
    ) -> Iterable[S]:
        ...
