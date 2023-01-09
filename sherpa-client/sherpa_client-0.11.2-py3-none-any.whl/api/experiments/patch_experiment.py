from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.experiment import Experiment
from ...models.experiment_patch import ExperimentPatch
from ...types import Response


def _get_kwargs(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: ExperimentPatch,
) -> Dict[str, Any]:
    url = "{}/projects/{projectName}/experiments/{name}".format(client.base_url, projectName=project_name, name=name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, Experiment]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Experiment.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Experiment]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: ExperimentPatch,
) -> Response[Union[Any, Experiment]]:
    """Partially update an experiment

    Args:
        project_name (str):
        name (str):
        json_body (ExperimentPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Experiment]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: ExperimentPatch,
) -> Optional[Union[Any, Experiment]]:
    """Partially update an experiment

    Args:
        project_name (str):
        name (str):
        json_body (ExperimentPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Experiment]]
    """

    return sync_detailed(
        project_name=project_name,
        name=name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: ExperimentPatch,
) -> Response[Union[Any, Experiment]]:
    """Partially update an experiment

    Args:
        project_name (str):
        name (str):
        json_body (ExperimentPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Experiment]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        name=name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_name: str,
    name: str,
    *,
    client: Client,
    json_body: ExperimentPatch,
) -> Optional[Union[Any, Experiment]]:
    """Partially update an experiment

    Args:
        project_name (str):
        name (str):
        json_body (ExperimentPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Experiment]]
    """

    return (
        await asyncio_detailed(
            project_name=project_name,
            name=name,
            client=client,
            json_body=json_body,
        )
    ).parsed
