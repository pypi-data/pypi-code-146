import dataclasses
from typing import TypeVar, Generic, Callable

T = TypeVar('T')

__all__ = ['Maybe', 'Some', 'Nothing']


class Maybe(Generic[T]):
    def or_else(self, maybe_callable: Callable[[], 'Maybe']):
        if isinstance(self, Some):
            return self
        else:
            return maybe_callable()

    def or_(self, maybe: 'Maybe'):
        if isinstance(self, Some):
            return self
        else:
            return maybe

    def unwrap(self):
        if isinstance(self, Some):
            return self.val
        else:
            raise ValueError('Нельзя вызвать unwrap для Nothing')


@dataclasses.dataclass(frozen=True)
class Some(Generic[T], Maybe[T]):
    val: T


class Nothing(Maybe):
    ...
