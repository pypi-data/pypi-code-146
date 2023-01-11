from datetime import datetime  # noqa: F401
from enum import Enum
from pathlib import Path
from typing import Any, Collection, Mapping, Union

from typepigeon.to_type import to_type


def to_json(input_value: Any) -> Union[str, float, int, dict, list, bool]:
    """
    convert the given value to a JSON-compatible format

    :param input_value: value to convert
    :return: JSON value

    >>> to_json(5)
    5
    >>> to_json('5')
    '5'

    >>> to_json(datetime(2021, 3, 26))
    '2021-03-26 00:00:00'

    >>> to_json([5, '6', {3: datetime(2021, 3, 27)}])
    [5, '6', {3: '2021-03-27 00:00:00'}]
    >>> to_json({'test': [5, '6', {3: datetime(2021, 3, 27)}]})
    {'test': [5, '6', {3: '2021-03-27 00:00:00'}]}
    """

    if isinstance(input_value, Path):
        input_value = input_value.as_posix()
    elif isinstance(input_value, Enum):
        input_value = input_value.name
    if type(input_value) not in (float, int, bool, str):
        if isinstance(input_value, Collection) and not isinstance(input_value, str):
            input_value = {to_json(key): to_json(entry) for key, entry in input_value.items()} if isinstance(input_value, Mapping) else [to_json(entry) for entry in input_value]
        else:
            try:
                input_value = to_type(input_value, float)
            except:
                try:
                    input_value = to_type(input_value, int)
                except:
                    try:
                        input_value = to_type(input_value, bool)
                    except:
                        input_value = to_type(input_value, str)
    return input_value
