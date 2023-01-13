import math
from torch import nn
import torch
from torch.nn import init


class nBitConv2dBase(nn.Module):
    def __init__(self, in_channels: int,
                        out_channels: int,
                        kernel_size: int,
                        stride: int = 1,
                        padding: int = 0,
                        dilation: int = 1,
                        a_bit: int = 4,
                        w_bit: int = 4,
                        device=None) -> None:
        """
        Args:
            in_channels (int): Number of channels in the input image
            out_channels (int): Number of channels produced by the convolution
            kernel_size (int): Size of the convolving kernel
            stride (int) Stride of the convolution. Default: 1
            padding (int): Padding added to all four sides of
                the input. Value: 0
            dilation (int): Spacing between kernel elements. Default: 1
        """
        super(nBitConv2dBase, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.device = device
        self.a_bit = a_bit
        self.w_bit = w_bit
        self.quantized_weight = None
        self.weight = torch.nn.Parameter(torch.empty(
                (out_channels, in_channels, kernel_size, kernel_size)))
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

