from typing import Optional, List, Any, Dict
from uuid import UUID

from pydantic import Field
from bodosdk.models.base import CamelCaseBase, BodoRole, WorkspaceStatus


class CreateUpdateNotebookConfig(CamelCaseBase):
    instance_type: Optional[str] = Field(..., alias="instanceType")
    image_version: Optional[str] = Field(..., alias="imageVersion")


class AWSNetworkData(CamelCaseBase):
    vpc_id: Optional[str] = Field(..., alias="vpcId")
    public_subnets_ids: Optional[List[str]] = Field(..., alias="publicSubnetsIds")
    private_subnets_ids: Optional[List[str]] = Field(..., alias="privateSubnetsIds")


class WorkspaceDefinition(CamelCaseBase):
    name: str
    cloud_config_uuid: str = Field(..., alias="cloudConfigUUID")
    region: str = Field(..., alias="region")
    infra_config_uuid: Optional[str] = Field(None, alias="infraConfigUUID")
    aws_network_data: Optional[AWSNetworkData] = Field(None, alias="awsNetworkData")
    default_notebook_config: Optional[CreateUpdateNotebookConfig] = Field(
        None, alias="defaultNotebookConfig"
    )
    notebook_auto_deploy_enabled: bool = Field(..., alias="notebookAutoDeployEnabled")
    workspace_version: Optional[int] = Field(None, alias="workspaceVersion")
    storage_endpoint: Optional[bool] = Field(False, alias="storageEndpoint")


class WorkspaceInfo(CamelCaseBase):
    id: Optional[str] = Field(None, hidden=True)
    uuid: str
    name: str
    status: str
    organization_uuid: str
    region: str
    cloud_config: Optional[Any] = Field(None, alias="cloudConfig")
    infra_config: Optional[Any] = Field(None, alias="infraConfig")
    data: Any
    created_by: Optional[str] = Field(None, alias="createdBy")
    default_notebook_config: Any
    notebook_autodeploy_enabled: bool = Field(..., alias="notebookAutoDeployEnabled")
    type: str


class WorkspaceCreatedResponse(WorkspaceInfo):
    notebook_auto_deploy_enabled: bool = Field(None, alias="notebookAutoDeployEnabled")
    assigned_at: Any = Field(..., alias="assignedAt")
    cluster_credits_used_this_month: int = Field(
        None, alias="clusterCreditsUsedThisMonth"
    )
    clusters: Any
    notebooks: Any
    jobs: Any


class WorkspaceListItem(CamelCaseBase):
    name: str
    uuid: str
    status: WorkspaceStatus
    provider: str
    region: str
    organization_uuid: str
    data: Optional[Any]
    server_time: Optional[str] = Field(..., alias="serverTime")
    cloud_config: Optional[Any] = Field(..., alias="cloudConfig")
    created_by: Optional[str] = Field(..., alias="createdBy")
    type: str
    tasks: Optional[List[Any]]


class WorkspaceResponse(CamelCaseBase):
    name: str
    uuid: str
    status: WorkspaceStatus
    region: str
    organization_uuid: UUID = Field(..., alias="organizationUUID")
    data: Optional[Any]
    cloud_config: Optional[Dict] = Field(..., alias="cloudConfig")
    created_by: Optional[str] = Field(..., alias="createdBy")
    notebook_auto_deploy_enabled: bool = Field(..., alias="notebookAutoDeployEnabled")
    default_notebook_config: Optional[Dict] = Field(None, alias="defaultNotebookConfig")
    type: str


class UserAssignment(CamelCaseBase):
    class Config:
        use_enum_values = True

    email: str
    skip_email: bool = Field(..., alias="skipEmail")
    bodo_role: BodoRole = Field(..., alias="bodoRole")
