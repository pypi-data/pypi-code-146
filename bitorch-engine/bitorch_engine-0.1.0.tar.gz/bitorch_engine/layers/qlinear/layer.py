from typing import Any

import torch
from bitorch import RuntimeMode
from bitorch.layers.extensions import LayerRecipe
from bitorch.layers.qlinear import QLinearImplementation, QLinearBase

from .binary import BinaryLinear
from .binary.layer import BinaryLinearBase
from .nbit import nBitLinearBase
from .qlinear_implementation import QLinearImplementationMixin


@QLinearImplementation(RuntimeMode.INFERENCE_AUTO)
class QLinearInf(QLinearImplementationMixin, BinaryLinearBase):
    @classmethod
    def create_clone_from(cls, recipe: LayerRecipe, device: torch.device = None) -> Any:
        args = QLinearBase.get_args_as_kwargs(recipe)
        input_features, output_features = args["in_features"], args["out_features"]
        input_features //= 32
        new_layer = cls(
            input_features,
            output_features,
            device=device,
            a_bit=args["input_quantization"].bit_width,
            w_bit=args["input_quantization"].bit_width,
        )
        new_layer.set_weight_data(recipe.layer.weight.data.to(device=device))
        new_layer.generate_quantized_weight()
        return new_layer

    def __init__(
            self,
            input_features: int,
            out_features: int,
            device=None,
            a_bit: int = 1,
            w_bit: int = 1,
            bias=False,
    ) -> None:
        """
        :param input_features: dim of input features after bit-packing
        :param out_features: dim of hidden states
        """
        super().__init__(input_features, out_features, device)
        assert not bias, "currently QLinearInf only supports bias = False"
        self.layer = None
        if a_bit == 1 and w_bit == 1:
            self.layer = BinaryLinear(input_features, out_features, device=device)
        else:
            self.layer = nBitLinearBase(
                input_features, out_features, a_bit, w_bit, device
            )

    def generate_quantized_weight(self) -> None:
        self.layer.generate_quantized_weight()

    def set_weight_data(self, x: torch.Tensor):
        self.layer.set_weight_data(x)

    def set_quantized_weight_data(self, x: torch.Tensor):
        self.layer.set_quantized_weight_data(x)

    @property
    def weight(self):
        return self.layer.weight

    @property
    def opt_weight(self):
        return self.layer.opt_weight

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forwards x through the qlinear layer.

        Args:
            x (torch.Tensor): tensor to forward

        Returns:
            torch.Tensors: forwarded tensor
        """
        return self.layer(x)
