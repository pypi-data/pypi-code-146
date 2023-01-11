from typing import Dict, Any, List

from algora.api.service.resource.__util import _upload_resource_request_info, _delete_resource_request_info
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import __put_request, __delete_request


@data_request(
    transformers=[no_transform],
    processor=lambda response: response.status_code
)
def upload_resources(path: str, file_locations: List[str]) -> Dict[str, Any]:
    """
    Uploads the resources.

    Args:
        path (str): Path where data is uploaded to
        file_locations (List[str]): List of paths to the file being uploaded

    Returns:
        Dict[str, Any]: Project package response
    """
    files = [open(location, 'rb') for location in file_locations]
    request_info = _upload_resource_request_info(path, files)
    response = __put_request(**request_info)
    [file.close() for file in files]
    return response


@data_request(
    transformers=[no_transform],
    processor=lambda response: response.status_code
)
def delete_resource(path: str) -> Dict[str, Any]:
    """
    Deletes the wheel file for the project package.

    Args:
        path (str): Path where data is uploaded to

    Returns:
        Dict[str, Any]: Project package response
    """
    request_info = _delete_resource_request_info(path)
    return __delete_request(**request_info)
