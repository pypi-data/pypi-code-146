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
"""Torch specific Helper Functions"""
from collections import OrderedDict
from typing import List

import numpy as np
import torch

from modalic.platforms.common.serde import _float_to_np_ndarray, _ser_np_weights
from modalic.utils.misc import all_equal_list


def serialize_torch_model(model: torch.nn.Module) -> list:
    r"""Serializes torch model as `py list`.

    :param model: Torch model.
    :returns: One level list of py floats.
    """
    weights = [val.cpu().numpy() for _, val in model.state_dict().items()]
    return _ser_np_weights(weights)


def deserialize_torch_model(
    model: torch.nn.Module, tensor: list, layer_shape: List[np.ndarray]
) -> torch.nn.Module:
    """Deserializes a py list to a torch model and sets the weights in the given model.

    :param model: Torch model.
    :param tensor: List of float representing the model weights.
    :layer_shape: Shape of the model which should be reconstructed.
    """
    weights = _float_to_np_ndarray(tensor, layer_shape)

    state_dict = OrderedDict(
        {k: torch.tensor(v) for k, v in zip(model.state_dict().keys(), weights)}
    )
    model.load_state_dict(state_dict, strict=True)
    return model


def get_torch_model_dtype(model: torch.nn.Module) -> str:
    r"""Extracts the data type of the pytorch model.

    :param model: Pytorch model object.
    :returns: dtype: Torch data type of the model.
    :raises ValueError:
    :raises TypeError:
    """
    if isinstance(model, torch.nn.Module):
        dtype_list = [layer[1].dtype for layer in list(model.state_dict().items())]
        if torch_type := all_equal_list(dtype_list):
            return torch_type
        else:
            raise ValueError(
                f"Found inconsistent data type for {model}. \
            Mixed precision policy is not allowed at this point. \
            Consider reimplementing model with consistent data type above all layers."
            )
    else:
        raise TypeError(
            f"Unknown model type: {type(model)}. Consider inheriting from torch.torch.nn.Module."
        )


def get_torch_model_shape(model: torch.nn.Module) -> List[np.ndarray]:
    r"""Extracts the shape of the pytorch model.

    :param model: Pytorch model object.
    :returns: List of np.ndarray which contains the shape (size)
        of each individual layer of the model.
    """
    return [
        np.array(model.state_dict()[param_tensor].size())
        for param_tensor in model.state_dict().keys()
    ]
