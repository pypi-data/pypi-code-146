from collections import Counter
from functools import lru_cache
from typing import Iterable, Union

from .exception import MyException


@lru_cache(maxsize=None)
def func_count(input_string: str) -> Union[int]:
    if not isinstance(input_string, str):
        raise MyException('The data is incorrect')
    counter_func = [value for value in Counter(input_string).values() if value == 1]
    return len(counter_func)


def len_func(input_list: Iterable) -> Iterable:
    if not isinstance(input_list, Iterable):
        raise MyException('The data type is not equal to a tuple or list')
    map_func = list(map(func_count, input_list))
    return map_func
