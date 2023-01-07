import functools
from typing import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
X1 = TypeVar("X1")
R = TypeVar("R")


class _SkipUntil:
    def __init__(self, filter_method: Callable[[T], bool], inclusive: bool):
        self.found = False
        self.inclusive = inclusive
        self.filter_method = filter_method

    def check(self, t: T) -> bool:
        if self.found:
            return True
        else:
            self.found = self.filter_method(t)
            if self.inclusive and self.found:
                return True
            else:
                return False


class _StopAfter:
    def __init__(self, filter_method: Callable[[T], bool], index_after: int):
        self.indexAfter = index_after
        self.found = False
        self.filter_method = filter_method

    def check(self, t: T) -> bool:

        if not self.found:
            match = self.filter_method(t)
            if match:
                self.found = True

        if self.found:
            if self.indexAfter > -1:
                self.indexAfter -= 1
                return True
            else:
                raise StopIteration
        else:
            return True


class Chains:
    __value: Iterable[T]

    def __init__(self, value: Iterable[T]):
        self.__value = value

    def map(self, mapper: Callable[[T], R]) -> 'Chains':
        return self.of(map(mapper, self.__value))

    def skip(self, count) -> 'Chains':
        try:
            generator = (item for item in self.__value)
            for i in range(0, count):
                next(generator)
            return Chains.of(generator)
        except StopIteration:
            return self.of([])

    def skipUntil(self, filter_method: Callable[[T], bool], inclusive: bool = True) -> 'Chains':
        skip_until = _SkipUntil(filter_method, inclusive)
        return self.filter(skip_until.check)

    def stopBefore(self, filter_method: Callable[[T], bool]) -> 'Chains':
        stop_at = _StopAfter(filter_method, -1)
        return self.filter(stop_at.check)

    def stopAt(self, filter_method: Callable[[T], bool]) -> 'Chains':
        stop_at = _StopAfter(filter_method, 0)
        return self.filter(stop_at.check)

    def stopAfter(self, filter_method: Callable[[T], bool], stopAfter: int) -> 'Chains':
        if stopAfter < 0:
            raise Exception("negative number not support for stopAfter parameter")
        stopAfter = _StopAfter(filter_method, stopAfter)
        return self.filter(stopAfter.check)

    def flatMap(self, mapper: Callable[[T], Iterable[R]]) -> 'Chains':
        return self.of(
            (
                xx for x in self.__value
                for xx in mapper(x)
            )
        )

    def flatten(self) -> 'Chains':
        return self.of(
            (
                xx for x in self.__value
                for xx in x
            )
        )

    def zip(self, *its) -> 'Chains':
        return self.of(zip(self.__value, *its))

    def mapIf(self, filter_method: Callable[[T], bool], mapper: Callable[[T], R]) -> 'Chains':
        return self.filter(filter_method).map(mapper)

    def filter(self, filter_method: Callable[[T], bool]) -> 'Chains':
        return self.of(filter(filter_method, self.__value))

    def enumerate(self) -> 'Chains':
        return self.of(enumerate(self.__value))

    def len(self) -> int:
        return sum((1 for _ in self.__value))

    def foldLeft(self, init: R, reducer: Callable[[R, T], R]) -> R:
        return functools.reduce(reducer, self.__value, init)

    def reduce(self, reducer: Callable[[T, T], R]) -> R:
        return functools.reduce(reducer, self.__value)

    def list(self) -> Iterable[T]:
        return list(self.__value)

    def generator(self) -> Iterable[T]:
        return (x for x in self.__value)

    def first(self) -> T:
        g = (i for i in self.__value)
        try:
            return next(g)
        except StopIteration:
            return None

    def last(self, default_val: T = None) -> T:
        if hasattr(self.__value, '__reversed__'):
            g = (i for i in reversed(self.__value))
            try:
                return next(g)
            except StopIteration:
                return None
        else:
            for default_val in self.__value:
                pass
            return default_val

    @staticmethod
    def of(o) -> 'Chains':
        if isinstance(o, Iterable):
            return Chains(o)
        else:
            return Chains([o])
