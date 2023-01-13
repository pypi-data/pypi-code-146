import math
from torch import nn
import torch
from torch.nn import init


class nBitLinearBase(nn.Module):
    def __init__(self, in_channels: int,
                        out_channels: int,
                        a_bit: int = 4,
                        w_bit: int = 4,
                        device=None) -> None:
        """
        Args:
            in_channels (int): dim of input features after bit-packing
            out_channels (int): dim of hidden states
        """
        super(nBitLinearBase, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.device = device
        self.a_bit = a_bit
        self.w_bit = w_bit
        self.quantized_weight = None
        self.weight = torch.nn.Parameter(
            torch.Tensor(out_channels, in_channels))
        self.reset_parameters()

    def reset_parameters(self) -> None:
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))

    def set_weight_data(self, x: torch.Tensor):
        self.weight = nn.Parameter(x, requires_grad=False)

    def set_quantized_weight_data(self, x: torch.Tensor):
        self.quantized_weight = nn.Parameter(x, requires_grad=False)

    def generate_quantized_weight(self) -> None:
        '''
        weight quantization. This should be executed before saving weights.
        :return: None
        '''
        raise NotImplementedError("Subclasses should implement this method.")

    def _check_forward(self, x: torch.Tensor):
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def opt_weight(self):
        return self.quantized_weight if self.quantized_weight is not None else self.weight



