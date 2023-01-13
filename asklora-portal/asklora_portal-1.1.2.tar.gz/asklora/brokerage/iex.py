# flake8: noqa
import json
import os
import time
from collections.abc import Callable
from threading import Thread

import requests
import sseclient
from requests.exceptions import HTTPError
from urllib3.exceptions import ProtocolError

from . import logs, vars
from .common import URL
from .exceptions import APIError, RetryException

"""
will be moved to own repository as module / submodules
will be installable to app that need this modules
"""


def default_event_handler(event: dict):
    logs.logger.info(event)


class IEXConnectionBroker:
    _base_url = vars.IEX_API_URL

    def __init__(self):
        self._session = requests.Session()
        self._retry = int(os.environ.get("IEX_RETRY_MAX", 3))
        self._retry_wait = int(os.environ.get("IEX_RETRY_WAIT", 3))
        self._retry_codes = [
            int(o) for o in os.environ.get("IEX_RETRY_CODES", "429,504").split(",")
        ]

    def _request(
        self,
        method,
        path,
        data=None,
        base_url=None,
    ):
        base_url = base_url or self._base_url
        url = base_url + "/" + path
        opts = {"allow_redirects": False}
        if method.upper() in ["GET", "DELETE"]:
            opts["params"] = data
        else:
            opts["json"] = data

        retry = self._retry
        if retry < 0:
            retry = 0
        while retry >= 0:
            try:
                return self._one_request(method, url, opts, retry)
            except RetryException:
                retry_wait = self._retry_wait
                logs.logger.warning(
                    "sleep {} seconds and retrying {} "
                    "{} more time(s)...".format(retry_wait, url, retry)
                )
                time.sleep(retry_wait)
                retry -= 1
                continue

    def _one_request(self, method: str, url: URL, opts: dict, retry: int):
        """
        Perform one request, possibly raising RetryException in the case
        the response is 429. Otherwise, if error text contain "code" string,
        then it decodes to json object and returns APIError.
        Returns the body json in the 200 status.
        """
        retry_codes = self._retry_codes
        resp = self._session.request(method, url, **opts)
        logs.logger.debug(
            {
                "method": method,
                "url": resp.request.url,
                "status": resp.status_code,
                "header": resp.request.headers,
                "body": resp.request.body,
            }
        )
        try:
            resp.raise_for_status()
        except HTTPError as http_error:
            # retry if we hit Rate Limit
            if resp.status_code in retry_codes and retry > 0:
                raise RetryException()
            if "code" in resp.text:
                error = resp.json()
                if "code" in error:
                    logs.logger.critical(
                        {
                            "method": method,
                            "url": resp.request.url,
                            "status": resp.status_code,
                            "header": resp.request.headers,
                            "body": resp.request.body,
                            "error_response": error,
                        }
                    )
                    raise APIError(error, http_error)
            else:
                raise
        if resp.text != "":
            logs.logger.debug(f"{method} {url} {resp.status_code}")
            return resp.json()
        return None

    def get(self, path, data=None):
        return self._request("GET", path, data)

    def post(self, path, data=None):
        return self._request("POST", path, data)

    def put(self, path, data=None):
        return self._request("PUT", path, data)

    def patch(self, path, data=None):
        return self._request("PATCH", path, data)

    def delete(self, path, data=None):
        return self._request("DELETE", path, data)


class PriceData(IEXConnectionBroker):
    _base_url = vars.IEX_API_URL
    _token = vars.IEX_TOKEN

    def get_quote(self, symbol: str):
        return self.get(f"stable/stock/{symbol.lower()}/quote?token={self._token}")

    def get_lastestPrice(self, symbol: str):
        result = self.get_quote(symbol)
        return result.get("latestPrice", None)

    def get_marketOpen(self, symbol: str):
        result = self.get_quote(symbol)
        return result.get("isUSMarketOpen", False)
