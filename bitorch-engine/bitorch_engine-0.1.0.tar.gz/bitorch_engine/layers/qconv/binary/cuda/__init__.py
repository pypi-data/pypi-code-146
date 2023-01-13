import torch

from .bcnv import BCNV

if torch.cuda.is_available():
    from .layer import BinaryConv2dCuda