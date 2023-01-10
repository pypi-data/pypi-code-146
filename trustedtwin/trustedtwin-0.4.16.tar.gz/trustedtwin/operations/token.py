"""Definition of Token access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class TokenOperations:
    """Interfaces for accessing Secrets API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def create(self, **kwargs) -> Dict:
        """Execute create_user_token API operation"""

        endpoint = "token"
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "secret_dict" in kwargs:
            body["secret_dict"] = kwargs["secret_dict"]
        if "options" in kwargs:
            body["options"] = kwargs["options"]
        if "validity_ts" in kwargs:
            body["validity_ts"] = kwargs["validity_ts"]

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body
        )

        return process_response(resp, "create_user_token", **self._service.kwargs)

    def refresh(self, **kwargs) -> Dict:
        """Execute refresh_user_token API operation"""

        endpoint = "token/refresh"
        endpoint = urllib.parse.quote(endpoint)

        body = {}

        if "validity_ts" in kwargs:
            body["validity_ts"] = kwargs["validity_ts"]

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body
        )

        return process_response(resp, "refresh_user_token", **self._service.kwargs)
