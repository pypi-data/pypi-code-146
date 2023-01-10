import itertools
from typing import Any, Tuple


def _immutable_version(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(value)
    elif isinstance(value, set):
        return frozenset(value)
    elif isinstance(value, dict):
        return tuple(sorted(value.items()))
    return value


class HashableMixin:
    def __hash__(self) -> int:
        return hash(self._value_tuple())

    def _value_tuple(self) -> Tuple[Any, ...]:
        return tuple(
            itertools.chain(
                (str(type(self))),
                (_immutable_version(val) for val in self.__dict__.values()),
            )
        )
