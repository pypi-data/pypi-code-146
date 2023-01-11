from bodosdk.models.base import CamelCaseBase


class InstanceRole(CamelCaseBase):
    role_arn: str  # only available for AWS


class InstanceRoleItem(CamelCaseBase):
    name: str
    uuid: str
    status: str
    description: str


class CreateRoleDefinition(CamelCaseBase):
    name: str
    description: str
    data: InstanceRole


class CreateRoleResponse(CreateRoleDefinition):
    uuid: str
    status: str
