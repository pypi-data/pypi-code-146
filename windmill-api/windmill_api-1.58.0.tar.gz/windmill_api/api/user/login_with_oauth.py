from typing import Any, Dict

import httpx

from ...client import Client
from ...models.login_with_oauth_json_body import LoginWithOauthJsonBody
from ...types import Response


def _get_kwargs(
    client_name: str,
    *,
    client: Client,
    json_body: LoginWithOauthJsonBody,
) -> Dict[str, Any]:
    url = "{}/oauth/login_callback/{client_name}".format(client.base_url, client_name=client_name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    client_name: str,
    *,
    client: Client,
    json_body: LoginWithOauthJsonBody,
) -> Response[Any]:
    """login with oauth authorization flow

    Args:
        client_name (str):
        json_body (LoginWithOauthJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client_name=client_name,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    client_name: str,
    *,
    client: Client,
    json_body: LoginWithOauthJsonBody,
) -> Response[Any]:
    """login with oauth authorization flow

    Args:
        client_name (str):
        json_body (LoginWithOauthJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client_name=client_name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
