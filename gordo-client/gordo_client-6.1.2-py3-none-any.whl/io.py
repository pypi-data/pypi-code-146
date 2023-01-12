"""Gordo client io."""
from typing import Optional, Union

import requests


class HttpUnprocessableEntity(Exception):
    """
    Represents an error from an HTTP status code of 422: UnprocessableEntity.
    Used in our case for calling /anomaly/prediction on a model which does not
    support anomaly behavior.
    """


class ResourceGone(Exception):
    """
    Represents an error from an HTTP status code of 410: Gone.
    Indicates that access to the target resource is no longer available at the origin
    server and that this condition is likely to be permanent.

    Used in our case for calling the server with a revision which is no longer used.
    """


class BadGordoRequest(Exception):
    """
    Represents a general 4xx bad request
    """


class BadGordoResponse(Exception):
    """
    Represents a general bad response (not json or model)
    """

    def __init__(self, msg: str, content: bytes, status_code: int = 200, content_type: Optional[str] = None):
        self.msg = msg
        self.content = content
        self.status_code = status_code
        self.content_type = content_type
        super().__init__(msg)

    def __reduce__(self):
        return self.__class__, (self.msg, self.content, self.status_code, self.content_type)


class NotFound(Exception):
    """
    Represents a 404
    """


def _handle_response(resp: requests.Response, resource_name: Optional[str] = None) -> Union[dict, bytes]:
    """
    Handle the response from the server.

    Either returning the parsed json (if it is json), the pure bytestream of the content, or raise an exception
    if something went wrong.


    Parameters
    ----------
    resp:
        The request to inspect for a result
    resource_name:
        An optional name to add to error messages. Should describe the resource we
        attempted to GET

    Returns
    -------
     Union[dict, bytes]

    Raises
    ------
    HttpUnprocessableEntitys
        In case of a 422 from the server
    ResourceGone
        In case of a 410 from the server
    NotFound
        In case of a 404 from the server
    BadGordoRequest
        Any other 4xx error
    IOError
        In case of network or IO errors
    """
    if 200 <= resp.status_code <= 299:
        if _is_model_response(resp):
            return resp.content
        elif _is_json_response(resp):
            return resp.json()
        resource_msg = f" while fetching resource: {resource_name}" if resource_name else ""
        raise BadGordoResponse(
            f"Bad gordo response found{resource_msg}.", resp.content, resp.status_code, resp.headers.get("content-type")
        )

    if resource_name:
        msg = (
            f"We failed to get response while fetching resource: {resource_name}. "
            f"Return code: {resp.status_code}. Return content: {resp.content!r}"
        )
    else:
        msg = f"Failed to get response: {resp.status_code}: {resp.content!r}"

    if resp.status_code == 422:
        raise HttpUnprocessableEntity(msg)
    elif resp.status_code == 410:
        raise ResourceGone(msg)
    elif resp.status_code == 404:
        raise NotFound(msg)
    elif 400 <= resp.status_code <= 499:
        raise BadGordoRequest(msg)
    raise IOError(msg)


def _is_json_response(response) -> bool:
    return response.headers.get("content-type") == "application/json"


def _is_model_response(response) -> bool:
    return response.headers.get("content-type") == "application/x-tar"
