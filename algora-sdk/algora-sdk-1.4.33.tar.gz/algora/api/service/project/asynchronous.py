from typing import Dict, Any, List

from algora.api.service.project.__util import (
    _create_project_request_info, _get_project_request_info, _get_projects_request_info, _update_project_request_info,
    _delete_project_request_info, _copy_project_request_info
)
from algora.api.service.project.model import ProjectRequest
from algora.common.decorators import async_data_request
from algora.common.function import no_transform
from algora.common.requests import (
    __async_put_request, __async_get_request, __async_post_request, __async_delete_request
)


@async_data_request(transformers=[no_transform])
async def async_get_project(id: str) -> Dict[str, Any]:
    """
    Asynchronously get project by ID.
    
    Args:
        id (str): Project ID

    Returns:
        Dict[str, Any]: Project response
    """
    request_info = _get_project_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_projects() -> List[Dict[str, Any]]:
    """
    Asynchronously get all projects.

    Returns:
        List[Dict[str, Any]]: List of project response
    """
    request_info = _get_projects_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_create_project(request: ProjectRequest) -> Dict[str, Any]:
    """
    Asynchronously create project.

    Args:
        request (ProjectRequest): Project request

    Returns:
        Dict[str, Any]: Project response
    """
    request_info = _create_project_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_update_project(id: str, request: ProjectRequest) -> Dict[str, Any]:
    """
    Asynchronously update project.

    Args:
        id (str): Project ID
        request (ProjectRequest): Project request

    Returns:
        Dict[str, Any]: Project response
    """
    request_info = _update_project_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_copy_project(id: str) -> Dict[str, Any]:
    """
    Asynchronously update project.

    Args:
        id (str): Project ID

    Returns:
        Dict[str, Any]: Project response
    """
    request_info = _copy_project_request_info(id)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_delete_project(id: str) -> None:
    """
    Asynchronously delete project by ID.

    Args:
        id (str): Project ID

    Returns:
        None
    """
    request_info = _delete_project_request_info(id)
    return await __async_delete_request(**request_info)
