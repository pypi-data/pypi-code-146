#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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

from ...tensors import FixedPoint


__all__ = ["QuantizedFlatten"]


@tf.keras.utils.register_keras_serializable()
class QuantizedFlatten(keras.layers.Flatten):
    """A Flatten layer that operates on quantized inputs
    """

    def call(self, inputs):
        # raise an error if the inputs are not FixedPoint
        if not isinstance(inputs, FixedPoint):
            raise TypeError("QuantizedFlatten only accepts FixedPoint inputs. "
                            f"Receives {type(inputs)} inputs.")
        if inputs.frac_bits.shape.ndims:
            raise ValueError("QuantizedFlatten only supports inputs quantized per-tensor.")
        # Flatten the values
        flattened_values = super().call(inputs.values)
        # Return a new reshaped FixedPoint
        return FixedPoint(flattened_values, inputs.value_bits, inputs.frac_bits)
