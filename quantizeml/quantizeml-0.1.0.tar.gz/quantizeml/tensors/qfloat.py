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

from .qtensor import QTensor
from .fixed_point import FixedPoint
from ..debugging import assert_equal


class QFloat(QTensor):
    """A Tensor of FixedPoint values and scales representing float numbers

    The QFloat is a dual representation of a float Tensor of float combining
    FixedPoint values and float scales.

    The QFloat is typically used to represent float tensors whose quantization
    range is not aligned on a power-of-two: the original tensor is first divided
    by the scales to be aligned on power-of-two ranges, then quantized to
    FixedPoint values.

    When converting back to float, values are dequantized and multiplied by the
    scales to obtain the approximated float tensor.

    Args:
        fp (:obj:`FixedPoint`): a FixedPoint of values
        scales (:obj:`tensorflow.Tensor`): a Tensor of scales
    """
    fp: FixedPoint = FixedPoint(1.0, 32, 0)
    scales: tf.Tensor = 1.0

    def __init__(self, fp, scales):
        self.scales = scales
        self.fp = fp
        self.shape = self.fp.shape

    @property
    def values(self):
        return self.fp.values

    @property
    def name(self):
        return self.fp.name

    @property
    def per_tensor(self):
        return self.fp.per_tensor and self.scales.shape.ndims == 0

    @staticmethod
    def max_frac_bits(value_bits, ranges, scales, clamp=True):
        """Evaluate the maximum fractional bit index for the quantization ranges.

        This method evaluates the minimum number of integer bits required to cover
        the specified quantization ranges after having rescaled them with the specified
        scales.
        It simply calls the equivalent FixedPoint method on the rescaled ranges.
        If specified, it clamps the results to the available value_bits.

        Args:
            value_bits (int): the number of value bits.
            ranges (:obj:`tensorflow:Tensor`): a tensor of float quantization ranges.
            scales (:obj:`Tensor`): the scales to apply to the quantization ranges.
            clamp (bool, optional): clamp the results to self.value_bits. Defaults to True.

        Returns:
            :obj:`tensorflow:Tensor`: a tensor of fractional bits.
        """
        return FixedPoint.max_frac_bits(value_bits, ranges / scales, clamp)

    @staticmethod
    def optimal_scales(ranges, value_bits):
        """Evaluates the optimal QFloat scales for quantization ranges.

        We choose the optimal quantization range for a given bitwidth as:
            [-int_max, int_max], with int_max = 2^bits - 1.

        This methods evaluates the scales as the ratio to align the specified ranges
        to the optimal ranges.

        Args:
            ranges (:obj:`tensorflow.Tensor`): a tensor of quantization ranges.
            value_bits (int): the number of value bits.

        Returns:
            :obj:`tensorflow.Tensor`: the optimal scales.
        """
        # Evaluate the scales as the ratio to align the ranges on the optimal quantization range
        optimal_ranges = QTensor.int_max(value_bits)
        scales = tf.cast(ranges, tf.float32) / optimal_ranges
        return scales

    @staticmethod
    def quantize_scales(scales, scale_bits):
        """Quantizes the QFloat scales with the specified bitwidth.

        Args:
            scales (:obj:`tensorflow.Tensor`): a tensor of float scales.
            scale_bits (int): the number of scales bits.

        Returns:
            :obj:`FixedPoint`: the FixedPoint scales.
        """
        # Evaluate QFloat scales fractional bits, without clamping to scale_bits
        scales_frac_bits = FixedPoint.max_frac_bits(scale_bits, scales, clamp=False)
        # Quantize the scales "up" to make sure they are at least equal to the actual scales.
        # Should they be lower, we would not cover the full quantization range.
        return FixedPoint.quantize(scales, scale_bits, scales_frac_bits, ceil=True)

    @staticmethod
    def quantize(x, value_bits, scales, frac_bits=0.):
        """Converts a float Tensor to a QFloat

        It first evaluates and quantizes the scales required to align the quantization ranges
        to the optimal range for the specified value bits.

        It then quantizes the inputs with the quantized scales.

        The resulting integer values are clipped to [-int_max-1, int_max].

        Args:
            x (:obj:`tensorflow.Tensor`): a tensor of float values.
            value_bits (int): the number of value bits.
            scales (:obj:`tensorflow.Tensor`): a tensor of alignment scales.
            frac_bits (int): the inner FixedPoint fractional bits (defaults to 0).

        Returns:
            :obj:`QFloat`: the QFloat representation.
        """
        # Rescale the inputs to project them in the actual quantization ranges
        x_scaled = x / scales
        # Quantize the rescaled inputs with the specified fractional bits
        fp_x_scaled = FixedPoint.quantize(x_scaled, value_bits, frac_bits)
        return QFloat(fp_x_scaled, scales)

    def to_float(self):
        """Returns a float representation of the QFloat

        Returns:
            :obj:`tensorflow.Tensor`: the float representation.
        """
        return self.fp.to_float() * self.scales

    def to_fixed_point(self, scale_bits=8):
        """Returns a FixedPoint representation of the QFloat

        Args:
            scale_bits (int, optional): the scales quantization bitwidth. Defaults to 8.

        Returns:
            (:obj:`FixedPoint`, :obj:`FixedPoint`): the FixedPoint representation and scales.
        """
        # Quantize the scales
        scales = QFloat.quantize_scales(self.scales, scale_bits)
        # Return the FixedPoint product of scales and values
        return self.fp * scales, scales

    def upscale(self, frac_bits, value_bits=None):
        """Align a QFloat to a specified precision

        The target precision must be higher than the current one.

        Args:
            frac_bits (:obj:`tensorflow.Tensor`): the target fractional bits
            value_bits (int, optional): the target value bits (defaults to current value bits)

        Returns:
            :obj:`FixedPoint`: the upscaled FixedPoint
        """
        if value_bits is None:
            value_bits = self.value_bits
        # Upscale the inner values FixedPoint
        fp, shift = self.fp.upscale(frac_bits, value_bits)
        # Return a new QFloat with updated values and the same scale
        return QFloat(fp, self.scales), shift

    def promote(self, bits):
        """Increase the number of value bits

        Args:
            bits (int): the new number of value bits

        Returns:
            :obj:`QFloat`: a QFloat with increased value bits
        """
        # Return a new QFloat with identical scales and a promoted inner FixedPoint
        return QFloat(self.fp.promote(bits), self.scales)

    def __add__(self, other):
        if isinstance(other, QFloat):
            # Check that self and other have the same scales
            assert_equal(self.scales, other.scales,
                         message=f"{self.name} and {other.name} have different scales.")
            # Return a new QFloat
            return QFloat(self.fp + other.fp, self.scales)
        raise TypeError(
            f"Unsupported operand type(s) for +: 'QFloat' and '{type(other)}'")

    def __truediv__(self, other):
        # We only support the division of the scales by a compatible type
        div_scales = self.scales / other
        # Return a Qfloat with updated scales
        return QFloat(self.fp, div_scales)
