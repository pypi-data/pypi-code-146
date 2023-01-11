from typing import Union

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ResourceNotFound,
    ValidationError,
    ServiceUnavailable,
    UnknownError,
)
from bodosdk.models.cloud_config import (
    AzureCloudConfig,
    AwsCloudConfig,
    CloudConfig,
    CreateAwsCloudConfig,
    CreateAzureCloudConfig,
)


class CloudConfigApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(CloudConfigApi, self).__init__(*args, **kwargs)
        self._resource_url = "cloudConfig"

    def create(
        self, cloud_config: Union[CreateAwsCloudConfig, CreateAzureCloudConfig]
    ) -> Union[AwsCloudConfig, AzureCloudConfig]:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url(),
            data=cloud_config.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            return CloudConfig.parse_obj(resp.json()).__root__
        if resp.status_code == 404:
            raise ResourceNotFound("Probably wrong organization keys")
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(resp)

    def update(
        self, cloud_config: Union[AwsCloudConfig, AzureCloudConfig]
    ) -> Union[AwsCloudConfig, AzureCloudConfig]:
        headers = self.get_auth_header()
        resp = self._requests.put(
            f"{self.get_resource_url()}/{cloud_config.uuid}",
            data=cloud_config.json(by_alias=True),
            headers=headers,
        )
        if resp.status_code == 200:
            return CloudConfig.parse_obj(resp.json()).__root__
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    def list(self):
        headers = self.get_auth_header()
        resp = self._requests.get(f"{self.get_resource_url()}", headers=headers)
        if resp.status_code == 200:
            return [CloudConfig.parse_obj(cfg).__root__ for cfg in resp.json()]
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    def get(self, uuid):
        headers = self.get_auth_header()
        resp = self._requests.get(f"{self.get_resource_url()}/{uuid}", headers=headers)
        if resp.status_code == 200:
            return CloudConfig.parse_obj(resp.json()).__root__
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    def delete(self, uuid):
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/{uuid}", headers=headers
        )
        if str(resp.status_code).startswith("2"):
            return
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(resp.content)
