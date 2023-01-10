from datetime import date, time
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def from_none(x: Any) -> None:
    """Get from a None object

    Args:
        x (Any): Object to get its value

    Raises:
        AssertionError: if x is not None

    Returns:
        None: if x is None
    """
    assert x is None
    return x


def from_str(x: Any) -> str:
    """Get from a string object

    Args:
        x (Any): Object to get its value

    Raises:
        AssertionError: if x is not a string

    Returns:
        str: if x is a string
    """
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    """Get from a boolean object

    Args:
        x (Any): Object to get its value

    Raises:
        AssertionError: if x is not a boolean

    Returns:
        bool: if x is a boolean
    """
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    """Get from an integer object

    Args:
        x (Any): Object to get its value

    Raises:
        AssertionError: if x is not an integer

    Returns:
        int: if x is an integer
    """
    assert isinstance(x, int)
    return x


def from_float(x: Any) -> float:
    """Get from a float object

    Args:
        x (Any): Object to get its value

    Raises:
        AssertionError: if x is not a float

    Returns:
        float: if x is a float
    """
    assert isinstance(x, float)
    return x


def from_union(fs, x):
    """Get from a object that can be given as argument to any of the given functions

    Args:
        fs (list[Callable[[Any], T]]): List of functions to get the object
        x (Any): Object to get its value

    Raises:
        AssertionError: if x is not suitable for any of the given functions

    Returns:
        func(x): if x is one of the given types
    """
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> list[T]:
    """Get from a list object such that its elements can be given as argument to the given function

    Args:
        f (Callable[[Any], T]): Function to handle the list elements
        x (Any): Object to get its value

    Raises:
        AssertionError: if x is not an list

    Returns:
        list[T]: if x is a list and its elements can be given as argument to the given function
    """
    assert isinstance(x, list)
    return [f(y) for y in x]


def str_to_time(string: Any) -> time:
    """Converts a string in the "HH:MM" format to time object

    Args:
        string (Any): String to convert

    Returns:
        time: Time object
    """
    string = from_str(string)
    str_list = string.split(":")
    return time(hour=int(str_list[0]), minute=int(str_list[1]))


def str_to_date(string: Any) -> date:
    """Converts a string in the "DD;MM;YYYY" format of to date object

    Args:
        string (Any): String to convert

    Returns:
        date: Date object
    """
    string = from_str(string)
    str_list = string.split(";")
    return date(year=int(str_list[2]), month=int(str_list[1]), day=int(str_list[0]))


def str_to_float(string: Any) -> float | None:
    """Converts a string to float object

    Args:
        string (Any): String to convert

    Returns:
        float: if string can be converted to float
        None: if string can not be converted to float
    """
    string = from_str(string)

    if string == "":
        return None
    return float(from_str(string).replace(",", "."))


def month_to_int(month: Any) -> int:
    """Converts a month string to integer

    Args:
        month (Any): Month string to convert

    Raises:
        AssertionError: If month is not a month

    Returns:
        int: int value of the month if month is a month
    """
    match from_str(month).lower():
        case "ocak":
            return 1
        case "şubat":
            return 2
        case "mart":
            return 3
        case "nisan":
            return 4
        case "mayıs":
            return 5
        case "haziran":
            return 6
        case "temmuz":
            return 7
        case "ağustos":
            return 8
        case "eylül":
            return 9
        case "ekim":
            return 10
        case "kasım":
            return 11
        case "aralık":
            return 12
        case _:
            raise AssertionError(f"{month} is not a month")


def day_to_int(day: Any) -> int:
    """Converts a day string to integer

    Args:
        day (Any): Day string to convert

    Raises:
        AssertionError: If day is not a day

    Returns:
        int: int value of the day if day is a day
    """
    match from_str(day).lower():
        case "pazartesi":
            return 0
        case "salı":
            return 1
        case "çarşamba":
            return 2
        case "perşembe":
            return 3
        case "cuma":
            return 4
        case "cumartesi":
            return 5
        case "pazar":
            return 6
        case _:
            raise AssertionError(f"{day} is not a day")
