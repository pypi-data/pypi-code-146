"""Definition of Stickers access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Optional, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class StickersOperations:
    """Interfaces for accessing Stickers API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def put_sticker(self, twin: str, **kwargs: Any) -> Dict:
        """Execute put_sticker API operation"""

        endpoint = "twins/{twin}/stickers".format(twin=twin)
        endpoint = urllib.parse.quote(endpoint)

        body = {"stickers": kwargs["stickers"]}

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "put_sticker", **self._service.kwargs)

    def list_stickers(
        self,
        color: Optional[str] = None,
        context: Optional[str] = None,
        ge: Optional[float] = None,
        le: Optional[float] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict:
        """Execute list_stickers API operation"""

        endpoint = "stickers"
        endpoint = urllib.parse.quote(endpoint)
        params = {
            "color": color,
            "context": context,
            "ge": ge,
            "le": le,
            "limit": limit,
            "offset": offset
        }
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(resp, "list_stickers", **self._service.kwargs)

    def get_sticker(self, twin: str, color: str) -> Dict:
        """Execute get_sticker API operation"""

        endpoint = "twins/{twin}/stickers/{color}".format(
            twin=twin, color=color
        )
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_sticker", **self._service.kwargs)

    def get_stickers(self, twin: str, context: Optional[str] = None) -> Dict:
        """Execute get_stickers API operation"""

        endpoint = "twins/{twin}/stickers".format(
            twin=twin
        )
        endpoint = urllib.parse.quote(endpoint)

        params = {
            "context": context,
        }
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params
        )

        return process_response(resp, "get_stickers", **self._service.kwargs)

    def remove_sticker(self, twin: str, color: str, context: Optional[str] = None) -> Dict:
        """Execute remove_sticker API operation"""

        endpoint = "twins/{twin}/stickers/{color}".format(
            twin=twin, color=color
        )
        endpoint = urllib.parse.quote(endpoint)

        params = {
            "context": context,
        }
        params = {k: v for k, v in params.items() if v is not None}

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params
        )

        return process_response(resp, "remove_sticker", **self._service.kwargs)
