from pydantic.main import BaseModel
from typing import Optional, Dict


class TrainCommand(BaseModel):
    dataset_name: str
    dataset_versions: list
    tenant_id: str
    machine_id: str
    task_id: str
    task_params: Optional[str] = "{}"
