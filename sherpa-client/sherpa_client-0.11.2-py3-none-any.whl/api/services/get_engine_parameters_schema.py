from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.get_engine_parameters_schema_response_200 import GetEngineParametersSchemaResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service: str,
    *,
    client: Client,
    nature: str,
    function: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/services/{service}/parameters".format(client.base_url, service=service)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["nature"] = nature

    params["function"] = function

    params["uiSchema"] = ui_schema

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, GetEngineParametersSchemaResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetEngineParametersSchemaResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, GetEngineParametersSchemaResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service: str,
    *,
    client: Client,
    nature: str,
    function: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Response[Union[Any, GetEngineParametersSchemaResponse200]]:
    """get the options of the given service in JSON schema format

    Args:
        service (str):
        nature (str):
        function (str):
        ui_schema (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetEngineParametersSchemaResponse200]]
    """

    kwargs = _get_kwargs(
        service=service,
        client=client,
        nature=nature,
        function=function,
        ui_schema=ui_schema,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service: str,
    *,
    client: Client,
    nature: str,
    function: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, GetEngineParametersSchemaResponse200]]:
    """get the options of the given service in JSON schema format

    Args:
        service (str):
        nature (str):
        function (str):
        ui_schema (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetEngineParametersSchemaResponse200]]
    """

    return sync_detailed(
        service=service,
        client=client,
        nature=nature,
        function=function,
        ui_schema=ui_schema,
    ).parsed


async def asyncio_detailed(
    service: str,
    *,
    client: Client,
    nature: str,
    function: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Response[Union[Any, GetEngineParametersSchemaResponse200]]:
    """get the options of the given service in JSON schema format

    Args:
        service (str):
        nature (str):
        function (str):
        ui_schema (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetEngineParametersSchemaResponse200]]
    """

    kwargs = _get_kwargs(
        service=service,
        client=client,
        nature=nature,
        function=function,
        ui_schema=ui_schema,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service: str,
    *,
    client: Client,
    nature: str,
    function: str,
    ui_schema: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, GetEngineParametersSchemaResponse200]]:
    """get the options of the given service in JSON schema format

    Args:
        service (str):
        nature (str):
        function (str):
        ui_schema (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetEngineParametersSchemaResponse200]]
    """

    return (
        await asyncio_detailed(
            service=service,
            client=client,
            nature=nature,
            function=function,
            ui_schema=ui_schema,
        )
    ).parsed
