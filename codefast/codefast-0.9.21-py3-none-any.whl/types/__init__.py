#!/usr/bin/env python
from typing import Dict, List, Tuple, Union


class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self) -> str:
        _dict = {}
        for k, v in self.__dict__.items():
            _dict[k] = v.__dict__ if isinstance(v, Struct) else v
        return str(_dict)

    def __getitem__(self, key):
        return self.__dict__[key]


def make_obj(
        obj: Union[Dict, List, Tuple,
                   Struct]) -> Union[Dict, List, Tuple, Struct]:
    if isinstance(obj, dict):
        _struct = Struct()
        for k, v in obj.items():
            if isinstance(v, dict) or isinstance(v, list):
                _struct.__dict__[k] = make_obj(v)
            else:
                _struct.__dict__[k] = v
        return _struct
    elif isinstance(obj, list):
        return [make_obj(o) for o in obj]
    else:
        return obj


def encapsulate(
        obj: Union[Dict, List, Tuple,
                   Struct]) -> Union[Dict, List, Tuple, Struct]:
    return make_obj(obj)
