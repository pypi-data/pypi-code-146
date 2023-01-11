from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    client: Client,
    only_member_of: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/groups/listnames".format(client.base_url, workspace=workspace)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["only_member_of"] = only_member_of

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == 200:
        response_200 = cast(List[str], response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Client,
    only_member_of: Union[Unset, None, bool] = UNSET,
) -> Response[List[str]]:
    """list group names

    Args:
        workspace (str):
        only_member_of (Union[Unset, None, bool]):

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        only_member_of=only_member_of,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    workspace: str,
    *,
    client: Client,
    only_member_of: Union[Unset, None, bool] = UNSET,
) -> Optional[List[str]]:
    """list group names

    Args:
        workspace (str):
        only_member_of (Union[Unset, None, bool]):

    Returns:
        Response[List[str]]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        only_member_of=only_member_of,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Client,
    only_member_of: Union[Unset, None, bool] = UNSET,
) -> Response[List[str]]:
    """list group names

    Args:
        workspace (str):
        only_member_of (Union[Unset, None, bool]):

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        only_member_of=only_member_of,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    workspace: str,
    *,
    client: Client,
    only_member_of: Union[Unset, None, bool] = UNSET,
) -> Optional[List[str]]:
    """list group names

    Args:
        workspace (str):
        only_member_of (Union[Unset, None, bool]):

    Returns:
        Response[List[str]]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            only_member_of=only_member_of,
        )
    ).parsed
