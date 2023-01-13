import torch
if torch.cuda.is_available():
    from .layer import Q4Conv2dCutlass