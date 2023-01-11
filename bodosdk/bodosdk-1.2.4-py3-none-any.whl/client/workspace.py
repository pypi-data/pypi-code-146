from typing import List, Union
from uuid import UUID

from bodosdk.api.workspace import WorkspaceApi
from bodosdk.models import (
    WorkspaceDefinition,
    WorkspaceCreatedResponse,
    WorkspaceListItem,
)
from bodosdk.models.workspace import UserAssignment


class WorkspaceClient:
    def __init__(self, api: WorkspaceApi):
        self._api = api

    def create(
        self, workspace_definition: WorkspaceDefinition
    ) -> WorkspaceCreatedResponse:
        """
        Creates workspace
        :param workspace_definition:
        :type workspace_definition: WorkspaceDefinition
        :return: workspace object
        :rtype: WorkspaceCreatedResponse
        """
        return self._api.create_workspace(workspace_definition)

    def remove(self, uuid: str, mark_as_terminated: bool = False):
        """
        Removes workspace
        :param uuid: uuid of workspace to remove
        :type uuid: str
        :param mark_as_terminated: if True workspace resources won't be removed, workspace will be marked as terminated
        :type mark_as_terminated: bool
        """
        return self._api.remove_workspace(uuid, mark_as_terminated)

    def list(self) -> List[WorkspaceListItem]:
        """
        Gets list of workspaces
        :return:
        """
        return self._api.list_all_workspaces()

    def get(self, workspace_uuid: Union[str, UUID]) -> WorkspaceListItem:
        """
        Get workspace for specific uuid
        :param workspace_uuid:
        :return:
        """
        return self._api.get_workspace(str(workspace_uuid))

    def assign_users(
        self, workspace_uuid: Union[str, UUID], users: List[UserAssignment]
    ):
        """
        Assign users to specifed workspace
        :param workspace_uuid:
        :param users:
        :type users: List[UserAssignment]
        :return:
        """
        self._api.assign_users(workspace_uuid, users)
