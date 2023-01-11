from typing import List

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ResourceNotFound,
    ServiceUnavailable,
    UnknownError,
    ValidationError,
)
from bodosdk.models import InstanceRoleItem, CreateRoleDefinition, CreateRoleResponse


class InstanceRoleApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(InstanceRoleApi, self).__init__(*args, **kwargs)
        self._resource_url = "instance-roles"

    def get_role(self, uuid) -> InstanceRoleItem:
        response = self._requests.get(
            f"{self.get_resource_url()}/{uuid}", headers=self.get_auth_header()
        )
        if str(response.status_code).startswith("2"):
            return InstanceRoleItem(**response.json())
        if response.status_code == 404:
            raise ResourceNotFound
        if response.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(response.content)

    def get_all_roles(self) -> List[InstanceRoleItem]:
        response = self._requests.get(
            f"{self.get_resource_url()}", headers=self.get_auth_header()
        )
        all_roles: List[InstanceRoleItem] = []
        if str(response.status_code).startswith("2"):
            for entry in response.json():
                role_info = InstanceRoleItem(**entry)
                all_roles.append(role_info)
            return all_roles
        if response.status_code == 404:
            raise ResourceNotFound
        if response.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(response.content)

    def create_role(self, role_definition: CreateRoleDefinition) -> CreateRoleResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url(), data=role_definition.json(), headers=headers
        )
        if str(resp.status_code).startswith("2"):
            return CreateRoleResponse(**resp.json())
        if resp.status_code == 404:
            raise ResourceNotFound("Probably wrong workspace keys")
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError

    def remove_role(self, uuid, mark_as_terminated):
        params = {"mark_as_terminated": str(mark_as_terminated).lower()}
        response = self._requests.delete(
            f"{self.get_resource_url()}/{uuid}",
            params=params,
            headers=self.get_auth_header(),
        )
        if str(response.status_code).startswith("2"):
            return
        if response.status_code == 404:
            raise ResourceNotFound
        if response.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(response.content)
