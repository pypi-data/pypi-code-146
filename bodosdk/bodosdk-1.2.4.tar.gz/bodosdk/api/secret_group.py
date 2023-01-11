import json
from typing import List
from requests import Response

from bodosdk.exc import (
    ServiceUnavailable,
    ValidationError,
    UnknownError,
    ResourceNotFound,
)
from bodosdk.api.base import BackendApi
from bodosdk.models.secret_group import SecretGroupDefinition, SecretGroupInfo


def handle_response(
    response: Response, name: str = None, is_list=False, is_delete=False
):
    if str(response.status_code).startswith("2"):
        if is_list:
            result: List = []
            for entry in response.json():
                result.append(SecretGroupInfo(**entry))
            return result
        elif is_delete:
            return
        else:
            return SecretGroupInfo(**response.json())

    elif response.status_code == 400:
        raise ValidationError(response.json())
    elif response.status_code == 404:
        raise ResourceNotFound(f"Could not find secret group with name: ${name}")
    elif str(response.status_code).startswith("5"):
        raise ServiceUnavailable
    raise UnknownError


class SecretGroupApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(SecretGroupApi, self).__init__(*args, **kwargs)
        self._resource_url = "secret-group"

    def create_secret_group(self, secret_group_definition: SecretGroupDefinition):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url(),
            data=secret_group_definition.json(by_alias=True),
            headers=headers,
        )

        return handle_response(resp)

    def get_secret_groups(self):
        response = self._requests.get(
            f"{self.get_resource_url()}", headers=self.get_auth_header()
        )
        return handle_response(response, is_list=True)

    def update_secret_group(self, secret_group_definition: SecretGroupDefinition):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())

        request_data = json.dumps({"description": secret_group_definition.description})

        response = self._requests.put(
            f"{self.get_resource_url()}/{secret_group_definition.name}",
            data=request_data,
            headers=headers,
        )

        return handle_response(response, secret_group_definition.name)

    def delete_secret_group(self, name: str):
        response = self._requests.delete(
            f"{self.get_resource_url()}/{name}",
            headers=self.get_auth_header(),
        )
        return handle_response(response, name, is_delete=True)
