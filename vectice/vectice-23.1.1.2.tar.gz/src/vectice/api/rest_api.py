from __future__ import annotations

import logging
import os
from enum import Enum
from json import JSONEncoder
from typing import Any, BinaryIO, Dict, Sequence, TYPE_CHECKING, cast

import requests

from vectice.api.http_error import HttpError
from vectice.api.http_error_handlers import ClientErrorHandler

if TYPE_CHECKING:
    from requests import Response

    from vectice.api._auth import Auth
    from vectice.api.json_object import JsonObject

logger = logging.getLogger("vectice.api.rest")


def log_request(method: str, path: str, headers: dict, payload: Any | None = None) -> None:
    should_log = os.getenv("LOG_VECTICE_HTTP_REQUEST")
    if should_log is not None and should_log != "0" and should_log.lower() != "false":
        logger.info("###")
        logger.info(f"{method} {path}")
        for item in headers.items():
            logger.info(f"{item[0]}: {item[1] if item[0] != 'Authorization' else '********'}")
        logger.info(payload)
    else:
        logger.debug("###")
        logger.debug(f"{method} {path}")
        for item in headers.items():
            logger.debug(f"{item[0]}: {item[1] if item[0] != 'Authorization' else '********'}")
        logger.debug(payload)


class VecticeEncoder(JSONEncoder):
    """
    Json Encoder with 2 specific behaviors:
    - handle datetime types so be serialized as a string following ISO8601 format
    - remove any null property from the serialized json.
    - handle nested objects
    """

    def default(self, obj: Any) -> Any:
        from copy import deepcopy

        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        internal_copy = deepcopy(obj.__dict__)
        return {k.lstrip("_"): v for (k, v) in internal_copy.items() if v is not None}


class RestApi:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.api_base_url = self.auth.api_base_url
        self.verify_certificate = self.auth.verify_certificate
        self._httpErrorHandler = ClientErrorHandler()

    def get(self, path: str) -> dict[str, Any]:
        headers = {**self.auth.http_headers, "Content-Type": "application/json"}
        log_request("GET", path, headers)
        response = requests.get(url=self.api_base_url + path, headers=headers, verify=self.verify_certificate)
        return self._response(self.api_base_url + path, headers, response, "GET")

    def post(self, path: str, payload: Any = None) -> JsonObject:
        headers = {**self.auth.http_headers, "Content-Type": "application/json"}
        cleaned_payload: Any = self._clean_dict(payload) if isinstance(payload, dict) else payload
        data = VecticeEncoder(indent=1).encode(cleaned_payload)
        log_request("POST", path, headers, data)
        response = requests.post(
            url=self.api_base_url + path, headers=headers, data=data, verify=self.verify_certificate
        )
        return self._response(self.api_base_url + path, headers, response, "POST", data)

    def put(self, path: str, payload: Any = None) -> JsonObject:
        headers = {**self.auth.http_headers, "Content-Type": "application/json"}
        cleaned_payload: Any = self._clean_dict(payload) if isinstance(payload, dict) else payload
        data = VecticeEncoder(indent=1).encode(cleaned_payload)
        log_request("PUT", path, headers, data)
        response = requests.put(
            url=self.auth.api_base_url + path, headers=headers, data=data, verify=self.verify_certificate
        )
        return self._response(self.auth.api_base_url + path, headers, response, "PUT", payload)

    def delete(self, path: str, payload: Any = None) -> JsonObject:
        headers = {**self.auth.http_headers, "Content-Type": "application/json"}
        if payload is None:
            data = None
        else:
            cleaned_payload: Any = self._clean_dict(payload) if isinstance(payload, dict) else payload
            data = VecticeEncoder(indent=1).encode(cleaned_payload)
        log_request("DELETE", path, headers, data)
        response = requests.delete(
            url=self.auth.api_base_url + path, headers=headers, data=data, verify=self.auth.verify_certificate
        )
        return self._response(self.auth.api_base_url + path, headers, response, "DELETE", data)

    def _post_attachments(
        self, path: str, files: Sequence[tuple[str, tuple[Any, BinaryIO]]] | None = None
    ) -> Response | None:
        headers = self.auth.http_headers
        response = requests.post(
            url=self.auth.api_base_url + path,
            headers=headers,
            files=files,
            verify=self.auth.verify_certificate,
        )
        return self._attachment_response(self.auth.api_base_url + path, headers, response, "POST")

    def _put_attachments(
        self, path: str, files: list[tuple[str, tuple[Any, BinaryIO]]] | None = None
    ) -> Response | None:
        headers = self.auth.http_headers
        response = requests.put(
            url=self.api_base_url + path,
            headers=headers,
            files=files,
            verify=self.verify_certificate,
        )
        return self._attachment_response(self.api_base_url + path, headers, response, "PUT")

    def _get_attachment(self, path: str) -> Response:
        headers = self.auth.http_headers
        response = requests.get(
            url=self.api_base_url + path, headers=headers, verify=self.verify_certificate, stream=True
        )
        return self._attachment_response(self.api_base_url + path, headers, response, "GET")

    def _delete_attachment(self, path: str) -> Response | None:
        headers = self.auth.http_headers
        response = requests.delete(url=self.api_base_url + path, headers=headers)
        return self._attachment_response(self.api_base_url + path, headers, response, "DELETE")

    def _list_attachments(self, path: str) -> Sequence[dict]:
        headers = {**self.auth.http_headers, "Content-Type": "application/json"}
        response = requests.get(url=self.api_base_url + path, headers=headers, verify=self.verify_certificate)
        self._attachment_response(self.api_base_url + path, headers, response, "GET")
        return cast(Sequence[Dict], response.json())

    @classmethod
    def raise_status(cls, path: str, response: Response, method: str, payload: Any | None = None) -> None:
        if not (200 <= response.status_code < 300):
            reason = response.text
            if not isinstance(payload, str):
                json = VecticeEncoder(indent=4, sort_keys=True).encode(payload) if payload is not None else None
            else:
                json = payload
            raise HttpError(response.status_code, reason, path, method, json)

    def _response(
        self, path: str, headers: dict[str, str], response: Response, method: str, payload: Any | None = None
    ) -> JsonObject:
        self.raise_status(path, response, method, payload)
        logger.debug(f"{method} {path} {response.status_code}")
        logger.debug("\n".join(f"{item[0]}: {item[1]}" for item in headers.items()))
        logger.debug(payload)
        if len(response.content) > 0:
            return cast(Dict[str, Any], response.json())
        return {response.reason: response.status_code}

    def _attachment_response(self, path: str, headers: dict[str, str], response: Response, method: str) -> Response:
        self.raise_status(path, response, method)
        logger.debug(f"{method} {path} {response.status_code}")
        logger.debug("\n".join(f"{item[0]}: {item[1]}" for item in headers.items()))
        return response

    def _clean_dict(self, payload: dict):
        cleaned_payload = {}
        for key, value in payload.items():
            if value is not None:
                if isinstance(value, dict):
                    cleaned_payload[key] = self._clean_dict(value)
                else:
                    cleaned_payload[key] = value
        return cleaned_payload
