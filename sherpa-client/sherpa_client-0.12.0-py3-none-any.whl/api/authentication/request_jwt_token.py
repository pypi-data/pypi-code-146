from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.bearer_token import BearerToken
from ...models.credentials import Credentials
from ...models.request_jwt_token_project_access_mode import RequestJwtTokenProjectAccessMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: Credentials,
    project_filter: Union[Unset, None, str] = UNSET,
    project_access_mode: Union[Unset, None, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, None, bool] = False,
    login_only: Union[Unset, None, bool] = False,
    no_permissions: Union[Unset, None, bool] = False,
    duration: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/auth/login".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["projectFilter"] = project_filter

    json_project_access_mode: Union[Unset, None, str] = UNSET
    if not isinstance(project_access_mode, Unset):
        json_project_access_mode = project_access_mode.value if project_access_mode else None

    params["projectAccessMode"] = json_project_access_mode

    params["annotateOnly"] = annotate_only

    params["loginOnly"] = login_only

    params["noPermissions"] = no_permissions

    params["duration"] = duration

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[BearerToken]:
    if response.status_code == HTTPStatus.OK:
        response_200 = BearerToken.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[BearerToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Credentials,
    project_filter: Union[Unset, None, str] = UNSET,
    project_access_mode: Union[Unset, None, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, None, bool] = False,
    login_only: Union[Unset, None, bool] = False,
    no_permissions: Union[Unset, None, bool] = False,
    duration: Union[Unset, None, str] = UNSET,
) -> Response[BearerToken]:
    """Request a bearer token

    Args:
        project_filter (Union[Unset, None, str]):
        project_access_mode (Union[Unset, None, RequestJwtTokenProjectAccessMode]):
        annotate_only (Union[Unset, None, bool]):
        login_only (Union[Unset, None, bool]):
        no_permissions (Union[Unset, None, bool]):
        duration (Union[Unset, None, str]):
        json_body (Credentials):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BearerToken]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        project_filter=project_filter,
        project_access_mode=project_access_mode,
        annotate_only=annotate_only,
        login_only=login_only,
        no_permissions=no_permissions,
        duration=duration,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: Credentials,
    project_filter: Union[Unset, None, str] = UNSET,
    project_access_mode: Union[Unset, None, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, None, bool] = False,
    login_only: Union[Unset, None, bool] = False,
    no_permissions: Union[Unset, None, bool] = False,
    duration: Union[Unset, None, str] = UNSET,
) -> Optional[BearerToken]:
    """Request a bearer token

    Args:
        project_filter (Union[Unset, None, str]):
        project_access_mode (Union[Unset, None, RequestJwtTokenProjectAccessMode]):
        annotate_only (Union[Unset, None, bool]):
        login_only (Union[Unset, None, bool]):
        no_permissions (Union[Unset, None, bool]):
        duration (Union[Unset, None, str]):
        json_body (Credentials):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BearerToken]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        project_filter=project_filter,
        project_access_mode=project_access_mode,
        annotate_only=annotate_only,
        login_only=login_only,
        no_permissions=no_permissions,
        duration=duration,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Credentials,
    project_filter: Union[Unset, None, str] = UNSET,
    project_access_mode: Union[Unset, None, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, None, bool] = False,
    login_only: Union[Unset, None, bool] = False,
    no_permissions: Union[Unset, None, bool] = False,
    duration: Union[Unset, None, str] = UNSET,
) -> Response[BearerToken]:
    """Request a bearer token

    Args:
        project_filter (Union[Unset, None, str]):
        project_access_mode (Union[Unset, None, RequestJwtTokenProjectAccessMode]):
        annotate_only (Union[Unset, None, bool]):
        login_only (Union[Unset, None, bool]):
        no_permissions (Union[Unset, None, bool]):
        duration (Union[Unset, None, str]):
        json_body (Credentials):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BearerToken]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        project_filter=project_filter,
        project_access_mode=project_access_mode,
        annotate_only=annotate_only,
        login_only=login_only,
        no_permissions=no_permissions,
        duration=duration,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Credentials,
    project_filter: Union[Unset, None, str] = UNSET,
    project_access_mode: Union[Unset, None, RequestJwtTokenProjectAccessMode] = UNSET,
    annotate_only: Union[Unset, None, bool] = False,
    login_only: Union[Unset, None, bool] = False,
    no_permissions: Union[Unset, None, bool] = False,
    duration: Union[Unset, None, str] = UNSET,
) -> Optional[BearerToken]:
    """Request a bearer token

    Args:
        project_filter (Union[Unset, None, str]):
        project_access_mode (Union[Unset, None, RequestJwtTokenProjectAccessMode]):
        annotate_only (Union[Unset, None, bool]):
        login_only (Union[Unset, None, bool]):
        no_permissions (Union[Unset, None, bool]):
        duration (Union[Unset, None, str]):
        json_body (Credentials):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BearerToken]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            project_filter=project_filter,
            project_access_mode=project_access_mode,
            annotate_only=annotate_only,
            login_only=login_only,
            no_permissions=no_permissions,
            duration=duration,
        )
    ).parsed
