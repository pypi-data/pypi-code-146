from typing import Union

__all__ = ["get_percentage", "get_percent_of"]


def get_percentage(num1: Union[int, float], num2: Union[int, float], /) -> float:
    """Returns the percentage of the smaller number, when it comes to the bigger number

    Parameters
    ----------
    number1: Union[`int`, `float`]
        the first number
    number2: Union[`int`, `float`]
        the second number

    Useage
    ----------
    ... get_percentage(5, 50)
    >>> 10.0

    ... get_percentage(25.123, 1000)
    >>> 2.5123

    Returns
    ----------
    float
        the percentage
    """

    if num1 > num2:
        big = num1
        small = num2
    else:
        big = num2
        small = num1

    return 100 * float(small) / float(big)


def get_percent_of(percentage: Union[int, float], num: Union[int, float]) -> float:
    """Returns the percentage given, of the number given

    Parameters
    ----------
    number1: Union[`int`, `float`]
        the first number
    number2: Union[`int`, `float`]
        the second number

    Useage
    ----------
    ... get_percent_of(10, 50)
    >>> 5.0

    ... get_percent_of(2.5123, 1000)
    >>> 25.123

    Returns
    ----------
    float
        the percentage
    """

    return (percentage * num) / 100.0
