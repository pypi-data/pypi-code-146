from typing import List
from requests import Response

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ResourceNotFound,
    ValidationError,
    ServiceUnavailable,
    UnknownError,
)
from bodosdk.models.catalog import (
    CatalogDefinition,
    CatalogInfo,
    CatalogUpdateDefinition,
)


def handle_response(
    response: Response, uuid: str = None, is_list=False, is_delete=False
):
    if str(response.status_code).startswith("2"):
        if is_list:
            result: List = []
            for entry in response.json():
                result.append(CatalogInfo(**entry))
            return result
        elif is_delete:
            return
        else:
            return CatalogInfo(**response.json())

    elif response.status_code == 400:
        raise ValidationError(response.json())
    elif response.status_code == 404:
        raise ResourceNotFound(f"Could not find catalog with uuid: ${uuid}")
    elif str(response.status_code).startswith("5"):
        raise ServiceUnavailable
    raise UnknownError


class CatalogApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(CatalogApi, self).__init__(*args, **kwargs)
        self._resource_url = "catalog"

    def create_catalog(self, catalog_definition: CatalogDefinition):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url(),
            data=catalog_definition.json(by_alias=True),
            headers=headers,
        )
        return handle_response(resp)

    def get_catalog(self, uuid):
        response = self._requests.get(
            f"{self.get_resource_url()}/{uuid}", headers=self.get_auth_header()
        )
        return handle_response(response, uuid)

    def get_catalog_by_name(self, name):
        response = self._requests.get(
            f"{self.get_resource_url()}/name/{name}", headers=self.get_auth_header()
        )
        return handle_response(response, name)

    def get_all_catalogs(self):
        response = self._requests.get(
            f"{self.get_resource_url()}", headers=self.get_auth_header()
        )
        return handle_response(response, is_list=True)

    def update_catalog(self, uuid, catalog_update_definition: CatalogUpdateDefinition):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        response = self._requests.put(
            f"{self.get_resource_url()}/{uuid}",
            data=catalog_update_definition.json(by_alias=True),
            headers=headers,
        )
        return handle_response(response, uuid)

    def delete_catalog(self, uuid):
        response = self._requests.delete(
            f"{self.get_resource_url()}/{uuid}", headers=self.get_auth_header()
        )
        return handle_response(response, uuid, is_delete=True)

    def delete_all_catalogs(self):
        response = self._requests.delete(
            f"{self.get_resource_url()}", headers=self.get_auth_header()
        )
        return handle_response(response, is_delete=True)
