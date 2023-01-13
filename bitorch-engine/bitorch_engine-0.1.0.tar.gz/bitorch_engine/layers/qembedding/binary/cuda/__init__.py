import torch

if torch.cuda.is_available():
    from .layer import BCompressedEmbeddingBagCuda
