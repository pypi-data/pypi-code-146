from torch import nn, Tensor
import torch


def get_first_parameter_or_buffer(module: nn.Module) -> Tensor:
    """
    Get first parameter or buffer from module
    """
    try:
        first = next(module.parameters())
        return first
    except StopIteration:
        try:
            first = next(module.buffers())
            return first
        except StopIteration:
            raise Exception(
                f'no parameter or buffer in module: {module.__class__}'
            )


def get_device(module: nn.Module) -> torch.device:
    return get_first_parameter_or_buffer(module).device


def get_dtype(module: nn.Module) -> torch.dtype:
    return get_first_parameter_or_buffer(module).dtype
