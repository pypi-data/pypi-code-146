import random
import re
import string

from typing import Union

from .check import isbytes, isstr


_RANDOM_LETTERS = string.ascii_letters + string.digits


# Case

def camel_to_snake(camel_str: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


def snake_to_camel(snake_str: str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def random_str(min_l: int = 8, max_l: int = 8):
    return ''.join(random.choice(_RANDOM_LETTERS) for i in range(random.randint(min_l, max_l)))


def s2b(data: Union[bytes, str], encoding: str = 'utf-8'):
    """Convert string to bytes."""

    if isstr(data):
        return data.encode(encoding)
    if not isbytes(data):
        raise ValueError('Data is not string or bytes!')
    return data


def b2s(data: Union[bytes, str], encoding: str = 'utf-8'):
    """Convert bytes to string."""

    if isbytes(data):
        return data.decode(encoding)
    if not isstr(data):
        raise ValueError('Data is not bytes or string!')
    return data


# Text

def search_text(
    pattern: re.Pattern,
    text: str,
    group_index: int = 0,
    **kwargs
):
    """Search text by passern and return result."""

    result = re.search(pattern, text, **kwargs)
    return result[group_index] if result else None
