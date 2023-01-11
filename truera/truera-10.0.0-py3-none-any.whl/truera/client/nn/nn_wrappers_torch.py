"""Deprecated"""

from truera.client.nn.wrappers import torch
from truera.client.util.func_utils import Deprecate

Deprecate.module(
    name=__name__,
    message="Use truera.client.nn.wrappers.torch instead.",
    dep_version="0.0.1",
    remove_version="0.1.0"
)

# replicate names from new location
Backend = torch.Backend
Torch = torch.Torch
