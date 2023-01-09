from typing import Protocol, TypeVar, Union

T_contra = TypeVar("T_contra", contravariant=True)


class SupportsDunderLT(Protocol[T_contra]):  # pragma: no cover
    def __lt__(self, __other: T_contra) -> bool:
        ...


class SupportsDunderGT(Protocol[T_contra]):  # pragma: no cover
    def __gt__(self, __other: T_contra) -> bool:
        ...


Comparable = Union[SupportsDunderLT, SupportsDunderGT]
