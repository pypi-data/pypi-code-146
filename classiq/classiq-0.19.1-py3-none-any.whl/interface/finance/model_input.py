import enum
from typing import Union

from pydantic import BaseModel

from classiq.interface.finance.gaussian_model_input import GaussianModelInput
from classiq.interface.finance.log_normal_model_input import LogNormalModelInput

Models = Union[GaussianModelInput, LogNormalModelInput]


class FinanceModelName(str, enum.Enum):
    GAUSSIAN = "gaussian"
    LOG_NORMAL = "log normal"


class FinanceModelInput(BaseModel):
    name: Union[FinanceModelName, str]
    params: Models
