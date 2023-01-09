from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.run_flow_preview_json_body import RunFlowPreviewJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    client: Client,
    json_body: RunFlowPreviewJsonBody,
    include_header: Union[Unset, None, str] = UNSET,
    invisible_to_owner: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/jobs/run/preview_flow".format(client.base_url, workspace=workspace)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["include_header"] = include_header

    params["invisible_to_owner"] = invisible_to_owner

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


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    workspace: str,
    *,
    client: Client,
    json_body: RunFlowPreviewJsonBody,
    include_header: Union[Unset, None, str] = UNSET,
    invisible_to_owner: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """run flow preview

    Args:
        workspace (str):
        include_header (Union[Unset, None, str]):
        invisible_to_owner (Union[Unset, None, bool]):
        json_body (RunFlowPreviewJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        json_body=json_body,
        include_header=include_header,
        invisible_to_owner=invisible_to_owner,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    workspace: str,
    *,
    client: Client,
    json_body: RunFlowPreviewJsonBody,
    include_header: Union[Unset, None, str] = UNSET,
    invisible_to_owner: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """run flow preview

    Args:
        workspace (str):
        include_header (Union[Unset, None, str]):
        invisible_to_owner (Union[Unset, None, bool]):
        json_body (RunFlowPreviewJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        json_body=json_body,
        include_header=include_header,
        invisible_to_owner=invisible_to_owner,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
