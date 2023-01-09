#!/usr/bin/env python
import traceback
from pprint import pprint

import numpy as np
import pyopenms

map_ = {-1: pyopenms}


BASIC_TYPES = (int, float, str, bool, bytes, type(None))

OBJECT_PROXY = 1
ND_ARRAY = 2
PICKLED = 3


def unwrap(data):
    try:
        type_, item = data
    except Exception:
        traceback.print_stack()
        raise
    if type_ is OBJECT_PROXY:
        return get_registered(item)

    if type_ is ND_ARRAY:
        bytes_, shape, dtype = item
        return np.ndarray(shape, dtype, bytes_)

    if isinstance(item, BASIC_TYPES):
        return item

    if isinstance(item, list):
        return [unwrap(ii) for ii in item]
    if isinstance(item, tuple):
        return tuple(unwrap(ii) for ii in item)
    if isinstance(item, set):
        return set(unwrap(ii) for ii in item)
    if isinstance(item, dict):
        return {unwrap(key): unwrap(value) for key, value in item.items()}

    if type_ == PICKLED:
        print("PICKLE", item)
        return item

    raise NotImplementedError(f"don't know how to unwrap {type(item)} {repr(item)}")


def wrap(data):
    if isinstance(data, BASIC_TYPES):
        return 0, data

    if isinstance(data, list):
        return 0, [wrap(ii) for ii in data]
    if isinstance(data, tuple):
        return 0, tuple(wrap(ii) for ii in data)
    if isinstance(data, set):
        return 0, set(wrap(ii) for ii in data)
    if isinstance(data, dict):
        return 0, {wrap(key): wrap(value) for key, value in data.items()}

    if isinstance(data, np.ndarray):
        return ND_ARRAY, (data.tobytes(), data.shape, data.dtype.name)

    return OBJECT_PROXY, register(data)


def register(data):
    id_ = id(data)
    if id_ not in map_:
        # print("REGISTER", hex(id_), data)
        map_[id_] = data
    return id_


def get_registered(id_):
    try:
        return map_[id_]
    except KeyError:
        pprint({hex(id_): value for id_, value in map_.items()})
        raise
