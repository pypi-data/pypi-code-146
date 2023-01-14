from itertools import chain
from typing import Collection, List, Optional, Union


def get_all(collection: Collection, attr: str) -> List:
    return [getattr(obj, attr)
            for obj in collection
            if getattr(obj, attr)]


def get_all_flattened(collection: Collection, attr: str,
                      unique: bool = True) -> List:
    ch = chain.from_iterable(get_all(collection, attr))
    if unique:
        return list(set(ch))
    else:
        return list(ch)


def combine_all_flattened(collection: Collection, attr: str, ) -> Optional[str]:
    return ''.join(list(set(getattr(obj, attr) for obj in collection)))


def longest(collection: Collection, attr: str) -> Optional[str]:
    all_attrs = get_all(collection, attr)
    return max(all_attrs, key=len) if all_attrs else None


def highest(collection: Collection, attr: str) -> Optional[str]:
    all_attrs = get_all(collection, attr)
    return max(all_attrs) if all_attrs else None


def longest_object(collection: Collection, attr: str) -> Optional[Collection]:
    all_attrs = get_all(collection, attr)
    if all_attrs:
        index = all_attrs.index(max(all_attrs, key=len))
        return list(collection)[index]
    else:
        return None


def shortest(collection: Collection, attr: str) -> Optional[str]:
    all_attrs = get_all(collection, attr)
    return min(all_attrs) if all_attrs else None


def first(collection: Collection, attr: str) -> Optional[Union[str, int]]:
    all_attrs = get_all(collection, attr)
    return all_attrs[0] if all_attrs else None
