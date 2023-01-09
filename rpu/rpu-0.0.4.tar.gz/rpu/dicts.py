from typing import TypeVar

__all__ = ["flip_dict"]

T = TypeVar("T")
D = TypeVar("D")


def flip_dict(dict_: dict[T, D], /) -> dict[D, T]:
    """Flips a dictionarys keys and values

    Parameters
    ----------
    dict_: `dict`
        the dict you want to flip

    Returns
    ----------
    dict
        the flipped dict

    Example
    ----------
    >>> flip_dict({'foo' : 'bar'})
    ... {'bar' : 'foo'}
    """

    return {v: k for k, v in dict_.items()}
