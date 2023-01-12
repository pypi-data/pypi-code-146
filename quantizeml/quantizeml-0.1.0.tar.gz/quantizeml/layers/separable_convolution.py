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
"""
QuantizedSeparableConv2D layer definition.
"""

import tensorflow as tf
from keras.layers import SeparableConv2D
from keras.utils import conv_utils
from keras import backend

from ..tensors import FixedPoint, MAX_BUFFER_BITWIDTH, QFloat
from .recorders import TensorRecorder
from .quantizers import (WeightQuantizer, AlignedWeightQuantizer,
                         OutputQuantizer)


__all__ = ["QuantizedSeparableConv2D", "SeparableConv2DTranspose",
           "QuantizedSeparableConv2DTranspose"]


@tf.keras.utils.register_keras_serializable()
class QuantizedSeparableConv2D(SeparableConv2D):
    """ A separable convolutional layer that operates on quantized inputs and weights.

    Args:
        quant_config (dict, optional): the serialized quantization configuration.
            Defaults to empty configuration.
    """

    def __init__(self, *args, quant_config={}, **kwargs):
        if 'dilation_rate' in kwargs:
            if kwargs['dilation_rate'] not in [1, [1, 1], (1, 1)]:
                raise ValueError("Keyword argument 'dilation_rate' is not supported in \
                                 QuantizedSeparableConv2D.")
        if 'depth_multiplier' in kwargs:
            if kwargs['depth_multiplier'] != 1:
                raise ValueError("Keyword argument 'depth_multiplier' is not supported in \
                                 QuantizedSeparableConv2D.")

        super().__init__(*args, **kwargs)
        self.quant_config = quant_config

        out_quant_cfg = quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(
                name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None

        # Separable layer has two weights quantizers to handle different max values
        self.dw_weight_quantizer = WeightQuantizer(
            name="dw_weight_quantizer", **quant_config["dw_weight_quantizer"])
        if self.dw_weight_quantizer.get_config()['axis'] != "per-tensor":
            raise ValueError("Separable depthwise weights must be quantized per tensor")

        self.pw_weight_quantizer = WeightQuantizer(
            name="pw_weight_quantizer", **quant_config["pw_weight_quantizer"])
        if self.use_bias:
            self.bias_quantizer = AlignedWeightQuantizer(
                name="bias_quantizer", **quant_config["bias_quantizer"])

        self.buffer_bitwidth = self.quant_config.get("buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        assert self.buffer_bitwidth > 0, "The buffer_bitwidth must be a strictly positive integer."

    def call(self, inputs):
        # raise an error if the inputs are not FixedPoint or tf.Tensor
        if not isinstance(inputs, (FixedPoint, tf.Tensor)):
            raise TypeError(f"QuantizedSeparableConv2D only accepts FixedPoint\
                               or tf.Tensor inputs. Receives {type(inputs)} inputs.")

        if isinstance(inputs, tf.Tensor):
            # Assume the inputs are integer stored as float, which is the only tf.Tensor
            # inputs that are allowed
            inputs = FixedPoint(inputs, 8, 0)

        # Although the dephwise operation does not require it, we only accept inputs quantized
        # per-tensor to avoid increasing too much the fractional bits of the depthwise outputs.
        inputs.assert_per_tensor()

        # Quantize the weights
        depthwise_kernel = self.dw_weight_quantizer(self.depthwise_kernel)
        pointwise_kernel = self.pw_weight_quantizer(self.pointwise_kernel)

        inputs = inputs.promote(self.buffer_bitwidth)
        dw_outputs_q = backend.depthwise_conv2d(
            inputs,
            depthwise_kernel,
            strides=self.strides,
            padding=self.padding,
            dilation_rate=self.dilation_rate,
            data_format=self.data_format)

        outputs = tf.nn.convolution(
            dw_outputs_q,
            pointwise_kernel,
            strides=[1, 1, 1, 1],
            padding='VALID',
            data_format=conv_utils.convert_data_format(self.data_format, ndim=4))

        if self.use_bias:
            # Quantize bias and align it on the outputs
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config


@tf.keras.utils.register_keras_serializable()
class SeparableConv2DTranspose(SeparableConv2D):
    """ A transposed separable convolutional layer.

    It performs a transposed depthwise convolution on inputs followed by a standard pointwise
    operation.
    """

    def __init__(self, *args, **kwargs):
        if 'dilation_rate' in kwargs:
            if kwargs['dilation_rate'] not in [1, [1, 1], (1, 1)]:
                raise ValueError("Keyword argument 'dilation_rate' is not supported in "
                                 "SeparableConv2DTranspose.")
        if 'depth_multiplier' in kwargs:
            if kwargs['depth_multiplier'] != 1:
                raise ValueError("Keyword argument 'depth_multiplier' is not supported in "
                                 "SeparableConv2DTranspose.")
        # Limit supported stride to 2. Standard separable should be used for stride 1 and greater
        # strides are not supported.
        if 'strides' in kwargs:
            if kwargs['strides'] not in [2, [2, 2], (2, 2)]:
                raise ValueError(f"Only supported stride is 2. Received {kwargs['strides']}.")
        # Also limit padding to 'same'
        if 'padding' in kwargs:
            if kwargs['padding'] != 'same':
                raise ValueError(f"Only supported padding is 'same'. Received {kwargs['padding']}.")
        super().__init__(*args, **kwargs)

    def call(self, inputs):
        # Infer the dynamic output shape
        inputs_shape = tf.shape(inputs)
        out_height = conv_utils.deconv_output_length(inputs_shape[1],
                                                     self.kernel_size[0],
                                                     padding=self.padding,
                                                     stride=self.strides[0],
                                                     dilation=self.dilation_rate[0])
        out_width = conv_utils.deconv_output_length(inputs_shape[2],
                                                    self.kernel_size[1],
                                                    padding=self.padding,
                                                    stride=self.strides[1],
                                                    dilation=self.dilation_rate[1])
        output_shape = tf.stack((inputs_shape[0], out_height, out_width, 1))

        # Inputs and kernels must be transposed to have their channel dimension first because the
        # tf.vectorized_map call that follows will unpack them on dimension 0. The channel dimension
        # is virtually restored using expand_dims so that elements have the appropriate shape for
        # the conv2d_transpose call (with a channel dimension of 1 which is expected in the
        # depthwise process).
        inputs_channel_first = tf.transpose(inputs, (3, 0, 1, 2))
        inputs_channel_first = tf.expand_dims(inputs_channel_first, -1)
        kernel_channel_first = tf.transpose(self.depthwise_kernel, (2, 0, 1, 3))
        kernel_channel_first = tf.expand_dims(kernel_channel_first, -2)

        dw_outputs = tf.vectorized_map(
            lambda x: backend.conv2d_transpose(x[0],
                                               x[1],
                                               output_shape=output_shape,
                                               strides=self.strides,
                                               padding=self.padding),
            (inputs_channel_first, kernel_channel_first))
        dw_outputs = tf.transpose(tf.squeeze(dw_outputs, axis=-1), (1, 2, 3, 0))

        # Pointwise operation
        outputs = tf.nn.convolution(
            dw_outputs,
            self.pointwise_kernel,
            strides=[1, 1, 1, 1],
            padding='VALID')

        if self.use_bias:
            outputs = tf.add(outputs, self.bias)
        return outputs


@tf.keras.utils.register_keras_serializable()
class QuantizedSeparableConv2DTranspose(SeparableConv2DTranspose):
    """ A transposed separable convolutional layer that operates on quantized inputs and weights.

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

        # Transposed Separable layer has two weights quantizers to handle different max values
        self.dw_weight_quantizer = WeightQuantizer(
            name="dw_weight_quantizer", **quant_config["dw_weight_quantizer"])
        self.pw_weight_quantizer = WeightQuantizer(
            name="pw_weight_quantizer", **quant_config["pw_weight_quantizer"])

        # Depthwise quantizer must be per-tensor
        if "axis" in self.quant_config["dw_weight_quantizer"]:
            if self.quant_config["dw_weight_quantizer"]["axis"] != "per-tensor":
                raise ValueError("Only supporting 'per-tensor' depthwise quantizer. Received "
                                 f"{self.quant_config['dw_weight_quantizer']['axis']}.")

        if self.use_bias:
            self.bias_quantizer = AlignedWeightQuantizer(
                name="bias_quantizer", **quant_config["bias_quantizer"])

        self.buffer_bitwidth = self.quant_config.get("buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        assert self.buffer_bitwidth > 0, "The buffer_bitwidth must be a strictly positive integer."
        intermediate_quant_cfg = quant_config.get("intermediate_quantizer", False)
        if out_quant_cfg:
            self.intermediate_quantizer = OutputQuantizer(
                name="intermediate_quantizer", **intermediate_quant_cfg)
        else:
            self.intermediate_quantizer = None

        if self.intermediate_quantizer:
            intermediate_quantizer_axis = self.intermediate_quantizer.get_config()['axis']
            if intermediate_quantizer_axis != "per-tensor":
                raise ValueError("Only supporting 'per-tensor' intermediate quantizer. Received "
                                 f"{intermediate_quantizer_axis}.")

        # Add objects that will store the shift values.
        self.input_shift = TensorRecorder()

    def call(self, inputs):
        # raise an error if the inputs are not FixedPoint or tf.Tensor
        if not isinstance(inputs, (FixedPoint, tf.Tensor)):
            raise TypeError("QuantizedSeparableConv2DTranspose only accepts FixedPoint or "
                            f"tf.Tensor inputs. Receives {type(inputs)} inputs.")

        if isinstance(inputs, tf.Tensor):
            # Assume the inputs are integer stored as float, which is the only tf.Tensor
            # inputs that are allowed
            inputs = FixedPoint.quantize(inputs, 0, 8)

        # Expand the inputs to a higher bitwidth to avoid saturation and align them
        inputs, shift = inputs.expand(self.buffer_bitwidth)
        self.input_shift(shift)

        # Infer the dynamic output shape
        inputs_shape = tf.shape(inputs)
        out_height = conv_utils.deconv_output_length(inputs_shape[1],
                                                     self.kernel_size[0],
                                                     padding=self.padding,
                                                     stride=self.strides[0],
                                                     dilation=self.dilation_rate[0])
        out_width = conv_utils.deconv_output_length(inputs_shape[2],
                                                    self.kernel_size[1],
                                                    padding=self.padding,
                                                    stride=self.strides[1],
                                                    dilation=self.dilation_rate[1])
        output_shape = tf.stack((inputs_shape[0], out_height, out_width, 1))

        # Quantize the depthwise kernels
        depthwise_kernel = self.dw_weight_quantizer(self.depthwise_kernel)

        # Inputs and kernels must be transposed to have their channel dimension first because the
        # tf.vectorized_map call that follows will unpack them on dimension 0. The channel dimension
        # is virtually restored using expand_dims so that elements have the appropriate shape for
        # the conv2d_transpose call (with a channel dimension of 1 which is expected in the
        # depthwise process).
        inputs_channel_first = tf.transpose(inputs, (3, 0, 1, 2))
        inputs_channel_first = tf.expand_dims(inputs_channel_first, -1)
        kernel_channel_first = tf.transpose(depthwise_kernel, (2, 0, 1, 3))
        kernel_channel_first = tf.expand_dims(kernel_channel_first, -2)

        # Perform the depthwise operation on values using conv2d_transpose on each channel
        dw_values = tf.vectorized_map(
            lambda x: backend.conv2d_transpose(x[0],
                                               x[1],
                                               output_shape=output_shape,
                                               strides=self.strides,
                                               padding=self.padding),
            (inputs_channel_first.values, kernel_channel_first.values))
        dw_values = tf.transpose(tf.squeeze(dw_values, axis=-1), (1, 2, 3, 0))

        # Build a new FixedPoint
        dw_outputs = FixedPoint(dw_values, inputs.value_bits, inputs.frac_bits)
        if isinstance(depthwise_kernel, QFloat):
            # Build a new QFloat
            dw_outputs = QFloat(dw_outputs, depthwise_kernel.scales)

        if self.intermediate_quantizer is not None:
            dw_outputs_q = self.intermediate_quantizer(dw_outputs)
            dw_outputs_q = dw_outputs_q.promote(self.buffer_bitwidth)
        else:
            dw_outputs_q = dw_outputs

        # Quantize the pointwise kernel
        pointwise_kernel = self.pw_weight_quantizer(self.pointwise_kernel)

        # Pointwise operation
        outputs = tf.nn.convolution(
            dw_outputs_q,
            pointwise_kernel,
            strides=[1, 1, 1, 1],
            padding='VALID')

        if self.use_bias:
            # Quantize biases and align them on the outputs
            bias = self.bias_quantizer(self.bias, outputs)
            # Add biases
            outputs = tf.add(outputs, bias)

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
