from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.resume_suspended_job_post_json_body import ResumeSuspendedJobPostJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    id: str,
    resume_id: int,
    signature: str,
    *,
    client: Client,
    json_body: ResumeSuspendedJobPostJsonBody,
    approver: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/jobs/resume/{id}/{resume_id}/{signature}".format(
        client.base_url, workspace=workspace, id=id, resume_id=resume_id, signature=signature
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["approver"] = approver

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
    id: str,
    resume_id: int,
    signature: str,
    *,
    client: Client,
    json_body: ResumeSuspendedJobPostJsonBody,
    approver: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """resume a job for a suspended flow

    Args:
        workspace (str):
        id (str):
        resume_id (int):
        signature (str):
        approver (Union[Unset, None, str]):
        json_body (ResumeSuspendedJobPostJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        resume_id=resume_id,
        signature=signature,
        client=client,
        json_body=json_body,
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
    signature: str,
    *,
    client: Client,
    json_body: ResumeSuspendedJobPostJsonBody,
    approver: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """resume a job for a suspended flow

    Args:
        workspace (str):
        id (str):
        resume_id (int):
        signature (str):
        approver (Union[Unset, None, str]):
        json_body (ResumeSuspendedJobPostJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        resume_id=resume_id,
        signature=signature,
        client=client,
        json_body=json_body,
        approver=approver,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
