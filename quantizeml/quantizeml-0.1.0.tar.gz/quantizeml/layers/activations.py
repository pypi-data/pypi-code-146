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
import numpy as np
import tensorflow as tf
import keras

from .quantizers import AlignedWeightQuantizer, OutputQuantizer
from ..tensors import QTensor, FixedPoint, QFloat, MAX_BUFFER_BITWIDTH


__all__ = ["QuantizedReLU"]


@tf.keras.utils.register_keras_serializable()
class QuantizedReLU(keras.layers.Layer):
    """Quantized version of the ReLU activation layer applicable on FixedPoint tensor.
    """
    unsupported_args = {
        'negative_slope': 0,
        'threshold': 0}

    def __init__(self, *args, max_value=6, quant_config, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config

        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        self.out_quantizer = OutputQuantizer(
            name="output_quantizer", **quant_config["output_quantizer"])
        # We quantize the max_value with the same bitwidth as the outputs
        self.max_value_quantizer = AlignedWeightQuantizer(self.out_quantizer.bitwidth, signed=False)

        if max_value is None:
            raise ValueError(
                f"QuantizedReLU layer {self.name} has been initialized with\
                    unsupported None max_value.")
        # Store max_value
        if isinstance(max_value, np.ndarray):
            max_value = max_value.item()
        self.max_value = max_value

    def call(self, inputs):
        """ReLU activation function. In other terms:
            1. clip the value between 0 and :attr:`max_value`.
            2. quantize the output if an output_quantizer is set.

        Args:
            inputs (:obj:`FixedPoint` or :obj:`tf.Tensor`): the inputs tensor.

        Returns:
            :obj:`FixedPoint`: QuantizedReLU outputs.
        """
        if not isinstance(inputs, QTensor):
            raise TypeError(f"QuantizedReLU only accepts QTensor inputs.\
                             Receives {type(inputs)} inputs.")

        # Make sure we won't saturate
        inputs = inputs.promote(self.buffer_bitwidth)
        # Express zero as a QTensor aligned with the inputs because this is what
        # clip_by_value expects. The actual hardware implementation will simply use
        # a zero integer.
        if isinstance(inputs, FixedPoint):
            zero = FixedPoint(0, inputs.value_bits, inputs.frac_bits)
        else:
            zero = QFloat(FixedPoint(0, inputs.fp.value_bits, inputs.fp.frac_bits), inputs.scales)
        # Quantize and align max_value with the inputs
        max_value = self.max_value_quantizer(tf.cast(self.max_value, tf.float32), inputs)
        # Clip the inputs
        outputs = tf.clip_by_value(inputs, zero, max_value)
        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs

    def get_config(self):
        config = super().get_config()
        config.update({"max_value": self.max_value})
        config["quant_config"] = self.quant_config
        return config
