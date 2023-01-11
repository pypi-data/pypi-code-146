from typing import Optional, List, Union
from datetime import datetime

import requests

from .. import _credentials
from .. import utils

__all__ = [
    "get_batch_types",
    "get_batch_type_details",
    "get_batches",
    "update_batch_value",
    "update_batch_feature_value",
    "update_batch_features_and_values",
    "update_vector_batch_values",
]


def get_batch_types(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/batch-types"
    response = requests.get(
        url=url,
        params={"page": page, "size": page_size,},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def get_batch_type_details(
    batch_type_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/batch-types/{batch_type_id}"
    response = requests.get(url=url, **api_credentials.auth_kwargs)

    # Output
    response.raise_for_status()
    return response.json()


def get_batches(
    batch_type_id: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    name: Optional[str] = None,
    features_value_ids: Optional[Union[str, List[str]]] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Format dates
    start_date_iso = utils.get_zulu_isoformat(start_date)
    end_date_iso = utils.get_zulu_isoformat(end_date)

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/batch-types/{batch_type_id}/batches"
    response = requests.get(
        url=url,
        params={
            "start": start_date_iso,
            "end": end_date_iso,
            "name": name,
            "feature-values": utils.join_list_query_param(features_value_ids),
            "page": page,
            "size": page_size,
        },
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def update_batch_value(
    batch_type_id: str,
    batch_id: str,
    data_id: str,
    value: Union[int, float],
    unit_id: Optional[str] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/batch-types/{batch_type_id}/batches/{batch_id}/value"
    response = requests.put(
        url=url,
        json={"dataId": data_id, "value": value, "unitId": unit_id,},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.status_code


def update_batch_feature_value(
    batch_type_id: str,
    batch_id: str,
    feature_id: str,
    value: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/batch-types/{batch_type_id}/batches/{batch_id}/feature"
    response = requests.put(
        url=url,
        json={"batchTagKeyId": feature_id, "batchTagValueValue": value,},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.status_code


def update_batch_features_and_values(
    batch_type_id: str,
    data: List[dict],
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):

    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/batch-types/{batch_type_id}/batches/features-and-values"
    response = requests.put(url=url, json=data, **api_credentials.auth_kwargs,)

    # Output
    response.raise_for_status()
    return response.status_code


def update_vector_batch_values(
    data: List[dict],
    use_external_reference: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/value-upload/vector-batch-values"
    response = requests.post(
        url=url,
        json=data,
        params={"use-external-reference": use_external_reference},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()
