from torch import nn
import torch
from bitorch_engine.layers.qconv.binary import BinaryConv2dBase
from bitorch_engine.layers.qconv.nbit import nBitConv2dBase


class QConv2dInf(nn.Module):
    """Applies a 2D convolution over an input signal composed of several input
        planes.

    Args:
        in_channels (int): Number of channels in the input image
        out_channels (int): Number of channels produced by the convolution
        kernel_size (int or tuple): Size of the convolving kernel
        stride (int or tuple, optional): Stride of the convolution. Default: 1
        padding (int, tuple or str, optional): Padding added to all four sides of
            the input. Value: 0
        dilation (int or tuple, optional): Spacing between kernel elements. Default: 1

    Examples:
        >>> # With square kernels and equal stride
        >>> m = nn.Conv2d(16, 33, 3, stride=2, padding=4, dilation=3)
        >>> input = torch.randn(20, 16, 50, 100)
        >>> output = m(input)
    """
    def __init__(self,  in_channels: int,
                        out_channels: int,
                        kernel_size: int,
                        stride: int = 1,
                        padding: int = 0,
                        dilation: int = 1,
                        device=None,
                        a_bit: int=1,
                        w_bit: int=1,
                        use_cutlass: bool = False) -> None:
        '''
        :param input_features: dim of input features after bit-packing
        :param out_features: dim of hidden states
        '''
        super(QConv2dInf, self).__init__()
        self.layer = None
        if a_bit == 1 and w_bit == 1:
            self.layer = BinaryConv2dBase(in_channels, out_channels, kernel_size, stride, padding, dilation, device, use_cutlass)
        else:
            self.layer = nBitConv2dBase(in_channels, out_channels, kernel_size, stride, padding, dilation, a_bit, w_bit, device)


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forwards x through the qlinear layer.

        Args:
            x (torch.Tensor): tensor to forward

        Returns:
            torch.Tensors: forwarded tensor
        """
        return self.layer(x)

