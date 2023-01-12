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
BatchNormalization transformations on models.
"""
import keras
import numpy as np
import tensorflow as tf

from copy import deepcopy
from keras.layers import (BatchNormalization, MaxPool2D, GlobalAvgPool2D, Conv2D, SeparableConv2D,
                          Dense, DepthwiseConv2D, Conv2DTranspose)

from ..utils import (deep_clone_model, _get_layers, _get_layer_index, _inbound_node_generator,
                     _replace_layer_name_for_connection_info)
from ...layers import (PaddedConv2D, QuantizedConv2D, QuantizedSeparableConv2D, QuantizedDense,
                       QuantizedDepthwiseConv2D, QuantizedConv2DTranspose, SeparableConv2DTranspose,
                       QuantizedSeparableConv2DTranspose)


def invert_batchnorm_pooling(model):
    """ Inverts pooling and BatchNormalization layers in a model to have BN layer before pooling.

    Returns a new model where pooling and batch normalization layers are inverted. From a Keras
    model where pooling layers precede batch normalization layers, this function places the BN
    layers before pooling layers. This is the first step before folding BN layers into processing
    layers.

    Note:
        Inversion of layers is equivalent only if the gammas of BN layers are positive. The
        function raises an error if not.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: the updated model

    Raises:
        RuntimeError: if a candidate BatchNormalization layer has gamma values that are not strictly
            positive.
    """

    # Maps between successive pooling->BN layers. These pairs will be inverted when cloning.
    pool2bn_map = {}
    bn2pool_map = {}

    # Map BatchNormalization layers that have only one inbound layer being a MaxPool2D or GAP2D
    for layer in model.layers:
        if (isinstance(layer, BatchNormalization) and len(layer.inbound_nodes) == 1
                and isinstance(layer.inbound_nodes[0].inbound_layers,
                               (MaxPool2D, GlobalAvgPool2D))):
            gammas = layer.get_weights()[0]
            if isinstance(layer.inbound_nodes[0].inbound_layers, MaxPool2D) and np.any(gammas <= 0):
                # It is impossible to invert MaxPool->BN with gammas <= 0
                raise RuntimeError(f"There are {np.sum(gammas <= 0)} negative gammas in the "
                                   f"BatchNormalization layer {layer.name}. Negative gammas are "
                                   "not supported.")
            bn2pool_map[layer] = layer.inbound_nodes[0].inbound_layers
            pool2bn_map[layer.inbound_nodes[0].inbound_layers] = layer

    if not pool2bn_map:
        return model

    def replace_layer(layer):
        if layer in pool2bn_map:
            # Replace pooling layer with the corresponding BN layer
            layer_bn = pool2bn_map[layer]
            config_bn = layer_bn.get_config()
            if isinstance(layer, GlobalAvgPool2D):
                config_bn['axis'] = [-1]
            return layer_bn.from_config(config_bn)
        if layer in bn2pool_map:
            # Replace BN layer with the corresponding pooling layer
            layer_pool = bn2pool_map[layer]
            return layer_pool.from_config(layer_pool.get_config())
        return layer.from_config(layer.get_config())

    return deep_clone_model(model, clone_function=replace_layer)


def fold_batchnorms(model):
    """Returns a new model where BatchNormalization layers are folded into previous layers.

    From a Keras model where BN layers follow processing layers, this function removes the BN layers
    and updates the preceding layers weights and bias accordingly. The new model is strictly
    equivalent to the previous one.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: the model with BN folded
    """
    # Clone model in order to modify before folding
    model_copy = deep_clone_model(model)

    # Get BN layers to fold mapping with the preceding layer
    map_prev_layer_to_bn = _find_batchnorms_to_fold(model_copy)

    # Rebuild a model without BN by editing the configuration
    model_folded = get_BN_less_model(model_copy, map_prev_layer_to_bn)

    # Set weights in the new model
    folded_model_names = [ly.name for ly in model_folded.layers]
    for layer in model_copy.layers:
        if layer.name not in folded_model_names:
            continue
        if layer in map_prev_layer_to_bn:
            new_weights = _compute_BN_folded_weights(layer, map_prev_layer_to_bn[layer])
        else:
            new_weights = layer.get_weights()
        model_folded.get_layer(layer.name).set_weights(new_weights)

    return model_folded


def _find_batchnorms_to_fold(model):
    """ Retrieves BatchNormalization layers that can be folded.

    This is limited to BN layers that follow supported layer types.

    Args:
        model (keras.Model): a model

    Returns:
        dict: map between a layer and its BN layer to be folded

    Raises:
        RuntimeError: if the candidate BN has null gammas or BN is not applied on the last axis.
    """

    supported_layers = (Conv2D, PaddedConv2D, Conv2DTranspose, SeparableConv2D, DepthwiseConv2D,
                        Dense, QuantizedConv2D, QuantizedConv2DTranspose, QuantizedSeparableConv2D,
                        QuantizedDepthwiseConv2D, QuantizedDense, SeparableConv2DTranspose,
                        QuantizedSeparableConv2DTranspose)

    # Map between a layer and its following BN layer and map between the BN layer and its next layer
    map_prev_layer_to_bn = {}

    # Find triplet "layer -> BN -> next layer"
    for layer in model.layers:
        # Find a supported layer followed by a BN layer
        if (type(layer) in supported_layers and len(layer.outbound_nodes) == 1 and
                isinstance(layer.outbound_nodes[0].layer, BatchNormalization)):
            # Null gammas are not supported: once folded, new kernel would be zero
            layer_bn = layer.outbound_nodes[0].layer
            gamma = layer_bn.get_weights()[0]
            if np.any(gamma == 0):
                raise RuntimeError(f"There are {np.sum(gamma == 0)} null gammas in the "
                                   f"BatchNormalization layer '{layer_bn.name}'. Null gammas are "
                                   "not supported.")

            # Check BN axis parameter
            if (len(layer_bn.axis) != 1 or layer_bn.axis[0] != len(layer_bn.input_shape) - 1):
                raise RuntimeError(f"The BatchNormalization must be applied on the last "
                                   f"axis. '{layer_bn.name}' layer has axis={layer_bn.axis}.")

            map_prev_layer_to_bn[layer] = layer_bn

    return map_prev_layer_to_bn


def get_BN_less_model(model, map_prev_layer_to_bn):
    """ Edits the model configuration to remove BN layer and rebuilds a model.

    Args:
        model (keras.Model): a model
        map_prev_layer_to_bn (dict): map between a layer and its BN layer to be folded

    Returns:
        keras.Model: an updated model without BN layers
    """
    # get_config documentation mentions that a copy should be made when planning to modify the
    # config
    config = deepcopy(model.get_config())
    layers = deepcopy(config['layers'])
    new_output_name = None

    for prev_layer, layer_bn in map_prev_layer_to_bn.items():
        # Set use_bias=True in layers where BN are folded to accept new computed weights
        prev_index = _get_layer_index(layers, prev_layer.name)
        layers[prev_index]['config']['use_bias'] = True

        # For sequential model, the changes stop here: the BN layers will simply be removed in the
        # following step. For other models, the layers inbounds/outbounds must be rebuilt.
        if isinstance(model, keras.Sequential):
            continue

        # Retrieve the BN input layer. Assumes that BN has only 1 inbound.
        bn_index = _get_layer_index(layers, layer_bn.name)
        # tfmot code: 'inbound_nodes' is a nested list where first element is the inbound layername,
        # e.g: [[['conv1', 0, 0, {} ]]]
        updated_inbound = layers[bn_index]['inbound_nodes'][0][0][0]

        # Get the layers after BN, ie. outbounds layers
        bn_outbound_names = [outbound.layer.name for outbound in layer_bn.outbound_nodes]
        outbound_ids = [_get_layer_index(layers, bn_outbound) for bn_outbound in bn_outbound_names]

        # If BN is the last layer (no outbound), store its name and inbound name so that the model
        # output can be updated later
        if len(outbound_ids) == 0:
            new_output_name = updated_inbound
            last_bn = layer_bn.name

        # Update BN outbounds layers: their current inbound is the BN layer that will be folded so
        # it must be replaced with the BN previous layer (folding target or the BN inbound). This
        # results in by-passing the BN layer: inbound > BN > outbounds becomes inbound > outbounds.
        for id in outbound_ids:
            for inbound_node in _inbound_node_generator(layers[id]):
                if isinstance(inbound_node, dict):
                    inbound_node = inbound_node.values()
                for connection_info in inbound_node:
                    _replace_layer_name_for_connection_info(connection_info, layer_bn.name,
                                                            updated_inbound)

    # Remove BN layers
    layers_to_remove = _get_layers(config, [bn.name for bn in map_prev_layer_to_bn.values()])
    for layer_to_remove in layers_to_remove:
        layers.remove(layer_to_remove)

    # Set the updated layers in config
    config['layers'] = layers

    # Update the model outputs if needed
    if new_output_name:
        for index, out_layer in enumerate(config['output_layers']):
            if out_layer[0] == last_bn:
                config['output_layers'][index][0] = new_output_name

    # Reconstruct model from the config, using the cloned layers.
    if isinstance(model, keras.Sequential):
        return keras.Sequential.from_config(config)
    else:
        return keras.Model.from_config(config)


def _compute_BN_folded_weights(target_layer, bn_layer):
    """ Computes the new weights of a layer after folding BatchNormalization into it.

    Args:
        target_layer (keras.Layer): the layer where BN will be folded
        bn_layer (keras.Layer): the BatchNormalization layer to fold into the preceding layer

    Returns:
        list: the new weights to set in the folded destination layer.
    """
    # Get kernel and bias weights of the target layer
    kernel_position = 0
    bias_position = 1
    if isinstance(target_layer, SeparableConv2DTranspose):
        # Pointwise kernel and bias are last in the list, the first weights are the C depthwise
        # kernels
        kernel_position = -2 if target_layer.use_bias else -1
        bias_position = -1
    elif isinstance(target_layer, SeparableConv2D):
        kernel_position = 1
        bias_position = 2

    weights = target_layer.get_weights()
    kernel = weights[kernel_position]
    bias = weights[bias_position] if target_layer.use_bias else 0

    # Get BN weights
    gamma, beta, mean, var = bn_layer.get_weights()
    scale_BN = gamma / np.sqrt(var + bn_layer.epsilon)

    # Compute new folded kernel and bias
    if isinstance(target_layer, DepthwiseConv2D):
        # Last dimension of DepthwiseConv2D kernel is 1 so scale_BN should be reshaped to (shape, 1)
        # (first two dimension will be broadcasted)
        new_kernel = kernel * scale_BN.reshape(*scale_BN.shape, 1)
    elif isinstance(target_layer, Conv2DTranspose):
        # Handle Conv2DTranspose kernels that are (h, w, filters, channels) instead of (h, w,
        # channels, filters)
        new_kernel = tf.transpose(kernel, (0, 1, 3, 2)) * scale_BN
        new_kernel = tf.transpose(new_kernel, (0, 1, 3, 2))
    else:
        new_kernel = kernel * scale_BN
    new_bias = beta + (bias - mean) * scale_BN

    # Return all weights with modified ones
    new_weights = weights
    new_weights[kernel_position] = new_kernel
    if target_layer.use_bias:
        new_weights[bias_position] = new_bias
    else:
        new_weights.append(new_bias)

    return new_weights
