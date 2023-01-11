from typing import Dict, List


from algora.api.service.resource.__util import _upload_resource_request_info, _delete_resource_request_info
from algora.common.decorators import async_data_request
from algora.common.function import no_transform
from algora.common.requests import __async_put_request, __async_delete_request


@async_data_request(
    transformers=[no_transform],
    processor=lambda response: response.status_code
)
async def async_upload_resources(path: str, file_locations: List[str]) -> None:
    """
    Asynchronously uploads the files.

    Args:
        path (str): Path where data is uploaded to
        file_locations (List[str]): List of paths to the file being uploaded

    Returns:
        Dict[str, Any]: Project package response
    """
    # aiofiles doesnt work atm so we are using the blocking open
    files = [open(location, 'rb') for location in file_locations]
    request_info = _upload_resource_request_info(path, files)
    response = await __async_put_request(**request_info)
    [file.close() for file in files]
    return response


@async_data_request(
    transformers=[no_transform],
    processor=lambda response: response.status_code
)
async def async_delete_resource(path: str) -> None:
    """
    Asynchronously deletes the wheel file for the project package.

    Args:
        path (str): Path where data is uploaded to

    Returns:
        Dict[str, Any]: Project package response
    """
    request_info = _delete_resource_request_info(path)
    return await __async_delete_request(**request_info)
