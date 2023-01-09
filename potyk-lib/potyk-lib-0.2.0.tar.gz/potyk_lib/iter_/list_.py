from functools import reduce
from potyk_lib.iter_.iter_ import flat_map, flatten

__all__ = ['list_wo_none', 'as_list', 'unique', 'unique_by', 'flat_map_list', 'flatten_list']


def list_wo_none(iter_):
    """
    >>> list_wo_none([1, 2, None])
    [1, 2]
    """
    return list(filter(None, iter_))


def as_list(item):
    """
    >>> as_list(1)
    [1]
    >>> as_list(None)
    []
    """
    if item is None:
        return []
    else:
        return [item]


def unique(list_):
    """
    >>> sorted(unique([2,2,3]))
    [2, 3]
    """
    return list(set(list_))


def unique_by(iter_, attr_):
    """
    >>> unique_by([1, 2, 2], '__str__')
    [1, 2]
    """
    return reduce(
        lambda unique_and_seen, item:
        unique_and_seen if getattr(item, attr_) in unique_and_seen[1] else
        ([*unique_and_seen[0], item], {*unique_and_seen[1], getattr(item, attr_)}),
        iter_,
        ([], set())
    )[0]


def flat_map_list(callable_, iter_):
    """
    >>> flat_map_list(lambda i: [i, i], range(2))
    [0, 0, 1, 1]
    """
    return list(flat_map(callable_, iter_))


def flatten_list(iter_):
    """
    >>> flatten_list([[1, 2], [3, 4]])
    [1, 2, 3, 4]
    """
    return list(flatten(iter_))
