import dataclasses
import logging
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Calculate accuracy of the given prediction results.

    This task supports only multiclass classification.
    The targets format is Tensor[N] or Tensor[N, 1]
    The prediction results format is torch.Tensor[(N, num_classes)].
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        predictions: torch.Tensor
        targets: torch.Tensor

    @dataclasses.dataclass
    class Outputs:
        accuracy: float = 0

    def execute(self, inputs):
        if len(inputs.predictions) == 0:
            raise ValueError("An empty prediction result is provided.")

        if len(inputs.predictions.shape) != 2:
            raise RuntimeError(f"Invalid input shape: {inputs.predictions.shape}")

        _, predicted_max_indexes = inputs.predictions.max(dim=1)
        predicted_max_indexes = predicted_max_indexes.flatten()
        targets = inputs.targets.flatten()

        if targets.shape != predicted_max_indexes.shape:
            raise RuntimeError(f"The predictions or the targets have unexpected shape: {targets.shape} vs {predicted_max_indexes.shape}")

        accuracy = ((predicted_max_indexes == targets).sum() / len(targets)).item()

        logger.info(f"Accuracy: {accuracy:.3f}")
        return self.Outputs(accuracy)
