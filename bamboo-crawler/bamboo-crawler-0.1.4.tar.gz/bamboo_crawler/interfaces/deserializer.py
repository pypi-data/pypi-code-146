from typing import Protocol, TypeVar

T = TypeVar("T", contravariant=True)
S = TypeVar("S", covariant=True)


class Deserializer(Protocol[T, S]):
    def deserialize(self, value: T) -> S:
        ...
