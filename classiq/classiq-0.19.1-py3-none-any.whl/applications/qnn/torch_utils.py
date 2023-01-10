from collections.abc import Sized
from functools import reduce
from typing import Callable, Optional, Tuple, Union

import torch
import torch.nn as nn
from torch import Tensor

from classiq.exceptions import ClassiqValueError

Shape = Union[torch.Size, Tuple[int, ...]]


def get_shape_second_dimension(shape: torch.Size):
    if not isinstance(shape, Sized):
        raise ClassiqValueError("Invalid shape type - must have `__len__`")

    if len(shape) == 1:
        return 1
    elif len(shape) == 2:
        return shape[1]
    else:
        raise ClassiqValueError("Invalid shape dimension - must be 1D or 2D")


def get_shape_first_dimension(shape: torch.Size):
    if not isinstance(shape, Sized):
        raise ClassiqValueError("Invalid shape type - must have `__len__`")

    if len(shape) in (1, 2):
        return shape[0]
    else:
        raise ClassiqValueError("Invalid shape dimension - must be 1D or 2D")


def iter_inputs_weights(
    function: Callable[[Tensor, Tensor], Tensor],
    inputs: Tensor,
    weights: Tensor,
    expected_shape: Optional[Shape] = None,
    force_single_weight_per_input: bool = False,
) -> Tensor:
    """
    inputs is of shape (batch_size, in_features)
    weights is of shape (out_features, num_weights)
    """
    if force_single_weight_per_input and get_shape_second_dimension(
        inputs.shape
    ) != get_shape_second_dimension(weights.shape):
        raise ClassiqValueError(
            f"Shape mismatch! the 2nd dimension of both the inputs ({get_shape_second_dimension(inputs.shape)}) and the weights ({get_shape_second_dimension(weights.shape)}) should be the same"
        )

    # Save all the results as:
    #     [
    #         weights[0] inputs[0]
    #         weights[0] inputs[1]
    #         weights[1] inputs[0]
    #         weights[1] inputs[1]
    #     ]
    all_results = [
        function(batch_item, out_weight)
        for batch_item in inputs  # this is the first for-loop
        for out_weight in weights  # this is the second
    ]

    expected_shape = expected_shape or torch.Size(
        [
            weights.shape[0],
            inputs.shape[0],
        ]
    )

    return torch.tensor(
        all_results,
        dtype=weights.dtype,  # could also choose inputs.dtype
        requires_grad=(inputs.requires_grad or weights.requires_grad),
    ).reshape(*expected_shape)


def calculate_amount_of_parameters(net: nn.Module) -> int:
    return sum(  # sum over all parameters
        reduce(int.__mul__, i.shape)  # multiply all dimensions
        for i in net.parameters()
    )
