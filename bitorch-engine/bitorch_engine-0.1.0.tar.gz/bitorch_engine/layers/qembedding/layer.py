from typing import Optional
from torch import nn, Tensor
from torch.nn.parameter import Parameter
import torch
from bitorch_engine.layers.qembedding.binary import BinaryEmbeddingBag


class QEmbeddingBag(nn.Module):
    """Quantized version of pytorchs embedding bag. With the input indices the embedding is computed with a quantized
    version of the layers weight table. The output embedding will be also quantized before return.
    """
    def __init__(self,  num_embeddings: int,
                        embedding_dim: int,
                        w_bit: int=1,
                        _weight: Optional[Tensor] = None,
                        padding_idx: Optional[int] = None,
                        device=None) -> None:
        '''
        :param num_embeddings: dim of dictionary
        :param embedding_dim: dim of word vector
        '''
        super(QEmbeddingBag, self).__init__()
        if padding_idx is not None:
            if padding_idx > 0:
                assert padding_idx < self.num_embeddings, 'padding_idx must be within num_embeddings'
            elif padding_idx < 0:
                assert padding_idx >= -self.num_embeddings, 'padding_idx must be within num_embeddings'
                padding_idx = self.num_embeddings + padding_idx
        self.padding_idx = padding_idx
        if _weight is None:
            self.weight = Parameter(torch.empty(num_embeddings, embedding_dim))
            self.reset_parameters()
        else:
            assert list(_weight.shape) == [num_embeddings, embedding_dim], \
                'Shape of weight does not match num_embeddings and embedding_dim'
            self.weight = Parameter(_weight)
        self.layer = None
        if w_bit == 1:
            self.layer = BinaryEmbeddingBag(num_embeddings, embedding_dim, self.weight, device)
        else:
            raise NotImplementedError("QEmbeddingBag layer with weight:{} bit, not supported yet.".format(w_bit))


    def reset_parameters(self) -> None:
        torch.nn.init.normal_(self.weight)
        self._fill_padding_idx_with_zero()


    def _fill_padding_idx_with_zero(self) -> None:
        if self.padding_idx is not None:
            with torch.no_grad():
                self.weight[self.padding_idx].fill_(0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forwards x through the qlinear layer.

        Args:
            x (torch.Tensor): tensor to forward

        Returns:
            torch.Tensors: forwarded tensor
        """
        return self.layer(x)

