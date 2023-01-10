import dataclasses
import logging
import pprint
from typing import Dict, Optional
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Print or Pretty Print the input object."""
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        data_dict_str_float: Optional[Dict[str, float]] = None
        data_float: Optional[float] = None
        data_int: Optional[int] = None
        data_tensor: Optional[torch.Tensor] = None

    @dataclasses.dataclass
    class Config:
        label: Optional[str] = None
        pretty: bool = False

    def execute(self, inputs):
        data_all = [getattr(inputs, f.name) for f in dataclasses.fields(inputs)]
        data_provided = [x for x in data_all if x is not None]
        if len(data_provided) != 1:
            raise ValueError("Zero or multiple inputs are provided.")

        if self.config.label:
            logger.info(f"LABEL: {self.config.label}")
        data = data_provided[0]
        if isinstance(data, torch.Tensor):
            logger.info(f"Tensor shape={data.shape}, dtype={data.dtype}")

        if self.config.pretty:
            logger.info(pprint.pformat(data))
        else:
            logger.info(str(data))

        return self.Outputs()

    def dry_run(self, inputs):
        return self.execute(inputs)
