from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.get_resume_urls_response_200 import GetResumeUrlsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    id: str,
    resume_id: int,
    *,
    client: Client,
    approver: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/jobs/resume_urls/{id}/{resume_id}".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[GetResumeUrlsResponse200]:
    if response.status_code == 200:
        response_200 = GetResumeUrlsResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GetResumeUrlsResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    workspace: str,
    id: str,
    resume_id: int,
    *,
    client: Client,
    approver: Union[Unset, None, str] = UNSET,
) -> Response[GetResumeUrlsResponse200]:
    """get resume urls given a job_id, resume_id and a nonce to resume a flow

    Args:
        workspace (str):
        id (str):
        resume_id (int):
        approver (Union[Unset, None, str]):

    Returns:
        Response[GetResumeUrlsResponse200]
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


def sync(
    workspace: str,
    id: str,
    resume_id: int,
    *,
    client: Client,
    approver: Union[Unset, None, str] = UNSET,
) -> Optional[GetResumeUrlsResponse200]:
    """get resume urls given a job_id, resume_id and a nonce to resume a flow

    Args:
        workspace (str):
        id (str):
        resume_id (int):
        approver (Union[Unset, None, str]):

    Returns:
        Response[GetResumeUrlsResponse200]
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        resume_id=resume_id,
        client=client,
        approver=approver,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    resume_id: int,
    *,
    client: Client,
    approver: Union[Unset, None, str] = UNSET,
) -> Response[GetResumeUrlsResponse200]:
    """get resume urls given a job_id, resume_id and a nonce to resume a flow

    Args:
        workspace (str):
        id (str):
        resume_id (int):
        approver (Union[Unset, None, str]):

    Returns:
        Response[GetResumeUrlsResponse200]
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


async def asyncio(
    workspace: str,
    id: str,
    resume_id: int,
    *,
    client: Client,
    approver: Union[Unset, None, str] = UNSET,
) -> Optional[GetResumeUrlsResponse200]:
    """get resume urls given a job_id, resume_id and a nonce to resume a flow

    Args:
        workspace (str):
        id (str):
        resume_id (int):
        approver (Union[Unset, None, str]):

    Returns:
        Response[GetResumeUrlsResponse200]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            resume_id=resume_id,
            client=client,
            approver=approver,
        )
    ).parsed
