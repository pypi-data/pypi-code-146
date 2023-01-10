
from typing import Dict
from re import compile as recompile


class RegexDict:
    def __init__(self, d: Dict[str, str] = None):
        self.__data = {recompile(
            f'^{key.lstrip("^").rstrip("$")}$'): value for key, value in d.items()}

    def get(self, key, default=None, /):
        return res if (res := self[key]) else default

    def items(self):
        return self.__data.items()

    def keys(self):
        return self.__data.keys()

    def values(self):
        return self.__data.values()

    def __getitem__(self, key, /):
        key = str(key)
        for regex_key, value in self.__data.items():
            if regex_key.match(key):
                return value
        return None

    def __setitem__(self, key, value, /):
        self.__data.__setitem__(key, value)

    def __len__(self):
        return self.__data.__len__()

    def __reversed__(self):
        return self.__data.__reversed__()

    def __iter__(self):
        return self.__data.__iter__()
