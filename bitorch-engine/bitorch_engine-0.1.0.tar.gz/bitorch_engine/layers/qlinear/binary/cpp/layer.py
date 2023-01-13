from typing import Any

import torch
from bitorch import RuntimeMode
from bitorch.layers import QLinearBase
from bitorch.layers.extensions import LayerRecipe
from bitorch.layers.register import QLinearImplementation
from torch.autograd import Function

from bitorch_engine.utils.quant_operators import get_binary_col
from bitorch_engine.utils.safe_import import import_extension
from ..binary_implementation import BinaryLinearImplementationMixin
from ..layer import BinaryLinearBase

binary_linear_cpp = import_extension("binary_linear_cpp")


class BinaryLinearForward(Function):
    @staticmethod
    def forward(ctx, input, weights, m, n, k, verbose=False):
        output = binary_linear_cpp.forward(input, weights, m, n, k, verbose)
        return output


@QLinearImplementation(RuntimeMode.CPU)
class BinaryLinearCPP(BinaryLinearImplementationMixin, BinaryLinearBase):
    @classmethod
    def create_clone_from(cls, recipe: LayerRecipe, device: torch.device = None) -> Any:
        args = QLinearBase.get_args_as_kwargs(recipe)
        input_features, output_features = args["in_features"], args["out_features"]
        input_features //= 32
        new_layer = cls(input_features, output_features)
        new_layer.set_weight_data(recipe.layer.weight.data)
        new_layer.generate_quantized_weight()
        return new_layer

    def __init__(
        self,
        input_features: int,
        out_features: int,
        device: torch.device = None,
    ) -> None:
        super().__init__(input_features, out_features, device)

    def generate_quantized_weight(self) -> None:
        packed_weights = torch.zeros(
            (self.output_features * self.input_features), dtype=torch.int64
        )
        packed_weights = get_binary_col(
            self.weight.transpose(0, 1).reshape(-1),
            packed_weights,
            self.input_features * self.bits_binary_word,
            self.output_features,
            self.bits_binary_word,
        )
        self.quantized_weight = packed_weights

    def forward(self, x: torch.Tensor, verbose: bool = False):
        self._check_forward(x)

        # pass m, n, k
        m = x.size(dim=0)  # batch size
        k = x.size(dim=1)  # input features
        n = self.output_features  # output features

        return BinaryLinearForward.apply(x, self.opt_weight, m, n, k, verbose)
