"""Definition of Usage API operation"""
import urllib.parse
from typing import TYPE_CHECKING, Dict

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class UsageOperations:
    """Interfaces for accessing Usage API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def account(self) -> Dict:
        """Execute get_account_usage API operation"""
        endpoint = "usage"
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_account_usage", **self._service.kwargs)

    def user(self, user: str) -> Dict:
        """Execute get_user_usage API operation"""
        endpoint = "usage/{}".format(user)
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_user_usage", **self._service.kwargs)
