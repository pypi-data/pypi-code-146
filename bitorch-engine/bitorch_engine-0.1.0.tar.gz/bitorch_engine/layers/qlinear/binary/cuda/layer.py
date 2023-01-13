from typing import TypeVar, Any

import torch
from bitorch import RuntimeMode
from bitorch.layers import QLinearBase
from bitorch.layers.extensions import LayerRecipe
from bitorch.layers.register import QLinearImplementation
from torch._utils import _get_device_index as _torch_get_device_index
from torch.autograd import Function

from bitorch_engine.utils.safe_import import import_extension
from .bmm import BMM
from ..binary_implementation import BinaryLinearImplementationMixin
from ..layer import BinaryLinearBase

binary_linear_cuda = import_extension("binary_linear_cuda")

T = TypeVar("T")


class BinaryLinearForward(Function):
    @staticmethod
    def forward(ctx, input, weights, m, n, k, bmm_type, device_id, verbose):
        return binary_linear_cuda.forward(input, weights, m, n, k, bmm_type.value, device_id, verbose).to(dtype=torch.float32)


@QLinearImplementation(RuntimeMode.GPU)
class BinaryLinearCuda(BinaryLinearImplementationMixin, BinaryLinearBase):
    def __init__(self, input_features: int, out_features: int, device: torch.device = None, bmm_type: BMM = BMM.ADAPTIVE):
        super().__init__(input_features, out_features, device)
        assert device is not None, "BinaryLinearCuda should receive one specific cuda device to work on."
        self.bmm_type = bmm_type

    @classmethod
    def create_clone_from(cls, recipe: LayerRecipe, device: torch.device = None) -> Any:
        args = QLinearBase.get_args_as_kwargs(recipe)
        input_features, output_features = args["in_features"], args["out_features"]
        input_features //= 32
        new_layer = cls(input_features, output_features, device)
        new_layer.set_weight_data(recipe.layer.weight.data)
        return new_layer

    @property
    def device_id(self):
        return _torch_get_device_index(self.device)

    @staticmethod
    def w_pack(weights, n, k, bmm_type, device_id, verbose=False):
        return binary_linear_cuda.w_pack(weights, n, k, bmm_type.value, device_id, verbose)

    def generate_quantized_weight(self) -> None:
        self.quantized_weight = BinaryLinearCuda.w_pack(
            self.weight,
            self.output_features,
            self.input_features * self.bits_binary_word,
            bmm_type=self.bmm_type,
            device_id=self.device_id,
        )

    def forward(self, x: torch.Tensor, bmm_type: BMM = BMM.ADAPTIVE, verbose: bool = False):
        '''
        :param activation: Input tensor with shape(batch size, features num)
        :param weight: Weight tensor with shape: (output num, features num)
        :param bmm_type: indicates which bmm kernel to use
        :return:
        '''
        self._check_forward(x)
        # m, n, k
        m = x.size(dim=0)
        k = x.size(dim=1)
        n = self.output_features

        if self.bmm_type is not bmm_type:
            self.bmm_type = bmm_type
        if self.bmm_type is BMM.BTC32: # constraint for bit-tensorcore kernel
            if m % 8 != 0 or k % 128 != 0 or n % 8 != 0:
                raise Exception("Invalid matrix dimensions for bit-tensorcore (BTC) kernel m:{}, n:{}, k:{}. "
                                "Guidelines: m and n must be multiplies of 8, and k must be multiplies of 128.".format(m, n, k))

        return BinaryLinearForward.apply(x, self.opt_weight, m, n, k, self.bmm_type, self.device_id, verbose)
