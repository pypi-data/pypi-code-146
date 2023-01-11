from typing import Dict, Any, List, Optional

from algora.api.service.project.package.__util import (
    _create_project_package_request_info, _get_project_package_request_info, _get_project_packages_request_info,
    _update_project_package_request_info, _delete_project_package_request_info, _search_project_packages_request_info
)
from algora.api.service.project.package.model import ProjectPackageRequest
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import __put_request, __get_request, __post_request, __delete_request


@data_request(transformers=[no_transform])
def get_project_package(id: str) -> Dict[str, Any]:
    """
    Get project package by ID.

    Args:
        id (str): Project package ID

    Returns:
        Dict[str, Any]: Project package response
    """
    request_info = _get_project_package_request_info(id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_project_packages() -> List[Dict[str, Any]]:
    """
    Get all project packages.

    Returns:
        List[Dict[str, Any]]: List of project package response
    """
    request_info = _get_project_packages_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def search_project_packages(
        name: Optional[str] = None,
        version: Optional[str] = None,
        tag: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get all project packages.

    Parameters:
        name: Optional name parameter to filter the results by
        version: Optional version parameter to filter the results by
        tag: Optional tag parameter to filter the results by

    Returns:
        List[Dict[str, Any]]: List of project package response
    """
    request_info = _search_project_packages_request_info(name, version, tag)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def create_project_package(request: ProjectPackageRequest) -> Dict[str, Any]:
    """
    Create project package.

    Args:
        request (ProjectPackageRequest): Project package request

    Returns:
        Dict[str, Any]: Project package response
    """
    request_info = _create_project_package_request_info(request)
    return __put_request(**request_info)


@data_request(transformers=[no_transform])
def update_project_package(id: str, request: ProjectPackageRequest) -> Dict[str, Any]:
    """
    Update project package.

    Args:
        id (str): Project package ID
        request (ProjectPackageRequest): Project package request

    Returns:
        Dict[str, Any]: Project package response
    """
    request_info = _update_project_package_request_info(id, request)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def delete_project_package(id: str) -> None:
    """
    Delete project package by ID.

    Args:
        id (str): Project package ID

    Returns:
        None
    """
    request_info = _delete_project_package_request_info(id)
    return __delete_request(**request_info)
