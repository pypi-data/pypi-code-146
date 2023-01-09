from typing import Optional

from algora.api.service.runner.enum import RunnerType
from algora.common.base import Base


class RunnerRequest(Base):
    name: str
    type: RunnerType
    min_cpu: str
    max_cpu: str
    min_ram: str
    max_ram: str
    image: Optional[str]


class RunnerResponse(Base):
    id: str
    name: str
    type: RunnerType
    min_cpu: str
    max_cpu: str
    min_ram: str
    max_ram: str
    image: Optional[str]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
