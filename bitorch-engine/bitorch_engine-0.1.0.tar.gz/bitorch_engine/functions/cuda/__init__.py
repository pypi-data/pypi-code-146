import torch

if torch.cuda.is_available():
    from .functions import *