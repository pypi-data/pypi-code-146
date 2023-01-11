from typing import List

from bodosdk.api.secrets import SecretsApi
from bodosdk.models.secrets import SecretDefinition, SecretInfo


class SecretsClient:
    def __init__(self, api: SecretsApi):
        self._api = api

    def create(self, secret_definition: SecretDefinition) -> SecretInfo:
        """
        Creates Secret
        :param secret_definition
        :type secret_definition: SecretDefinition
        :return Secret object
        :rtype SecretInfo
        """
        return self._api.create_secret(secret_definition)

    def get(self, uuid: str) -> SecretInfo:
        """
        Get Secret by uuid
        :param uuid
        :type uuid: str
        :return Secret object
        :rtype SecretInfo
        """
        return self._api.get_secret(uuid)

    def list(self) -> List[SecretInfo]:
        """
        Get Secrets by Workspace
        :return List of Secrets
        :rtype List[SecretInfo]
        """
        return self._api.get_all_secrets()

    def list_by_group(self, secret_group_name: str) -> List[SecretInfo]:
        """
        Get Secrets by Secret Group
        :param secret_group_name
        :type secret_group_name: str
        :return List of Secrets
        :rtype List[SecretInfo]
        """
        return self._api.get_all_secrets_by_group(secret_group_name)

    def update(self, uuid: str, data: object) -> SecretInfo:
        """
        Updates the Secret
        :param uuid
        :type uuid: str
        :param data
        :type data: object
        :return Secret object
        :rtype SecretInfo
        """
        return self._api.update_secret(uuid, data)

    def remove(self, uuid: str):
        """
        Delete the Secret
        :param uuid
        :type uuid:str
        :return
        """
        return self._api.delete_secret(uuid)
