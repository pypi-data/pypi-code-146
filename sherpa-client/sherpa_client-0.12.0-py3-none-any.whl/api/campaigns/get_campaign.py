from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.campaign import Campaign
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    inline_messages: Union[Unset, None, bool] = False,
    inline_user_session_events: Union[Unset, None, str] = "none",
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/campaigns/{campaignId}".format(
        client.base_url, projectName=project_name, campaignId=campaign_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["inlineMessages"] = inline_messages

    params["inlineUserSessionEvents"] = inline_user_session_events

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, Campaign]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Campaign.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Campaign]]:
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
    inline_messages: Union[Unset, None, bool] = False,
    inline_user_session_events: Union[Unset, None, str] = "none",
) -> Response[Union[Any, Campaign]]:
    """Get campaign

    Args:
        project_name (str):
        campaign_id (str):
        inline_messages (Union[Unset, None, bool]):
        inline_user_session_events (Union[Unset, None, str]):  Default: 'none'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Campaign]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        campaign_id=campaign_id,
        client=client,
        inline_messages=inline_messages,
        inline_user_session_events=inline_user_session_events,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    inline_messages: Union[Unset, None, bool] = False,
    inline_user_session_events: Union[Unset, None, str] = "none",
) -> Optional[Union[Any, Campaign]]:
    """Get campaign

    Args:
        project_name (str):
        campaign_id (str):
        inline_messages (Union[Unset, None, bool]):
        inline_user_session_events (Union[Unset, None, str]):  Default: 'none'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Campaign]]
    """

    return sync_detailed(
        project_name=project_name,
        campaign_id=campaign_id,
        client=client,
        inline_messages=inline_messages,
        inline_user_session_events=inline_user_session_events,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    inline_messages: Union[Unset, None, bool] = False,
    inline_user_session_events: Union[Unset, None, str] = "none",
) -> Response[Union[Any, Campaign]]:
    """Get campaign

    Args:
        project_name (str):
        campaign_id (str):
        inline_messages (Union[Unset, None, bool]):
        inline_user_session_events (Union[Unset, None, str]):  Default: 'none'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Campaign]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        campaign_id=campaign_id,
        client=client,
        inline_messages=inline_messages,
        inline_user_session_events=inline_user_session_events,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    inline_messages: Union[Unset, None, bool] = False,
    inline_user_session_events: Union[Unset, None, str] = "none",
) -> Optional[Union[Any, Campaign]]:
    """Get campaign

    Args:
        project_name (str):
        campaign_id (str):
        inline_messages (Union[Unset, None, bool]):
        inline_user_session_events (Union[Unset, None, str]):  Default: 'none'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Campaign]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            campaign_id=campaign_id,
            client=client,
            inline_messages=inline_messages,
            inline_user_session_events=inline_user_session_events,
        )
    ).parsed
