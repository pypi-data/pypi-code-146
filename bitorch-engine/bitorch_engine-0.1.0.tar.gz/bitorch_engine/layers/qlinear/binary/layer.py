import torch
from torch import nn


class BinaryLinearBase(nn.Module):
    def __init__(
        self, input_features: int, out_features: int, device: torch.device = None
    ) -> None:
        """
        :param input_features: dim of input features after bit-packing
        :param out_features: dim of hidden states
        """
        super().__init__()
        self.bits_binary_word = 32
        self.input_features = input_features
        self.output_features = out_features
        self.weight = nn.Parameter(
            torch.Tensor(
                self.output_features, self.input_features * self.bits_binary_word
            )
        )
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
        assert (
            x.size(dim=1) % 32 == 0
        ), "Input tensor dimension ({}) must be divisible by 32.".format(x.size(dim=1))

        assert (
            x.size(dim=1) / self.bits_binary_word == self.input_features
        ), "Dimension mismatch of the input Tensor {}:{}".format(
            x.size(dim=1) / 32, self.input_features
        )

        if self.quantized_weight is not None:
            # print(x.size())
            # print(self.output_features)
            assert (
                self.quantized_weight.nelement()
                == x.size(dim=1) / self.bits_binary_word * self.output_features
            ), "Weight and input tensor mismatch. {}:{}".format(
                self.quantized_weight.nelement(),
                x.size(dim=1) / self.bits_binary_word * self.output_features
            )
        else:
            assert self.weight.size(dim=1) == x.size(
                dim=1
            ), "Weight and input tensor mismatch."

    @property
    def opt_weight(self):
        return (
            self.quantized_weight if self.quantized_weight is not None else self.weight
        )
