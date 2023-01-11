import pandas as pd
from requests import Response

from algora.api.data.query.__util import _query_datasets_request_info, _query_dataset_csv_request_info, \
    _query_timeseries_request_info
from algora.api.data.query.model import TimeseriesQueryRequest
from algora.common.decorators import data_request
from algora.common.function import data_required_transform
from algora.common.requests import __post_request, __get_request


def query_dataset(id: str, data=None, json=None) -> Response:
    """
    Query dataset by ID.

    Args:
        id (str): Dataset ID
        data (Any): Data to POST
        json (Any): Data to POST

    Returns:
        Response: HTTP response object
    """
    request_info = _query_datasets_request_info(id, data, json)
    return __post_request(**request_info)


def query_dataset_csv(id: str, data=None) -> Response:
    """
    Query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        data (Any): Data to POST

    Returns:
        Response: HTTP response object
    """
    request_info = _query_dataset_csv_request_info(id, data)
    return __get_request(**request_info)


@data_request(transformers=[data_required_transform])
def query_timeseries(request: TimeseriesQueryRequest) -> pd.DataFrame:
    """
    Query timeseries dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    request_info = _query_timeseries_request_info(request)
    return __post_request(**request_info)
