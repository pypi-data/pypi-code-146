from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.get_public_app_by_secret_response_200 import GetPublicAppBySecretResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/apps_u/public_app/{path}".format(client.base_url, workspace=workspace, path=path)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[GetPublicAppBySecretResponse200]:
    if response.status_code == 200:
        response_200 = GetPublicAppBySecretResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GetPublicAppBySecretResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    workspace: str,
    path: str,
    *,
    client: Client,
) -> Response[GetPublicAppBySecretResponse200]:
    """get public app by secret

    Args:
        workspace (str):
        path (str):

    Returns:
        Response[GetPublicAppBySecretResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    workspace: str,
    path: str,
    *,
    client: Client,
) -> Optional[GetPublicAppBySecretResponse200]:
    """get public app by secret

    Args:
        workspace (str):
        path (str):

    Returns:
        Response[GetPublicAppBySecretResponse200]
    """

    return sync_detailed(
        workspace=workspace,
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Client,
) -> Response[GetPublicAppBySecretResponse200]:
    """get public app by secret

    Args:
        workspace (str):
        path (str):

    Returns:
        Response[GetPublicAppBySecretResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    workspace: str,
    path: str,
    *,
    client: Client,
) -> Optional[GetPublicAppBySecretResponse200]:
    """get public app by secret

    Args:
        workspace (str):
        path (str):

    Returns:
        Response[GetPublicAppBySecretResponse200]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            path=path,
            client=client,
        )
    ).parsed
