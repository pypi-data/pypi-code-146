import torch
from torch._utils import _get_device_index as _torch_get_device_index

from bitorch_engine.utils.safe_import import import_extension

functions_cuda = import_extension("functions_cuda")


def fp32toint4(input: torch.Tensor, device: torch.device = None):
    return functions_cuda.fp32toint4(input, _torch_get_device_index(device))
