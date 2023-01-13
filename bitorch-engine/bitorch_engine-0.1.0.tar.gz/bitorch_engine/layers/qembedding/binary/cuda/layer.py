import torch
from typing import Optional
from torch import nn
from torch.autograd import Function
from torch._utils import _get_device_index as _torch_get_device_index
import typing
from typing import Any
from bitorch_engine.utils.safe_import import import_extension
from bitorch_engine.utils.quant_operators import nv_tensor_quant
from ..layer import BCompressedEmbeddingBagBase

bcompressed_embedding_bag_cuda = import_extension("bcompressed_embedding_bag_cuda")


class BCompressedEmbeddingBagForward(Function):
    @staticmethod
    def forward(ctx, bag_of_words_uint, device_id):
        return bcompressed_embedding_bag_cuda.forward(bag_of_words_uint, device_id)

    @staticmethod
    @typing.no_type_check
    def backward(ctx: Any, output_gradient: torch.Tensor) -> torch.Tensor:
        """just passes the unchanged output gradient as input gradient.

        Args:
            ctx (Any): autograd context
            output_gradient (torch.Tensor): output gradient

        Returns:
            torch.Tensor: the unchanged output gradient
        """
        return output_gradient


class BCompressedEmbeddingBagCuda(BCompressedEmbeddingBagBase):
    '''
    BCompressedEmbeddingBag implements a binary embedding bag that uses a 32x compressed dictionary.
    '''
    def __init__(self, *args, **kwargs) -> None:
        '''
        :param num_embeddings: dim of dictionary
        :param embedding_dim: dim of word vector
        '''
        super(BCompressedEmbeddingBagCuda, self).__init__(*args, **kwargs)

    @property
    def device_id(self):
        return _torch_get_device_index(self.device)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        '''
        :param x (torch.Tensor) {NCHW}: tensor to forward
        :return: torch.Tensors: forwarded tensor
        '''
        # get the embedding matrix
        bag_of_words = nn.functional.embedding(x, self.weight)
        # quantize to unsigned int8 torch.uint8
        bag_of_words_uint = nv_tensor_quant(bag_of_words, num_bits=8)[0].to(torch.uint8)
        # get the binary embedding bag
        return BCompressedEmbeddingBagForward.apply(bag_of_words_uint, self.device_id)

