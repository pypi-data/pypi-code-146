from typing import Dict, Any, List, Optional

from algora.api.service.project.package.__util import (
    _create_project_package_request_info, _get_project_package_request_info, _get_project_packages_request_info,
    _update_project_package_request_info, _delete_project_package_request_info, _search_project_packages_request_info
)
from algora.api.service.project.package.model import ProjectPackageRequest
from algora.common.decorators import async_data_request
from algora.common.function import no_transform
from algora.common.requests import (
    __async_put_request, __async_get_request, __async_post_request, __async_delete_request
)


@async_data_request(transformers=[no_transform])
async def async_get_project_package(id: str) -> Dict[str, Any]:
    """
    Asynchronously get project package by ID.
    
    Args:
        id (str): Project package ID

    Returns:
        Dict[str, Any]: Project package response
    """
    request_info = _get_project_package_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_project_packages() -> List[Dict[str, Any]]:
    """
    Asynchronously get all project packages.

    Returns:
        List[Dict[str, Any]]: List of project package response
    """
    request_info = _get_project_packages_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_search_project_packages(
        name: Optional[str] = None,
        version: Optional[str] = None,
        tag: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Asynchronously get all project packages.

    Parameters:
        name: Optional name parameter to filter the results by
        version: Optional version parameter to filter the results by
        tag: Optional tag parameter to filter the results by

    Returns:
        List[Dict[str, Any]]: List of project package response
    """
    request_info = _search_project_packages_request_info(name, version, tag)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_create_project_package(request: ProjectPackageRequest) -> Dict[str, Any]:
    """
    Asynchronously create project package.

    Args:
        request (ProjectPackageRequest): Project package request

    Returns:
        Dict[str, Any]: Project package response
    """
    request_info = _create_project_package_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_update_project_package(id: str, request: ProjectPackageRequest) -> Dict[str, Any]:
    """
    Asynchronously update project package.

    Args:
        id (str): Project package ID
        request (ProjectPackageRequest): Project package request

    Returns:
        Dict[str, Any]: Project package response
    """
    request_info = _update_project_package_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_delete_project_package(id: str) -> None:
    """
    Asynchronously delete project package by ID.

    Args:
        id (str): Project package ID

    Returns:
        None
    """
    request_info = _delete_project_package_request_info(id)
    return await __async_delete_request(**request_info)
