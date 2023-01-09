import dataclasses
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Calculate cosine similarity between two sets of vectors.

    Inputs:
        tensor0 (torch.Tensor): Shape [N0, M]
        tensor1 (torch.Tensor): Shape [N1, M]

    Outputs:
        cosine_similarity (torch.Tensor): Shape [N0, N1]
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        tensor0: torch.Tensor
        tensor1: torch.Tensor

    @dataclasses.dataclass
    class Outputs:
        cosine_similarity: torch.Tensor

    def execute(self, inputs):
        if inputs.tensor0.shape[1] != inputs.tensor1.shape[1] or len(inputs.tensor0.shape) != 2 or len(inputs.tensor1.shape) != 2:
            raise RuntimeError(f"Input tensors have unexpected shape: tensor0.shape={inputs.tensor0.shape}, tensor1.shape={inputs.tensor1.shape}")

        eps = 1e-8
        norm0 = inputs.tensor0.norm(dim=1)[:, None]
        norm1 = inputs.tensor1.norm(dim=1)[:, None]
        normalized_tensor0 = inputs.tensor0 / torch.clamp(norm0, min=eps)
        normalized_tensor1 = inputs.tensor1 / torch.clamp(norm1, min=eps)
        cosine_similarity = torch.mm(normalized_tensor0, normalized_tensor1.transpose(0, 1))
        assert cosine_similarity.shape == (inputs.tensor0.shape[0], inputs.tensor1.shape[0])
        return self.Outputs(cosine_similarity)

    def dry_run(self, inputs):
        fake_result = torch.zeros((inputs.tensor0.shape[0], inputs.tensor1.shape[0]))
        return self.Outputs(fake_result)
