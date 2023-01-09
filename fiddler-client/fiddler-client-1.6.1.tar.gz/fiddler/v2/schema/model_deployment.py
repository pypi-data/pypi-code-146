from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from fiddler.v2.schema.user import UserCompact


class ArtifactType(str, Enum):
    SURROGATE = 'SURROGATE'
    PYTHON_PACKAGE = 'PYTHON_PACKAGE'


class DeploymentType(str, Enum):
    BASE_CONTAINER = 'BASE_CONTAINER'


class DeploymentParams(BaseModel):
    artifact_type: ArtifactType = ArtifactType.PYTHON_PACKAGE
    deployment_type: DeploymentType = DeploymentType.BASE_CONTAINER
    image_uri: Optional[str]
    replicas: Optional[int]
    cpu: Optional[int]
    memory: Optional[int]


class ModelDeployment(BaseModel):
    id: int
    uuid: UUID
    model_name: str
    project_name: str
    organization_name: str
    artifact_type: ArtifactType
    deployment_type: DeploymentType
    active: bool
    image_uri: Optional[str]
    replicas: Optional[int]
    cpu: Optional[int]
    memory: Optional[int]
    created_by: UserCompact
    updated_by: UserCompact
    created_at: datetime
    updated_at: datetime
    job_uuid: Optional[UUID]
