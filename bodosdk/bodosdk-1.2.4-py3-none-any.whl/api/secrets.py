import json
import logging
from typing import List
from requests import Response

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ValidationError,
    ServiceUnavailable,
    UnknownError,
    ResourceNotFound,
)
from bodosdk.models.secrets import SecretDefinition, SecretInfo


def handle_response(
    response: Response, uuid: str = None, is_list=False, is_delete=False
):
    if str(response.status_code).startswith("2"):
        if is_list:
            result: List = []
            logging.debug(response.json())
            for entry in response.json():
                if bool(entry):
                    result.append(SecretInfo(**entry))
            return result
        elif is_delete:
            return
        else:
            return SecretInfo(**response.json())

    elif response.status_code == 400:
        raise ValidationError(response.json())
    elif response.status_code == 404:
        raise ResourceNotFound(f"Could not find secret with uuid: ${uuid}")
    elif str(response.status_code).startswith("5"):
        raise ServiceUnavailable
    raise UnknownError


class SecretsApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(SecretsApi, self).__init__(*args, **kwargs)
        self._resource_url = "secrets"

    def create_secret(self, secret_definition: SecretDefinition):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url(),
            data=secret_definition.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        return handle_response(resp)

    def get_secret(self, uuid):
        response = self._requests.get(
            f"{self.get_resource_url()}/{uuid}", headers=self.get_auth_header()
        )
        return handle_response(response, uuid)

    def get_all_secrets(self):
        response = self._requests.get(
            f"{self.get_resource_url()}", headers=self.get_auth_header()
        )
        return handle_response(response, is_list=True)

    def get_all_secrets_by_group(self, secret_group: str):
        response = self._requests.get(
            f"{self.get_resource_url()}/secret-group/{secret_group}",
            headers=self.get_auth_header(),
        )
        return handle_response(response, is_list=True)

    def update_secret(self, uuid, data):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        response = self._requests.put(
            f"{self.get_resource_url()}/{uuid}",
            data=json.dumps({"data": data}),
            headers=headers,
        )
        return handle_response(response, uuid)

    def delete_secret(self, uuid):
        response = self._requests.delete(
            f"{self.get_resource_url()}/{uuid}", headers=self.get_auth_header()
        )
        return handle_response(response, uuid, is_delete=True)
