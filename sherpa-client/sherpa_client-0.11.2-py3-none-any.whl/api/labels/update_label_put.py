from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.label import Label
from ...models.label_update import LabelUpdate
from ...types import Response


def _get_kwargs(
    project_name: str,
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/labels/{labelName}".format(
        client.base_url, projectName=project_name, labelName=label_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Label]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Label.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Label]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Response[Label]:
    """Update a label (Please use PATCH instead of PUT)

    Args:
        project_name (str):
        label_name (str):
        json_body (LabelUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Label]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
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
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Optional[Label]:
    """Update a label (Please use PATCH instead of PUT)

    Args:
        project_name (str):
        label_name (str):
        json_body (LabelUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Label]
    """

    return sync_detailed(
        project_name=project_name,
        label_name=label_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Response[Label]:
    """Update a label (Please use PATCH instead of PUT)

    Args:
        project_name (str):
        label_name (str):
        json_body (LabelUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Label]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        label_name=label_name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    label_name: str,
    *,
    client: Client,
    json_body: LabelUpdate,
) -> Optional[Label]:
    """Update a label (Please use PATCH instead of PUT)

    Args:
        project_name (str):
        label_name (str):
        json_body (LabelUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Label]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            label_name=label_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
