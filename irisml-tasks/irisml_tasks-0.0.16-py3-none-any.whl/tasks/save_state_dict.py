import dataclasses
import logging
import pathlib
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Save the model's state_dict to the specified file.

    Config:
        path (pathlib.Path): The output filepath.
        fp16 (bool): If True, FP32 tensors will be converted to FP16.
    """
    VERSION = '0.1.1'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        model: torch.nn.Module

    @dataclasses.dataclass
    class Config:
        path: pathlib.Path
        fp16: bool = False

    def execute(self, inputs):
        state_dict = inputs.model.state_dict()

        if self.config.fp16:
            original_size = self._get_size_in_bytes(state_dict)
            state_dict = {k: (v.half() if torch.is_tensor(v) and v.dtype == torch.float32 else v) for k, v in state_dict.items()}
            new_size = self._get_size_in_bytes(state_dict)
            logger.info(f"Converted the state_dict to FP16. {original_size=}, {new_size=}")

        self.config.path.parent.mkdir(exist_ok=True, parents=True)
        torch.save(state_dict, self.config.path)
        return self.Outputs()

    @staticmethod
    def _get_size_in_bytes(state_dict):
        return sum(t.element_size() * t.numel() for t in state_dict.values() if torch.is_tensor(t))
