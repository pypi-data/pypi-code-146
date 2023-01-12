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
import keras
import tensorflow as tf

from ...tensors import FixedPoint

__all__ = ["UnfoldPatches", "QuantizedUnfoldPatches", "FoldPatches", "QuantizedFoldPatches"]


@tf.keras.utils.register_keras_serializable()
class UnfoldPatches(keras.layers.Layer):
    """ Unfold an input feature map into patches.

    Args:
        patch_size (int): the desired patch size
    """

    def __init__(self, patch_size, **kwargs):
        super().__init__(**kwargs)
        self.patch_size = patch_size
        self.patch_area = patch_size * patch_size

    def build(self, input_shape):
        assert len(input_shape) == 4, "UnfoldPatches only accepts 4D inputs"
        x, y = input_shape[1:3]
        self.num_patch_x = x // self.patch_size
        self.num_patch_y = y // self.patch_size
        self.num_patches = self.num_patch_x * self.num_patch_y

    def call(self, inputs):
        inputs_shape = tf.shape(inputs)
        batch_size = inputs_shape[0]
        channels = inputs_shape[3]

        # Convert from shape (batch_size, x, y, channels) to shape
        # (batch_size * patch_area, num_patches, channels)
        features = tf.transpose(inputs, [0, 3, 1, 2])
        patches = tf.reshape(features, (batch_size * channels * self.num_patch_x,
                             self.patch_size, self.num_patch_y, self.patch_size))
        patches = tf.transpose(patches, [0, 2, 1, 3])
        patches = tf.reshape(patches, (batch_size, channels, self.num_patches, self.patch_area))
        patches = tf.transpose(patches, [0, 3, 2, 1])
        patches = tf.reshape(patches, (batch_size * self.patch_area, self.num_patches, channels))

        # Return both the inputs shape tf.Tensor along with the patches because the tf.shape call
        # needs to be wrapped in the layer or it will be an issue for quantization
        return patches, inputs_shape

    def get_config(self):
        config = super().get_config()
        config["patch_size"] = self.patch_size
        return config


@tf.keras.utils.register_keras_serializable()
class QuantizedUnfoldPatches(UnfoldPatches):
    """An UnfoldPatches layer that operates on quantized inputs

    """
    def call(self, inputs):
        # raise an error if the inputs are not FixedPoint
        if not isinstance(inputs, FixedPoint):
            raise TypeError(f"QuantizedUnfoldPatches only accepts FixedPoint inputs.\
                            Receives {type(inputs)} inputs.")
        inputs_shape = tf.shape(inputs)
        batch_size = inputs_shape[0]
        channels = inputs_shape[3]

        # Convert from shape (batch_size, x, y, channels) to shape
        # (batch_size * patch_area, num_patches, channels)
        features = tf.transpose(inputs, [0, 3, 1, 2])
        patches = tf.reshape(features, (batch_size * channels * self.num_patch_x,
                             self.patch_size, self.num_patch_y, self.patch_size))
        patches = tf.transpose(patches, [0, 2, 1, 3])
        patches = tf.reshape(patches, (batch_size, channels, self.num_patches, self.patch_area))
        patches = tf.transpose(patches, [0, 3, 2, 1])
        patches = tf.reshape(patches, (batch_size * self.patch_area, self.num_patches, channels))
        return patches, inputs_shape


@tf.keras.utils.register_keras_serializable()
class FoldPatches(keras.layers.Layer):
    """ Fold patches into a feature maps tensor.

    Args:
        patch_size (int): the desired patch size
        num_patch_x (int): number of patches along x dimension
        num_patch_y (int): number of patches along y dimension
    """

    def __init__(self, patch_size, num_patch_x, num_patch_y, **kwargs):
        super().__init__(**kwargs)
        self.patch_size = patch_size
        self.patch_area = patch_size * patch_size
        self.num_patch_x = num_patch_x
        self.num_patch_y = num_patch_y
        self.num_patches = self.num_patch_x * self.num_patch_y

    def call(self, inputs):
        # inputs is made of patches inputs and the features shape tf.Tensor
        patches, features_shape = inputs

        tf.assert_equal(tf.size(features_shape), 4, "FoldPatches only accepts 4D features shape")
        batch_size = features_shape[0]
        channels = features_shape[3]

        # Convert from shape (batch_size * patch_area, num_patches, channels) back to shape
        # (batch_size, channels, x, y)
        features = tf.reshape(patches, (batch_size, self.patch_area, self.num_patches, -1))
        features = tf.transpose(features, (0, 3, 2, 1))
        features = tf.reshape(features, (batch_size * channels * self.num_patch_x,
                              self.num_patch_y, self.patch_size, self.patch_size))
        features = tf.transpose(features, (0, 2, 1, 3))
        features = tf.reshape(features, (batch_size, channels, self.num_patch_x *
                              self.patch_size, self.num_patch_y * self.patch_size))
        features = tf.transpose(features, (0, 2, 3, 1))
        return features

    def get_config(self):
        config = super().get_config()
        config["patch_size"] = self.patch_size
        config["num_patch_x"] = self.num_patch_x
        config["num_patch_y"] = self.num_patch_y
        return config


@tf.keras.utils.register_keras_serializable()
class QuantizedFoldPatches(FoldPatches):
    """A FoldPatches layer that operates on quantized inputs

    """
    def call(self, inputs):
        # inputs is made of patches inputs and the features shape tf.Tensor
        patches, features_shape = inputs

        # raise an error if the inputs are not FixedPoint
        if not isinstance(patches, FixedPoint):
            raise TypeError(f"QuantizedFoldPatches only accepts FixedPoint inputs.\
                            Receives {type(patches)} inputs.")

        tf.assert_equal(tf.size(features_shape), 4,
                        "QuantizedFoldPatches only accepts 4D features shape")
        batch_size = features_shape[0]
        channels = features_shape[3]

        # Convert from shape (batch_size * patch_area, num_patches, channels) back to shape
        # (batch_size, channels, x, y)
        features = tf.reshape(patches, (batch_size, self.patch_area, self.num_patches, -1))
        features = tf.transpose(features, (0, 3, 2, 1))
        features = tf.reshape(features, (batch_size * channels * self.num_patch_x,
                              self.num_patch_y, self.patch_size, self.patch_size))
        features = tf.transpose(features, (0, 2, 1, 3))
        features = tf.reshape(features, (batch_size, channels, self.num_patch_x *
                              self.patch_size, self.num_patch_y * self.patch_size))
        features = tf.transpose(features, (0, 2, 3, 1))
        return features
