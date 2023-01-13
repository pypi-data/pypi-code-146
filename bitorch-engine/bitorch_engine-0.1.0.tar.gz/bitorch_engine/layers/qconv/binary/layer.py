import torch
from torch import nn


class BinaryConv2dBase(nn.Module):
    def __init__(self, in_channels: int,
                        out_channels: int,
                        kernel_size: int,
                        stride: int = 1,
                        padding: int = 0,
                        dilation: int = 1,
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
        super(BinaryConv2dBase, self).__init__()
        self.bits_binary_word = 32
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.weight = torch.nn.Parameter(torch.empty(
                (out_channels, in_channels * self.bits_binary_word, kernel_size*kernel_size)))
        self.quantized_weight = None
        self.device = device

    def set_weight_data(self, x: torch.Tensor):
        self.weight = nn.Parameter(x, requires_grad=False)

    def set_quantized_weight_data(self, x: torch.Tensor):
        self.quantized_weight = nn.Parameter(x, requires_grad=False)

    def generate_quantized_weight(self) -> None:
        """
        Do bit-packing on the 32-bit weights.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def _check_forward(self, x: torch.Tensor):
        assert x.size(dim=1) % 32 == 0, "Input tensor dimension must be divisible by 32."
        assert x.size(dim=1) / self.bits_binary_word == self.in_channels, \
            "Dimension mismatch of the input Tensor {}:{}".format(x.size(dim=1)/self.bits_binary_word, \
                                                                  self.in_channels)

    @property
    def opt_weight(self):
        return self.quantized_weight if self.quantized_weight is not None else self.weight

