from typing import List

from bodosdk.api.instance_role import InstanceRoleApi
from bodosdk.models import InstanceRoleItem, CreateRoleResponse, CreateRoleDefinition


class InstanceRoleClient:
    def __init__(self, api: InstanceRoleApi):
        self._api = api

    def list(self) -> List[InstanceRoleItem]:
        """
        Return metadata about all the roles which are currently defined by the client.

        :rtype: List of InstanceRoleItem
        """
        return self._api.get_all_roles()

    def get(self, uuid) -> InstanceRoleItem:
        """
        Given a uuid for a specific cluster, returns a InstanceRoleItem object to list out the details about the cluster
        """
        return self._api.get_role(uuid)

    def create(self, role_definition: CreateRoleDefinition) -> CreateRoleResponse:
        """
        Creates a new role for the client to use. Takes in a CreateRoleDefinition object as an input and
        creates a role based on the data specified in the objects.

        :param: Details about the new role to be created
        :type: CreateRoleDefinition
        :return: response after creating a role
        :rtype: CreateRoleResponse
        """
        return self._api.create_role(role_definition)

    def remove(self, uuid, mark_as_terminated=False):
        """
        Removes the role with the given uuid.
        Also takes in an options: to mark it as permanently terminated, with default value false
        """
        return self._api.remove_role(uuid, mark_as_terminated)
