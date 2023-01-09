from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.sherpa_job_bean import SherpaJobBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    status_filter: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/jobs".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["statusFilter"] = status_filter

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["SherpaJobBean"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_sherpa_job_bean_array_item_data in _response_200:
            componentsschemas_sherpa_job_bean_array_item = SherpaJobBean.from_dict(
                componentsschemas_sherpa_job_bean_array_item_data
            )

            response_200.append(componentsschemas_sherpa_job_bean_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["SherpaJobBean"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    *,
    client: Client,
    status_filter: Union[Unset, None, str] = UNSET,
) -> Response[List["SherpaJobBean"]]:
    """Get current jobs

    Args:
        project_name (str):
        status_filter (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['SherpaJobBean']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        status_filter=status_filter,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    *,
    client: Client,
    status_filter: Union[Unset, None, str] = UNSET,
) -> Optional[List["SherpaJobBean"]]:
    """Get current jobs

    Args:
        project_name (str):
        status_filter (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['SherpaJobBean']]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        status_filter=status_filter,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    status_filter: Union[Unset, None, str] = UNSET,
) -> Response[List["SherpaJobBean"]]:
    """Get current jobs

    Args:
        project_name (str):
        status_filter (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['SherpaJobBean']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        status_filter=status_filter,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    status_filter: Union[Unset, None, str] = UNSET,
) -> Optional[List["SherpaJobBean"]]:
    """Get current jobs

    Args:
        project_name (str):
        status_filter (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['SherpaJobBean']]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            status_filter=status_filter,
        )
    ).parsed
