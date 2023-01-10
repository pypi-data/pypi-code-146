from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, List

from strapi_api_client.resources.base import BaseResource


class SubgroupResource(BaseResource):
    @dataclass
    class Subgroup:
        id: int
        name: str
        includedCommunities: str
        createdAt: datetime
        updatedAt: datetime

    resource_class = Subgroup

    def get_subgroup(self, name: str) -> Optional[Union[Subgroup, List[Subgroup]]]:
        response = self._requestor.request(
            method='GET',
            endpoint_url=f"{self._api_url}/interests",
            query={'filters[name][$eqi]': name}
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response

    def create_subgroup(self, data: dict) -> Optional[Union[Subgroup, List[Subgroup]]]:
        response = self._requestor.request(
            method='POST',
            endpoint_url=f"{self._api_url}/interests",
            payload={'data': data}
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response

    def delete_subgroup(self, subgroup_id: int) -> Optional[Union[Subgroup, List[Subgroup]]]:
        response = self._requestor.request(
            method='DELETE',
            endpoint_url=f"{self._api_url}/interests/{subgroup_id}"
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response
