from typing import List

from bodosdk.api.secret_group import SecretGroupApi
from bodosdk.models.secret_group import SecretGroupDefinition, SecretGroupInfo


class SecretGroupClient:
    def __init__(self, api: SecretGroupApi):
        self._api = api

    def create(self, secret_group_definition: SecretGroupDefinition) -> SecretGroupInfo:
        """
        Creates Secret Group
        :param secret_group_definition
        :type secret_group_definition: SecretGroupDefinition
        :return Secret Group Object
        :rtype SecretGroupInfo
        """
        return self._api.create_secret_group(secret_group_definition)

    def list(self) -> List[SecretGroupInfo]:
        """
        List Secret Groups in a workspace
        :return List of Secret Groups
        :rtype List[SecretGroupInfo]
        """
        return self._api.get_secret_groups()

    def update(self, secret_group_definition: SecretGroupDefinition) -> SecretGroupInfo:
        """
        Updates Secret Group description
        :param secret_group_definition
        :type secret_group_definition: SecretGroupDefinition
        :return Updated Secret Group Object
        :rtype SecretGroupInfo
        """
        return self._api.update_secret_group(secret_group_definition)

    def remove(self, name: str):
        """
        Delete Secret Group
        :param name
        :type name: str
        :return:
        """
        return self._api.delete_secret_group(name)
