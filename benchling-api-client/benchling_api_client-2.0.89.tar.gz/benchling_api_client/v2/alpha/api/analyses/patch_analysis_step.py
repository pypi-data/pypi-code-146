from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...extensions import UnknownType
from ...models.analysis_step import AnalysisStep
from ...models.analysis_step_update_with_message import AnalysisStepUpdateWithMessage
from ...models.analysis_step_update_without_message import AnalysisStepUpdateWithoutMessage
from ...models.bad_request_error import BadRequestError
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    analysis_step_id: str,
    json_body: Union[AnalysisStepUpdateWithoutMessage, AnalysisStepUpdateWithMessage, UnknownType],
) -> Dict[str, Any]:
    url = "{}/analysis-steps/{analysis_step_id}".format(client.base_url, analysis_step_id=analysis_step_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    if isinstance(json_body, UnknownType):
        json_json_body = json_body.value
    elif isinstance(json_body, AnalysisStepUpdateWithoutMessage):
        json_json_body = json_body.to_dict()

    else:
        json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AnalysisStep, BadRequestError, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = AnalysisStep.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AnalysisStep, BadRequestError, ForbiddenError, NotFoundError]]:
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
    json_body: Union[AnalysisStepUpdateWithoutMessage, AnalysisStepUpdateWithMessage, UnknownType],
) -> Response[Union[AnalysisStep, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        analysis_step_id=analysis_step_id,
        json_body=json_body,
    )

    response = client.httpx_client.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    analysis_step_id: str,
    json_body: Union[AnalysisStepUpdateWithoutMessage, AnalysisStepUpdateWithMessage, UnknownType],
) -> Optional[Union[AnalysisStep, BadRequestError, ForbiddenError, NotFoundError]]:
    """ Update an analysis step. Call this endpoint to mark the step as `SUCCEEDED` or `FAILED`. """

    return sync_detailed(
        client=client,
        analysis_step_id=analysis_step_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    analysis_step_id: str,
    json_body: Union[AnalysisStepUpdateWithoutMessage, AnalysisStepUpdateWithMessage, UnknownType],
) -> Response[Union[AnalysisStep, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        analysis_step_id=analysis_step_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    analysis_step_id: str,
    json_body: Union[AnalysisStepUpdateWithoutMessage, AnalysisStepUpdateWithMessage, UnknownType],
) -> Optional[Union[AnalysisStep, BadRequestError, ForbiddenError, NotFoundError]]:
    """ Update an analysis step. Call this endpoint to mark the step as `SUCCEEDED` or `FAILED`. """

    return (
        await asyncio_detailed(
            client=client,
            analysis_step_id=analysis_step_id,
            json_body=json_body,
        )
    ).parsed
