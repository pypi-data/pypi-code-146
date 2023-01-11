from typing import Any


def _upload_resource_request_info(path: str, files: Any) -> dict:
    return {
        'endpoint': f"config/resource?path={path}",
        'files':  [('files', file) for file in files]
    }


def _delete_resource_request_info(path: str) -> dict:
    return {
        'endpoint': f"config/resource?path={path}",
    }
