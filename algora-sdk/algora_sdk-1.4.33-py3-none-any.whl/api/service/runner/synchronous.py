from typing import Dict, Any, List

from algora.api.service.runner.__util import (
    _create_runner_request_info, _get_runner_request_info, _get_runners_request_info, _update_runner_request_info,
    _delete_runner_request_info
)
from algora.api.service.runner.model import RunnerRequest
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import __put_request, __get_request, __post_request, __delete_request


@data_request(transformers=[no_transform])
def get_runner(id: str) -> Dict[str, Any]:
    """
    Get runner by ID.

    Returns:
        Dict[str, Any]: Runner response
    """
    request_info = _get_runner_request_info(id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_runners() -> List[Dict[str, Any]]:
    """
    Get all runners.

    Returns:
        List[Dict[str, Any]]: List of runner response
    """
    request_info = _get_runners_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def create_runner(request: RunnerRequest) -> Dict[str, Any]:
    """
    Get or create runner.

    Returns:
        Dict[str, Any]: Runner response
    """
    request_info = _create_runner_request_info(request)
    return __put_request(**request_info)


@data_request(transformers=[no_transform])
def update_runner(id: str, request: RunnerRequest) -> Dict[str, Any]:
    """
    Update runner.

    Args:
        id (str): Runner ID
        request (RunnerRequest): Runner request

    Returns:
        Dict[str, Any]: Runner response
    """
    request_info = _update_runner_request_info(id, request)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def delete_runner(id: str) -> None:
    """
    Delete Runner by ID.

    Args:
        id (str): Runner ID

    Returns:
        None
    """
    request_info = _delete_runner_request_info(id)
    return __delete_request(**request_info)
