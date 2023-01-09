from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Context(Generic[T]):
    body: T

    def __init__(self, body: T, **kwargs: Any) -> None:
        self.body = body
        self.metadata = kwargs.copy()

    def add_metadata(self, **kwargs: Any) -> None:
        self.metadata.update(kwargs)
