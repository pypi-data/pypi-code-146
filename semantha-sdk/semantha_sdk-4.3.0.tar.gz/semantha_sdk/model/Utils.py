from __future__ import annotations


def check_key(data: dict, key: str, type_class: type):
    assert key in dict.keys() and type(dict[key]) is type_class
