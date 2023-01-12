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
from tensorflow.python.framework import ops

from .recorders import TensorRecorder
from .quantizers import WeightQuantizer, OutputQuantizer
from ..tensors import FixedPoint, MAX_BUFFER_BITWIDTH


__all__ = ["QuantizedLayerNormalization", "LayerMadNormalization"]


@tf.keras.utils.register_keras_serializable()
class LayerMadNormalization(keras.layers.LayerNormalization):
    r"""Approximates the :obj:`keras.layers.LayerNormalization` (LN), replacing the computation of
    the standard deviation by the mean average deviation (mad).

    Taking into account the complexity of the calculate required in the standard deviation,
    the LayerMadNormalization (LMN) is intended to replace the :math:`std(x)` by :math:`mad(x)`
    on a Power of Two (PoT), defined as:

    .. math:: mad(x) = |x - mean(x)| * 2^\text{-nb_channels}

    To simplify it even more and make it more hardware-friendly, :math:`mean(x)` is considered
    as 0, so. These are the resulting calculations:

    .. math:: mad(x) = sum(|x|) * 2^\text{-nb_channels}

    Then, the equation of the layer is defined as:

    .. math:: LMN(x) = \gamma\frac{x}{mad(x)} + \beta

    .. note::
        A tuning step in the switching procedure between the LN to LMN layer will be required
        to find the :math:`(\gamma, \beta)` parameters that match the standard deviation changes.
    """

    def build(self, input_shape):
        super().build(input_shape)

        # Save an approximation of nb_channels as PoT to calculate the mad of inputs as:
        # mad = sum(abs(inputs)) * 2 ** -mad_shift
        if len(self.axis) > 1:
            raise ValueError(f"{self.__class__.__name__} does not support multiple axis.")
        nb_channels = tf.cast(input_shape[self.axis[0]], tf.float32)
        self.mad_shift = tf.math.round(tf.math.log(nb_channels) / tf.math.log(2.))

    def _get_mad(self, inputs, axis, *args, name=None, **kwargs):
        """Compute the mean absolute deviation (mad).

        Args:
            inputs (:obj:`tensorflow.Tensor`): input tensor.
            axis (array of ints): axis along which to compute mad.
            name (str, optional): name used to scope the operations that compute the mad.
                Defaults to None.
            *args, **kwargs (dict, optional): additional arguments of :func:`tf.math.reduce_sum`.

        Returns:
            :obj:`tensorflow.Tensor`: mean absolute deviation (mad).
        """
        # Compute the mad, taking into account the approximations:
        # mad \approx sum(abs(inputs))
        # nb_channels \approx 2 ** round(log2(inputs.shape[axis]))
        nb_channels_inv = 2.0 ** -self.mad_shift
        with ops.name_scope(name, "_mad", [inputs, axis]):
            mad = tf.math.reduce_sum(tf.math.abs(inputs), axis, *args, **kwargs, name="mad")
            mad = mad * nb_channels_inv
        return mad

    def call(self, inputs):
        """Use the same call as the parent, changing tf.nn.moments instead of self._get_mad,
        and replacing mean by 0"""
        # Compute the axis along which to reduce the mad
        input_shape = inputs.shape
        ndims = len(input_shape)

        # Broadcasting only necessary for norm when the axis is not just the last dimension
        broadcast_shape = [1] * ndims
        for dim in self.axis:
            broadcast_shape[dim] = input_shape.dims[dim].value

        def _broadcast(v):
            if (v is not None and len(v.shape) != ndims and self.axis != [ndims - 1]):
                return tf.reshape(v, broadcast_shape)
            return v

        input_dtype = inputs.dtype
        if input_dtype in ('float16', 'bfloat16') and self.dtype == 'float32':
            # If mixed precision is used, cast inputs to float32 so that this is at
            # least as numerically stable as the fused version.
            inputs = tf.cast(inputs, 'float32')

        # Calculate the mad on the last axis (layer activations).
        mad = self._get_mad(inputs, self.axis, keepdims=True)
        scale, offset = _broadcast(self.gamma), _broadcast(self.beta)

        # Compute layer normalization as layer mad normalization
        outputs = scale * inputs / mad + offset
        outputs = tf.cast(outputs, input_dtype)

        # If some components of the shape got lost due to adjustments, fix that.
        outputs.set_shape(input_shape)

        return outputs


@tf.keras.utils.register_keras_serializable()
class QuantizedLayerNormalization(LayerMadNormalization):
    """ A LayerNormalization layer that operates on quantized inputs and weights.

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
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        self.mad_rec_frac_bits = self.quant_config.get("mad_rec_frac_bits", 16)
        assert self.buffer_bitwidth > 0, "The buffer_bitwidth must be a strictly positive integer."
        assert self.mad_rec_frac_bits >= 0, "The mad_rec_frac_bits must be a non-negative integer."
        self.gamma_quantizer = WeightQuantizer(
            name="gamma_quantizer", **quant_config["gamma_quantizer"])
        self.beta_quantizer = WeightQuantizer(
            name="beta_quantizer", **quant_config["beta_quantizer"])

        # Add objects that will store the shift values.
        self.input_shift = TensorRecorder()
        self.x_rescaled_shift = TensorRecorder()
        self.one_bits = TensorRecorder()
        self.beta_shift = TensorRecorder()
        self.output_shift = TensorRecorder()

    def call(self, inputs):
        """The quantized version of the LayerNormalization with Integer-only operations.

            This normalizes the input tensor then returns a quantized output.

        Args:
            inputs (:obj:`FixedPoint`): the inputs tensor.

        Returns:
            :obj:`FixedPoint`: output tensor.
        """
        # raise an error if the inputs are not FixedPoint
        if not isinstance(inputs, FixedPoint):
            raise TypeError(f"QuantizedLayerNormalization only accepts FixedPoint\
                              inputs. Receives {type(inputs)} inputs.")

        # Expand the inputs to a higher bitwidth to avoid saturation and align them
        inputs, shift = inputs.expand(self.buffer_bitwidth)
        self.input_shift(shift)

        # Compute the Absolute Deviation (MAD)
        mad_sum = tf.math.reduce_sum(
            inputs.abs(), self.axis, keepdims=True, name="mad")
        # Calculate a gamma_rescaled = gamma * 2 ** mad_shift. This is the
        # value that will be quantized.
        gamma_rescaled = self.gamma * (2 ** self.mad_shift)
        # Quantize the learnable parameters gamma_rescaled and beta
        gamma_rescaled = self.gamma_quantizer(gamma_rescaled)
        beta = self.beta_quantizer(self.beta)

        # Calculate the gamma_on_mad_sum = (gamma * 2**mad_shift) / mad_sum.
        # This can be evaluated once on hardware.
        gamma_on_mad_sum = gamma_rescaled / mad_sum

        # Multiply inputs by gamma
        x_rescaled = inputs * gamma_on_mad_sum

        # Downscale to recover the initial fractional bits
        outputs, shift = x_rescaled.downscale(inputs.frac_bits)
        self.x_rescaled_shift(shift)

        # Before adding the bias, we need aligned results
        outputs, shift = outputs.align(beta)
        self.output_shift(shift)
        beta, shift = beta.align(outputs, self.buffer_bitwidth)
        self.beta_shift(shift)
        outputs = tf.add(outputs, beta)

        # If no quantizer output is provided return the FixedPoint output tensor directly
        if self.out_quantizer is None:
            return outputs

        return self.out_quantizer(outputs)

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
