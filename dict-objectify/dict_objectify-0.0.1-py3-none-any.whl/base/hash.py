import hashlib
from collections.abc import Iterable
from typing import Any

from dict_objectify.base.constants import NONE_EQUIVALENT_VALUES


def dict_base_hash(value: Any) -> int:
    if value in NONE_EQUIVALENT_VALUES:
        return 0
    elif isinstance(value, str):
        return __int_hash(value)
    elif isinstance(value, (int, float, bool)):
        return __int_hash(str(value))
    elif isinstance(value, dict):
        return sum([dict_base_hash(f'{k}{dict_base_hash(v)}')
                    for k, v in value.items()
                    if v not in NONE_EQUIVALENT_VALUES])
    elif isinstance(value, Iterable):
        return sum([dict_base_hash(_value) for _value in value])
    else:
        raise AttributeError(f'Hashing function received unsupported '
                             f'[Value: {value}] of [Type: {type(value)}].')


def __int_hash(value: str, length: int = 20) -> int:
    return int(hashlib.sha256(
        value.encode('utf-8')).hexdigest(), 16) % 10 ** length
