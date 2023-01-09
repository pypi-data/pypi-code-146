from typing import Dict, Any, List

from algora.api.service.runner.__util import (
    _create_runner_request_info, _get_runner_request_info, _get_runners_request_info, _update_runner_request_info,
    _delete_runner_request_info
)
from algora.api.service.runner.model import RunnerRequest
from algora.common.function import no_transform
from algora.common.decorators import async_data_request
from algora.common.requests import (
    __async_put_request, __async_get_request, __async_post_request, __async_delete_request
)


@async_data_request(transformers=[no_transform])
async def async_get_runner(id: str) -> Dict[str, Any]:
    """
    Asynchronously get runner by ID.

    Args:
        id (str): Runner ID

    Returns:
        Dict[str, Any]: Runner response
    """
    request_info = _get_runner_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_runners() -> List[Dict[str, Any]]:
    """
    Asynchronously get all runners.

    Returns:
        List[Dict[str, Any]]: List of Runner response
    """
    request_info = _get_runners_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_create_runner(request: RunnerRequest) -> Dict[str, Any]:
    """
    Asynchronously get or create runner.

    Returns:
        Dict[str, Any]: Runner response
    """
    request_info = _create_runner_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_update_runner(id: str, request: RunnerRequest) -> Dict[str, Any]:
    """
    Asynchronously update runner.

    Args:
        id (str): Runner ID
        request (RunnerRequest): Runner request

    Returns:
        Dict[str, Any]: Runner response
    """
    request_info = _update_runner_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_delete_runner(id: str) -> None:
    """
    Asynchronously delete runner by ID.

    Args:
        id (str): Runner ID

    Returns:
        None
    """
    request_info = _delete_runner_request_info(id)
    return await __async_delete_request(**request_info)

