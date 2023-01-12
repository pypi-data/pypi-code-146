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

from ...tensors import QTensor, QFloat, FixedPoint
from ..recorders import TensorRecorder, FixedPointRecorder, QFloatRecorder
from .quantizers import Quantizer


__all__ = ["AlignedWeightQuantizer"]


@tf.keras.utils.register_keras_serializable()
class AlignedWeightQuantizer(Quantizer):
    """A uniform quantizer that converts a float Tensor to a QTensor representation.

    Unlike its sibling the WeightQuantizer, it does not evaluate the fractional bits
    and scales of the resulting QTensor, but instead aligns them on those of another
    QFloat input.

    Args:
        bitwidth (int): the quantization bitwidth.
        signed (bool, optional): whether the quantizer expects signed values or unsigned.
            Defaults to True.
    """

    def __init__(self, bitwidth, signed=True, **kwargs):
        super().__init__(bitwidth, signed, **kwargs)
        # Add the object that will store the shift values.
        self.shift = TensorRecorder()
        # We don't know until the first call the type of the quantized weights
        # so we need to wait before initializing their recorder.
        self.qweights = None

    def call(self, inputs, other):
        """Quantize the float inputs, aligned on another QFloat

        The quantization is done in several steps:

            1. Compute the quantization ranges,
            2. Evaluate the maximum fractional bits,
            3. Quantize the inputs as a QFloat,
            4. Align the QFloat fractional bits on the other.

        Args:
            inputs (:obj:`tensorflow.Tensor`): the inputs tensor.
            other (:obj:`QTensor`): a tensor to align on.

        Returns:
            :obj:`QTensor`: a quantized tensor of the same types than other.
        """
        if not isinstance(inputs, (tf.Tensor, tf.Variable)):
            raise ValueError(
                f"{type(inputs)} as first param is not supported."
                "AlignedWeightQuantizer only accepts tf.Tensor.")
        if not isinstance(other, QTensor):
            raise ValueError(
                f"{type(other)} as second param is not supported."
                "AlignedWeightQuantizer only accepts QTensor types.")

        if isinstance(other, FixedPoint):
            other_value_bits = other.value_bits
            other_frac_bits = other.frac_bits
            if self.qweights is None:
                self.qweights = FixedPointRecorder()
        else:
            other_value_bits = other.fp.value_bits
            other_frac_bits = other.fp.frac_bits
            if self.qweights is None:
                self.qweights = QFloatRecorder()
        # Compute the symmetric quantization ranges from the inputs
        ranges = tf.math.reduce_max(tf.math.abs(inputs))
        # Evaluate the maximum fractional bits we can use for the specified ranges
        if isinstance(other, FixedPoint):
            frac_bits = FixedPoint.max_frac_bits(self.value_bits, ranges)
        else:
            frac_bits = QFloat.max_frac_bits(self.value_bits, ranges, other.scales)
        # Remove the input-dependent fractional bits from the gradient tape to avoid a loopback
        frac_bits = tf.stop_gradient(frac_bits)
        # Clamp the ideal frac_bits to the other fractional bits, to avoid downscaling afterwards
        frac_bits = tf.minimum(frac_bits, other_frac_bits)
        # Quantize the inputs with the resulting fractional bits
        if isinstance(other, FixedPoint):
            outputs = FixedPoint.quantize(inputs, self.value_bits, frac_bits)
        else:
            # If the other is a QFloat, adopt its scales
            outputs = QFloat.quantize(inputs, self.value_bits, other.scales, frac_bits)
        # Now, upscale to the other fractional bits
        outputs, shift = outputs.upscale(other_frac_bits, other_value_bits)
        # record quantized weights (including shift and promote)
        self.qweights(outputs)
        # record shift values to be able to recreate and store unshifted weights
        self.shift(shift)
        return outputs
