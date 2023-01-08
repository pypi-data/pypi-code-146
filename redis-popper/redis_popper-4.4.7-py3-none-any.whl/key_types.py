from enum import Enum


class KeyCacheProp(Enum):
    DEFAULT = 1,
    WRITE_ONCE = 2


"""
Currently supported commands with WRITE_ONCE:
    GET,
    HGET,
    HGETALL,
    HMGET,
"""


# For now we only support single level key suffixes
# dict [key_suffix (str) -> KeyCacheProp]
def get_key_type(key: str, key_types):
    toks = key.split(":")
    suffix = toks[-1] if len(toks) > 1 else ""
    return key_types.get(suffix, KeyCacheProp.DEFAULT)
