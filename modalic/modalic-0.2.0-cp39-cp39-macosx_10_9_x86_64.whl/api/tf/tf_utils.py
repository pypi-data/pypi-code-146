#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

"""Utilities for using Tensorflow as primary ML framework."""
from typing import List

import numpy as np
import tensorflow as tf

from modalic.utils import shared


def check_keras_model(func):
    r"""Decorator that determines wether the model is a Tf keras model object or not."""

    def inner(model, *args, **kwargs):
        if isinstance(model, tf.keras.Model):
            return func(model)
        else:
            raise TypeError(
                f"Unknown model type: {type(model)}. Consider inheriting from tf.keras.Model."
            )

    return inner


def _set_tf_weights(model: tf.keras.Model, weights: shared.Weights) -> tf.keras.Model:
    r"""Set model weights from a list of NumPy ndarrays.

    :param model: Tf keras model object.
    :param weights: Model weights as a list of NumPy ndarrays.
    :returns: Tensorflow model object that is updated with input weights.
    """
    model.set_weights(weights)
    return model


@check_keras_model
def _get_tf_weights(model: tf.keras.Model) -> shared.Weights:
    r"""Get model weights as a list of NumPy ndarrays.

    :param model: Tf keras model object.
    :returns: Weights as a list of NumPy ndarrays.
    """
    return model.get_weights()


def _translate_tf_model_dtype(tf_type: str) -> str:
    r"""Translates the data type of tensorflow model to server interpretable dtype.

    :param tf_type: Extracted tf dtype (https://www.tensorflow.org/api_docs/python/tf/dtypes)
    :returns: dtype: Encodes the data type of the model as a String. Options are
        "F32" and "F64".
    :raises ValueError: If data type is not either 'float32' or 'float64'."""
    if tf_type == "float32":
        dtype = "F32"
    elif tf_type == "float64":
        dtype = "F64"
    else:
        raise ValueError(
            f"{tf_type} is not supported by aggregation server. \
            Federation will fail. Please use 'float32' or 'float64'."
        )
    return dtype


@check_keras_model
def _get_tf_model_dtype(model: tf.keras.Model) -> str:
    r"""Extracts the data type of the Tensorflow model.

    :param model: Tf keras model object.
    :returns: dtype: Encodes the data type of the model as a String. Options are
        "F32" and "F64".
    :raises TypeError:
    """
    return _translate_tf_model_dtype(model.dtype)


@check_keras_model
def _get_tf_model_shape(model: tf.keras.Model) -> List[np.ndarray]:
    r"""Extracts the shape of the Tensorflow model.

    :param model: Tensorflow model object.
    :returns: List of np.ndarray which contains the shape (size) of each individual layer of the model.
    """
    weights = model.get_weights()
    if len(weights) != 0:
        return [np.array(layer.shape) for layer in weights]
    else:
        raise AttributeError(
            f"The {model} has never been called, therefore the model is empty and its shape cannot determined."
        )
