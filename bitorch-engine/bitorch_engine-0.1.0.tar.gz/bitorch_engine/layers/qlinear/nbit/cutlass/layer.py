import torch
from torch.autograd import Function
import typing
from typing import Any

from bitorch_engine.utils.quant_operators import nv_tensor_quant
from bitorch_engine.utils.safe_import import import_extension
from ..layer import nBitLinearBase
from torch._utils import _get_device_index as _torch_get_device_index

q4_linear_cutlass = import_extension("q4_linear_cutlass")


class Q4LinearForward(Function):
    @staticmethod
    def forward(ctx, activation, weight, m, n, k, device_id):
        output = q4_linear_cutlass.forward(activation, weight, m, n, k, device_id)
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


class Q4LinearCutlass(nBitLinearBase):
    def __init__(self, *args, **kwargs):
        super(Q4LinearCutlass, self).__init__(*args, **kwargs)

    def generate_quantized_weight(self) -> None:
        '''
        weight quantization. This should be executed before saving weights.
        :return: None
        '''
        self.quantized_weight = nv_tensor_quant(self.weight, num_bits=4)[0].to(torch.int8)
        self.quantized_weight = self.quantized_weight.transpose(0, 1).contiguous()

    @property
    def device_id(self):
        return _torch_get_device_index(self.device)

    def forward(self, x: torch.Tensor, quantize_act: bool = False):
        '''
        :param x: Input tensor with shape(batch size, features num)
        :param quantize_act: Set if we need to quantize activation tensor to 4-bit
        :return:
        '''
        # get m, k, n
        m = x.size(dim=0)
        k = x.size(dim=1)
        n = self.out_channels
        assert m % 32 == 0, "Batch size must be divisible by 32."
        assert n % 32 == 0, "Output channel dimension must be divisible by 32."
        assert k % 32 == 0, "Input channel dimension must be divisible by 32."

        # quantize activation and weight, quantize x is very time consuming,
        # we assume that the input tensor is already 4-bit value saved in 8-bit tensor.
        if quantize_act:
            # TODO: The static quantization method from tensorRT is very slow.
            # An optimized CUDA kernel for this is necessary.
            x = nv_tensor_quant(x, num_bits=4)[0].to(torch.int8)
        elif x.dtype is not torch.int8:
            x = x.to(torch.int8)
        if self.quantized_weight is None:
            self.generate_quantized_weight()
        return Q4LinearForward.apply(x, self.quantized_weight, m, n, k, self.device_id)
