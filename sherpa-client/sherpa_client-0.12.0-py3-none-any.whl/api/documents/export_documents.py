from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.document import Document
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = 0,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/documents".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["outputFields"] = output_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["Document"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_document_array_item_data in _response_200:
            componentsschemas_document_array_item = Document.from_dict(componentsschemas_document_array_item_data)

            response_200.append(componentsschemas_document_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["Document"]]:
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
    limit: Union[Unset, None, int] = 0,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Response[List["Document"]]:
    """Get documents within project

    Args:
        project_name (str):
        limit (Union[Unset, None, int]):
        output_fields (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['Document']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        limit=limit,
        output_fields=output_fields,
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
    limit: Union[Unset, None, int] = 0,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Optional[List["Document"]]:
    """Get documents within project

    Args:
        project_name (str):
        limit (Union[Unset, None, int]):
        output_fields (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['Document']]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        limit=limit,
        output_fields=output_fields,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = 0,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Response[List["Document"]]:
    """Get documents within project

    Args:
        project_name (str):
        limit (Union[Unset, None, int]):
        output_fields (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['Document']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        limit=limit,
        output_fields=output_fields,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = 0,
    output_fields: Union[Unset, None, str] = UNSET,
) -> Optional[List["Document"]]:
    """Get documents within project

    Args:
        project_name (str):
        limit (Union[Unset, None, int]):
        output_fields (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['Document']]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            limit=limit,
            output_fields=output_fields,
        )
    ).parsed
