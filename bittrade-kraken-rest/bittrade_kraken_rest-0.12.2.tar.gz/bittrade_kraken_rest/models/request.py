from typing import Any

import requests
from returns.io import IOResult, impure_safe
from returns.pipeline import flow
from returns.pointfree import bind_result
from returns.result import safe

from bittrade_kraken_rest.connection.session import session


def fetch(request: requests.PreparedRequest) -> IOResult[dict[str, Any], Exception]:
    return flow(
        request,
        _make_request,
        bind_result(_parse_json),
        bind_result(_get_result),
    )


@impure_safe
def _make_request(request: requests.PreparedRequest) -> requests.Response:
    response = session.send(request)
    response.raise_for_status()
    return response


@safe
def _parse_json(response: requests.Response) -> dict[str, Any]:
    return response.json()


@safe
def _get_result(json_response: dict[str, Any]) -> list | dict:
    if "result" in json_response:
        return json_response["result"]
    raise Exception(json_response["error"][0])
