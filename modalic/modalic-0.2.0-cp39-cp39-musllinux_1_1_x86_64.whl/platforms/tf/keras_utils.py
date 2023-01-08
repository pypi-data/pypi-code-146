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
"""Tf Keras specific Helper Functions"""
from typing import List

import numpy as np
import tensorflow as tf

from modalic.platforms.common.serde import _float_to_np_ndarray, _ser_np_weights


def check_keras_model(func):
    r"""Decorator that determines wether the model
    is a tf.keras.Model object or not.
    """

    def inner(model, *args, **kwargs):
        if isinstance(model, tf.keras.Model):
            return func(model)
        else:
            raise TypeError(
                f"Unknown model type: {type(model)}. Consider inheriting from tf.keras.Model."
            )

    return inner


@check_keras_model
def serialize_tf_keras_model(model: tf.keras.Model) -> list:
    r"""Serializes tf keras model as `py list`.

    :param model: tf.keras.Model: Model groups layers into
        an object with training and inference features.
    :returns: One level list of py floats.
    """
    return _ser_np_weights(model.get_weights())


@check_keras_model
def deserialize_tf_keras_model(
    model: tf.keras.Model, tensor: list, layer_shape: List[np.ndarray]
) -> tf.keras.Model:
    """Deserializes a py list to a torch model and sets the weights in the given model.

    :param model: Torch model.
    :param tensor: List of float representing the model weights.
    :layer_shape: Shape of the model which should be reconstructed.
    """
    weights = _float_to_np_ndarray(tensor, layer_shape)

    model.set_weights(weights)
    return model


@check_keras_model
def get_tf_keras_model_dtype(model: tf.keras.Model) -> str:
    r"""Extracts the data type of the Tensorflow model.

    :param model: Tf keras model object.
    :returns: dtype: Encodes the data type of the model as a String. Options are
        "F32" and "F64".
    :raises TypeError:
    """
    return model.dtype


@check_keras_model
def get_tf_keras_model_shape(model: tf.keras.Model) -> List[np.ndarray]:
    r"""Extracts the shape of the Tf.keras.Model.

    :param model: Tensorflow model object.
    :returns: List of np.ndarray which contains the shape (size)
        of each individual layer of the model.
    """
    weights = model.get_weights()
    if len(weights) != 0:
        return [np.array(layer.shape) for layer in weights]
    else:
        raise AttributeError(
            f"The {model} has never been called, therefore the model is empty and its shape cannot determined."
        )
