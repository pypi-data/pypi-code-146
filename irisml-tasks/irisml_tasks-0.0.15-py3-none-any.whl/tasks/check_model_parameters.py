import dataclasses
import logging
import torch.nn
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Check Inf/NaN values in model parameters.

    If throw_exception is True, throws an exception if the model parameters contain Inf or NaN.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        model: torch.nn.Module

    @dataclasses.dataclass
    class Config:
        throw_exception: bool = False

    @dataclasses.dataclass
    class Outputs:
        has_nan_or_inf: bool

    def execute(self, inputs):
        has_nan_or_infinite = False
        for name, param in inputs.model.named_parameters():
            if not torch.isfinite(param).all():
                logger.info(f"The parameter {name} contains NaN or Inf values")
                has_nan_or_infinite = True

        if has_nan_or_infinite and self.config.throw_exception:
            raise ValueError("The model contains NaN or Inf parameters.")

        return self.Outputs(has_nan_or_infinite)

    def dry_run(self, inputs):
        return self.execute(inputs)
