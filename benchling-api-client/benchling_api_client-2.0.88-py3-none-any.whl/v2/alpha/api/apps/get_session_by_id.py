from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.not_found_error import NotFoundError
from ...models.session import Session
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    id: str,
) -> Dict[str, Any]:
    url = "{}/sessions/{id}".format(client.base_url, id=id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Session, NotFoundError]]:
    if response.status_code == 200:
        response_200 = Session.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Session, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    id: str,
) -> Response[Union[Session, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    id: str,
) -> Optional[Union[Session, NotFoundError]]:
    """ Get a session """

    return sync_detailed(
        client=client,
        id=id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: str,
) -> Response[Union[Session, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    id: str,
) -> Optional[Union[Session, NotFoundError]]:
    """ Get a session """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
        )
    ).parsed
