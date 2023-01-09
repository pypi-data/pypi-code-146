from typing import Optional, Dict

from algora.api.service.project.enum import ProjectType
from algora.common.base import Base


class ProjectRequest(Base):
    name: str
    description: Optional[str]
    language: str
    entrypoint: str
    args: Dict[str, str]
    type: ProjectType
    packages: Dict[str, str]


class ProjectResponse(Base):
    id: str
    name: str
    description: Optional[str]
    language: str
    entrypoint: str
    args: Dict[str, str]
    type: ProjectType
    packages: Dict[str, str]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
