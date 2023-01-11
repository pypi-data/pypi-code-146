from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.analysis_step import AnalysisStep
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    analysis_step_id: str,
) -> Dict[str, Any]:
    url = "{}/analysis-steps/{analysis_step_id}".format(client.base_url, analysis_step_id=analysis_step_id)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AnalysisStep, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = AnalysisStep.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AnalysisStep, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    analysis_step_id: str,
) -> Response[Union[AnalysisStep, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        analysis_step_id=analysis_step_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    analysis_step_id: str,
) -> Optional[Union[AnalysisStep, ForbiddenError, NotFoundError]]:
    """Get an analysis step, which represents a concrete unit of work being executed in an analysis. It
    tracks its execution status, the input data it received, and the output data it generated.

    Call this endpoint so you can get the IDs of the *input* data and download them with their
    corresponding endpoint, like [Get a dataset](#/Analyses/getDataset).

    Or call this endpoint so you can get the IDs of the *output* data, upload files with the
    [Create a file](#/Analyses/createFile) endpoint, and attach them to the step with the
    [Update analysis step data](#/Analyses/patchAnalysisStepData) endpoint.
    """

    return sync_detailed(
        client=client,
        analysis_step_id=analysis_step_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    analysis_step_id: str,
) -> Response[Union[AnalysisStep, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        analysis_step_id=analysis_step_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    analysis_step_id: str,
) -> Optional[Union[AnalysisStep, ForbiddenError, NotFoundError]]:
    """Get an analysis step, which represents a concrete unit of work being executed in an analysis. It
    tracks its execution status, the input data it received, and the output data it generated.

    Call this endpoint so you can get the IDs of the *input* data and download them with their
    corresponding endpoint, like [Get a dataset](#/Analyses/getDataset).

    Or call this endpoint so you can get the IDs of the *output* data, upload files with the
    [Create a file](#/Analyses/createFile) endpoint, and attach them to the step with the
    [Update analysis step data](#/Analyses/patchAnalysisStepData) endpoint.
    """

    return (
        await asyncio_detailed(
            client=client,
            analysis_step_id=analysis_step_id,
        )
    ).parsed
