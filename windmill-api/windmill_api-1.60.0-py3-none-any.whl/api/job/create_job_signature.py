from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    id: str,
    resume_id: int,
    *,
    client: Client,
    approver: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/jobs/job_signature/{id}/{resume_id}".format(
        client.base_url, workspace=workspace, id=id, resume_id=resume_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["approver"] = approver

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    id: str,
    resume_id: int,
    *,
    client: Client,
    approver: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """create an HMac signature given a job id and a resume id

    Args:
        workspace (str):
        id (str):
        resume_id (int):
        approver (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        resume_id=resume_id,
        client=client,
        approver=approver,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    workspace: str,
    id: str,
    resume_id: int,
    *,
    client: Client,
    approver: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """create an HMac signature given a job id and a resume id

    Args:
        workspace (str):
        id (str):
        resume_id (int):
        approver (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        resume_id=resume_id,
        client=client,
        approver=approver,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
