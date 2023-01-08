#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

"""ProtoBuf serialization and deserialization."""
from __future__ import annotations

import itertools
import struct
import typing
from typing import Any, Iterable, List

import numpy as np

from modalic.utils import protocol, shared


@typing.no_type_check
def weights_to_parameters(
    weights: shared.Weights, dtype: str, model_version: int
) -> protocol.Parameters:
    r"""Convert NumPy weights to parameters object."""
    tensor = _weights_to_bytes(weights, _dtype_to_struct(dtype))
    return protocol.Parameters(
        tensor=tensor, data_type=dtype, model_version=model_version
    )


@typing.no_type_check
def parameters_to_weights(
    parameters: protocol.Parameters,
    shapes: List[np.ndarray[int, np.dtype[Any]]],
    dtype: str,
) -> shared.Weights:
    r"""Convert parameters object to NumPy weights."""
    return _bytes_to_ndarray(parameters.tensor, shapes, _dtype_to_struct(dtype))


def _ndarray_to_bytes(
    ndarray: np.ndarray[Any, np.dtype[Any]], sdtype: str
) -> List[int]:
    r"""Serialize NumPy ndarray to list of u8 bytes."""
    res: list[int] = list()
    for single in np.nditer(ndarray):
        res.extend(struct.pack(sdtype, single))
    return res


def _weights_to_bytes(weights: shared.Weights, dtype: str) -> bytes:
    r"""Serialize NumPy ndarray to bytes."""
    layers = [_ndarray_to_bytes(ndarray, dtype) for ndarray in weights]
    return bytes(list(itertools.chain(*layers)))


def _bytes_to_ndarray(
    tensor: bytes, layer_shape: List[np.ndarray], sdtype: str
) -> shared.Weights:
    r"""Deserialize NumPy ndarray from u8 bytes."""
    layer: list[Any] = list()
    if sdtype == "!f":
        for content in _chunk(tensor, 4):
            layer.append(struct.unpack(">f", bytes(content)))
    elif sdtype == "!d":
        for content in _chunk(tensor, 8):
            layer.append(struct.unpack(">d", bytes(content)))
    else:
        raise TypeError(f"data type '{sdtype}' is not known.")

    layers = np.split(np.array(layer), _indexing([np.prod(s) for s in layer_shape]))

    return [np.reshape(layer, shapes) for layer, shapes in zip(layers, layer_shape)]


def _chunk(iterable: Iterable[Any], chunksize: int) -> zip[Any]:
    r"""helper chunking an iterable with fixed size."""
    return zip(*[iter(iterable)] * chunksize)


def _indexing(length: List[int]) -> List[int]:
    r"""helper for preparing the indices at which array is splitted."""
    for idx, _ in enumerate(length):
        if idx == 0:
            continue
        if (idx - 1) == len(length):
            break
        length[idx] += length[idx - 1]
    return length


def _dtype_to_struct(dtype: str) -> str:
    r"""Prepare dtype for conversion with struct.

    :param dtype: String that represents the data type that is used for the model.
    :raises TypeError: When dtype is unkown. Choose 'F32' or 'F64'.
    """
    if dtype == "F32":
        return "!f"
    elif dtype == "F64":
        return "!d"
    else:
        raise TypeError(f"data type '{dtype}' is not known.")
