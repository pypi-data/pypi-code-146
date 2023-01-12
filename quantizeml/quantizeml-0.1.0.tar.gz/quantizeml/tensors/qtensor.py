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
from copy import copy
import tensorflow as tf


from ..debugging import assert_equal


@tf.function
@tf.custom_gradient
def round_through(x):
    rounded = tf.math.round(x)

    def grad(upstream):
        return upstream
    return rounded, grad


@tf.function
@tf.custom_gradient
def floor_through(x):
    floored = tf.math.floor(x)

    def grad(upstream):
        return upstream
    return floored, grad


@tf.function
@tf.custom_gradient
def ceil_through(x):
    ceiled = tf.math.ceil(x)

    def grad(upstream):
        return upstream
    return ceiled, grad


class QTensor(tf.experimental.ExtensionType):
    """Abstract class to exchange quantized tensors between layers
    """
    shape: tf.TensorShape  # Required to convert to a KerasTensor

    @property
    def name(self):
        """Returns the QTensor name

        Returns:
            str: the QTensor name
        """
        raise NotImplementedError

    @property
    def per_tensor(self):
        """Returns if QTensor is quantized per-tensor

        Returns:
            bool: True if QTensor is quantized per-tensor or False on per-axis case.
        """
        raise NotImplementedError

    def to_float(self):
        """Returns a float representation of the QTensor

        Returns:
            :obj:`tensorflow.Tensor`: the float representation.
        """
        raise NotImplementedError

    def clone(self):
        """Returns a copy of the QTensor

        Returns:
            :obj:`QTensor`: the copy.
        """
        return copy(self)

    def __str__(self):
        class_name = self.__class__.__name__
        x_float = self.to_float()
        return f"{class_name}: {x_float}"

    @staticmethod
    def int_max(value_bits):
        return 2 ** value_bits - 1

    @staticmethod
    def clamp(values, value_bits):
        int_max = QTensor.int_max(value_bits)
        return tf.clip_by_value(values, -int_max - 1, int_max)

    def assert_per_tensor(self):
        """Asserts that a QTensor is quantized per-tensor"""
        assert_equal(self.per_tensor, True, message=f"{self.name} is not per-tensor.")


def pow2(n):
    """Return the power of two of an integer

    Note that this goes through a float64 operation to obtain a float32 tensor.
    This makes sure the operation can run on a GPU without losing precision.

    Args:
        n (`tf.tensor`, int): the positive or negative exponent

    Returns:
        :obj:`tensorflow.Tensor`: a float tensor containing the PoT of the input.
    """
    return tf.cast(2.0 ** tf.cast(n, tf.float64), tf.float32)


def ceil_log2(x):
    """Return the closest power of two exponent of a float tensor.

    This evaluates for each element of the input tensor the integer exponent leading
    to the closest power-of-two higher than the input.

    In hardware, if the inputs are represented as integer, this operation can
    be implemented by identifying the leading bit index and increment the result
    by 1.

    Example: ceil_log2(7) = ceil_log2(0b00000111) = 2 + 1 = 3

    Args:
        x (:obj:`tensorflow.tensor`): the source tensor

    Returns:
        :obj:`tensorflow.Tensor`: a float tensor containing integer values
            representing the closest PoT exponents.
    """
    return ceil_through(tf.experimental.numpy.log2(tf.cast(x, tf.float32)))


def floor_log2(x):
    """Return the closest power of two exponent of a float tensor.

    This evaluates for each element of the input tensor the integer exponent leading
    to the closest power-of-two lower than the input (except if x < 1).

    In hardware, if the inputs are represented as integer, this operation can
    be implemented by identifying the leading bit index.

    Example: floor_log2(7) = floor_pow2(0b00000111) = 2

    Args:
        x (:obj:`tensorflow.tensor`): the source tensor

    Returns:
        :obj:`tensorflow.Tensor`: a float tensor containing integer values
            representing the closest PoT exponents.
    """
    return floor_through(tf.experimental.numpy.log2(tf.cast(x, tf.float32)))


def round_log2(x):
    """Return the closest power of two exponent of a float tensor.

    This evaluates for each element of the input tensor the integer exponent leading
    to the closest power-of-two.

    In hardware, if the inputs are represented as integer, this operation can
    be implemented by:
    - identifying the leading bit index,
    - increment by 1 if the previous bit is 1 also.

    Example: round_log2(7) = round_log2(0b00000111) = 2 + 1 = 3
             round_log2(5) = round_log2(0b00000101) = 2

    Args:
        x (:obj:`tensorflow.tensor`): the source tensor

    Returns:
        :obj:`tensorflow.Tensor`: a float tensor containing integer values
            representing the closest PoT exponents.
    """
    return round_through(tf.experimental.numpy.log2(tf.cast(x, tf.float32)))
