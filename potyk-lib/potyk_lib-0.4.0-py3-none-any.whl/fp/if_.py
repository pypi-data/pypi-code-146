from typing import TypeVar, Generic, Callable, Union

__all__ = ['If', 'Then']

T = TypeVar('T')
TorCallable = Union[T, Callable[[], T]]
V = TypeVar('V')
VorCallable = Union[V, Callable[[], V]]


class _IfPart(Generic[T]):
    def __init__(self, val: TorCallable):
        self.val = val() if callable(val) else val

    def then(self, other: VorCallable) -> '_IfPart[V]': ...

    def el(self, other: VorCallable) -> '_IfPart[V]': ...

    def get(self) -> T: ...


class If(_IfPart[T]):
    """
    >>> If(True).then('then').el('else').get()
    'then'
    >>> If(False).then('then').el('else').get()
    'else'
    >>> If(True).then(lambda: 2).get()
    2
    """

    def then(self, other: VorCallable) -> _IfPart[V]: return Then.wrap(other) if self.val else self

    def el(self, other): return Then.wrap(other)


class Then(_IfPart):
    def get(self): return self.val

    def then(self, other): return self

    def el(self, other): return self

    @classmethod
    def wrap(cls, other: TorCallable) -> 'Then[T]':
        other = other() if callable(other) else other
        return other if isinstance(other, _IfPart) else cls(other)
