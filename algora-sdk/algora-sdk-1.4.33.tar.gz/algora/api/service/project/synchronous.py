from typing import Dict, Any, List

from algora.api.service.project.__util import (
    _create_project_request_info, _get_project_request_info, _get_projects_request_info, _update_project_request_info,
    _delete_project_request_info, _copy_project_request_info
)
from algora.api.service.project.model import ProjectRequest
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import __put_request, __get_request, __post_request, __delete_request


@data_request(transformers=[no_transform])
def get_project(id: str) -> Dict[str, Any]:
    """
    Get project by ID.

    Returns:
        Dict[str, Any]: Project response
    """
    request_info = _get_project_request_info(id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_projects() -> List[Dict[str, Any]]:
    """
    Get all projects.

    Returns:
        List[Dict[str, Any]]: List of project response
    """
    request_info = _get_projects_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def create_project(request: ProjectRequest) -> Dict[str, Any]:
    """
    Create project.

    Args:
        request (ProjectRequest): Project request

    Returns:
        Dict[str, Any]: Project response
    """
    request_info = _create_project_request_info(request)
    return __put_request(**request_info)


@data_request(transformers=[no_transform])
def update_project(id: str, request: ProjectRequest) -> Dict[str, Any]:
    """
    Update project.

    Args:
        id (str): Project ID
        request (ProjectRequest): Project request

    Returns:
        Dict[str, Any]: Project response
    """
    request_info = _update_project_request_info(id, request)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def copy_project(id: str) -> Dict[str, Any]:
    """
    Copy project.

    Args:
        id (str): Project ID

    Returns:
        Dict[str, Any]: Project response
    """
    request_info = _copy_project_request_info(id)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def delete_project(id: str) -> None:
    """
    Delete project by ID.

    Args:
        id (str): Project ID

    Returns:
        None
    """
    request_info = _delete_project_request_info(id)
    return __delete_request(**request_info)
