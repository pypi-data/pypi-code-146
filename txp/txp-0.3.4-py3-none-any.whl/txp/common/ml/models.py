from enum import Enum
from pydantic import BaseModel
from typing import Union, List, Dict, Optional


class ModelFeedback(BaseModel):
    pass


class ErrorModelFeedback(ModelFeedback):
    error_message: str


class SuccessModelFeedback(ModelFeedback):
    metrics: dict
    failed_predictions: List[Dict]


class DefaultModelFeedback(ModelFeedback):
    pass


class ModelMetadata(BaseModel):
    feedback: Union[ErrorModelFeedback, SuccessModelFeedback, DefaultModelFeedback]
    tenant_id: str
    machine_id: str
    task_id: str


class ModelStateValue(Enum):
    ACKNOWLEDGE = "acknowledge"
    ACTIVE = "active"
    OLD = "old"
    TRAINING = "training"
    ERROR = "error"


class ModelState(BaseModel):
    value: ModelStateValue
    creation_date: str
    publishment_date: str
    deprecation_date: str
    is_pre_annotating: bool = False


class ModelRegistry(BaseModel):
    metadata: ModelMetadata
    file_path: str
    state: ModelState
    parameters: Optional[Dict]
