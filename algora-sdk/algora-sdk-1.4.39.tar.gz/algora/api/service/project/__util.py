from algora.api.service.project.model import ProjectRequest
from algora.common.enum import UpdateRequestAction


def _get_project_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/project/{id}"
    }


def _get_projects_request_info() -> dict:
    return {
        'endpoint': f"config/project"
    }


def _create_project_request_info(request: ProjectRequest) -> dict:
    return {
        'endpoint': f"config/project",
        'json': request.request_dict()
    }


def _update_project_request_info(id: str, request: ProjectRequest) -> dict:
    return {
        'endpoint': f"config/project/{id}?action={UpdateRequestAction.UPDATE}",
        'json': request.request_dict()
    }


def _copy_project_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/project/{id}?action={UpdateRequestAction.COPY}",
    }


def _delete_project_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/project/{id}"
    }
