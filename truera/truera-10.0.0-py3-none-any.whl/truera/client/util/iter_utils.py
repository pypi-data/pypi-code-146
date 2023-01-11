"""
Utilities for use with iterators or iteration. Batching-related iteration is
included.

TODO: similar utilities are likely found in other parts of the codebase. Please
move them here once found.

# CSV Loading:

ChunkyCSVGenerator loads batches of rows from a CSV file without loading
everything at once. You can also use iter_csv to produce batched csv with length
using the custom iterables described below.

# Sized Iterables:

LenIterable and LenIterator provide variants of Iterable and Iterator
respectively that provide len and batch_size if they are constructed with these
parameters. This allow ones to work with potentially lazy iterations while still
having some sense of how many items there are or how larger each item is in
terms of intended batch_size.

In order to preserve the functionality in the Len* classes, you should not use
generator comprehesion notation as in:

```
    squares = (number ** 2 for number in numbers)
    odds = (number for number in numbers if number % 2 == 1)
```

This will produce a default generator object without the additional
functionality. Instead you should use the provided map and filter methods:

```
    squares = numbers.map(lambda number: number ** 2)
    odds = numbers.filter(lambda number: number % 2 == 1)
```

The result will be a LenIterable with length and batch_size equal to that of
numbers. Note though that filter preserved length even if there is
actualy filtering occuring.

# Collecting Iterables:

The custom iterator and generators in general may not be able to generate their
items multiple times. If you need to process elements from a generator, you
should try to do all processing for an element before proceeding to the next one
instead of iterating through all elements multiple times with different
processing steps. If this is difficult, and the number of items is not large,
you can collect the items as in LenIterable.collect which will load all items
into memory and then be able to generate them multiple times.
"""

from __future__ import annotations

from collections.abc import Generator
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sized
import itertools
from math import ceil
import mmap
from pathlib import Path
from typing import (
    Any, Callable, Dict, Generic, Iterable, Iterator, List, Tuple, TypeVar
)

from truera.client.util.python_utils import import_optional

pd = import_optional("pandas", "neural networks")
from tqdm.auto import tqdm

A = TypeVar("A")
B = TypeVar("B")


def tqdm_or_not(options: Dict[str, Any]) -> Callable:
    """
    Return tqdm with the given configuration options if not None, otherwise
    return identity.
    """

    tqdm_func = lambda items: tqdm(items, **options)

    if options is None:
        tqdm_func = lambda items: items

    return tqdm_func


class LenIterable(Iterable, Sized, Generic[A]):
    """
    An iterable that has a length. Still cannot index it. To preserve this
    information, do not use comprehensions but instead use the provided map
    method. Also tracks batch_size field if you pass it in.
    """

    def __init__(
        self, items: Iterable, len: int = None, batch_size: int = None
    ):
        if len is None and isinstance(items, Sized):
            len = items.__len__()

        self._batch_size = batch_size
        self._items = items
        self._len = len

    def collect(self) -> LenIterable[A]:
        """
        Return a version of this iterable that can be iterated multiple times.
        This requires listing all items first which may be memory prohibitive in
        some cases. Do not do this until after you take a subset.
        """

        items = list(self._items)
        return LenIterable(items, len=len(items), batch_size=self._batch_size)

    def enumerate(self):
        return LenIterator(
            enumerate(self), len=self._len, batch_size=self._batch_size
        )

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @staticmethod
    def of_batches(batches: Iterable, batch_size: int, total_size: int):
        return LenIterable(
            items=batches,
            len=ceil(total_size / batch_size),
            batch_size=batch_size
        )

    def unit(self):
        return f"Batch of {self._batch_size} instance(s)"

    def __tqdm_options(self, tqdm_options):
        if tqdm_options is not None and self._batch_size is not None:
            if "unit" not in tqdm_options:
                tqdm_options['unit'] = "Batch"

            tqdm_options['unit'] += f" of {self._batch_size} instance(s)"

        return tqdm_options

    def map(self,
            func: Callable[[A], B],
            tqdm_options: Dict[str, Any] = None) -> LenIterable[B]:
        """
        Maps (lazily) the items in this iterable while preserving the length
        information.
        """

        tqdm_options = self.__tqdm_options(tqdm_options)

        return LenIterable(
            tqdm_or_not(tqdm_options)(func(i) for i in self),
            len=self._len,
            batch_size=self._batch_size
        )

    def filter(
        self,
        func: Callable[[A], bool],
        tqdm_options: Dict[str, Any] = None
    ) -> LenIterable[A]:
        """
        Filters (lazily) the items in this iterable while preserving the length
        information. Length is preserved even if items are filtered out.
        """

        tqdm_options = self.__tqdm_options(tqdm_options)

        return LenIterable(
            tqdm_or_not(tqdm_options)(i for i in self if func(i)),
            len=self._len,
            batch_size=self._batch_size
        )

    def foreach(
        self,
        func: Callable[[A], None],
        tqdm_options: Dict[str, Any] = None
    ) -> None:
        """
        Evaluates the items in this iterable using the given func. Func
        is assumed to return nothing.
        """

        tqdm_options = self.__tqdm_options(tqdm_options)

        for _ in tqdm_or_not(tqdm_options)(func(i) for i in self):
            pass

    def items(self, tqdm_options: Dict[str, Any]) -> LenIterator[A]:

        tqdm_options = self.__tqdm_options(tqdm_options)

        return tqdm_or_not(tqdm_options)(iter(self))

    # Sized requirement
    def __len__(self) -> int:
        return self._len

    # Iterable requirement
    def __iter__(self) -> LenIterator[A]:
        """
        Returns an iterator over the wrapped items. 
        """
        return LenIterator(
            self._items, len=self._len, batch_size=self._batch_size
        )


class LenIterator(Generator, Sized, Generic[A]):
    """
    A generator/iterator that has a length. Also stores a batch_size field if you give it.
    """

    def __init__(
        self, items: Iterable[A], len: int = None, batch_size: int = None
    ):
        if len is None and isinstance(items, Sized):
            len = items.__len__()

        self._len = len
        self._items = items
        self._it: Iterator[A] = iter(self._items)
        self._batch_size = batch_size

    @property
    def batch_size(self) -> int:
        return self._batch_size

    # Generator requirement
    def send(self, value):
        return next(self._it)

    # Generator requirement
    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    # Sized requirement
    def __len__(self) -> int:
        return self._len


# adapted from
# https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
def num_lines(path: Path):
    """
    Get the number of lines in the given file.
    """

    with path.open("r+") as f:
        buf = mmap.mmap(f.fileno(), 0)

        lines = 0
        readline = buf.readline

        while readline():
            lines += 1

    return lines


class ChunkyCSVGenerator(Generator):
    """
    Generator for csv chunks with proper teardown on completion or deletion.
    """

    def __init__(self, path: Path, chunksize: int, *args, **kwargs):
        self._path = path
        self._chunksize = chunksize
        self._reader = None
        self._it = None

        self._args = args
        self._kwargs = kwargs

    # Generator requirement.
    def send(self, value):
        if self._reader is None:
            self._reader = pd.read_csv(
                self._path,
                chunksize=self._chunksize,
                *self._args,
                **self._kwargs
            )
            self._it = iter(self._reader)

        return next(self._it)

    # Generator requirement
    def throw(self, type=None, value=None, traceback=None):
        if self._reader is not None:
            self._reader.close()
            self._reader = None
            self._it = None

        raise StopIteration

    def __del__(self):
        if self._reader is not None:
            self._reader.close()


# TODO: CSV iterator that collects iterated items for iterating again (if memory permits)


def iter_pandas(dataframe: pd.DataFrame,
                batch_size: int = 1024) -> LenIterable[pd.DataFrame]:
    """
    Breaks up the given dataframe into batches.
    """

    assert batch_size > 0, f"batch_size:int={batch_size} must be greater than 0"

    num_rows = len(dataframe)

    def generator():
        for first_index in range(0, num_rows, batch_size):
            last_index = min(first_index + batch_size, num_rows)
            indices = list(range(first_index, last_index))
            yield dataframe.take(indices)

    return LenIterable(
        generator(), len=ceil(num_rows / batch_size), batch_size=batch_size
    )


def iter_csv(path: Path,
             chunksize: int = 1024,
             *args,
             **kwargs) -> LenIterable[pd.DataFrame]:
    """
    Read a CSV in chunksize pieces, iterating over chunksized dataframes. Extra
    args passed to Pandas.read_csv .
    """

    assert chunksize > 0, f"chunksize:int={chunksize} must be greater than 0"

    # Estimate the number of rows via the number of lines (may be an overestimate).
    rows = num_lines(path) - 1

    return LenIterable(
        ChunkyCSVGenerator(path, chunksize, *args, **kwargs),
        len=ceil(rows / chunksize),
        batch_size=chunksize
    )


def it_take(it: Iterator[A], n: int) -> List[A]:
    """
    EFFECT: take and return the first n items in the iteration. May return fewer
    at end of iterator.
    """

    ret = []

    try:
        for _ in range(n):
            ret.append(next(it))
    except StopIteration:
        pass

    return ret


def batch_len(items: Iterable[A], batch_size: int,
              len: int) -> LenIterable[List[A]]:
    it: Iterator[A] = iter(items)

    def gen():
        while True:
            batch = it_take(it, n=batch_size)
            if batch.__len__() == 0:
                return
            else:
                yield batch

    return LenIterable(gen(), len=len, batch_size=batch_size)


def batch(items: Iterable[A], batch_size: int) -> Iterable[List[A]]:
    """
    Batch the given iterable items into batches of `batch_size` (except the last
    batch potentially).
    """

    it: Iterator[A] = iter(items)

    while True:
        batch = it_take(it, n=batch_size)
        if len(batch) == 0:
            return
        else:
            yield batch


def flatten(batches: Iterable[Iterable[A]]) -> Iterable[A]:
    """
    Flatten iterables of iterables into an interable.
    """

    for batch in batches:
        for item in batch:
            yield item


def rebatch(batches: Iterable[Iterable[A]],
            batch_size: int) -> Iterable[List[A]]:
    """
    Takes batches from the given iterable and rebatches it into the given
    batch_size.
    """

    assert batch_size > 0, f"batch_size:int={batch_size} must be greater than 0"

    flat: Iterable[A] = flatten(batches)

    return batch(flat, batch_size=batch_size)


def it_peek(it: Iterator[A]) -> Tuple[A, Iterator[A]]:
    """
    Get the first value in the given iterator, returning it and an iterator that 
    still has it as the first value, i.e. peek at it.
    """

    first = next(it)
    return first, itertools.chain([first], it)
