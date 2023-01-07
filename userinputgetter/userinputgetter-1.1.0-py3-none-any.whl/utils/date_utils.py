import itertools
from typing import Iterable


def get_day_suffix(day_number: int) -> str:
    """
    Get the suffix portion of a date from the date number, e.g.
    2 -> 'nd', 13 -> 'th'
    """

    if not isinstance(day_number, int):
        raise TypeError("Error in get_day_suffix: 'day_number' argument must be an integer")

    if day_number in itertools.chain(range(4, 21), range(24, 31)):
        return "th"
    return ("st", "nd", "rd")[day_number % 10 - 1]
