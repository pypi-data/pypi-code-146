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

from keras.layers import MaxPool2D, GlobalAveragePooling2D
from keras.utils import conv_utils

from .quantizers import OutputQuantizer
from ..tensors import QTensor, MAX_BUFFER_BITWIDTH

__all__ = ["QuantizedMaxPool2D", "QuantizedGlobalAveragePooling2D"]


@tf.keras.utils.register_keras_serializable()
class QuantizedMaxPool2D(MaxPool2D):
    """A max pooling layer that operates on quantized inputs.

    """

    def call(self, inputs):
        # Raise an error if the inputs are not QTensor
        if not isinstance(inputs, QTensor):
            raise TypeError(f"QuantizedMaxPool2D only accepts QTensor inputs. \
                             Receives {type(inputs)} inputs.")

        if self.data_format == "channels_last":
            ksize = (1,) + self.pool_size + (1,)
            strides = (1,) + self.strides + (1,)
        else:
            ksize = (1, 1) + self.pool_size
            strides = (1, 1) + self.strides

        data_format = conv_utils.convert_data_format(self.data_format, 4)
        padding = self.padding.upper()
        outputs = tf.nn.max_pool(inputs, ksize=ksize, strides=strides, padding=padding,
                                 data_format=data_format)
        return outputs


@tf.keras.utils.register_keras_serializable()
class QuantizedGlobalAveragePooling2D(GlobalAveragePooling2D):
    """A global average pooling layer that operates on quantized inputs.

     Args:
        quant_config (dict): the serialized quantization configuration.
    """

    def __init__(self, quant_config, **kwargs):
        super().__init__(**kwargs)
        self.quant_config = quant_config
        out_quant_cfg = quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        self.buffer_bitwidth = self.quant_config.get("buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        assert self.buffer_bitwidth > 0, "The buffer_bitwidth must be a strictly positive integer."

    def build(self, input_shape):
        super().build(input_shape)
        # Build the spatial size
        self.spatial_size = (input_shape[1] * input_shape[2])

    def call(self, inputs):
        # Raise an error if the inputs are not QTensor
        if not isinstance(inputs, QTensor):
            raise TypeError(f"QuantizedGlobalAveragePooling2D only accepts QTensor inputs. \
                             Receives {type(inputs)} inputs.")

        # Promote the inputs to a higher bitwidth to avoid saturation
        inputs = inputs.promote(self.buffer_bitwidth)
        inputs_sum = tf.reduce_sum(inputs, axis=[1, 2], keepdims=self.keepdims)
        inputs_mean = inputs_sum / self.spatial_size

        if self.out_quantizer is not None:
            return self.out_quantizer(inputs_mean)
        return inputs_mean

    def get_config(self):
        config = super().get_config()
        config.update({"quant_config": self.quant_config})
        return config
