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

import re
import warnings

from keras import Model

from .utils import deep_clone_model, insert_layer
from .transforms import invert_batchnorm_pooling, fold_batchnorms
from ..layers import (QuantizedDense, QuantizedLayerNormalization, QuantizedAddPositionEmbs,
                      QuantizedClassToken, QuantizedReLU, QuantizedAdd, QDropout,
                      QuantizedReshape, QuantizedAttention, QuantizedConv2D, QuantizedMaxPool2D,
                      QuantizedGlobalAveragePooling2D, QuantizedExtractToken, Dequantizer,
                      QuantizedSeparableConv2D, QuantizedFlatten,
                      OutputQuantizer, WeightQuantizer, QuantizedConv2DTranspose,
                      QuantizedShiftmax, QuantizedSeparableConv2DTranspose,
                      QuantizedDepthwiseConv2D, QuantizedUnfoldPatches, QuantizedFoldPatches,
                      QuantizedConcatenate, QuantizedRescaling)

# Mapper to match float layer with its quantized version
CUSTOM_QLAYERS = {
    "Conv2D": QuantizedConv2D, "Dense": QuantizedDense, "Add": QuantizedAdd,
    "AddPositionEmbs": QuantizedAddPositionEmbs, "ClassToken": QuantizedClassToken,
    "ReLU": QuantizedReLU, "Dropout": QDropout,
    "LayerMadNormalization": QuantizedLayerNormalization, "Reshape": QuantizedReshape,
    "Attention": QuantizedAttention, 'MaxPooling2D': QuantizedMaxPool2D,
    'GlobalAveragePooling2D': QuantizedGlobalAveragePooling2D,
    "ExtractToken": QuantizedExtractToken, "SeparableConv2D": QuantizedSeparableConv2D,
    "Flatten": QuantizedFlatten, "PaddedConv2D": QuantizedConv2D,
    "Conv2DTranspose": QuantizedConv2DTranspose, "Shiftmax": QuantizedShiftmax,
    "SeparableConv2DTranspose": QuantizedSeparableConv2DTranspose,
    "DepthwiseConv2D": QuantizedDepthwiseConv2D, "UnfoldPatches": QuantizedUnfoldPatches,
    "FoldPatches": QuantizedFoldPatches, "Concatenate": QuantizedConcatenate,
    "Rescaling": QuantizedRescaling
}
# List of Quantizer layer's that do not have a float layer representation
NO_FLOAT_CUSTOM_QLAYERS = [Dequantizer, OutputQuantizer, WeightQuantizer]


def _handle_not_quantizable_layers(model):
    """ Checks if the model has not quantizable layers and adds a Dequantizer before.

    Args:
        model (keras.Model): model to check

    Returns:
        keras.Model: the updated model
    """
    def is_quantizable(layer):
        layer_class = layer.__class__
        return (layer_class.__name__ in CUSTOM_QLAYERS or layer_class in CUSTOM_QLAYERS.values()
                or layer_class in NO_FLOAT_CUSTOM_QLAYERS)

    # Find layers that cannot be quantized
    for layer in model.layers:
        if not is_quantizable(layer):
            # This layer cannot be quantized, check its inbounds
            inbound = layer.inbound_nodes[0]
            if not inbound.inbound_layers:
                # Skip input layers
                continue
            elif isinstance(inbound.inbound_layers, list):
                raise RuntimeError(f"'{layer.name}' is not quantizable and has multiple inbounds "
                                   "which is not supported.")

            # Check if the layer inbound will be quantized but is not a Dequantizer to prevent
            # adding an additional Dequantizer.
            if (is_quantizable(inbound.inbound_layers) and
                    not isinstance(inbound.inbound_layers, Dequantizer)):
                # Inbound will be quantized, add a Dequantizer after it and return the model
                inbound_name = inbound.inbound_layers.name
                model = insert_layer(model, inbound_name,
                                     Dequantizer(name=f"{inbound_name}_float_output"))
                warnings.warn(f"'{layer.name}' of type {layer.__class__} is not supported to "
                              "quantize, a Dequantizer is added before it and quantization will "
                              "stop at this layer.")
                return model
    return model


def quantize(model, q_config, add_dequantizer=True):
    """Quantizes the model using the provided configuration.

    Applying the quantization configuration is done in two steps, giving priority to the first:

    1. Match the quantization configuration from the layer name, as long as the final part of its
       name matches with the configuration key.
       Example: To quantize all "Transformer/EncoderBlock_x/MlpBlock/activation" layers, a
       configuration with the key "activation" or "MlpBlock/activation" will be enough. This allows
       the possibility to have a specific configuration for the activation function of block 5 using
       the "Transformer/EncoderBlock_5/MlpBlock/activation" key.

       Notes:

            * If configuration for all blocks are not defined, a global configuration is required.
            * To avoid ambiguity, the key with the most details in terms of hierarchy should be
              selected, e.g. "activation" key in the quantization configuration will be enough to
              quantize all "activation" layers. However, if it is required to define a different
              configuration in all MLP blocks activations, configuration key should be
              "MlpBlock/activation" instead.

    2. Match the quantization configuration from the layer name, as long as the format
       '.../ParentLayer<_i>/SubParentLayer<_j>/.../Layer<_k>' matches with layer.name, where {i, j,
       k} are optional integers. Example: "EncoderBlock/add" key will quantize all layers ending
       with the format "EncoderBlock_i/add_j" ("EncoderBlock_0/add_0", "EncoderBlock_0/add_1",
       "EncoderBlock_1/add_0", "EncoderBlock_1/add_1", ...).

        Note:

            The configuration priority in this case is defined by the number of hierarchical terms
            and the detail in subindices from the end to the beginning of the key name. That is
            "EncoderBlock/add_0" will have priority over "EncoderBlock/add" and
            "EncoderBlock_0/add". The "EncoderBlock_0/add_0" case is covered by the previous point.

    Args:
        model (keras.Model): the model to quantize
        q_config (dict): quantization configuration
        add_dequantizer (bool, optional): allows to convert output to float. Defaults to True.

    Returns:
        keras.Model: the quantized model
    """
    # Add "/" at the beginning of the names, to avoid ambiguity (e.g. "Dense" and "DropoutDense")
    q_config = {key if key[0] == "/" else "/" + key: value for key, value in q_config.items()}

    # This iterates through the <key, config> in the JSON, and creates a regexp based on the key.
    # The regexp is built by:
    #   - identifying items with the '/' separator,
    #   - replace trailing <_N> in each item by a matching pattern,
    #   - concatenate back items matching patterns.
    q_config_regex = {re.compile("/" + r"(?:|_[\d]+)/".join(key[1:].split('/')) + r"(?:|_[\d]+)$"):
                      (key[1:], obj) for key, obj in q_config.items()}

    # Layers will no longer be quantized as soon as a Dequantizer is found
    quantization_stopped = False

    def _replace_layer(layer):
        nonlocal quantization_stopped
        config = layer.get_config()

        # Function to handle unsupported arguments in config
        def pop_unsupported_args(class_type):
            for arg, default_value in getattr(class_type, "unsupported_args", {}).items():
                if (arg in config and config[arg] != default_value):
                    raise RuntimeError(
                        f"Argument '{arg}' in layer '{layer.name}' is only "
                        f"supported with default value '{default_value}'. "
                        f"Receives '{config[arg]}'.")
                config.pop(arg, None)

        # Function that return a quantized layer given its float version
        def get_quantize_layer(layer, quantize_config={}):
            """Quantize float layer in three steps:
                - first, we get its quantized version,
                - second, remove unsupported arguments,
                - then, we return the quantized layer with config updated
            """
            nonlocal quantization_stopped
            class_name = layer.__class__.__name__
            # 1.1 Check if qlayer exists in custom layers
            if class_name in CUSTOM_QLAYERS:
                qlayer = CUSTOM_QLAYERS[class_name]
            # 1.2 Else, return the float version of the layer
            else:
                qlayer = layer
                qlayer_class = qlayer.__class__
                if not (qlayer_class in CUSTOM_QLAYERS.values() or
                        qlayer_class in NO_FLOAT_CUSTOM_QLAYERS):
                    warnings.warn(
                        f"'{class_name}' is not supported to quantize. It will be ignored.")
                # If a Dequantizer is found, quantization must be stopped
                quantization_stopped = isinstance(layer, Dequantizer)

            # 2. Remove unsupported arguments
            pop_unsupported_args(qlayer)

            # 3. Instantiate quantized layer
            if len(quantize_config) > 0:
                config['quant_config'] = quantize_config
            return qlayer.from_config(config)

        # When a not quantizable layer is found, stop quantization returning initial layer
        if quantization_stopped:
            return layer.from_config(config)

        # Replace float layer by quantized layer in three different ways:
        # 1. Check if layer is in quant_config (to quantize specific layers)
        layer_name = layer.name if layer.name[0] == "/" else "/" + layer.name
        match_name = [key for key in q_config.keys() if layer_name.endswith(key)]
        if len(match_name) > 0:
            # In case of multiple matches, take the most hierarchical specific one
            match_name = sorted(match_name, key=lambda x: len(
                x.split('/')), reverse=True)[0]
            match_conf = q_config[match_name]
            return get_quantize_layer(layer, match_conf)

        # 2. Suppose that the layer name has the following format:
        #    .../ParentLayer<_i>/SubParentLayer<_j>/.../Layer<_k>, where ijk are integers and
        #    <_i>, <_j>, <_k> are optional.
        #    Match the pattern and replace the layer with a quantized version.
        match_tuples = []
        for rkey, qobj in q_config_regex.items():
            if rkey.search(layer_name):
                match_tuples.append(qobj)
        if len(match_tuples) > 0:
            # In case of multiple matches, takes the configurations with the highest hierarchy
            max_hierarchy = max([len(qobj[0].split('/'))
                                for qobj in match_tuples])
            match_tuples = {tuple(qobj[0].split('/')[::-1]): qobj[1]
                            for qobj in match_tuples if len(qobj[0].split('/')) == max_hierarchy}
            # And then, chooses the configuration with the most detailed sub-indices,
            # from the end to the beginning.
            #
            # For example, if the layer name is: A_1/B_2/C_3/D_4, and the config keys are:
            # keys = [B_2/C/D, B/C_3/D], the code will search the first exact match from bottom
            # to top, following:
            # First step (layer_name[0], keys[0]): if D_4 == D ? No, go to next step
            # Second step (layer_name[0], keys[1]): if D_4 == D ? No, go to next step
            # Third step (layer_name[1], keys[0]): if C_3 == C ? No, go to next step
            # Fourth step (layer_name[1], keys[1]): if C_3 == C_3 ? Yes, match with config[key[1]]
            #
            # Note: If only exist this keys in config file, keys[0] will be used in the following
            # layers: A_i/B_2/C_j/D_k, for all ijk in [0, ..., n] and j != 3.
            for (idx, pattern) in enumerate(layer_name[1:].split('/')[::-1]):
                match_tuples_copy = {}
                for (key, match_conf) in match_tuples.items():
                    if key[idx] == pattern:
                        match_tuples_copy[key] = match_conf
                # If only one match is found, it is used as the configuration
                if len(match_tuples_copy) == 1:
                    match_conf = list(match_tuples_copy.values())[0]
                    break
                # If length of keys is smaller than hierarchical name, use the last match_conf
                if idx + 1 >= max_hierarchy:
                    break
                # Update match_tuples only when patterns match, in case of a tie
                if len(match_tuples_copy) > 1:
                    match_tuples = match_tuples_copy
            return get_quantize_layer(layer, match_conf)

        # 3. Special cases for Embedding layers
        #    Cases covered in previous steps

        # If no match, return the qlayer with config unchanged
        try:
            qlayer = get_quantize_layer(layer)
        except TypeError as e:
            if "required keyword-only argument: 'quant_config'" in str(e):
                raise TypeError(f"Make sure layer '{layer.name}' is not missing a configuration.") \
                    from e
            raise e
        return qlayer

    # Invert BN <-> Pooling layers and fold BN into their preceding layers
    model = invert_batchnorm_pooling(model)
    model = fold_batchnorms(model)

    # Check if the model has not quantizable layers and add a Dequantizer before
    model = _handle_not_quantizable_layers(model)

    # Quantize the model replacing layers with their quantized version
    new_model = deep_clone_model(model, clone_function=_replace_layer)
    out = new_model.outputs

    # Append Dequantizer at the end of the model to convert the output to float value
    if (add_dequantizer and not isinstance(new_model.layers[-1], Dequantizer)
            and not quantization_stopped):
        out = Dequantizer(name="float_output")(out)
    return Model(new_model.input, out)


def dump_config(model):
    """Dump the quantization configuration of a quantized model, exporting the configuration for
    each quantized layer.

    Args:
        model (keras.Model): a quantized model.

    Returns:
        dict: the configuration of the model.
    """
    # Get the configuration of the model, iterating over each layer and updating on config.
    config = {}
    for layer in model.layers:
        # Try to take the current quantized configuration
        ly_config = layer.get_config().get('quant_config')

        # Only append quantized configuration
        if layer.__class__ in CUSTOM_QLAYERS.values() and ly_config is not None:
            config[layer.name] = ly_config

    return config
