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

from ...debugging import assert_equal
from ...tensors import QTensor, QFloat, FixedPoint
from ..recorders import FixedPointRecorder, QFloatRecorder
from .quantizers import Quantizer


__all__ = ["WeightQuantizer"]


@tf.keras.utils.register_keras_serializable()
class WeightQuantizer(Quantizer):
    """A uniform quantizer that converts a float Tensor to a QTensor representation.

    By default, it quantizes the float Tensor using quantization ranges aligned
    on powers of two and outputs a FixedPoint.

    If rescale is True, it:

    - evaluates the scales required to align the quantization ranges on powers of two,
    - quantizes the rescaled Tensor and returns a QFloat.

    Args:
        bitwidth (int): the quantization bitwidth.
        signed (bool, optional): whether the quantizer expects signed values or unsigned.
            Defaults to True.
        axis (str, optional): the quantization range is a scalar ('per-tensor') or a vector
            corresponding to the last axis ('per-axis'). Defaults to 'per-tensor'.
        rescale (bool, optional): rescale weights before quantizing. Defaults to True.
    """

    def __init__(self, bitwidth, signed=True, axis="per-tensor", rescale=True, **kwargs):
        super().__init__(bitwidth, signed, **kwargs)
        self.rescale = rescale
        self._axis = axis
        if not (isinstance(axis, str) and axis in ["per-tensor", "per-axis"]):
            raise ValueError(f"Only support reduction 'per-tensor' or 'per-axis'. Given {axis}.")
        self.qweights = QFloatRecorder() if self.rescale else FixedPointRecorder()

    def build(self, input_shape):
        """Build the layer.

        Args:
            input_shape (list): the shape of input tensor.
        """
        # Convert axis to a list of int
        if self._axis == "per-axis" and len(input_shape) > 1:
            axis_list = list(range(len(input_shape) - 1))
            # When input_shape last dimension is 1, move operation from axis -1 to axis -2 by
            # adding 1 to the last element in the list. Practical use case is for Depthwise kernels
            # that will be quantized per-channel.
            if input_shape[-1] == 1:
                axis_list[-1] = axis_list[-1] + 1
            self.axis = axis_list
        else:
            self.axis = None

    def call(self, inputs):
        """Quantize the float inputs

        The quantization is done in two steps:

            1. Compute the quantization ranges,
            2. Quantize the inputs.

        Args:
            inputs (:obj:`tensorflow.Tensor`): the inputs tensor.

        Returns:
            :obj:`QTensor`: the quantized tensor.
        """
        if isinstance(inputs, QTensor):
            raise ValueError(
                f"{type(inputs)} input is not supported. WeightQuantizer only accepts float"
                " inputs.")

        # Compute the quantization ranges from the inputs
        ranges = tf.math.reduce_max(tf.math.abs(inputs), self.axis)
        if self.axis is not None and inputs.shape[-1] == 1:
            # Expand the shape of the ranges so that it is broacastable on the inputs
            ranges = tf.expand_dims(ranges, -1)
        if self.rescale:
            # Evaluate the scales to align on the optimal quantization ranges
            scales = QFloat.optimal_scales(ranges, self.value_bits)
            # Remove the input-dependent scales from the gradient tape to avoid a loopback
            scales = tf.stop_gradient(scales)
            # Since we use the optimal quantization ranges [-int_max -1, int_max], the inner
            # FixedPoint can be quantized with exactly zero fractional bits
            assert_equal(0., QFloat.max_frac_bits(self.value_bits, ranges, scales))
            # Quantize the inputs projected in the optimal ranges
            qweights = QFloat.quantize(inputs, self.value_bits, scales, 0.)
        else:
            # Evaluate the maximum fractional bits we can use for the specified range
            frac_bits = FixedPoint.max_frac_bits(self.value_bits, ranges)
            # Remove the input-dependent fractional bits from the gradient tape to avoid a loopback
            frac_bits = tf.stop_gradient(frac_bits)
            qweights = FixedPoint.quantize(inputs, self.value_bits, frac_bits)
        # Record the quantized weights (it does nothing if recording is disabled)
        self.qweights(qweights)
        return qweights

    def get_config(self):
        """Get the config of the layer.

        Returns:
            dict: the config of the layer.
        """
        config = super().get_config()
        config.update({"rescale": self.rescale})
        config.update({"axis": self._axis})
        return config
