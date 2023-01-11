from algora.api.service.runner.model import RunnerRequest


def _get_runners_request_info() -> dict:
    return {
        'endpoint': f"config/runner"
    }


def _get_runner_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/runner{id}"
    }


def _create_runner_request_info(request: RunnerRequest) -> dict:
    return {
        'endpoint': f"config/runner",
        'json': request.request_dict()
    }


def _update_runner_request_info(id: str, request: RunnerRequest) -> dict:
    return {
        'endpoint': f"config/runner/{id}",
        'json': request.request_dict()
    }


def _delete_runner_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/runner/{id}"
    }
