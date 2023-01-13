from typing import Optional
from torch import nn
import torch
from torch.nn.parameter import Parameter


class BinaryEmbeddingBag(nn.Module):
    '''
    BinaryEmbeddingBag is an accelerated version for 1-bit QEmbeddingBag layer of Bitorch
    '''
    def __init__(self, num_embeddings: int, embedding_dim: int, _weight: Optional[torch.Tensor] = None,
                 device=None) -> None:
        '''
        :param num_embeddings: dim of dictionary
        :param embedding_dim: dim of word vector
        '''
        super(BinaryEmbeddingBag, self).__init__()
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        self.weight = _weight

    def forward(self, x: torch.Tensor,
                _weight: Optional[torch.Tensor] = None) -> torch.Tensor:
        '''
        :param x (torch.Tensor) {NCHW}: tensor to forward
        :return: torch.Tensors: forwarded tensor
        '''
        if _weight is not None:
            assert list(_weight.shape) == [self.num_embeddings, self.embedding_dim], \
                'Shape of weight does not match num_embeddings and embedding_dim'
            self.weight = _weight
        bag_of_words = nn.functional.embedding(x, self.weight)
        mask = bag_of_words.ge(0)
        ones = torch.count_nonzero(mask, dim=0).to(torch.float)
        r = ones.ge(x.numel()/2).to(torch.float)
        r[r == 0] = -1
        return r.view(1, self.weight.size(1))


class BCompressedEmbeddingBagBase(nn.Module):
    '''
    BCompressedEmbeddingBag implements a binary embedding bag that uses a 32x compressed dictionary.
    '''
    def __init__(self, num_embeddings: int, embedding_dim: int, _weight: Optional[torch.Tensor] = None,
                 padding_idx: Optional[int] = None, device=None) -> None:
        '''
        :param num_embeddings: dim of dictionary
        :param embedding_dim: dim of word vector
        '''
        super(BCompressedEmbeddingBagBase, self).__init__()

        assert num_embeddings % 32 == 0, "The vocabulary size of BCompressedEmbeddingBag ({}) must be divisible by 32."\
                                        .format(num_embeddings)
        self.device = device
        self.num_embeddings = num_embeddings//32
        self.embedding_dim = embedding_dim
        if padding_idx is not None:
            if padding_idx > 0:
                assert padding_idx < self.num_embeddings, 'padding_idx must be within num_embeddings'
            elif padding_idx < 0:
                assert padding_idx >= -self.num_embeddings, 'padding_idx must be within num_embeddings'
                padding_idx = self.num_embeddings + padding_idx
        self.padding_idx = padding_idx
        if _weight is None:
            self.weight = Parameter(torch.empty(self.num_embeddings, self.embedding_dim))
            self.reset_parameters()
        else:
            assert list(_weight.shape) == [self.num_embeddings, self.embedding_dim], \
                'Shape of weight does not match num_embeddings and embedding_dim'
            self.weight = Parameter(_weight)

    def reset_parameters(self) -> None:
        torch.nn.init.normal_(self.weight)
        self._fill_padding_idx_with_zero()

    def _fill_padding_idx_with_zero(self) -> None:
        if self.padding_idx is not None:
            with torch.no_grad():
                self.weight[self.padding_idx].fill_(0)

    def set_weight_data(self, x: torch.Tensor):
        self.weight = nn.Parameter(x, requires_grad=False)

    def _check_forward(self, x: torch.Tensor):
        assert list(self.weight.shape) == [self.num_embeddings, self.embedding_dim], \
            'Shape of weight does not match num_embeddings and embedding_dim'


