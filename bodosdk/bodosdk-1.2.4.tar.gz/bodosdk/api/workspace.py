from typing import Union, List
from uuid import UUID

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ResourceNotFound,
    ServiceUnavailable,
    UnknownError,
    ValidationError,
)
from bodosdk.models import (
    WorkspaceListItem,
    WorkspaceDefinition,
    WorkspaceCreatedResponse,
    UserAssignment,
    WorkspaceResponse,
)


class WorkspaceApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(WorkspaceApi, self).__init__(*args, **kwargs)
        self._resource_url = "workspace"

    def create_workspace(self, workspace_definition: WorkspaceDefinition):
        headers = {"Content-type": "application/json"}
        print(workspace_definition)
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url()}",
            data=workspace_definition.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            return WorkspaceCreatedResponse(**resp.json())
        if resp.status_code == 404:
            raise ResourceNotFound(
                "Check if personal keys or the definition passed is correct."
            )
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError

    def get_workspace(self, uuid):
        response = self._requests.get(
            f"{self.get_resource_url()}/{uuid}", headers=self.get_auth_header()
        )
        if str(response.status_code).startswith("2"):
            result = WorkspaceResponse(**response.json())
            return result
        if response.status_code == 404:
            raise ResourceNotFound()
        if response.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(response.content)

    def list_all_workspaces(self, with_tasks: bool = False):
        params = {"withTasks": str(with_tasks).lower()}
        response = self._requests.get(
            f"{self.get_resource_url()}", params=params, headers=self.get_auth_header()
        )
        if str(response.status_code).startswith("2"):
            result: List = []
            for entry in response.json():
                result.append(WorkspaceListItem(**entry))
            return result
        if response.status_code == 404:
            raise ResourceNotFound
        if response.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(response.content)

    def remove_workspace(self, uuid, mark_as_terminated):
        params = {"mark_as_terminated": str(mark_as_terminated).lower()}
        response = self._requests.delete(
            f"{self.get_resource_url()}/{uuid}",
            params=params,
            headers=self.get_auth_header(),
        )
        if str(response.status_code).startswith("2"):
            return
        elif str(response.status_code).startswith("5"):
            raise ServiceUnavailable
        elif response.status_code in (400, 422):
            raise ResourceNotFound(response.json())
        elif response.status_code == 409:
            raise ServiceUnavailable(
                "Check if you have deleted all resources being used in the workspace before deleting"
            )
        raise UnknownError(response.content)

    def assign_users(self, uuid: Union[str, UUID], users: List[UserAssignment]):
        response = self._requests.post(
            f"{self.get_resource_url()}/{str(uuid)}/users",
            json={"users": [u.dict(by_alias=True) for u in users]},
            headers=self.get_auth_header(),
        )
        if str(response.status_code).startswith("2"):
            return
        elif str(response.status_code).startswith("5"):
            raise ServiceUnavailable()
        elif response.status_code in (400, 422):
            raise ResourceNotFound(response.json())
        raise UnknownError(response.content)
