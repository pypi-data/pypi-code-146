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

from quantizeml.layers import WeightQuantizer, OutputQuantizer, QuantizedReLU
from quantizeml.tensors import QFloat, ceil_log2, floor_log2


def check_quantization(model):
    """Checks the specified model quantization.

    It looks for errors that can be fixed in the quantization configuration:

    - inaccurate weight scales quantization,
    - saturation in integer operations.

    Args:
        model (keras.Model): the model to check

    Returns:
        list(str): the quantization issues that were detected
    """
    messages = []
    for layer in model.layers:
        for name, attr in layer.__dict__.items():
            if isinstance(attr, WeightQuantizer):
                quantizer = attr
                if name == "bias_quantizer":
                    w = layer.bias
                elif name == "dw_weight_quantizer":
                    w = layer.depthwise_kernel
                elif name == "pw_weight_quantizer":
                    w = layer.pointwise_kernel
                elif name == "beta_quantizer":
                    w = layer.get_weights()[1]
                else:
                    w = layer.get_weights()[0]
                w_q = quantizer(w)
                if isinstance(w_q, QFloat):
                    axis = list(range(len(w.shape) - 1))
                    max_values = tf.reduce_max(tf.abs(w), axis)
                    ideal_scales = QFloat.optimal_scales(max_values, quantizer.value_bits)
                    err = tf.abs(ideal_scales - w_q.scales) / tf.abs(ideal_scales)
                    mean_err = tf.reduce_mean(err)
                    if mean_err > 5e-2:
                        message = f"Scales quantization relative error is high in " \
                                    f"{layer.name}/{quantizer.name}: {mean_err:.4f}."
                        if quantizer._axis == "per-tensor":
                            message += "Use a per-axis quantizer and/or increase scales bits."
                        else:
                            message += "Try increasing scales bits."
                        messages.append(message)
            elif isinstance(attr, OutputQuantizer):
                quantizer = attr
                max_value = quantizer.get_weights()[0]
                if tf.reduce_all(max_value == 1):
                    messages.append(f"{layer.name}/{quantizer.name} is not calibrated.")
                    continue
                # Since output quantizer max_values are evaluated by dividing the FixedPoint
                # integer values by their PoT scales, the result can only be a PoT (positive
                # or negative) if the initial value was a PoT. This is very unlikely to
                # happen except if the previous operation saturated its output, resulting in
                # a clip to a PoT.
                pot_max_value = ceil_log2(max_value) == floor_log2(max_value)
                if isinstance(layer, QuantizedReLU):
                    # Remove false positives clipped to zero
                    pot_max_value = tf.math.logical_and(max_value != 0., pot_max_value)
                    # Remove false positives clipped to the ReLU max_value
                    pot_max_value = tf.math.logical_and(max_value != layer.max_value, pot_max_value)
                if tf.reduce_any(pot_max_value):
                    messages.append(f"Saturation detected before {layer.name}/{quantizer.name}: "
                                    "check the previous operation and/or increase buffer bitwidth.")
    return messages
