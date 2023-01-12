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

from .quantizers import AlignedWeightQuantizer, OutputQuantizer
from ..tensors import QTensor, FixedPoint, MAX_BUFFER_BITWIDTH


# Restrict list of exported symbols on default import
__all__ = ["ClassToken", "QuantizedClassToken",
           "AddPositionEmbs", "QuantizedAddPositionEmbs",
           "ExtractToken", "QuantizedExtractToken"]


@tf.keras.utils.register_keras_serializable()
class ClassToken(keras.layers.Layer):
    """Append a class token to an input layer."""

    def build(self, input_shape):
        super().build(input_shape)
        cls_init = keras.initializers.TruncatedNormal(stddev=0.02)
        self.hidden_size = input_shape[-1]
        self.cls = tf.Variable(
            name="cls",
            initial_value=cls_init(
                shape=(1, 1, self.hidden_size), dtype="float32"),
            trainable=True,
        )

    def call(self, inputs):
        batch_size = tf.shape(inputs)[0]
        cls_broadcasted = tf.cast(
            tf.broadcast_to(self.cls, [batch_size, 1, self.hidden_size]),
            dtype=inputs.dtype,
        )
        return tf.concat([cls_broadcasted, inputs], 1)


@tf.keras.utils.register_keras_serializable()
class AddPositionEmbs(keras.layers.Layer):
    """Adds (optionally learned) positional embeddings to the inputs."""

    def build(self, input_shape):
        assert len(
            input_shape) == 3, f"Number of dimensions should be 3, got {len(input_shape)}"
        super().build(input_shape)
        pe_init = keras.initializers.TruncatedNormal(stddev=0.02)
        self.pe = tf.Variable(
            name="pos_embedding",
            initial_value=pe_init(shape=(1, input_shape[1], input_shape[2])),
            dtype="float32",
            trainable=True,
        )

    def call(self, inputs):
        return inputs + tf.cast(self.pe, dtype=inputs.dtype)


@tf.keras.utils.register_keras_serializable()
class QuantizedClassToken(ClassToken):
    """Quantize the :class:`ClassToken` layer, allowing quantization of the output.

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
        self.cls_quantizer = AlignedWeightQuantizer(
            name="cls_quantizer", **quant_config["cls_quantizer"])
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1

    def call(self, inputs):
        # raise an error if the inputs are not QTensor
        if not isinstance(inputs, QTensor):
            raise TypeError(f"QuantizedClassToken only accepts QTensor\
                              inputs. Receives {type(inputs)} inputs.")

        batch_size = tf.shape(inputs.values)[0]
        inputs = inputs.promote(self.buffer_bitwidth)

        # Quantize the token and align it with the inputs
        cls = self.cls_quantizer(self.cls, inputs)

        # We need to broadcast the token along the batch size and set its token dimension to 1
        cls_broadcasted = tf.broadcast_to(cls, [batch_size, 1, self.hidden_size])

        outputs = tf.concat([cls_broadcasted, inputs], 1)

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config


@tf.keras.utils.register_keras_serializable()
class QuantizedAddPositionEmbs(AddPositionEmbs):
    """Quantize the :class:`AddPositionEmbs` layer, allowing operations in FixedPoint domain.

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
        self.pe_quantizer = AlignedWeightQuantizer(
            name="pe_quantizer", **quant_config["pe_quantizer"])
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1

    def call(self, inputs):
        # raise an error if the inputs are not QTensor
        if not isinstance(inputs, QTensor):
            raise TypeError(f"QuantizedAddPositionEmbs only accepts QTensor\
                              inputs. Receives {type(inputs)} inputs.")

        inputs = inputs.promote(self.buffer_bitwidth)
        # Quantize position embeddings and align them on the inputs
        pe = self.pe_quantizer(self.pe, inputs)

        # Add position embeddings
        outputs = inputs + pe

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config


@tf.keras.utils.register_keras_serializable()
class ExtractToken(keras.layers.Layer):
    """ Wrapper class of `tf.gather` operation that allows to extract a Token.

    Args:
        token (int): the indice of the token to extract.

    """

    def __init__(self, *args, token, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token

    def call(self, inputs):
        return tf.gather(inputs, self.token, axis=1)

    def get_config(self):
        config = super().get_config()
        config.update({"token": self.token})
        return config


@tf.keras.utils.register_keras_serializable()
class QuantizedExtractToken(ExtractToken):
    """ Quantized version of the ExtractToken layer. Accepts only FixedPoint inputs.
    """

    def call(self, inputs):
        if not isinstance(inputs, FixedPoint):
            # If the inputs is not a FixedPoint, raise an error
            raise TypeError(f"QuantizedExtractToken only accepts FixedPoint\
                              inputs. Receives {type(inputs)} inputs.")
        return tf.gather(inputs, self.token, axis=1)
