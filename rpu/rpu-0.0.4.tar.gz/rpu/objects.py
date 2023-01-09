from typing import Union

__all__ = ["Object"]


class Object:
    """A rebuilt object that already has basic things like a repr."""

    __slots__: Union[tuple[str], list[str]] = []

    def __repr__(self) -> str:
        data = " ".join(f"{attr}={getattr(self, attr)}" for attr in self.__slots__)
        return f"<{self.__class__.__name__} {data}>"
