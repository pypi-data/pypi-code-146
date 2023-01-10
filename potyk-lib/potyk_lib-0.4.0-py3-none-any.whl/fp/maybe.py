import dataclasses
from typing import TypeVar, Generic, Callable

T = TypeVar('T')

__all__ = ['Maybe', 'Some', 'Nothing']


class Maybe(Generic[T]):
    def map(self, callable_):
        """
        >>> Some(123).map(lambda a: a+1).val
        124
        >>> Nothing().map(lambda a: a+1).val is None
        True
        """
        if isinstance(self, Some):
            return Some(callable_(self.val))
        else:
            return self

    def __getattr__(self, item):
        """
        >>> falsy(None).attr is None
        True
        >>> list(falsy({'a': 1}).keys())
        ['a']
        """
        if isinstance(self, Some):
            return getattr(self.val, item)
        else:
            return None

    @classmethod
    def none_guess(cls, val):
        """
        >>> isinstance(Maybe.none_guess(None), Nothing)
        True
        >>> isinstance(Maybe.none_guess(''), Some)
        True
        """

        return Nothing() if val is None else Some(val)

    @classmethod
    def falsy_guess(cls, val):
        # type: (T) -> Maybe[T]
        """
        >>> isinstance(Maybe.falsy_guess(''), Nothing)
        True
        >>> isinstance(Maybe.falsy_guess(1), Some)
        True
        """
        return Nothing() if not val else Some(val)

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

    def get(self):
        """
        >>> falsy(None).get() is None
        True
        >>> falsy(1).get()
        1
        """
        return self.val if isinstance(self, Some) else None


nullish = Maybe.none_guess
falsy = Maybe.falsy_guess


@dataclasses.dataclass(frozen=True)
class Some(Generic[T], Maybe[T]):
    val: T


class Nothing(Maybe):
    ...
