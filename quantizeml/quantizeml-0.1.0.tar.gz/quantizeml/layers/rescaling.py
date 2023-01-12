#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
import tensorflow as tf
import keras

from ..tensors import FixedPoint, QFloat

__all__ = ["QuantizedRescaling"]


@tf.keras.utils.register_keras_serializable()
class QuantizedRescaling(keras.layers.Rescaling):
    """A layer that multiplies integer inputs by a scale

    This is a simplified version of the keras Rescaling layer:

    - it only supports a scalar scale,
    - it only supports zero offsets.

    This layer assumes the inputs are 8-bit integer: it simply wraps them into
    an 8-bit per-tensor QFloat with the specified scale.

    Args:
        scale (float): a scalar scale.
    """

    def __init__(self, scale, **kwargs):
        super().__init__(scale, **kwargs)
        if tf.rank(self.scale) > 0:
            raise ValueError("QuantizedRescaling only accepts scalar scale.")
        if tf.reduce_any(self.offset != 0):
            raise ValueError("QuantizedRescaling only accepts zero offset.")

    def call(self, inputs):
        # Assume the inputs are 8-bit unsigned integer
        fp = FixedPoint(tf.round(inputs), 8, 0)
        # Wrap them into a QFloat with the specified scale
        return QFloat(fp, self.scale)
