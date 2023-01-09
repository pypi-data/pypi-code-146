from typing import Union

__all__ = ["make_plural", "possessive", "ordinal"]


def make_plural(num: Union[int, float], /, text: str) -> str:
    """Returns the plural version of the given text

    Parameters
    ----------
    num: Union[`int`, `float`]
        the number you want to use for getting the plural of text
    text: str
        the text to become plural

    Notes
    ----------
        Is this giving an incorrect plural version? Create an issue on the github repo (or PR it yourself :D)

    Returns
    ----------
    str
        the plural version
    """

    if abs(num) != 1:
        text += "s"

    return f"{num} {text}"


def possessive(text: str, /) -> str:
    """Returns the possessive version of the given text

    Parameters
    ----------
    text: `str`
        The text you want the possessive version of

    Returns
    ----------
    str
        The possessive version of the text
    """

    if text.endswith("s"):
        text += "'"
    else:
        text += "'s"

    return text


def ordinal(number: int, /) -> str:
    """Returns the ordinal version of a number

    Parameters
    ----------
    number: `int`
        the number to be turned ordinal

    Returns
    ----------
    str
        the ordinal version

    Examples
    ----------
    >>> ordinal(5)
    ... 5th

    >>> ordinal(2)
    ... 2nd
    """

    return f"{number}{'tsnrhtdd'[(number//10%10!=1)*(number%10<4)*number%10::4]}"
