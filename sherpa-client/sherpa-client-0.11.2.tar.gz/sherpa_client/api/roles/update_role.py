from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.ack import Ack
from ...models.role_update import RoleUpdate
from ...types import Response


def _get_kwargs(
    rolename: str,
    *,
    client: Client,
    json_body: RoleUpdate,
) -> Dict[str, Any]:
    url = "{}/roles/{rolename}".format(client.base_url, rolename=rolename)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Ack, Any]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Ack.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Ack, Any]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    rolename: str,
    *,
    client: Client,
    json_body: RoleUpdate,
) -> Response[Union[Ack, Any]]:
    """Update role

    Args:
        rolename (str):
        json_body (RoleUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        rolename=rolename,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rolename: str,
    *,
    client: Client,
    json_body: RoleUpdate,
) -> Optional[Union[Ack, Any]]:
    """Update role

    Args:
        rolename (str):
        json_body (RoleUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    return sync_detailed(
        rolename=rolename,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    rolename: str,
    *,
    client: Client,
    json_body: RoleUpdate,
) -> Response[Union[Ack, Any]]:
    """Update role

    Args:
        rolename (str):
        json_body (RoleUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        rolename=rolename,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rolename: str,
    *,
    client: Client,
    json_body: RoleUpdate,
) -> Optional[Union[Ack, Any]]:
    """Update role

    Args:
        rolename (str):
        json_body (RoleUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    return (
        await asyncio_detailed(
            rolename=rolename,
            client=client,
            json_body=json_body,
        )
    ).parsed
