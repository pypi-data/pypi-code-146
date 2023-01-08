"""Iterator utilities."""

from typing import Callable, Iterator, List, Optional, TypeVar

_T = TypeVar("_T")


def pop_all(list_: List[_T], predicate: Callable[[_T], bool]) -> List[_T]:
    """
    Pop all elements from the list matching the given predicate.

    Order is preserved and the predicate will be called exactly once per
    element.
    """
    matches: List[_T] = []
    for index in reversed(
        [index for index, element in enumerate(list_) if predicate(element)]
    ):
        matches.insert(0, list_.pop(index))
    return matches


def pop_first(list_: List[_T], predicate: Callable[[_T], bool]) -> Optional[_T]:
    """
    Pop the first element from the list matching the given predicate.

    Order is preserved and the predicate will be called at most once per
    element.

    Returns None if no matching element is found.
    """
    for index, element in enumerate(list_):
        if predicate(element):
            return list_.pop(index)
    return None


def is_empty(iterator: Iterator[object]) -> bool:
    try:
        next(iterator)
    except StopIteration:
        return True
    return False
