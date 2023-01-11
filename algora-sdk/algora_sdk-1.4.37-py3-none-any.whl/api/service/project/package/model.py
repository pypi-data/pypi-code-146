from typing import Optional

from algora.api.service.project.package.enum import ProjectPackageTag
from algora.common.base import Base


class ProjectPackageRequest(Base):
    name: str
    version: str
    tag: Optional[ProjectPackageTag]
    path: str


class ProjectPackageResponse(Base):
    id: str
    name: str
    version: str
    tag: Optional[ProjectPackageTag]
    path: str
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
