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
"""Common Functions for De-/Serialization"""
import itertools
from typing import List

import numpy as np


def _indexing(length: List[int]) -> List[int]:
    r"""helper for preparing the indices at which array is splitted."""
    for idx, _ in enumerate(length):
        if idx == 0:
            continue
        if (idx - 1) == len(length):
            break
        length[idx] += length[idx - 1]
    return length


def _float_to_np_ndarray(tensor: list, layer_shape: List[np.ndarray]) -> list:
    r"""Deserialize NumPy ndarray from u8 bytes."""
    layers = np.split(np.array(tensor), _indexing([np.prod(s) for s in layer_shape]))

    return [np.reshape(layer, shapes) for layer, shapes in zip(layers, layer_shape)]


def _np_ndarray_to_float(ndarray: np.ndarray) -> list:
    r"""Serialize NumPy ndarray to list of u8 bytes."""
    return [float(single) for single in np.nditer(ndarray)]


def _ser_np_weights(weights: list) -> list:
    r"""Serialize NumPy ndarray to bytes."""
    layers = [_np_ndarray_to_float(ndarray) for ndarray in weights]
    return list(itertools.chain(*layers))
