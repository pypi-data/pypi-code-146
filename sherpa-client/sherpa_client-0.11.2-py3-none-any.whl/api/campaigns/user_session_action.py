from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.ack import Ack
from ...models.user_session_action_action import UserSessionActionAction
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    user_session_id: str,
    action: UserSessionActionAction,
    action_value: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/campaigns/{campaignId}/_user_session_action".format(
        client.base_url, projectName=project_name, campaignId=campaign_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["userSessionId"] = user_session_id

    json_action = action.value

    params["action"] = json_action

    params["actionValue"] = action_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    user_session_id: str,
    action: UserSessionActionAction,
    action_value: Union[Unset, None, str] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Perform an action on a user session

    Args:
        project_name (str):
        campaign_id (str):
        user_session_id (str):
        action (UserSessionActionAction):
        action_value (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        campaign_id=campaign_id,
        client=client,
        user_session_id=user_session_id,
        action=action,
        action_value=action_value,
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
    user_session_id: str,
    action: UserSessionActionAction,
    action_value: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Perform an action on a user session

    Args:
        project_name (str):
        campaign_id (str):
        user_session_id (str):
        action (UserSessionActionAction):
        action_value (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    return sync_detailed(
        project_name=project_name,
        campaign_id=campaign_id,
        client=client,
        user_session_id=user_session_id,
        action=action,
        action_value=action_value,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    user_session_id: str,
    action: UserSessionActionAction,
    action_value: Union[Unset, None, str] = UNSET,
) -> Response[Union[Ack, Any]]:
    """Perform an action on a user session

    Args:
        project_name (str):
        campaign_id (str):
        user_session_id (str):
        action (UserSessionActionAction):
        action_value (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        campaign_id=campaign_id,
        client=client,
        user_session_id=user_session_id,
        action=action,
        action_value=action_value,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    campaign_id: str,
    *,
    client: Client,
    user_session_id: str,
    action: UserSessionActionAction,
    action_value: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Ack, Any]]:
    """Perform an action on a user session

    Args:
        project_name (str):
        campaign_id (str):
        user_session_id (str):
        action (UserSessionActionAction):
        action_value (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Ack, Any]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            campaign_id=campaign_id,
            client=client,
            user_session_id=user_session_id,
            action=action,
            action_value=action_value,
        )
    ).parsed
