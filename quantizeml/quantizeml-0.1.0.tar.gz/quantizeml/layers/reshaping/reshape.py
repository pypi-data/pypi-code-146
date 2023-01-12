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

from ...tensors import QTensor, FixedPoint


__all__ = ["QuantizedReshape"]


@tf.keras.utils.register_keras_serializable()
class QuantizedReshape(keras.layers.Reshape):
    """A Reshape layer that operates on quantized inputs

    Args:
        target_shape (tuple of ints): Target shape, does not include the samples
            dimension (batch size).
    """

    def call(self, inputs):
        # raise an error if the inputs are not QTensor
        if not isinstance(inputs, QTensor):
            raise TypeError(f"QuantizedReshape only accepts QTensor inputs.\
                             Receives {type(inputs)} inputs.")
        # Return a new reshaped QTensor
        result = tf.reshape(inputs, (tf.shape(inputs)[0],) + self.target_shape)
        if not tf.executing_eagerly():
            # Set the static shape for the result since it might lost during
            # array_ops reshape, eg, some `None` dim in the result could be
            # inferred.
            if isinstance(result, FixedPoint):
                result.values.set_shape(self.compute_output_shape(inputs.shape))
            else:
                result.fp.values.set_shape(self.compute_output_shape(inputs.shape))
        return result
