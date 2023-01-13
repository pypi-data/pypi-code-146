import torch
from bitorch_engine.layers.qlinear.binary.layer import BinaryLinearBase
from bitorch_engine.utils.safe_import import import_extension
from torch.autograd import Function

if torch.cuda.is_available():
    from bitorch_engine.layers.qlinear.binary.cuda import BinaryLinearCuda
    from torch._utils import _get_device_index as _torch_get_device_index


binary_linear_cutlass = import_extension("binary_linear_cutlass")


class BinaryLinearForward(Function):
    @staticmethod
    def forward(ctx, input, weights, m, n, k, device_id, verbose=False):
        output = binary_linear_cutlass.forward(input, weights, m, n, k, device_id, verbose)
        return output


class BinaryLinearCutlass(BinaryLinearBase):
    def generate_quantized_weight(self) -> None:
        self.quantized_weight = BinaryLinearCuda.w_pack(
            self.weight,
            self.output_features,
            self.input_features,
            bmm_type=self.bmm_type,
            device_id=self.device_id,
        )

    @property
    def device_id(self):
        return _torch_get_device_index(self.device)

    def forward(self, activations: torch.Tensor, weights: torch.Tensor, verbose: bool = False):
        '''
        :param activations: Input tensor with shape(batch size, features num)
        :param weights: Weight tensor with shape: (output num, features num)
        :return:
        '''
        assert activations.size(dim=1) % 32 == 0, "Input tensor dimension must be divisible by 32."
        assert activations.size(dim=1) / 32 == self.input_features, \
            "Dimension mismatch of the input Tensor {}:{}".format(activations.size(dim=1)/32, self.input_features)

        # pass m, n, k
        m = activations.size(dim=0)
        k = activations.size(dim=1)
        n = self.output_features

        return BinaryLinearForward.apply(activations, weights, m, n, k, self.device_id, verbose)
