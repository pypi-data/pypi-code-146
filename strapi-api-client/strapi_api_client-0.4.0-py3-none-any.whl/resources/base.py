from abc import ABC
from typing import Union, List

from strapi_api_client.requestor import Requestor


class BaseResource(ABC):
    class Resource:
        pass

    resource_class = Resource

    def __init__(self, api_url: str, requestor: Requestor):
        self._requestor = requestor
        self._api_url = api_url

    def serialize_response(self, response: dict) -> Union[Resource, List[Resource]]:
        def get_result(result_data: dict):
            my_result = None
            identification = result_data.get('id')
            attributes = result_data.get('attributes')
            if identification and attributes:
                my_result = self.resource_class(id=identification, **attributes)
            return my_result

        result = None
        data = response.get('data')
        if data:
            if isinstance(data, list):
                if len(data) == 1:
                    result = get_result(result_data=data[0])
                elif len(data) > 1:
                    results = []
                    for item in data:
                        result = get_result(result_data=item)
                        if result:
                            results.append(result)
                    if results and len(results) > 1:
                        result = results
            elif isinstance(data, dict):
                result = get_result(result_data=data)
        return result

    @property
    def requestor(self) -> Requestor:
        return self._requestor
