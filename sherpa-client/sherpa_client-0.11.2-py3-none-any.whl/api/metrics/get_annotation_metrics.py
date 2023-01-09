from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.annotation_metrics import AnnotationMetrics
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    *,
    client: Client,
    facet: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/annotationMetrics".format(client.base_url, projectName=project_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["facet"] = facet

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[AnnotationMetrics]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AnnotationMetrics.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[AnnotationMetrics]:
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
    facet: Union[Unset, None, str] = "",
) -> Response[AnnotationMetrics]:
    """Get some metrics on annotations

    Args:
        project_name (str):
        facet (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        facet=facet,
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
    facet: Union[Unset, None, str] = "",
) -> Optional[AnnotationMetrics]:
    """Get some metrics on annotations

    Args:
        project_name (str):
        facet (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationMetrics]
    """

    return sync_detailed(
        project_name=project_name,
        client=client,
        facet=facet,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    *,
    client: Client,
    facet: Union[Unset, None, str] = "",
) -> Response[AnnotationMetrics]:
    """Get some metrics on annotations

    Args:
        project_name (str):
        facet (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationMetrics]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        client=client,
        facet=facet,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    *,
    client: Client,
    facet: Union[Unset, None, str] = "",
) -> Optional[AnnotationMetrics]:
    """Get some metrics on annotations

    Args:
        project_name (str):
        facet (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationMetrics]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            client=client,
            facet=facet,
        )
    ).parsed
