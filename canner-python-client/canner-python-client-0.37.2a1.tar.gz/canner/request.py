import sys
import requests
from typing import Optional
from http import HTTPStatus
from requests.models import Response
from canner.exceptions import CannerError, ConnectionError
from canner.logging import get_logger

__all__ = ["CannerRequest"]
logger = get_logger("CannerRequest")


class CannerRequest(object):
    def __init__(self, endpoint: str, headers: Optional[dict] = None):
        self._endpoint = endpoint
        self._headers = headers

    def _parse_graphql(self, resp: Response):
        # handle non 200 error (not from web backend graphql e.g: some middlewares)
        if HTTPStatus(resp.status_code) != HTTPStatus.OK:
            # Check the graphql response error format
            if resp.text and "code" in resp.text:
                error = resp.json()
                raise CannerError(error_code=error["code"], message=error["message"])
            raise ConnectionError(message=resp.text)
        else:
            result = resp.json()
            # handle graphql error (status code is 200, but check error from errors)
            if "errors" in result:
                error = result["errors"][0]
                raise CannerError(
                    error_code=error["extensions"]["code"], message=error["message"]
                )
            data = result.get("data")
            return data

    def _parse_restful(self, resp: Response):
        if HTTPStatus(resp.status_code) != HTTPStatus.OK:
            # Check the restful response error format
            if resp.text and "code" in resp.text:
                error = resp.json()
                raise CannerError(error_code=error["code"], message=error["message"])
            raise ConnectionError(message=resp.text)
        # If status code is 200 or not 200
        data = resp.json()
        return data

    def graphql_exec(self, payload: dict):
        """
        The graphql request method
        """
        graphql_url = f"{self._endpoint}/graphql"
        resp: Response = requests.post(
            url=graphql_url, json=payload, headers=self._headers
        )
        return self._parse_graphql(resp)

    def get(self, path: str):
        """
        The restful HTTP Get request method
        """
        rest_url = f"{self._endpoint}/{path}"
        resp: Response = requests.get(url=rest_url, headers=self._headers)
        return self._parse_restful(resp)
