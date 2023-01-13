from torch.autograd import Function
import torch
from .bcnv import BCNV
from torch._utils import _get_device_index as _torch_get_device_index

from bitorch_engine.utils.safe_import import import_extension

binary_conv_cuda = import_extension("binary_conv_cuda")

from ..layer import BinaryConv2dBase


class BinaryConv2dForward(Function):
    @staticmethod
    def forward(ctx, activations, weights, m, n, k, kernel_size, stride, padding, dilation, output_edge,
                                        bmm_type, device_id, verbose=False):
        return binary_conv_cuda.forward(activations, weights, m, n, k, kernel_size, stride, padding, dilation,
                                          output_edge, bmm_type.value, device_id, verbose)


class BinaryConv2dCuda(BinaryConv2dBase):
    def __init__(self, *args, bcnv_type: BCNV = BCNV.BCNV_32, **kwargs):
        super(BinaryConv2dCuda, self).__init__( *args, **kwargs)
        self.bits_binary_word = 32
        self.bcnv_type = bcnv_type
        self.weight_reshaped = False

    @property
    def device_id(self):
        return _torch_get_device_index(self.device)

    @staticmethod
    def w_pack(weight, m, k, bcnv_type, device_id, verbose):
        return binary_conv_cuda.w_pack(weight, m, k, bcnv_type.value, device_id, verbose)

    def check_and_reshape_weight(self) -> None:
        # if self.dilation == 1 and (self.bcnv_type is BCNV.BCNV_BMMA_FMT
        #                                or self.bcnv_type is BCNV.BCNV_32
        #                                or self.bcnv_type is BCNV.BCNV_64):
        #     # change (out, in, kernel, kernel) -> (out, kernel, kernel, in)
        #     if not self.weight.is_contiguous(memory_format=torch.channels_last):
        #         self.set_weight_data(self.weight.to(memory_format=torch.channels_last))
        # if self.bcnv_type.value < 3 and self.weight.is_contiguous(memory_format=torch.channels_last):
        #     #(out, kernel, kernel, in) -> (out, in, kernel, kernel)
        #     self.set_weight_data(self.weight.to(memory_format=torch.contiguous_format))
        w = self.weight
        if not self.weight_reshaped and self.dilation == 1 and (self.bcnv_type is BCNV.BCNV_BMMA_FMT
                                                                or self.bcnv_type is BCNV.BCNV_32
                                                                or self.bcnv_type is BCNV.BCNV_64):
            # change (out, in, kernel*kernel) -> (out, kernel*kernel, in)
            self.set_weight_data(w.view(w.size(0), w.size(2)*w.size(2), w.size(1)))
            self.weight_reshaped = True
        if self.bcnv_type.value < 3 and self.weight_reshaped:
            # (out, kernel * kernel, in) -> (out, in, kernel*kernel)
            self.set_weight_data(w.view(w.size(0), w.size(2), w.size(1)))
            self.weight_reshaped = False

    def generate_quantized_weight(self, verbose: bool = False) -> None:
        '''
        Do bit-packing on the 32-bit weights.
        :return: None
        '''
        ## reshape weight to OHWC for 3 BCNV methods
        self.check_and_reshape_weight()
        self.quantized_weight = BinaryConv2dCuda.w_pack(
            self.weight,
            self.out_channels, # m
            self.in_channels*self.bits_binary_word*self.kernel_size*self.kernel_size, # k
            bcnv_type=self.bcnv_type,
            device_id=self.device_id,
            verbose=verbose,
        )

    def adaptively_set_bconv_type(self, in_channel, out_channel, batch_size, k) -> None:
        use_bmm = False
        if self.dilation == 1:
            if batch_size % 8 == 0 and out_channel % 8 == 0 and in_channel % 128 == 0:
                self.bcnv_type = BCNV.BCNV_BMMA_FMT
            elif in_channel % 64 == 0 and out_channel % 64 == 0:
                self.bcnv_type = BCNV.BCNV_64
            elif in_channel % 32 == 0 and out_channel % 32 == 0:
                self.bcnv_type = BCNV.BCNV_32
            else:
                use_bmm = True
        else:
            use_bmm = True
        if use_bmm:
            if out_channel % 8 == 0 and batch_size % 8 == 0 and k % 128 == 0:
                self.bcnv_type = BCNV.BMM_BTC32
            else:
                self.bcnv_type = BCNV.BMM_BSTC32

    def bcnv_specific_check(self, m, k, n, batch_size):
        if self.bcnv_type is BCNV.BMM_BTC32: # constraint for bit-tensorcore kernel
            if m % 8 != 0 or k % 128 != 0 or n % 8 != 0:
                raise Exception("Invalid matrix dimensions for bit-tensorcore (BTC) kernel m:{}, n:{}, k:{}. "
                                "Guidelines: m and n must be multiplies of 8, and k must be multiplies of 128."
                                .format(m, n, k))
        elif self.bcnv_type is BCNV.BCNV_BMMA_FMT:
            if m % 8 != 0 or batch_size % 8 != 0 or k % 128 != 0:
                raise Exception("Invalid matrix dimensions for BCNV_BMMA_FMT kernel batch:{}, out:{}, input:{}. "
                                "Guidelines: batch and out must be multiplies of 8, and input must be multiplies of 128."
                                .format(batch_size, m, k))
        if self.dilation > 1 and self.bcnv_type.value > 3:
            raise Exception("The BCNV type BCNV_32, BCNV_64 and BCNV_BMMA_FMT do not support dilation convolution yet!"
                          "Please use BMM_BSTC32 or BMM_BTC32.")

    def get_output_tensor(self, batch_size, output_channels, output_edge) -> torch.Tensor:
        out_dtype = torch.float32
        if self.bcnv_type is BCNV.BCNV_BMMA_FMT or self.bcnv_type is BCNV.BMM_BTC32:
            out_dtype = torch.int32
        output = torch.empty((batch_size, output_channels, output_edge, output_edge),
                             dtype=out_dtype,
                             device=self.device)
        if self.dilation == 1 and self.bcnv_type.value > 3:
            output = output.to(memory_format=torch.channels_last)
        return output

    def check_input_channels_last(self, x: torch.Tensor) -> torch.Tensor:
        if not x.is_contiguous(memory_format=torch.channels_last):
            return x.to(memory_format=torch.channels_last)
        return x

    def forward(self, x: torch.Tensor, bcnv_type: BCNV = BCNV.BCNV_32, verbose: bool = False):
        '''
        :param activation: Input tensor with shape: (NCHW)
        :param weights: Weight tensor with shape: (C_out, C_in, k*k)
        :return:
        '''
        self._check_forward(x)

        # pass m, n, k
        in_channel = x.size(dim=1)
        batch_size = x.size(dim=0)
        m = self.out_channels                                       # number of output channel
        k = in_channel * self.kernel_size * self.kernel_size; # number of input channels * kernel size^2
        # (Image_w – filter_w + 2*pad_w) / stride + 1
        output_edge = int((x.size(dim=2) - self.kernel_size + 2 * self.padding) / self.stride + 1)
        n = output_edge * output_edge                               # number of pixels of output images per channel

        if self.bcnv_type is not bcnv_type:
            self.bcnv_type = bcnv_type
        # adaptively choose the cuda implemenation
        if self.bcnv_type is BCNV.ADAPTIVE:
            self.adaptively_set_bconv_type(in_channel, m, batch_size, k)

        self.bcnv_specific_check(m, k, n, batch_size)
        ## reshape weight to NHWC
        # if self.quantized_weight is None:
        #     self.check_and_reshape_weight()
        ## output tensor
        # output = self.get_output_tensor(batch_size, m, output_edge)
        # x = self.check_input_channels_last(x)
        return BinaryConv2dForward.apply(x, self.opt_weight, m, n, k, self.kernel_size, self.stride, self.padding,
                                         self.dilation, output_edge, self.bcnv_type, self.device_id, verbose)
