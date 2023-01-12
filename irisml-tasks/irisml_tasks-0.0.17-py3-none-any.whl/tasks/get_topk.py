import dataclasses
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Get the largest Topk values and indices.

    Inputs:
        tensor (torch.Tensor): The input tensor

    Config:
        k (int): The "k".
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        tensor: torch.Tensor

    @dataclasses.dataclass
    class Config:
        k: int

    @dataclasses.dataclass
    class Outputs:
        values: torch.Tensor
        indices: torch.LongTensor

    def execute(self, inputs):
        result = torch.topk(inputs.tensor, self.config.k)
        return self.Outputs(result.values, result.indices)

    def dry_run(self, inputs):
        shape = [*inputs.tensor.shape[:-1], self.config.k]
        fake_values = torch.zeros(shape)
        fake_indices = torch.arange(self.config.k).expand(shape)
        return self.Outputs(fake_values, fake_indices)
