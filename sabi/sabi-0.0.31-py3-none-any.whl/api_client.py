import json
import requests
from os import path
import logging
import time


class ApiClient:
    headers = None
    api_host = None
    api_base = None
    logger = None

    def __init__(self, api_key, base, host):
        if host is None:
            host = "https://api.sabi.ai"

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.headers = {"content-type": "application/json", "Authorization": f"Bearer {api_key}"}
        self.api_host = host
        self.api_base = base

    def _request(self, method, *endpoints, **kwargs):
        kwargs["headers"] = self.headers
        if not endpoints[0].startswith(self.api_base):
            endpoints = [self.api_base, *endpoints]
        url = path.join(self.api_host, *[str(s).strip("/") for s in endpoints])

        attempts = 1
        success = False

        while attempts <= 5 and not success:
            response = requests.request(method, url, **kwargs)
            if response.status_code > 299:
                self.logger.warning(f"Failed to call ({method}) - {url}")
                self.logger.info(f"**** Status code: {response.status_code}, Content: {response.text} sleeping for {attempts} ****")
                time.sleep(attempts)
                attempts += 1
            else:
                success = True

        if not success:
            raise Exception(f"Status code: {response.status_code}, Content: {response.text}")

        if response.status_code == 204:
            return {}
        return json.loads(response.text)

    def get(self, *segments, **kwargs):
        return self._request("get", *segments, **kwargs)

    def post(self, *segments, **kwargs):
        return self._request("post", *segments, **kwargs)

    def put(self, *segments, **kwargs):
        return self._request("put", *segments, **kwargs)

    def delete(self, *segments, **kwargs):
        return self._request("delete", *segments, **kwargs)
