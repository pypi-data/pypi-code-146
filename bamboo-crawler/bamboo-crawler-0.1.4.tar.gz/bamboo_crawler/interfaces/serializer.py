from typing import Protocol, TypeVar

T = TypeVar("T", contravariant=True)
S = TypeVar("S", covariant=True)


class Serializer(Protocol[T, S]):
    def serialize(self, value: T) -> S:
        ...
