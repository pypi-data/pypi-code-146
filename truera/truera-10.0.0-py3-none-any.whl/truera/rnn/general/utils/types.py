from typing import Iterable, List


def to_iterable(i):
    if not isinstance(i, Iterable):
        return [i]
    else:
        return i


def to_list(i):
    if not isinstance(i, List):
        return [i]
    else:
        return i
