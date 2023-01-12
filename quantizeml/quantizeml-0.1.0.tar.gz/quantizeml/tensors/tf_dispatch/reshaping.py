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
from typing import List

from ...debugging import assert_equal
from .. import FixedPoint, QFloat


@tf.experimental.dispatch_for_api(tf.shape)
def fp_shape(input: FixedPoint, out_type=tf.dtypes.int32, name=None):
    return tf.shape(input.values, out_type, name)


@tf.experimental.dispatch_for_api(tf.shape)
def qf_shape(input: QFloat, out_type=tf.dtypes.int32, name=None):
    return tf.shape(input.fp, out_type, name)


@tf.experimental.dispatch_for_api(tf.reshape)
def fp_reshape(tensor: FixedPoint, shape, name=None):
    if not tensor.per_tensor:
        # Different fractional-bits are defined for the last axis, so
        # it must be preserved during the reshape
        assert_equal(shape[-1], tf.shape(tensor)[-1])
    output = tf.reshape(tensor.values, shape, name)
    return FixedPoint(output, tensor.value_bits, tensor.frac_bits)


@tf.experimental.dispatch_for_api(tf.reshape)
def qf_reshape(tensor: QFloat, shape, name=None):
    if not tensor.per_tensor:
        # Different scales are defined for the last axis, so it must be preserved
        # during the reshape
        assert_equal(shape[-1], tf.shape(tensor.scales)[-1])
    # Reshape inner FixedPoint
    output_fp = tf.reshape(tensor.fp, shape, name)
    return QFloat(output_fp, tensor.scales)


@tf.experimental.dispatch_for_api(tf.transpose)
def fp_transpose(a: FixedPoint, perm=None, conjugate=False, name="transpose"):
    a.assert_per_tensor()
    output = tf.transpose(a.values, perm, conjugate, name)
    return FixedPoint(output, a.value_bits, a.frac_bits)


@tf.experimental.dispatch_for_api(tf.transpose)
def qf_transpose(a: QFloat, perm=None, conjugate=False, name="transpose"):
    a.assert_per_tensor()
    output_fp = tf.transpose(a.fp, perm, conjugate, name)
    return QFloat(output_fp, a.scales)


@tf.experimental.dispatch_for_api(tf.broadcast_to)
def fp_brodcast_to(input: FixedPoint, shape, name=None):
    """Broadcast a FixedPoint tensor for a compatible shape.

    Args:
        input (:obj:`FixedPoint`): a FixedPoint to broadcast.
        shape (:obj:`tf.Tensor`): an 1-D `int` Tensor representing
            the shape of the desired output. Must be one of the
            following types: `int32`, `int64`.
        name (str, optional): a name for the operation. Defaults to None.

    Returns:
        :obj:`FixedPoint`: the brodcasted output. Has the same
            type as `input`.
  """
    # Check first that the last dimension is unchanged
    tf.assert_equal(input.shape[-1], shape[-1], message="To brodcast FixedPoint input,\
                        last dimension should remain unchanged")
    output = tf.broadcast_to(input.values, shape, name)
    return FixedPoint(output, input.value_bits, input.frac_bits)


@tf.experimental.dispatch_for_api(tf.broadcast_to)
def qf_brodcast_to(input: QFloat, shape, name=None):
    """Broadcast a QFloat tensor for a compatible shape.

    Args:
        input (:obj:`QFloat`): a QFloat to broadcast.
        shape (:obj:`tf.Tensor`): an 1-D `int` Tensor representing
            the shape of the desired output. Must be one of the
            following types: `int32`, `int64`.
        name (str, optional): a name for the operation. Defaults to None.

    Returns:
        :obj:`QFloat`: the brodcasted output. Has the same
            type as `input`.
  """
    output_fp = tf.broadcast_to(input.fp, shape, name)
    return QFloat(output_fp, input.scales)


@tf.experimental.dispatch_for_api(tf.concat)
def fp_concat(values: List[FixedPoint], axis, name="concat"):
    """Concatenates FixedPoint tensors along one dimension.

    Args:
        values (List of :obj:`FixedPoint`): List of FixedPoint tensors
            to concatenate.
        axis (list): Dimension along which to concatenate.
        name (str, optional): the name for the Tensorflow ops.
            Defaults to "concat".

    Returns:
        :obj:`FixedPoint`: the concatenate output FixedPoint.
    """
    # For now we only support concatenation of one or two elements
    tf.debugging.assert_less_equal(
        len(values),
        2, f"We only support concatenation of one or two FixedPoint. \
           Receives {len(values)} tensors as input.")

    if len(values) == 1:
        return FixedPoint(values[0].values, values[0].value_bits, values[0].frac_bits)

    # Only support inputs with the same value bits
    tf.assert_equal(values[0].value_bits, values[1].value_bits, "We only support concatenation of "
                    f"inputs with same value_bits. Receives {values[0].value_bits} and "
                    f"{values[1].value_bits}.")

    # For now we don't support concatenation over last dimension
    rank_input = values[0].values.shape.ndims
    if axis < 0:
        dim = axis + rank_input
    else:
        dim = axis

    last_dim = dim == rank_input - 1

    # When dim is not last dimension FixedPoint tensors to concatenate should have the same
    # fractional bits
    if not last_dim:
        tf.assert_equal(values[0].frac_bits, values[1].frac_bits, message=f"the two\
                FixedPoint must have the same frac_bits. Receives {values[0].frac_bits}\
                and {values[1].frac_bits}")
        frac_bits_out = values[0].frac_bits
    else:
        # When dim is last dimension, if one of the two FixedPoint tensors to concatenate is
        # per-tensor, its frac_bits shape is extended like if it was per-axis, then frac_bits can be
        # concatenated
        frac_bits_a = values[0].frac_bits
        frac_bits_b = values[1].frac_bits
        if values[0].per_tensor:
            frac_bits_a = tf.fill((values[0].shape[axis],), values[0].frac_bits)
        if values[1].per_tensor:
            frac_bits_b = tf.fill((values[1].shape[axis],), values[1].frac_bits)
        # Concatenate frac_bits
        frac_bits_out = tf.concat([frac_bits_a, frac_bits_b], axis, f"{name}_frac_bits")

    values_out = tf.concat([values[0].values, values[1].values], axis, name)
    return FixedPoint(values_out, values[0].value_bits, frac_bits_out)


@tf.experimental.dispatch_for_api(tf.concat)
def qf_concat(values: List[QFloat], axis, name="concat"):
    """Concatenates QFloat tensors along one dimension.

    Args:
        values (List of :obj:`QFloat`): List of QFloat tensors
            to concatenate.
        axis (list): Dimension along which to concatenate.
        name (str, optional): the name for the Tensorflow ops.
            Defaults to "concat".

    Returns:
        :obj:`QFloat`: the concatenated output QFloat.
    """
    if len(values) == 1:
        return QFloat(values[0].fp, values[0].scales)

    # For now we only support concatenation of one or two elements
    tf.assert_equal(
        len(values),
        2, f"We only support concatenation of one or two QFloat. \
           Receives {len(values)} tensors as input.")

    # Convenience variables
    a, b = values

    # First, concatenate inner FixedPoint
    output_fp = tf.concat([a.fp, b.fp], axis, name)

    # Evaluate the index of the dimension on which we concatenate
    rank_input = a.values.shape.ndims
    if axis < 0:
        concat_dim = axis + rank_input
    else:
        concat_dim = axis

    if concat_dim == rank_input - 1:
        # When concatenating along the last dimension, we concatenate shapes.
        # If any one of the two QFloat tensors has a scalar shape, its scales
        # shape is extended to a vector as if it was per-axis.
        scales_a = a.scales
        if scales_a.shape.ndims == 0:
            n_scales = tf.shape(a.fp)[-1]
            scales_a = tf.fill((n_scales,), scales_a)
        scales_b = b.scales
        if scales_b.shape.ndims == 0:
            n_scales = tf.shape(b.fp)[-1]
            scales_b = tf.fill((n_scales,), scales_b)
        # The output scales is the concatenation of a and b scales
        output_scales = tf.concat([scales_a, scales_b], axis=-1, name=f"{name}_scales")
    else:
        # When concatenating on another axis, inputs must have the same scales
        tf.assert_equal(values[0].scales, values[1].scales,
                        "We only support concatenation of QFloat inputs with same scales."
                        f"Receives {a.scales} and {b.scales}.")
        output_scales = a.scales

    return QFloat(output_fp, output_scales)


@tf.experimental.dispatch_for_api(tf.expand_dims)
def fp_expand_dims(input: FixedPoint, axis, name=None):
    """Returns a tensor with a length 1 axis inserted at index `axis`.

    Args:
        input (FixedPoint): a `Tensor`.
        axis (int): integer specifying the dimension index at which to expand the shape of `input`.
            Given an input of D dimensions, `axis` must be in range `[-(D+1), D]` (inclusive).
        name (str, optional): name of the output `Tensor`. Defaults to None.

    Returns:
        FixedPoint: a tensor with the same data as `input`, with an additional dimension inserted at
            the index specified by `axis`.
    """
    # Only support per-tensor inputs
    input.assert_per_tensor()

    # Expand dimension on values
    values = tf.expand_dims(input.values, axis, name)

    # Return a new FixedPoint
    return FixedPoint(values, input.value_bits, input.frac_bits)


@tf.experimental.dispatch_for_api(tf.expand_dims)
def qf_expand_dims(input: QFloat, axis, name=None):
    """Returns a tensor with a length 1 axis inserted at index `axis`.

    Args:
        input (QFloat): a `Tensor`.
        axis (int): integer specifying the dimension index at which to expand the shape of `input`.
            Given an input of D dimensions, `axis` must be in range `[-(D+1), D]` (inclusive).
        name (str, optional): name of the output `Tensor`. Defaults to None.

    Returns:
        QFloat: a tensor with the same data as `input`, with an additional dimension inserted at
            the index specified by `axis`.
    """
    # Only support per-tensor inputs
    input.assert_per_tensor()

    # Expand dimension on inner FixedPoint
    expanded_fp = tf.expand_dims(input.fp, axis, name)

    # Return a new QFloat
    return QFloat(expanded_fp, input.scales)


@tf.experimental.dispatch_for_api(tf.compat.v1.gather)
def fp_gather(params: FixedPoint, indices, validate_indices=None,
              name=None, axis=None, batch_dims=0):
    """Gather slices from params along axis.

    Args:
        params (:obj:`FixedPoint`, :obj:`QFloat`): the input QTensor.
        indices (int, list): the indices to gather.
        validate_indices (bool, optional): whether to validate the indices. Defaults to None.
        name (str, optional): the name for the Tensorflow ops. Defaults to None.
        axis (int, optional): the axis to gather along. Defaults to None.
        batch_dims (int, optional): the number of batch dimensions to keep. Defaults to 0.

    Returns:
        :obj:`QTensor`: a QTensor containing the gathered values.
    """
    # We do not support gather along the last axis if the QTensor is per-axis
    if axis in (-1, len(params.shape)):
        params.assert_per_tensor()
    # Create a new QTensor, gather the indices in a desired axis
    x_gather = tf.gather(params.values, indices, validate_indices, axis, batch_dims, name)
    return FixedPoint(x_gather, params.value_bits, params.frac_bits)
