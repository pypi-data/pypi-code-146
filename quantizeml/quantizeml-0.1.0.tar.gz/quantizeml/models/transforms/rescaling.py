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
Rescaling transformation for quantized models.
"""
import numpy as np

from keras.layers import Rescaling, Conv2D, Dense

from quantizeml.layers.convolution import PaddedConv2D

from ...models.utils import deep_clone_model

__all__ = ["fold_rescaling"]


def fold_rescaling(model):
    """Folds the Rescaling layer of the model into the next layer weights.

    Args:
        model (keras.Model): a Keras model to fold

    Returns:
        keras.Model: the model with Rescaling layer folded
    """
    supported_dst_layers = [Conv2D, Dense]

    # Create a clone model
    clone_model = deep_clone_model(model)

    # Find the model has a Rescaling layer and check limitations on folding
    rescaling_layer = None
    dst_layer = None

    for ly in clone_model.layers:
        if isinstance(ly, Rescaling):
            # Folding is limited to single outbound node Rescaling layers
            if len(ly.outbound_nodes) != 1:
                raise ValueError("Found a Rescaling layer in the model but with multiple "
                                 "outbounds which is not supported.")
            # Retrieve the destination layer and check its type
            dst_layer = ly.outbound_nodes[0].layer
            if type(dst_layer) not in supported_dst_layers:
                raise ValueError(f"Layer type {type(dst_layer)} after Rescaling not supported, "
                                 "must be Conv2D or Dense.")
            # When destination layer is a Conv2D with padding 'same', reject:
            #   - offsets defined per axis,
            #   - scales defined per axis when offset is not null.
            # Otherwise it would require a padding value per-axis which is not supported.
            same_conv2d = (isinstance(dst_layer, Conv2D)
                           and dst_layer.get_config()['padding'].lower() == 'same')
            offset_per_axis = isinstance(ly.offset, list) and len(ly.offset) > 1
            scale_per_axis = isinstance(ly.scale, list) and len(ly.scale) > 1
            if same_conv2d and (offset_per_axis or ly.offset != 0 and scale_per_axis):
                raise NotImplementedError("Folding with offset per-axis or scale per-axis with an "
                                          "offset into a Conv2D with 'same' padding is not "
                                          "supported.")
            # Rescaling was found, exit the loop
            rescaling_layer = ly
            break

    # If no Rescaling was found, nothing to do, simply return the original model
    if rescaling_layer is None:
        return clone_model

    # Remove the Rescaling layer so that it will be ignored by clone_model
    clone_model._self_tracked_trackables.remove(rescaling_layer)

    # Bypass the Rescaling layer by connecting its inbound node to the dst_layer inbound node
    dst_layer._inbound_nodes[0] = rescaling_layer.inbound_nodes[0]

    # Clone model, rescaling layer will disappear in this step
    def replace_layer(layer):
        config = layer.get_config()
        if layer is dst_layer:
            # Force bias if there is a rescaling offset
            if rescaling_layer.offset != 0:
                config['use_bias'] = True
                # Replace Conv2D with 'same' padding by PaddedConv2D with correct padding value
                if isinstance(dst_layer, Conv2D) and config['padding'].lower() == 'same':
                    # Both offset and scale have a single value at this point
                    offset = rescaling_layer.offset[0] if isinstance(
                        rescaling_layer.offset, list) else rescaling_layer.offset
                    scale = rescaling_layer.scale[0] if isinstance(
                        rescaling_layer.scale, list) else rescaling_layer.scale
                    config['padding_value'] = -offset / scale
                    return PaddedConv2D.from_config(config)
        return layer.__class__.from_config(config)

    folded_model = deep_clone_model(clone_model, clone_function=replace_layer)
    folded_layer = folded_model.get_layer(dst_layer.name)

    # Set weights in the layer of the new model, using the Rescaling parameters:
    base_weights = dst_layer.get_weights()
    new_w = base_weights[0].copy()
    filters = new_w.shape[-1]
    # new_weights = base_weights * scale,
    for i in range(filters):
        # Rescale weights filter by filter to enable broadcast if scales are per channel
        new_w[..., i] *= rescaling_layer.scale
    new_weights = [new_w]

    if folded_layer.use_bias:
        # Build zero initialized biases if the original layer didn't have any
        new_biases = base_weights[1].copy() if dst_layer.use_bias else np.zeros(filters)
        # new_biases = base_biases + sum(base_weights_per_filter * offset)
        for i in range(filters):
            # Rescale biases filter by filter to enable broadcast if offsets are per channel
            w_i = base_weights[0][..., i]
            new_biases[i] += np.sum(w_i * rescaling_layer.offset)
        new_weights += [new_biases]

    folded_layer.set_weights(new_weights)
    return folded_model
