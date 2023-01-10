from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, List

from strapi_api_client.resources.base import BaseResource


class CommunityResource(BaseResource):
    @dataclass
    class Community:
        id: int
        name: str
        isPremium: str
        createdAt: datetime
        updatedAt: datetime

    resource_class = Community

    def get_community(self, name: str) -> Optional[Union[Community, List[Community]]]:
        response = self._requestor.request(
            method='GET',
            endpoint_url=f"{self._api_url}/communities",
            query={'filters[name][$eqi]': name}
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response

    def create_community(self, data: dict) -> Optional[Union[Community, List[Community]]]:
        response = self._requestor.request(
            method='POST',
            endpoint_url=f"{self._api_url}/communities",
            payload={'data': data}
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response

    def delete_community(self, community_id: int) -> Optional[Union[Community, List[Community]]]:
        response = self._requestor.request(
            method='DELETE',
            endpoint_url=f"{self._api_url}/communities/{community_id}"
        )
        serialized_response = self.serialize_response(response=response)
        return serialized_response
