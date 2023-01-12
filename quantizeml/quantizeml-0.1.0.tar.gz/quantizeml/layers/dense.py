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

from ..tensors import FixedPoint, MAX_BUFFER_BITWIDTH
from .recorders import TensorRecorder
from .quantizers import (WeightQuantizer, OutputQuantizer,
                         AlignedWeightQuantizer)

__all__ = ["QuantizedDense"]


@tf.keras.utils.register_keras_serializable()
class QuantizedDense(keras.layers.Dense):
    """A Dense layer that operates on quantized inputs and weights

    Args:
        quant_config (dict): the serialized quantization configuration.
    """

    def __init__(self, *args, quant_config, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        out_quant_cfg = quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        self.weight_quantizer = WeightQuantizer(
            name="weight_quantizer", **quant_config["weight_quantizer"])
        if self.use_bias:
            self.bias_quantizer = AlignedWeightQuantizer(
                name="bias_quantizer", **quant_config["bias_quantizer"])
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        assert self.buffer_bitwidth > 0, "The buffer_bitwidth must be a strictly positive integer."

        # Add object that will store the shift values.
        self.input_shift = TensorRecorder()

    def call(self, inputs):
        # raise an error if the inputs are not FixedPoint or tf.Tensor
        if not isinstance(inputs, (FixedPoint, tf.Tensor)):
            raise TypeError(f"QuantizedDense only accepts FixedPoint or tf.Tensor\
                              inputs. Receives {type(inputs)} inputs.")

        # Quantize the weights
        kernel = self.weight_quantizer(self.kernel)

        if isinstance(inputs, tf.Tensor):
            # Assume the inputs are integer stored as float, which is the only tf.Tensor
            # inputs that are allowed
            inputs = FixedPoint(inputs, 8, 0)

        # Expand the inputs to a higher bitwidth to avoid saturation and align them
        inputs, shift = inputs.expand(self.buffer_bitwidth)
        self.input_shift(shift)

        outputs = tf.matmul(inputs, kernel)

        if self.use_bias:
            # Quantize and align biases
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
