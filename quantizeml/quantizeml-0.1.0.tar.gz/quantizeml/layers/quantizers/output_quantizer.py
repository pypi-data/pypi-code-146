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
import keras.backend as K
from contextlib import contextmanager

from ...tensors import QTensor, FixedPoint, QFloat
from ..calibrable import Calibrable
from ..recorders import TensorRecorder, FixedPointRecorder
from .quantizers import Quantizer


__all__ = ["OutputQuantizer"]


@contextmanager
def disable_partitioner(layer):
    partitioner = None
    try:  # Disable variable partitioning when creating the moving tensors
        if hasattr(layer, "_scope") and layer._scope:
            partitioner = layer._scope.partitioner
            layer._scope.set_partitioner(None)
        yield layer
    finally:  # Restore partitioner
        if partitioner:
            layer._scope.set_partitioner(partitioner)


@tf.keras.utils.register_keras_serializable()
class OutputQuantizer(Calibrable, Quantizer):
    """A uniform quantizer that aligns its quantization ranges to powers of two.

    The quantization ranges are updated during the calibration using a moving average.

    inspired by the BatchNormalizationLayer moving average algorithm.

    Args:
        bitwidth (int): the quantization bitwidth.
        signed (bool, optional): whether the quantizer expects signed values or unsigned.
            Defaults to True.
        axis (str, optional): the quantization range is a scalar ('per-tensor') or a vector
            corresponding to the last axis ('per-axis'). Defaults to 'per-tensor'.
        momentum (float, optional): the momentum for the moving average. Defaults to 0.9.
        scale_bits: (int, optional): the bitwidth to use when quantizing output scales.
            Defaults to None.
    """

    def __init__(self, bitwidth, signed=True, axis="per-tensor",
                 momentum=0.9, scale_bits=None, **kwargs):
        super().__init__(bitwidth, signed, **kwargs)
        self._axis = axis
        if not (isinstance(axis, str) and axis in ["per-tensor", "per-axis"]):
            raise ValueError(f"Only support reduction 'per-tensor' or 'per-axis'. Given {axis}.")
        self.momentum = momentum
        # Add object that will store the shift values.
        self.shift = TensorRecorder()
        self.scale_bits = scale_bits
        if scale_bits is not None:
            self.qscales = FixedPointRecorder()

    def build(self, input_shape):
        """Build the layer.

        Args:
            input_shape (list): the shape of input tensor.
        """
        # Convert axis to a list of int
        if self._axis == "per-axis" and len(input_shape) > 1:
            self.axis = list(range(len(input_shape) - 1))
        else:
            self.axis = None

        # Declares the constant/vector that will store the maximum values of the input.
        with disable_partitioner(self):
            self.max_value = self.add_weight(
                name="max_value",
                shape=input_shape[-1] if self.axis is not None else (),
                dtype=tf.float32,
                initializer="ones",
                synchronization=tf.VariableSynchronization.ON_READ,
                trainable=False,
                aggregation=tf.VariableAggregation.MEAN,
                experimental_autocast=False,
            )

    @staticmethod
    def _assign_new_value(variable, value):
        """Given a variable, assign a new value to it. Function taken of
        `BatchNormalizationLayer <https://bit.ly/3v0gzll>`_ code.

        Args:
            variable (:obj:`tensorflow.Variable`): the variable to assign.
            value (:obj:`tensorflow.Tensor`): the new value to assign.

        Returns:
            :obj:`tensorflow.Tensor`: the new value of the variable.
        """
        with K.name_scope("AssignNewValue") as scope:
            # Expected match shape
            value_r = tf.reshape(value, tf.shape(variable))
            if tf.compat.v1.executing_eagerly_outside_functions():
                return variable.assign(value_r, name=scope)
            else:
                with tf.compat.v1.colocate_with(variable):
                    return tf.compat.v1.assign(variable, value_r, name=scope)

    @staticmethod
    def _assign_moving_average(variable, value, momentum, inputs_size):
        """Given a variable, assign a new value to it, using a moving average.
        Function taken of `BatchNormalizationLayer <https://bit.ly/3JUcLGd>`_ code.

        Args:
            variable (:obj:`tensorflow.Variable`): the variable to assign.
            value (:obj:`tensorflow.Tensor`): the new value to assign.
            momentum (float): the momentum for the moving average.
            inputs_size (int): the size of the inputs.

        Returns:
            :obj:`tensorflow.Tensor`: the new value of the variable.
        """

        def calculate_update_delta():
            decay = tf.convert_to_tensor(1.0 - momentum, name="decay")
            if decay.dtype != variable.dtype.base_dtype:
                decay = tf.cast(decay, variable.dtype.base_dtype)
            # Expected match shape
            value_r = tf.reshape(value, tf.shape(variable))
            update_delta = (variable - tf.cast(value_r, variable.dtype)) * decay
            if inputs_size is not None:
                update_delta = tf.where(
                    inputs_size > 0, update_delta, K.zeros_like(update_delta))
            return update_delta

        with K.name_scope("AssignMovingAvg") as scope:
            if tf.compat.v1.executing_eagerly_outside_functions():
                return variable.assign_sub(calculate_update_delta(), name=scope)
            else:
                with tf.compat.v1.colocate_with(variable):
                    return tf.compat.v1.assign_sub(variable, calculate_update_delta(), name=scope)

    def call(self, inputs):
        """Quantize the QTensor inputs to a lower bitwidth.

        The quantization happens in three steps:

            1. If calibration is enabled, update the quantization range(s) using a moving average,
            2. Evaluate the nearest power(s) of two containing the quantization range(s)
            3. Quantize the inputs.

        Args:
            inputs (:obj:`QTensor`): the inputs tensor.

        Returns:
            :obj:`FixedPoint`: the quantized tensor.
        """
        if not isinstance(inputs, QTensor):
            raise TypeError("The OutputQuantizer accepts only QTensor inputs."
                            f"Received {type(inputs)} inputs.")

        if isinstance(inputs, QFloat):
            if self.scale_bits is None:
                raise ValueError(f"{self.name} receives QFloat inputs: the scale_bits parameter"
                                 " needs to be specified.")
            inputs, qscales = inputs.to_fixed_point(self.scale_bits)
            self.qscales(qscales)

        if inputs.value_bits <= self.value_bits:
            msg = f"Quantizing a {inputs.value_bits}-bit QTensor to "\
                f"{self.value_bits}-bit is pointless."
            if inputs.value_bits < self.value_bits:
                msg += " Use a promotion instead."
            raise ValueError(msg)

        if self.calibration:
            # Retrieve information from the inputs and update the weights
            input_batch_size = tf.shape(inputs)[0]
            if tf.reduce_all(tf.math.equal(self.max_value, tf.constant(1.))):
                momentum = tf.constant(-1.)
            else:
                momentum = tf.convert_to_tensor(self.momentum)
            # Compute the new value for all weights
            max_value = tf.math.reduce_max(tf.math.abs(inputs.to_float()), self.axis)
            # If max_values never updated set their newly computed values otherwise
            # update with moving average algorithm
            if momentum == -1:
                OutputQuantizer._assign_new_value(self.max_value, max_value)
            else:
                OutputQuantizer._assign_moving_average(
                    self.max_value, max_value, momentum, input_batch_size)

        # Rescale to center around max_value and compress to a lower bitwidth
        frac_bits = tf.stop_gradient(FixedPoint.max_frac_bits(self.value_bits, self.max_value))
        inputs, shift_value = inputs.rescale(frac_bits, self.value_bits)
        # update shift values
        self.shift(shift_value)
        return inputs

    def get_config(self):
        """Get the config of the layer.

        Returns:
            dict: the config of the layer.
        """
        config = super().get_config()
        config.update({"momentum": self.momentum})
        config.update({"scale_bits": self.scale_bits})
        config.update({"axis": self._axis})
        return config
