import logging

from ..clients.common import ResourceType


class Client:
    TIMEOUT_SEC = 3 * 60

    def __init__(self, resource_type, resource_name: str, multi_service_endpoint, resource_key: str) -> None:
        if resource_type == ResourceType.MultiServiceResource:
            assert multi_service_endpoint
            self._endpoint = f'{multi_service_endpoint.strip("/")}:443/vision/v4.0-preview.1'
        else:
            assert resource_name
            self._endpoint = f'https://{resource_name}.cognitiveservices.azure.com:443/vision/v4.0-preview.1'

        self._headers = {
            'Ocp-Apim-Subscription-Key': resource_key
        }

    @property
    def headers(self) -> dict:
        return self._headers

    def _request_wrapper(self, request):
        r = request()
        if not r.ok:
            logging.error(r.content)
        r.raise_for_status()
        return r
