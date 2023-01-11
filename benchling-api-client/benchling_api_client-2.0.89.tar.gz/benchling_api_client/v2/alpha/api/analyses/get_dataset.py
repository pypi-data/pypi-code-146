from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.dataset import Dataset
from ...models.forbidden_error import ForbiddenError
from ...models.get_dataset_content_format import GetDatasetContentFormat
from ...models.not_found_error import NotFoundError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    dataset_id: str,
    content_format: Union[Unset, GetDatasetContentFormat] = UNSET,
) -> Dict[str, Any]:
    url = "{}/datasets/{dataset_id}".format(client.base_url, dataset_id=dataset_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_content_format: Union[Unset, int] = UNSET
    if not isinstance(content_format, Unset):
        json_content_format = content_format.value

    params: Dict[str, Any] = {}
    if not isinstance(json_content_format, Unset) and json_content_format is not None:
        params["contentFormat"] = json_content_format

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = Dataset.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    dataset_id: str,
    content_format: Union[Unset, GetDatasetContentFormat] = UNSET,
) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dataset_id=dataset_id,
        content_format=content_format,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    dataset_id: str,
    content_format: Union[Unset, GetDatasetContentFormat] = UNSET,
) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    """Get a dataset, which is a tabular data construct that stores typed columns and rows of data. Call this endpoint to download the data.
    If the Dataset has `SUCCEEDED` status, the response will contain a `Content-Location` header with a URL to download the Dataset in the requested `contentFormat`. If the Dataset has `FAILED_VALIDATION` or `IN_PROGRESS ` status, the `Content-Location` header will always be empty.
    """

    return sync_detailed(
        client=client,
        dataset_id=dataset_id,
        content_format=content_format,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    dataset_id: str,
    content_format: Union[Unset, GetDatasetContentFormat] = UNSET,
) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dataset_id=dataset_id,
        content_format=content_format,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    dataset_id: str,
    content_format: Union[Unset, GetDatasetContentFormat] = UNSET,
) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    """Get a dataset, which is a tabular data construct that stores typed columns and rows of data. Call this endpoint to download the data.
    If the Dataset has `SUCCEEDED` status, the response will contain a `Content-Location` header with a URL to download the Dataset in the requested `contentFormat`. If the Dataset has `FAILED_VALIDATION` or `IN_PROGRESS ` status, the `Content-Location` header will always be empty.
    """

    return (
        await asyncio_detailed(
            client=client,
            dataset_id=dataset_id,
            content_format=content_format,
        )
    ).parsed
