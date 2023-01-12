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
import warnings
import tensorflow as tf

from ..fixed_point import FixedPoint


def warn_float_conversion(x, op):
    if tf.executing_eagerly():
        x_name = "FixedPoint"
    else:
        x_name = x.name
    warnings.warn(f"Reverting {x_name} to float to perform {op} with Tensor")


@tf.experimental.dispatch_for_binary_elementwise_apis(FixedPoint, tf.Tensor)
def fp_tensor_binary_elementwise_api_handler(api_func, x, y):
    warn_float_conversion(x, api_func)
    return api_func(x.to_float(), y)


@tf.experimental.dispatch_for_binary_elementwise_apis(tf.Tensor, FixedPoint)
def tensor_fp_binary_elementwise_api_handler(api_func, x, y):
    warn_float_conversion(y, api_func)
    return api_func(x, y.to_float())
