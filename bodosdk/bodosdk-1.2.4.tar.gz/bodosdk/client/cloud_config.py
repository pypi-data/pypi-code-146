from typing import Union, List

from bodosdk.api.cloud_config import CloudConfigApi
from bodosdk.exc import ResourceNotFound, Unauthorized
from bodosdk.models.cloud_config import (
    CreateAwsCloudConfig,
    CreateAzureCloudConfig,
    AzureCloudConfig,
    AwsCloudConfig,
)


class CloudConfigClient:
    def __init__(self, api: CloudConfigApi):
        self._api = api

    def create(
        self, cloud_config: Union[CreateAwsCloudConfig, CreateAzureCloudConfig]
    ) -> Union[AwsCloudConfig, AzureCloudConfig]:
        """
        Creates a cloud config

        :param cloud_config:
        :type cloud_config: Union[CreateAwsCloudConfig, CreateAzureCloudConfig]
        :return: cloud config
        :rtype: Union[AwsCloudConfig, AzureCloudConfig]
        :raises Unauthorized: when keys are invali
        :raises ValidationError: when JobDefinition is invalid
        """
        try:
            return self._api.create(cloud_config)
        except ResourceNotFound:
            raise Unauthorized

    def update(
        self, cloud_config: Union[AwsCloudConfig, AzureCloudConfig]
    ) -> Union[AwsCloudConfig, AzureCloudConfig]:
        """
        Updates cloud config

        :param cloud_config:
        :type cloud_config: Union[AwsCloudConfig, AzureCloudConfig]
        :return: cloud config
        :rtype: Union[AwsCloudConfig, AzureCloudConfig]
        :raises ResourceNotFound:
        """
        return self._api.update(cloud_config)

    def list(self) -> List[Union[AwsCloudConfig, AzureCloudConfig]]:
        """
        Returns defined cloud configs

        :rtype: List of Union[AwsCloudConfig, AzureCloudConfig]

        """
        return self._api.list()

    def get(self, uuid) -> Union[AwsCloudConfig, AzureCloudConfig]:
        """

        Returns cloud config by uuid
        :param uuid:
        :return: cloud config
        :rtype: Union[AwsCloudConfig, AzureCloudConfig]
        :raises ResourceNotFound:
        """
        return self._api.get(uuid)

    def remove(self, uuid):
        """

        Deletes cloud config by uuid
        :param uuid:
        :return: cloud config
        :rtype: Union[AwsCloudConfig, AzureCloudConfig]
        :raises ResourceNotFound:
        """
        return self._api.delete(str(uuid))
