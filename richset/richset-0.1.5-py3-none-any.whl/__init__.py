from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import (
    Callable,
    Generic,
    Hashable,
    Iterable,
    Iterator,
    Literal,
    TypeVar,
    overload,
)

from .comparable import Comparable

T = TypeVar("T")
S = TypeVar("S")
Key = TypeVar("Key", bound=Hashable)
OnDuplicateActions = Literal["error", "first", "last"]


@dataclass(frozen=True)
class RichSet(Generic[T]):
    records: tuple[T, ...]

    # factory classmethods

    @classmethod
    def from_list(cls, lst: list[T]) -> RichSet[T]:
        """Returns a new RichSet from a list."""
        return cls.from_iterable(lst)

    @classmethod
    def from_tuple(cls, tpl: tuple[T, ...]) -> RichSet[T]:
        """Returns a new RichSet from a tuple."""
        return cls.from_iterable(tpl)

    @classmethod
    def from_set(cls, s: set[T]) -> RichSet[T]:
        """Returns a new RichSet from a set."""
        return cls.from_iterable(s)

    @classmethod
    def from_frozenset(cls, s: frozenset[T]) -> RichSet[T]:
        """Returns a new RichSet from a frozenset."""
        return cls.from_iterable(s)

    @classmethod
    def from_iterable(cls, itr: Iterable[T]) -> RichSet[T]:
        """Returns a new RichSet from an iterable."""
        return cls(tuple(itr))

    @classmethod
    def from_empty(cls) -> RichSet[T]:
        """Returns an empty RichSet."""
        return cls(records=())

    # magic methods

    def __iter__(self) -> Iterator[T]:
        return iter(self.records)

    def __len__(self) -> int:
        return self.size()

    # conversions

    def to_list(self) -> list[T]:
        """Returns a list of records."""
        return list(self.records)

    def to_tuple(self) -> tuple[T, ...]:
        """Returns a tuple of records."""
        return tuple(self.records)

    def to_set(
        self,
    ) -> set[T]:  # intersection of T & Hashable
        """Returns a set of records."""
        for r in self.records:
            if not isinstance(r, Hashable):
                raise TypeError(f"non-hashable record: {r}")
        return set(self.records)

    def to_frozenset(
        self,
    ) -> frozenset[T]:  # intersection of T & Hashable
        """Returns a frozenset of records."""
        return frozenset(self.to_set())

    def to_dict(
        self,
        key: Callable[[T], Key],
        *,
        duplicated: OnDuplicateActions | Callable[[list[T]], T] = "error",
    ) -> dict[Key, T]:
        """Returns a dictionary mapping keys to values.

        if duplicated is 'error' (default), raises an error if \
there are multiple records with the same key.
        if duplicated is 'first', returns the first record with the same key.
        if duplicated is 'last', returns the last record with the same key."""
        base = self.to_dict_of_list(key=key)

        if duplicated == "error":
            if len(base) != self.size():
                raise ValueError("duplicate keys")
            return {k: v[0] for k, v in base.items()}
        elif duplicated == "first":
            return {k: v[0] for k, v in base.items()}
        elif duplicated == "last":
            return {k: v[-1] for k, v in base.items()}
        else:
            return {k: duplicated(v) for k, v in base.items()}

    def to_dict_of_list(
        self,
        key: Callable[[T], Key],
    ) -> dict[Key, list[T]]:
        """Returns a dictionary mapping keys to lists of values."""
        d: dict[Key, list[T]] = {}
        for r in self.records:
            k = key(r)
            if k not in d:
                d[k] = []
            d[k].append(r)
        return d

    # list accessors

    @overload
    def get_first(self) -> T | None:
        ...

    @overload
    def get_first(self, default: S) -> T | S:
        ...

    def get_first(self, default: S | None = None) -> T | S | None:
        """Returns the first record in the RichSet
        or default value (None) if the RichSet is empty."""
        if self.records:
            return self.records[0]
        return default

    def first(self) -> T:
        """Returns the first record in the RichSet."""
        if self.records:
            return self.records[0]
        raise IndexError("RichSet is empty")

    @overload
    def get_last(self) -> T | None:
        ...

    @overload
    def get_last(self, default: S) -> T | S:
        ...

    def get_last(self, default: S | None = None) -> T | S | None:
        """Returns the last record in the RichSet
        or default value (None) if the RichSet is empty."""
        if self.records:
            return self.records[-1]
        return default

    def last(self) -> T:
        """Returns the last record in the RichSet."""
        if self.records:
            return self.records[-1]
        raise IndexError("RichSet is empty")

    def nth(self, index: int) -> T:
        """Returns the record at the given index."""
        if index < self.size():
            return self.records[index]
        raise IndexError("index out of range")

    @overload
    def get_nth(self, index: int) -> T | None:
        ...

    @overload
    def get_nth(self, index: int, default: S) -> T | S:
        ...

    def get_nth(self, index: int, default: S | None = None) -> T | S | None:
        """Returns the record at the given index
        or default value (None) if the index is out of range."""
        if index < self.size():
            return self.records[index]
        return default

    def one(self) -> T:
        """Returns the one record in the RichSet.

        Currently this method is exactly equivalent to `first()`.
        But this method is intended to be used in uncertain order.
        So this method might not returns not the first record in the future.
        """
        return self.first()

    @overload
    def get_one(self) -> T | None:
        ...

    @overload
    def get_one(self, default: S) -> T | S:
        ...

    def get_one(self, default: S | None = None) -> T | S | None:
        """Returns the one record in the RichSet
        or default value (None) if the RichSet is empty.

        See also `one()`."""
        return self.get_first(default)

    # list manipulations

    def filter(self, f: Callable[[T], bool]) -> RichSet[T]:
        """Returns a new RichSet with filtered records."""
        return RichSet.from_list(list(filter(f, self.records)))

    def unique(self, key: Callable[[T], Key]) -> RichSet[T]:
        """Returns a new RichSet with unique records."""
        new_records = []
        seen = set()
        for r in self.records:
            key_ = key(r)
            if key_ not in seen:
                new_records.append(r)
                seen.add(key_)
        return RichSet.from_list(new_records)

    def map(self, f: Callable[[T], S]) -> RichSet[S]:
        """Returns a new RichSet with mapped records."""
        return RichSet.from_list(list(map(f, self.records)))

    def reduce(
        self,
        fn: Callable[[S, T], S],
        initial: S,
    ) -> S:
        """Returns a reduced value."""
        return functools.reduce(fn, self.records[:], initial)

    def slice(self, start: int, stop: int) -> RichSet[T]:
        """Returns a new RichSet with sliced records."""
        return RichSet.from_tuple(self.records[start:stop])

    def divide_at(self, index: int) -> tuple[RichSet[T], RichSet[T]]:
        """Returns a tuple of two RichSets,
        where the first contains records before the index,
        and the second contains records after the index."""
        return (
            self.slice(0, index),
            self.slice(index, self.size()),
        )

    def pushed(self, record: T) -> RichSet[T]:
        """Returns a new RichSet with the given record pushed to the end."""
        return RichSet.from_tuple(self.records + (record,))

    def pushed_all(self, records: Iterable[T]) -> RichSet[T]:
        """Returns a new RichSet with the given records pushed to the end."""
        return RichSet.from_tuple(self.records + tuple(records))

    def unshifted(self, record: T) -> RichSet[T]:
        """Returns a new RichSet with the given record \
unshifted to the beginning."""
        return RichSet.from_tuple((record,) + self.records)

    def unshifted_all(self, records: Iterable[T]) -> RichSet[T]:
        """Returns a new RichSet with the given records \
unshifted to the beginning."""
        return RichSet.from_tuple(tuple(records) + self.records)

    def popped(self) -> tuple[T, RichSet[T]]:
        """Returns a tuple of the popped record and a new RichSet."""
        if self.is_empty():
            raise IndexError("pop from empty RichSet")
        copied = self.to_list()
        return copied.pop(), RichSet.from_list(copied)

    def popped_n(self, n: int) -> tuple[RichSet[T], RichSet[T]]:
        """Returns a tuple of the popped records and a new RichSet.

        similar to divide_at, but popped records are reversed."""
        if self.size() < n:
            raise IndexError("pop more than size")
        remains, popped_r = self.divide_at(-n)
        return popped_r.reversed(), remains

    def shifted(self) -> tuple[T, RichSet[T]]:
        """Returns a tuple of the shifted record and a new RichSet."""
        if self.is_empty():
            raise IndexError("shift from empty RichSet")
        copied = self.to_list()
        return copied.pop(0), RichSet.from_list(copied)

    def shifted_n(self, n: int) -> tuple[RichSet[T], RichSet[T]]:
        """Returns a tuple of the shifted records and a new RichSet.

        (same as divide_at(n))"""
        if self.size() < n:
            raise IndexError("shift more than size")
        return self.divide_at(n)

    # search

    def index_of(
        self,
        predicate: Callable[[T], bool],
        *,
        reverse: bool = False,
    ) -> int:
        """Returns the index of the first record satisfying the predicate.

        returns -1 if no record satisfies the predicate."""
        if reverse:
            size = self.size()
            for i, item in enumerate(reversed(self.records)):
                if predicate(item):
                    return size - i - 1
            return -1

        for i, r in enumerate(self.records):
            if predicate(r):
                return i
        return -1

    def indices_of(self, predicate: Callable[[T], bool]) -> list[int]:
        """Returns a list of indices of records satisfying the predicate."""
        return [i for i, r in enumerate(self.records) if predicate(r)]

    def search_first(
        self,
        predicate: Callable[[T], bool],
    ) -> tuple[int, T | None]:
        """Returns the first record satisfying the predicate.

        if no record satisfies the predicate, returns (-1, None)."""
        idx = self.index_of(predicate)
        if idx == -1:
            return (-1, None)
        return (idx, self.records[idx])

    def search_last(
        self,
        predicate: Callable[[T], bool],
    ) -> tuple[int, T | None]:
        """Returns the last record satisfying the predicate.

        if no record satisfies the predicate, returns (-1, None)."""
        idx = self.index_of(predicate, reverse=True)
        if idx == -1:
            return (-1, None)
        return (idx, self.records[idx])

    def search_all(
        self,
        predicate: Callable[[T], bool],
    ) -> list[tuple[int, T]]:
        """Returns a list of tuples of indices and records
        satisfying the predicate.

        returns an empty list if no record satisfies the predicate."""
        indices = self.indices_of(predicate)
        return [(i, self.records[i]) for i in indices]

    # set operations

    def union(self, other: RichSet[T]) -> RichSet[T]:
        """Returns a new RichSet with the union of the records."""
        return RichSet.from_list(list(set(self.records) | set(other.records)))

    def intersection(self, other: RichSet[T]) -> RichSet[T]:
        """Returns a new RichSet with the intersection of the records."""
        return RichSet.from_list(list(set(self.records) & set(other.records)))

    def difference(self, other: RichSet[T]) -> RichSet[T]:
        """Returns a new RichSet with the difference of the records."""
        return RichSet.from_list(list(set(self.records) - set(other.records)))

    def symmetric_difference(self, other: RichSet[T]) -> RichSet[T]:
        """Returns a new RichSet with the \
symmetric difference of the records."""
        return RichSet.from_list(list(set(self.records) ^ set(other.records)))

    def is_subset(self, other: RichSet[T]) -> bool:
        """Returns True if self is a subset of other."""
        return set(self.records).issubset(set(other.records))

    def is_superset(self, other: RichSet[T]) -> bool:
        """Returns True if self is a superset of other."""
        return set(self.records).issuperset(set(other.records))

    def is_disjoint(self, other: RichSet[T]) -> bool:
        """Returns True if self and other are disjoint."""
        return set(self.records).isdisjoint(set(other.records))

    def is_equal_as_set(self, other: RichSet[T]) -> bool:
        """Returns True if self and other are same set."""
        return set(self.records) == set(other.records)

    # sortings

    def sorted(
        self,
        *,
        key: Callable[[T], Comparable],
        reverse: bool = False,
    ) -> RichSet[T]:
        """Returns a new RichSet sorted bythe given key."""
        sorted_ = tuple(sorted(self.records, key=key, reverse=reverse))
        return RichSet.from_tuple(sorted_)

    def reversed(self) -> RichSet[T]:
        """Returns a new RichSet with reversed records."""
        return RichSet.from_tuple(self.records[::-1])

    # statistics

    def is_empty(self) -> bool:
        """Returns True if the RichSet is empty."""
        return not self.records

    def is_non_empty(self) -> bool:
        """Returns True if the RichSet is non-empty."""
        return not self.is_empty()

    def size(self) -> int:
        """Returns the number of records in the RichSet."""
        return len(self.records)

    def count(self, predicate: Callable[[T], bool]) -> int:
        """Returns the number of records satisfying the predicate."""
        return sum(1 for r in self.records if predicate(r))

    # groupings

    def group_by(
        self,
        key: Callable[[T], Key],
    ) -> dict[Key, RichSet[T]]:
        """Returns a dict of RichSets grouped by the given key."""
        return {
            k: RichSet.from_list(list(v))
            for k, v in self.to_dict_of_list(key).items()
        }

    def size_of_group_by(
        self,
        key: Callable[[T], Key],
    ) -> dict[Key, int]:
        """Returns a dict of sizes of RichSets grouped by the given key."""
        return {k: v.size() for k, v in self.group_by(key).items()}

    def count_of_group_by(
        self, *, key: Callable[[T], Key], predicate: Callable[[T], bool]
    ) -> dict[Key, int]:
        """Returns a dict of the number of records satisfying \
the predicate grouped by the given key."""
        return {k: v.count(predicate) for k, v in self.group_by(key).items()}

    def aggregate_by(
        self,
        *,
        key: Callable[[T], Key],
        fn: Callable[[S, T], S],
        initial: S,
    ) -> dict[Key, S]:
        """Returns a dict of aggregated values grouped by the given key."""
        return {
            k: v.reduce(fn, initial=initial)
            for k, v in self.group_by(key).items()
        }
