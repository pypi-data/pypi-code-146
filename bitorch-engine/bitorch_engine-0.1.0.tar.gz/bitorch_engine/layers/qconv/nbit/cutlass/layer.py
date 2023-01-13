import torch
from torch._utils import _get_device_index as _torch_get_device_index
from torch.autograd import Function
import typing
from typing import Any

from bitorch_engine.utils.quant_operators import nv_tensor_quant
from bitorch_engine.utils.safe_import import import_extension
from ..layer import nBitConv2dBase

q4_conv_cutlass = import_extension("q4_conv_cutlass")


class Q4Conv2dForward(Function):
    @staticmethod
    def forward(ctx, activation, weight, kernel_size, stride, padding, dilation, device_id):
        output = q4_conv_cutlass.forward(activation, weight, kernel_size, stride, padding, dilation, device_id)
        return output

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

class Q4Conv2dCutlass(nBitConv2dBase):
    def __init__(self, *args, **kwargs):
        super(Q4Conv2dCutlass, self).__init__(*args, **kwargs)

    @property
    def device_id(self):
        return _torch_get_device_index(self.device)

    def generate_quantized_weight(self) -> None:
        '''
        weight quantization. This should be executed before saving weights.
        :return: None
        '''
        self.quantized_weight = nv_tensor_quant(self.weight, num_bits=4)[0].to(torch.int8)

        ## NOTE THAT this implementation is too slow. We apply tensor.view method in c++ file instead.
        ## reshape weight (C_out,C_in,k*k) to (C_out, k, k, C_in)
        # if not self.quantized_weight.is_contiguous(memory_format=torch.channels_last):
        #     self.quantized_weight = self.quantized_weight.to(memory_format=torch.channels_last)

    def forward(self, x: torch.Tensor, quantize_act: bool = False, no_quant = False):
        '''
        :param activations: Input tensor with shape: (NCHW)
        :param weights: Weight tensor with shape: (C_out, C_in, k*k)
        :return:
        '''
        # this is the cutlass specific constraints
        assert self.in_channels % 32 == 0, "Input channel dimension must be divisible by 32."
        assert self.out_channels % 32 == 0, "Output channel dimension must be divisible by 32."

        # quantize activation and weight
        # quantize activation and weight, quantize x is very time consuming,
        # we assume that the input tensor is already 4-bit value saved in 8-bit tensor.
        if quantize_act and not no_quant:
            # TODO: The static quantization method from tensorRT is very slow.
            # An optimized CUDA kernel for this is necessary.
            x = nv_tensor_quant(x, num_bits=4)[0].to(torch.int8)
            if self.quantized_weight is None:
                self.generate_quantized_weight()
            return Q4Conv2dForward.apply(x, self.opt_weight, self.kernel_size, self.stride, self.padding,
                                         self.dilation, self.device_id)
        # elif x.dtype is not torch.int8:
        #     x = x.to(torch.int8)
        if no_quant:
            if x.dtype is not torch.int8:
                x = x.to(torch.int8)
            return Q4Conv2dForward.apply(x, self.opt_weight, self.kernel_size, self.stride, self.padding,
                                         self.dilation, self.device_id)
        ## NOTE THAT this implementation is too slow. We apply tensor.view method in c++ file instead.
        ## reshape input NCHW to NHWC
        # if not x.is_contiguous(memory_format=torch.channels_last):
        #     x = x.to(memory_format=torch.channels_last)

        return Q4Conv2dForward.apply(x, self.opt_weight, self.kernel_size, self.stride, self.padding,
                                         self.dilation, self.device_id)
