from __future__ import annotations

from enum import IntEnum
from typing import Any, Generic, Optional, Type, TypeVar

E = TypeVar("E", bound=IntEnum)
T = TypeVar("T")


class CommandDataType(Generic[T]):
    def to_typed(self, value: Any) -> T:
        raise NotImplementedError()

    def validate(self, value: Any, raise_error: bool = True) -> bool:
        try:
            self.to_typed(value)
            return True
        except ValueError as e:
            if raise_error:
                raise e
            else:
                return False

    def to_byte(self, value: T) -> int:
        raise NotImplementedError()

    def to_byte_any(self, value: Any) -> int:
        return self.to_byte(self.to_typed(value))


class Boolean(CommandDataType[bool]):
    def to_typed(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        elif isinstance(value, int):
            return bool(value)
        elif isinstance(value, str):
            if value.lower() in ("false", "0", "off", "no"):
                return False
            elif value.lower() in ("true", "1", "on", "yes"):
                return True
            else:
                raise ValueError("cannot interpret %s as boolean value" % value)
        else:
            raise ValueError("unsupported type for normalization")

    def to_byte(self, value: bool) -> int:
        return 1 if value else 0


class Integer(CommandDataType[int]):
    def __init__(self, _min: int, _max: int) -> None:
        self._min = _min
        self._max = _max

    def to_typed(self, value: Any) -> int:
        if isinstance(value, int):
            return self._ensure_min_max(value)
        elif isinstance(value, str):
            return self._ensure_min_max(int(value))
        else:
            raise ValueError("cannot parse %s to int" % type(value))

    def to_byte(self, value: int) -> int:
        return self._ensure_min_max(value)

    def _ensure_min_max(self, value: int) -> int:
        if self._min < 0 and value > 127:
            value -= 256

        if value < self._min or value > self._max:
            raise ValueError(
                "value must between %d and %d, got %d" % (self._min, self._max, value)
            )
        else:
            return value


class OptionalInteger(CommandDataType[Optional[int]]):
    def __init__(self, _min: int, _max: int, _none: int) -> None:
        self._int = Integer(_min, _max)
        self._none = _none

    def to_typed(self, value: Any) -> Optional[int]:
        if value is None:
            return None
        elif value == self._none:
            return None
        else:
            return self._int.to_typed(value)

    def to_byte(self, value: Optional[int]) -> int:
        if value is None:
            return self._none
        else:
            return self._int.to_byte(value)


class IntegerEnum(CommandDataType[IntEnum]):
    def __init__(self, enum: Type[E]) -> None:
        self._enum = enum

    def to_typed(self, value: Any | E) -> E:
        if isinstance(value, self._enum):
            return value
        elif isinstance(value, int):
            return self._enum(value)
        elif isinstance(value, str):
            return self._enum[value.upper()]
        else:
            raise ValueError("cannot parse %s to %s" % (type(value), type(self._enum)))

    def to_byte(self, value: E) -> int:
        return value.__int__()
