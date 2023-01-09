import itertools
import operator
from functools import partial
from itertools import groupby
from typing import Iterable, TypeVar, Optional, Union, Callable, Mapping, List

__all__ = ['first', 'groupby_as_dict', 'all_eq', 'flatten', 'flat_map']

T = TypeVar('T')
K = TypeVar('K')


def first(iter_):
    # type: (Iterable[T]) -> Optional[T]
    """
    >>> first([0, 1])
    0
    >>> first(range(2))
    0
    >>> first([]) is None
    True
    >>> first(None) is None
    True
    """
    if not iter_:
        return None
    return next(iter(iter_), None)


def groupby_as_dict(
    iter_,
    key_func,
    sort=False,
    flat=False,
    sort_func=None,
):
    # type: (Iterable[T], Callable[[T], K], bool, bool, Callable[[T], K]) -> Union[Mapping[K, List[T]], Mapping[K,T]]
    """
    >>> dict(groupby_as_dict([{"a": 1, "b": 2}, {"a": 2, "b": 3}], lambda obj: obj["a"]))
    {1: [{'a': 1, 'b': 2}], 2: [{'a': 2, 'b': 3}]}
    >>> dict(groupby_as_dict([{'a': 1}, {'a': 2}, {'a': 2}], lambda d: d['a']))
    {1: [{'a': 1}], 2: [{'a': 2}, {'a': 2}]}
    >>> dict(groupby_as_dict([{'a': 3}, {'a': 1}, {'a': 2}, {'a': 2}], lambda d: d['a'], sort=True))
    {1: [{'a': 1}], 2: [{'a': 2}, {'a': 2}], 3: [{'a': 3}]}
    >>> dict(groupby_as_dict([{'a': 1}, {'a': 2}, {'a': 2}], lambda d: d['a'], flat=True))
    {1: {'a': 1}, 2: {'a': 2}}
    """
    if sort or sort_func:
        sort_func = sort_func or key_func
        iter_ = sorted(iter_, key=sort_func)

    return {
        k: first(g) if flat else list(g)
        for k, g in groupby(iter_, key_func)
    }


def all_eq(iter_):
    """
    >>> all_eq([3, 3, 3])
    True
    >>> all_eq([1, 1, 2])
    False
    >>> all_eq([1, 2, 1])
    False
    >>> all_eq([1, 2, 1, 1])
    False
    """
    iter_ = iter(iter_)
    try:
        return all(map(partial(operator.eq, next(iter_)), iter_))
    except StopIteration:
        return True


def flatten(iter_):
    """
    >>> list(flatten([[1, 2], [3, 4]]))
    [1, 2, 3, 4]
    """
    return itertools.chain.from_iterable(iter_)


def flat_map(callable_, iter_):
    """
    >>> list(flat_map(lambda i: [i, i], range(2)))
    [0, 0, 1, 1]
    """
    return flatten(map(callable_, iter_))
