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
"""
Common utility methods used in quantization models.
"""

import warnings
from copy import deepcopy
from pathlib import Path

import numpy as np
import tensorflow_addons as tfa
from keras.models import clone_model, load_model as kload_model, Model, Sequential
from keras.layers import serialize, Layer

from quantizeml.layers.quantizers import OutputQuantizer, Dequantizer

__all__ = ['load_model', 'deep_clone_model', 'insert_layer', 'load_weights', 'save_weights',
           'get_layers_by_type']


def load_model(model_path, custom_layers={}, compile_model=True):
    """Loads a model with Vision Transformer custom layers.

    Args:
        model_path (str): path of the model to load
        custom_layers (dict, optional): custom layers to add to the model. Defaults to {}.
        compile_model (bool, optional): whether to compile the model. Defaults to True.

    Returns:
        :class:`keras.models.Model`: the loaded model
    """
    # Given that all layers were imported in __init__.py, they are registered.
    # Therefore, we just need append GroupNormalization in the custom layers.
    custom_layers.update({'GroupNormalization': tfa.layers.GroupNormalization})
    return kload_model(model_path, custom_objects=custom_layers, compile=compile_model)


def deep_clone_model(model, *args, **kwargs):
    """Clone a model, assign variable to variable. Useful when a clone function is used,
    and new layers have not the same number of parameters as the original layer.

    Args:
        model (:class:`keras.models.Model`): model to be cloned
        args, kwargs (optional): arguments pass to :func:`keras.models.clone_model` function

    Returns:
        :class:`keras.models.Model`: the cloned model
    """
    new_model = clone_model(model, *args, **kwargs)
    variables_dict = {var.name: var for var in model.variables}
    apply_weights_to_model(new_model, variables_dict, False)
    return new_model


def insert_layer(model, target_layer_name, new_layer):
    """ Inserts the given layer in the model after the layer with the name target_layer_name.

    Note that new_layer type is restricted to (OutputQuantizer, Dequantizer).

    Args:
        model (keras.Model): the model to update
        target_layer_name (str): name of the layer after which to insert a layer
        new_layer (keras.Layer): layer to insert

    Raises:
        ValueError: when target_layer_name is not found in model or new_layer is not in
            (OutputQuantizer, Dequantizer)

    Returns:
        keras.Model: the new model
    """
    # Check that the model has a layer with then given target_layer_name
    if not any(ly.name == target_layer_name for ly in model.layers):
        raise ValueError(f'{target_layer_name} not found in model.')

    # Check added layer type
    if not isinstance(new_layer, (OutputQuantizer, Dequantizer)):
        raise ValueError(f'Inserted layer must be of type OutputQuantizer or Dequantizer, \
                        received {type(new_layer)}.')

    # get_config documentation mentions that a copy should be made when planning to modify the
    # config
    config = deepcopy(model.get_config())
    layers = deepcopy(config['layers'])

    # Prepare the layer configuration to be inserted
    new_layer_config = serialize(new_layer)

    # Handling sequential and functional models differently:
    #   - sequential models 'layers' configuration is a sorted list of the layers, so we just need
    #     to insert the new layer within that list,
    #   - for functional models, the layers inbound and outbounds are updated first
    if not isinstance(model, Sequential):
        # The layer name is added to the configuration
        new_layer_config['name'] = new_layer.name

        # Retrieve target_layer outbounds
        target_outbounds = model.get_layer(target_layer_name).outbound_nodes
        outbound_names = [outbound.layer.name for outbound in target_outbounds]

        # OutputQuantizer does not support multiple inputs so target layers with multiple outputs
        # are rejected
        if len(outbound_names) > 1 and isinstance(new_layer, OutputQuantizer):
            raise RuntimeError("Inserting an OutputQuantizer after a layer with multiple outputs "
                               "is not supported.")

        if len(outbound_names):
            # Initialize the new layer inbounds
            new_layer_inbounds = []

            # Replace inbounds from the layers after the target layer with the inserted layer
            outbound_ids = [_get_layer_index(layers, outbound) for outbound in outbound_names]
            for id in outbound_ids:
                for inbound_node in _inbound_node_generator(layers[id]):
                    if isinstance(inbound_node, dict):
                        inbound_node = inbound_node.values()
                    for connection_info in inbound_node:
                        matched = _replace_layer_name_for_connection_info(connection_info,
                                                                          target_layer_name,
                                                                          new_layer.name)
                        # Store the replaced inbound as it will later be used by the inserted layer
                        if matched and matched not in new_layer_inbounds:
                            new_layer_inbounds.append(matched)

            # Set the inserted layer inbounds
            new_layer_config['inbound_nodes'] = [[new_layer_inbounds]]

        else:
            # If target layer has no outbounds (ie. it's a model output), update the model
            # output layers list
            for index, out_layer in enumerate(config['output_layers']):
                if out_layer[0] == target_layer_name:
                    config['output_layers'][index][0] = new_layer.name

            # The inserted layer takes the target layer as its inbound
            new_layer_config['inbound_nodes'] = [[[target_layer_name, 0, 0, {}]]]

    # The new layer configuration can now be inserted into the layers config
    layers.insert(_get_layer_index(layers, target_layer_name) + 1, new_layer_config)

    # Set the updated layers in config
    config['layers'] = layers

    # Reconstruct model from the config
    custom_objects = {"OutputQuantizer": OutputQuantizer, "Dequantizer": Dequantizer}
    if isinstance(model, Sequential):
        new_model = Sequential.from_config(config, custom_objects)
    else:
        new_model = Model.from_config(config, custom_objects)

    # Load original weights
    variables_dict = {var.name: var for var in model.variables}
    apply_weights_to_model(new_model, variables_dict, False)
    return new_model


def apply_weights_to_model(model, weights, verbose=True):
    """Loads weights from a dictionary and apply it to a model.

    Go through the dictionary of weights, find the corresponding variable in the
    model and partially load its weights.

    Args:
        model (keras.Model): the model to update
        weights (dict): the dictionary of weights
        verbose (bool, optional): if True, throw warning messages if a dict item is not found in the
            model. Defaults to True.
    """
    if len(weights) == 0:
        warnings.warn("There is no weight to apply to the model.")
        return

    # Go through the dictionary of weights with each item
    for key, value in weights.items():
        value_applied = False
        for dest_var in model.variables:
            if key == dest_var.name:
                # Apply the current item value
                dest_var.assign(value)
                value_applied = True
                break
        if not value_applied and verbose:
            warnings.warn(f"Variable '{key}' not found in the model.")


def load_weights(model, weights_path):
    """Loads weights from a npz file and apply it to a model.

    Go through the dictionary of weights of the npz file, find the corresponding variable in the
    model and partially load its weights.

    Args:
        model (keras.Model): the model to update
        weights_path (str): the path of the npz file to load
    """
    # Check the npz file validity
    path = Path(weights_path)
    if not path.is_file():
        raise ValueError(f"File `{weights_path}` not found.")

    # Open the npz file
    weights_dict = np.load(weights_path)

    # Apply the weights to the model
    apply_weights_to_model(model, weights_dict)


def save_weights(model, weights_path):
    """Save model weights on an npz file.

    Takes a model and save the weights of all its layers into an npz file.

    Args:
        model (keras.Model): the model to save its weights
        weights_path (str): the path of the npz file to save
    """
    weights_dict = {}
    for var in model.variables:
        weights_dict[var.name] = var

    np.savez(weights_path, **weights_dict)


def _get_layers(config, layer_names):
    """Extracts layers from a model configuration.

    Args:
        config (dict): JSON formatted model configuration
        layer_names (list): list of layer names to extract

    Returns:
        list: layers configurations
    """
    return [layer for layer in config['layers'] if layer['config']['name'] in layer_names]


def _get_layer_index(layers, layer_name):
    """Retrieves the layer index within the layer list.

    Args:
        layers (list): list of JSON formatted layers configurations
        layer_name (str): layer name to retrieve

    Returns:
        int: the layer index
    """
    for index, ly in enumerate(layers):
        if ly['config']['name'] == layer_name:
            return index
    return -1


def _inbound_node_generator(layer):
    """Layer configuration inbound node generator.

    Args:
        layer (dict): JSON formatted layer configuration

    Yields:
        list: inbound node
    """
    for inbound_node in layer['inbound_nodes']:
        if (isinstance(inbound_node, list) and len(inbound_node) > 0 and
                isinstance(inbound_node[0], str)):
            yield [inbound_node]
        else:
            yield inbound_node


def _replace_layer_name_for_connection_info(connection_info, match_name, replacement_name):
    """Updates an inbound node name.

    Args:
        connection_info (list): inbound node information
        match_name (str): inbound node name to update
        replacement_name (str): inbound node name to set

    Returns:
        list: the original inbound node if an update happened, None otherwise
    """
    # Note that is from tfmot and the connection_info structure is not really documented:
    # it is a nested list where the first item is the inbound layer name.
    # For example: [[['conv1', 0, 0, {} ]]] or [[['batch_normalization', 0, 0, {}]]]
    original_info = connection_info.copy()
    match_found = False
    if connection_info[0] == match_name:
        match_found = True
        connection_info[0] = replacement_name
    for key in connection_info[3]:
        if isinstance(connection_info[3][key], list):
            if connection_info[3][key][0] == match_name:
                match_found = True
                connection_info[3][key][0] = replacement_name
    return original_info if match_found else None


def get_layers_by_type(model, layer_type):
    """Recursively find layers matching the specified type.

    Args:
        model (:obj:`keras.Model`): the source model.
        layer_type (class): the Layer class to look for.

    Returns:
        list(:obj:`keras.layers.Layer`): a list of layers
    """
    def _get_layers(layer, layers):
        if isinstance(layer, layer_type):
            layers.append(layer)
        for attr in layer.__dict__.values():
            if isinstance(attr, Layer):
                _get_layers(attr, layers)
    layers = []
    for layer in model.layers:
        _get_layers(layer, layers)
    return layers
