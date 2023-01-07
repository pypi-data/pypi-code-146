import json
import os
import sys
from typing import Dict, List, Union

from rich.console import Console

from norma2.config.config_class import Config

__FILE_NAME = ".norma2.json"


def _append(l1: list, elem, key: str) -> list:
    if elem in l1:
        print(f"{elem} is already in {key} (= {l1})", file=sys.stderr)
        return l1
    l1.append(elem)
    return l1


def _remove(l1: list, elem, key: str) -> list:
    if elem not in l1:
        print(f"{elem} is not in {key} (= {l1})", file=sys.stdout)
    l1.remove(elem)
    return l1


def from_json(console: Console, conf_path: str = ".") -> Config:
    conf = Config(console)
    filepath = os.path.join(conf_path, __FILE_NAME)
    if not os.path.isfile(filepath):
        return conf
    with open(filepath) as file:
        data: Dict[str, Union[str, List[str], bool]] = json.load(file)
    for key, value in data:
        if not hasattr(Config(console), key) and not hasattr(
            Config(console), f"{key.replace('no_', '', 1)}"
        ):
            print(f"{key} don't exists in config", file=sys.stdout)
            continue
        func, name = None, None
        if key.startswith("no_") and isinstance(value, list):
            func, name = _remove, key.replace("no_", "", 1)
        elif isinstance(value, list):
            func, name = _append, key
        if func is not None and name is not None:
            setattr(conf, name, func(getattr(conf, name), value, name))
        else:
            setattr(conf, key, value)
    return conf
