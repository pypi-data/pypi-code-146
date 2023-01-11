from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.get_hub_script_by_path_response_200 import GetHubScriptByPathResponse200
from ...types import Response


def _get_kwargs(
    path: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/scripts/hub/get_full/{path}".format(client.base_url, path=path)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[GetHubScriptByPathResponse200]:
    if response.status_code == 200:
        response_200 = GetHubScriptByPathResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GetHubScriptByPathResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    path: str,
    *,
    client: Client,
) -> Response[GetHubScriptByPathResponse200]:
    """get full hub script by path

    Args:
        path (str):

    Returns:
        Response[GetHubScriptByPathResponse200]
    """

    kwargs = _get_kwargs(
        path=path,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    path: str,
    *,
    client: Client,
) -> Optional[GetHubScriptByPathResponse200]:
    """get full hub script by path

    Args:
        path (str):

    Returns:
        Response[GetHubScriptByPathResponse200]
    """

    return sync_detailed(
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
) -> Response[GetHubScriptByPathResponse200]:
    """get full hub script by path

    Args:
        path (str):

    Returns:
        Response[GetHubScriptByPathResponse200]
    """

    kwargs = _get_kwargs(
        path=path,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    path: str,
    *,
    client: Client,
) -> Optional[GetHubScriptByPathResponse200]:
    """get full hub script by path

    Args:
        path (str):

    Returns:
        Response[GetHubScriptByPathResponse200]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
        )
    ).parsed
