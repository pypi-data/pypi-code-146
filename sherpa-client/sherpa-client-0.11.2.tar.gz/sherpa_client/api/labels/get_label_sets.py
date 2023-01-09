from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.label_set import LabelSet
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    include_labels: Union[Unset, None, bool] = True,
    include_labels_count: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/label_sets".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["includeLabels"] = include_labels

    params["includeLabelsCount"] = include_labels_count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["LabelSet"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_label_set_array_item_data in _response_200:
            componentsschemas_label_set_array_item = LabelSet.from_dict(componentsschemas_label_set_array_item_data)

            response_200.append(componentsschemas_label_set_array_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["LabelSet"]]:
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
    include_labels: Union[Unset, None, bool] = True,
    include_labels_count: Union[Unset, None, bool] = False,
) -> Response[List["LabelSet"]]:
    """Get list of labelSet

    Args:
        project_name (str):
        include_labels (Union[Unset, None, bool]):  Default: True.
        include_labels_count (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['LabelSet']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
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
    include_labels: Union[Unset, None, bool] = True,
    include_labels_count: Union[Unset, None, bool] = False,
) -> Optional[List["LabelSet"]]:
    """Get list of labelSet

    Args:
        project_name (str):
        include_labels (Union[Unset, None, bool]):  Default: True.
        include_labels_count (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['LabelSet']]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    include_labels: Union[Unset, None, bool] = True,
    include_labels_count: Union[Unset, None, bool] = False,
) -> Response[List["LabelSet"]]:
    """Get list of labelSet

    Args:
        project_name (str):
        include_labels (Union[Unset, None, bool]):  Default: True.
        include_labels_count (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['LabelSet']]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        include_labels=include_labels,
        include_labels_count=include_labels_count,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    include_labels: Union[Unset, None, bool] = True,
    include_labels_count: Union[Unset, None, bool] = False,
) -> Optional[List["LabelSet"]]:
    """Get list of labelSet

    Args:
        project_name (str):
        include_labels (Union[Unset, None, bool]):  Default: True.
        include_labels_count (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['LabelSet']]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            include_labels=include_labels,
            include_labels_count=include_labels_count,
        )
    ).parsed
