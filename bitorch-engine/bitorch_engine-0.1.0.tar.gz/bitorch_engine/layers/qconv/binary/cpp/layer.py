import torch
from torch.autograd import Function

from bitorch_engine.utils.safe_import import import_extension

binary_conv_cpp = import_extension("binary_conv_cpp")


from bitorch_engine.utils.quant_operators import get_binary_row
from ..layer import BinaryConv2dBase

class BinaryConv2dForward(Function):
    @staticmethod
    def forward(ctx, activations, weights, m, n, k, kernel_size, stride, padding, dilation, output_edge, verbose=False):
        output = binary_conv_cpp.forward(activations, weights, m, n, k, kernel_size, stride, padding, dilation, output_edge, verbose)
        return output


class BinaryConv2dCPP(BinaryConv2dBase):
    def __init__(self, *args, **kwargs):
        super(BinaryConv2dCPP, self).__init__(*args, **kwargs)
        self.bits_binary_word = 32

    def generate_quantized_weight(self) -> None:
        w_size = self.out_channels * self.in_channels * self.kernel_size * self.kernel_size
        self.quantized_weight = get_binary_row(self.weight.reshape(-1, ),
                                               torch.empty(w_size, dtype=torch.int64),
                                               w_size * self.bits_binary_word,
                                               self.bits_binary_word)

    def forward(self, x: torch.Tensor, verbose: bool = False):
        '''
        :param activations: Input tensor with shape: (NCHW)
        :param weights: Weight tensor with shape: (C_out, C_in, k*k)
        :return:
        '''
        self._check_forward(x)
        # pass m, n, k
        m = self.out_channels                                       # number of output channel
        k = x.size(dim=1) * self.kernel_size * self.kernel_size; # number of input channels * kernel size
        # (Image_w – filter_w + 2*pad_w) / stride + 1
        output_edge = int((x.size(dim=2) - self.kernel_size + 2 * self.padding) / self.stride + 1)
        n = output_edge * output_edge                               # number of pixels of output images per channel
        return BinaryConv2dForward.apply(x, self.opt_weight, m, n, k, self.kernel_size, self.stride, self.padding,
                                         self.dilation, output_edge, verbose)
