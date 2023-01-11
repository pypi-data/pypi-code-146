from typing import Any, Optional

from algora.api.service.project.package.model import ProjectPackageRequest


def _get_project_package_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/project/package/{id}"
    }


def _get_project_packages_request_info() -> dict:
    return {
        'endpoint': f"config/project/package",
    }


def _search_project_packages_request_info(
        name: Optional[str] = None,
        version: Optional[str] = None,
        tag: Optional[str] = None
) -> dict:
    params = {
        'name': name,
        'version': version,
        'tag': tag
    }
    return {
        'endpoint': f"config/project/package/search",
        'params': {k: v for k, v in params.items() if v}
    }


def _create_project_package_request_info(request: ProjectPackageRequest) -> dict:
    return {
        'endpoint': f"config/project/package",
        'json': request.request_dict()
    }


def _update_project_package_request_info(id: str, request: ProjectPackageRequest) -> dict:
    return {
        'endpoint': f"config/project/package/{id}",
        'json': request.request_dict()
    }


def _delete_project_package_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/project/package/{id}"
    }
