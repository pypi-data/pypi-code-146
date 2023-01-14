import itertools
from typing import Generator, Iterable, TypeVar

T = TypeVar('T')


def chunks(iterator: Iterable, n: int) -> Generator[Iterable, None, None]:
    iterator = iter(iterator)
    if n == 1:
        yield iterator
    else:
        for first in iterator:
            rest_of_chunk = itertools.islice(iterator, 0, n - 1)
            yield itertools.chain([first], rest_of_chunk)
