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
import keras
import tensorflow as tf

from ..tensors import QTensor


__all__ = ["QDropout"]


@tf.keras.utils.register_keras_serializable()
class QDropout(keras.layers.Dropout):
    """ A dropout layer that operates on quantized inputs and weights.

    It is only implemented as a passthrough.
    """

    def call(self, inputs):
        # raise an error if the inputs are not QTensor
        if not isinstance(inputs, QTensor):
            raise TypeError(f"QDropout only accepts QTensor inputs.\
                             Receives {type(inputs)} inputs.")

        # QuantizedDropout act as a pass through.
        return inputs
