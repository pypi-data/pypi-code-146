import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, create_model


class BuildResponse(BaseModel):
    id: str
    name: str
    # TODO: make status an enum
    status: str
    # TODO: should we just make these fields
    # snake-case and add camelCase aliases?
    deploymentId: str
    componentName: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    imageUri: Optional[str]
    failureReason: Optional[str]
    getLogsUrl: str
    tailLogsUrl: str
    logsStartTs: int

    class Config:
        extra = Extra.allow


class AppDeploymentStatusResponse(BaseModel):
    state: create_model(
        "State",
        isTerminalState=(bool, ...),
        type=(str, ...),
        transitions=(List[str], ...),
    )

    id: str
    status: str
    message: Optional[str]
    transition: Optional[str]

    class Config:
        extra = Extra.allow


class DeploymentFqnResponse(BaseModel):
    deploymentId: str
    applicationId: str
    workspaceId: str
