from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    user_session_id: str,
    session_label: Union[Unset, None, str] = "",
    username: Union[Unset, None, str] = "",
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/campaigns/{campaignId}/_export_user_session".format(
        client.base_url, projectName=project_name, campaignId=campaign_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["userSessionId"] = user_session_id

    params["sessionLabel"] = session_label

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    user_session_id: str,
    session_label: Union[Unset, None, str] = "",
    username: Union[Unset, None, str] = "",
) -> Response[Any]:
    """export a user session

    Args:
        project_name (str):
        campaign_id (str):
        user_session_id (str):
        session_label (Union[Unset, None, str]):  Default: ''.
        username (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        campaign_id=campaign_id,
        client=client,
        user_session_id=user_session_id,
        session_label=session_label,
        username=username,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    user_session_id: str,
    session_label: Union[Unset, None, str] = "",
    username: Union[Unset, None, str] = "",
) -> Response[Any]:
    """export a user session

    Args:
        project_name (str):
        campaign_id (str):
        user_session_id (str):
        session_label (Union[Unset, None, str]):  Default: ''.
        username (Union[Unset, None, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        campaign_id=campaign_id,
        client=client,
        user_session_id=user_session_id,
        session_label=session_label,
        username=username,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
