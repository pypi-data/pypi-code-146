from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...extensions import UnknownType
from ...models.analysis_dataset_ids import AnalysisDatasetIds
from ...models.analysis_step_dataset_data import AnalysisStepDatasetData
from ...models.analysis_step_file_data import AnalysisStepFileData
from ...models.bad_request_error import BadRequestError
from ...models.file_ids import FileIds
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    analysis_step_data_id: str,
    json_body: Union[FileIds, AnalysisDatasetIds, UnknownType],
) -> Dict[str, Any]:
    url = "{}/analysis-step-data/{analysis_step_data_id}".format(
        client.base_url, analysis_step_data_id=analysis_step_data_id
    )

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    if isinstance(json_body, UnknownType):
        json_json_body = json_body.value
    elif isinstance(json_body, FileIds):
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
) -> Optional[
    Union[
        Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType],
        BadRequestError,
        ForbiddenError,
        NotFoundError,
    ]
]:
    if response.status_code == 200:

        def _parse_response_200(
            data: Union[Dict[str, Any]]
        ) -> Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]:
            response_200: Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType]
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                analysis_step_data = AnalysisStepFileData.from_dict(data, strict=True)

                return analysis_step_data
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                analysis_step_data = AnalysisStepDatasetData.from_dict(data, strict=True)

                return analysis_step_data
            except:  # noqa: E722
                pass
            return UnknownType(data)

        response_200 = _parse_response_200(response.json())

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
) -> Response[
    Union[
        Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType],
        BadRequestError,
        ForbiddenError,
        NotFoundError,
    ]
]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    analysis_step_data_id: str,
    json_body: Union[FileIds, AnalysisDatasetIds, UnknownType],
) -> Response[
    Union[
        Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType],
        BadRequestError,
        ForbiddenError,
        NotFoundError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        analysis_step_data_id=analysis_step_data_id,
        json_body=json_body,
    )

    response = client.httpx_client.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    analysis_step_data_id: str,
    json_body: Union[FileIds, AnalysisDatasetIds, UnknownType],
) -> Optional[
    Union[
        Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType],
        BadRequestError,
        ForbiddenError,
        NotFoundError,
    ]
]:
    """Update a piece of data that is associated with a third-party analysis step.

    After uploading one or more files with the [Create a file](#/Analyses/createFile) endpoint, call this
    endpoint to attach those output files to the step.

    This endpoint also similarly supports attaching datasets (`datasetIds`).
    """

    return sync_detailed(
        client=client,
        analysis_step_data_id=analysis_step_data_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    analysis_step_data_id: str,
    json_body: Union[FileIds, AnalysisDatasetIds, UnknownType],
) -> Response[
    Union[
        Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType],
        BadRequestError,
        ForbiddenError,
        NotFoundError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        analysis_step_data_id=analysis_step_data_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    analysis_step_data_id: str,
    json_body: Union[FileIds, AnalysisDatasetIds, UnknownType],
) -> Optional[
    Union[
        Union[AnalysisStepFileData, AnalysisStepDatasetData, UnknownType],
        BadRequestError,
        ForbiddenError,
        NotFoundError,
    ]
]:
    """Update a piece of data that is associated with a third-party analysis step.

    After uploading one or more files with the [Create a file](#/Analyses/createFile) endpoint, call this
    endpoint to attach those output files to the step.

    This endpoint also similarly supports attaching datasets (`datasetIds`).
    """

    return (
        await asyncio_detailed(
            client=client,
            analysis_step_data_id=analysis_step_data_id,
            json_body=json_body,
        )
    ).parsed
