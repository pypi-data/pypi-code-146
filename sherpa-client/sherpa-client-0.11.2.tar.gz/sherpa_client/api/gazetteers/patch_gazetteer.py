from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.gazetteer import Gazetteer
from ...models.gazetteer_patch import GazetteerPatch
from ...types import Response


def _get_kwargs(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: GazetteerPatch,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/gazetteers/{name}".format(client.base_url, projectName=project_name, name=name)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, Gazetteer]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Gazetteer.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Gazetteer]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: GazetteerPatch,
) -> Response[Union[Any, Gazetteer]]:
    """Partially update a gazetteer

    Args:
        project_name (str):
        name (str):
        json_body (GazetteerPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Gazetteer]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: GazetteerPatch,
) -> Optional[Union[Any, Gazetteer]]:
    """Partially update a gazetteer

    Args:
        project_name (str):
        name (str):
        json_body (GazetteerPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Gazetteer]]
    """

    return sync_detailed(
        project_name=project_name,
        name=name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: GazetteerPatch,
) -> Response[Union[Any, Gazetteer]]:
    """Partially update a gazetteer

    Args:
        project_name (str):
        name (str):
        json_body (GazetteerPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Gazetteer]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: GazetteerPatch,
) -> Optional[Union[Any, Gazetteer]]:
    """Partially update a gazetteer

    Args:
        project_name (str):
        name (str):
        json_body (GazetteerPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Gazetteer]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            name=name,
            client=client,
            json_body=json_body,
        )
    ).parsed
