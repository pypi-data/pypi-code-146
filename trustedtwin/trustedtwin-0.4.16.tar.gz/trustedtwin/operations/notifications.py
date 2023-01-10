"""Definition of Notifications access methods."""
from base64 import b64decode
import urllib.parse
from typing import TYPE_CHECKING, Dict, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


def _get_acc_from_token(tkn: str) -> str:
    decoded = b64decode(tkn).decode('utf-8')
    _, account, _, _ = decoded.split('___')
    return account


class NotificationsOperations:
    """Interfaces for accessing Notifications API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def webhook_subscribe(self, **kwargs: Any) -> Dict:
        """Execute webhook_subscribe API operation"""
        endpoint = "notifications/webhooks"
        endpoint = urllib.parse.quote(endpoint)

        body = {
            "callback_url": kwargs.get("callback_url"),
            "topic": kwargs.get("topic"),
            "client_secret": kwargs.get("client_secret"),
            "expires": kwargs.get("expires"),
        }
        body = {x: y for x, y in body.items() if y}

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "webhook_subscribe", **self._service.kwargs)

    def webhook_unsubscribe(self, token: str) -> Dict:
        """Execute webhook_unsubscribe API operation"""
        endpoint = "notifications/webhooks/{account}".format(account=_get_acc_from_token(token))
        endpoint = urllib.parse.quote(endpoint)

        params = {"token": token}

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(resp, "webhook_unsubscribe", **self._service.kwargs)

    def webhook_refresh_subscription(self, token: str, **kwargs: Any) -> Dict:
        """Execute webhook_refresh_subscription API operation"""
        endpoint = "notifications/webhooks/{account}".format(account=_get_acc_from_token(token))
        endpoint = urllib.parse.quote(endpoint)

        params = {"token": token}

        body = {}
        if "expires" in kwargs:
            body["expires"] = kwargs["expires"]
        if "client_secret" in kwargs:
            body["client_secret"] = kwargs["client_secret"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
            body=body,
        )

        return process_response(
            resp, "webhook_refresh_subscription", **self._service.kwargs
        )

    def webhook_confirm_subscription(self, token: str) -> Dict:
        """Execute webhook_confirm_subscription API operation"""
        endpoint = "notifications/webhooks/{account}".format(account=_get_acc_from_token(token))
        endpoint = urllib.parse.quote(endpoint)

        params = {"token": token}

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
        )

        return process_response(
            resp, "webhook_confirm_subscription", **self._service.kwargs
        )
