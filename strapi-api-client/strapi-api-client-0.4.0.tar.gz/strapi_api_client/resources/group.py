from datetime import datetime
from dataclasses import dataclass
from typing import Union, List, Optional

from strapi_api_client.resources.base import BaseResource


class GroupResource(BaseResource):
    @dataclass
    class Group:
        id: int
        name: str
        isPremium: str
        createdAt: datetime
        updatedAt: datetime

    resource_class = Group

    def get_group(self, name: str) -> Optional[Union[Group, List[Group]]]:
        response = self._requestor.request(
            method='GET',
            endpoint_url=f"{self._api_url}/interest-categories",
            query={'filters[name][$eqi]': name}
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response

    def create_group(self, data: dict) -> Optional[Union[Group, List[Group]]]:
        response = self._requestor.request(
            method='POST',
            endpoint_url=f"{self._api_url}/interest-categories",
            payload={'data': data}
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response

    def delete_group(self, group_id: int) -> Optional[Union[Group, List[Group]]]:
        response = self._requestor.request(
            method='DELETE',
            endpoint_url=f"{self._api_url}/interest-categories/{group_id}"
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response
