from typing import Any, Dict

import httpx

from ...client import Client
from ...models.add_owner_to_folder_json_body import AddOwnerToFolderJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    name: str,
    *,
    client: Client,
    json_body: AddOwnerToFolderJsonBody,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/folders/addowner/{name}".format(client.base_url, workspace=workspace, name=name)

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
    workspace: str,
    name: str,
    *,
    client: Client,
    json_body: AddOwnerToFolderJsonBody,
) -> Response[Any]:
    """add owner to folder

    Args:
        workspace (str):
        name (str):
        json_body (AddOwnerToFolderJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        name=name,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    workspace: str,
    name: str,
    *,
    client: Client,
    json_body: AddOwnerToFolderJsonBody,
) -> Response[Any]:
    """add owner to folder

    Args:
        workspace (str):
        name (str):
        json_body (AddOwnerToFolderJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        name=name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
