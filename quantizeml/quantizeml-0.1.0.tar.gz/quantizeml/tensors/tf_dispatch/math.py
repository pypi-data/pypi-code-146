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
from ..fixed_point import FixedPoint
from ..qfloat import QFloat


@tf.experimental.dispatch_for_api(tf.add)
def fp_add(x: FixedPoint, y: FixedPoint):
    return x + y


@tf.experimental.dispatch_for_api(tf.add)
def qf_add(x: QFloat, y: QFloat):
    return x + y


@tf.experimental.dispatch_for_api(tf.clip_by_value)
def fp_clip_by_value(t: FixedPoint,
                     clip_value_min: FixedPoint,
                     clip_value_max: FixedPoint,
                     name=None):
    """Clips tensor values to a specified min and max.

    Args:
        t (:obj:`FixedPoint`): the FixedPoint to be clipped.
        clip_value_min (:obj:`FixedPoint`): the minimum value.
        clip_value_max (:obj:`FixedPoint`): the maximum value.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the clipped FixedPoint.
    """
    # The fractional bits of all inputs must be equal
    assert_equal(t.frac_bits, clip_value_min.frac_bits)
    assert_equal(t.frac_bits, clip_value_max.frac_bits)
    clip_values = tf.clip_by_value(t.values, clip_value_min.values, clip_value_max.values, name)
    return FixedPoint(clip_values, t.value_bits, t.frac_bits)


@tf.experimental.dispatch_for_api(tf.clip_by_value)
def qf_clip_by_value(t: QFloat,
                     clip_value_min: QFloat,
                     clip_value_max: QFloat,
                     name=None):
    """Clips tensor values to a specified min and max.

    Args:
        t (:obj:`QFloat`): the QFloat to be clipped.
        clip_value_min (:obj:`QFloat`): the minimum value.
        clip_value_max (:obj:`QFloat`): the maximum value.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`QFloat`: the clipped QFloat.
    """
    # The scales of all inputs must be equal
    assert_equal(t.scales, clip_value_min.scales)
    assert_equal(t.scales, clip_value_max.scales)
    clip_fp = tf.clip_by_value(t.fp, clip_value_min.fp, clip_value_max.fp, name)
    return QFloat(clip_fp, t.scales)


def _check_last_dim_reduced(input_tensor, axis):
    last_dim = input_tensor.shape.ndims - 1
    last_dim_reduced = axis is None or axis == -1 or axis == last_dim
    if isinstance(axis, (list, tuple)):
        last_dim_reduced = last_dim_reduced or last_dim in axis
    if last_dim_reduced:
        # The last dimension will be collapsed: inputs must be quantized per-tensor
        input_tensor.assert_per_tensor()


@tf.experimental.dispatch_for_api(tf.math.reduce_sum)
def fp_reduce_sum(input_tensor: FixedPoint, axis=None, keepdims=False, name=None):
    """Computes the sum of elements across dimensions of a FixedPoint.

    Args:
        input_tensor (:obj:`FixedPoint`): the FixedPoint to be summed.
        axis (list, optional): the dimensions to reduce. If None, reduces all
            dimensions. Defaults to None.
        keepdims (bool, optional): if true, retains reduced dimensions with length 1.
            Defaults to False.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the summed FixedPoint.
    """
    _check_last_dim_reduced(input_tensor, axis)

    # Reduce sum
    s_values = tf.math.reduce_sum(
        input_tensor.values, axis, keepdims=keepdims, name=name)

    # Return a new FixedPoint
    return FixedPoint(s_values, input_tensor.value_bits, input_tensor.frac_bits)


@tf.experimental.dispatch_for_api(tf.math.reduce_sum)
def qf_reduce_sum(input_tensor: QFloat, axis=None, keepdims=False, name=None):
    """Computes the sum of elements across dimensions of a QFloat.

    Args:
        input_tensor (:obj:`QFloat`): the QFloat to be summed.
        axis (list, optional): the dimensions to reduce. If None, reduces all
            dimensions. Defaults to None.
        keepdims (bool, optional): if true, retains reduced dimensions with length 1.
            Defaults to False.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`QFloat`: the summed QFloat.
    """
    _check_last_dim_reduced(input_tensor, axis)

    # Reduce sum
    s_fp = tf.math.reduce_sum(input_tensor.fp, axis, keepdims=keepdims, name=name)

    # Return a new QFloat with the same scales
    return QFloat(s_fp, input_tensor.scales)


@tf.experimental.dispatch_for_api(tf.math.reduce_max)
def fp_reduce_max(input_tensor: FixedPoint,
                  axis=None,
                  keepdims=False,
                  name=None):
    """Computes the maximum of elements across dimensions of a FixedPoint.

    Args:
        input_tensor (:obj:`FixedPoint`): the FixedPoint to be estimated.
        axis (list, optional): the dimensions to reduce. If None, reduces all
            dimensions. Defaults to None.
        keepdims (bool, optional): if true, retains reduced dimensions with length 1.
            Defaults to False.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the maximum FixedPoint.
    """
    # We only support reduce_max if the input is per-tensor
    input_tensor.assert_per_tensor()

    # Reduce max
    s_values = tf.math.reduce_max(input_tensor.values,
                                  axis,
                                  keepdims=keepdims,
                                  name=name)
    # Return a new FixedPoint
    return FixedPoint(s_values, input_tensor.value_bits, input_tensor.frac_bits)
