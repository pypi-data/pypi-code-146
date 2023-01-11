from typing import Optional, Union, List
from datetime import datetime

import requests

from .. import _credentials
from .. import utils

__all__ = ["get_event_types", "get_event_type_details", "get_events"]


def get_event_types(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/event-types"
    response = requests.get(
        url=url,
        params={"page": page, "size": page_size,},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def get_event_type_details(
    event_type_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}"
    response = requests.get(url=url, **api_credentials.auth_kwargs)

    # Output
    response.raise_for_status()
    return response.json()


def get_events(
    event_type_id: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    description: Optional[str] = None,
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
    url = (
        f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}/events"
    )
    response = requests.get(
        url=url,
        params={
            "start": start_date_iso,
            "end": end_date_iso,
            "description": description,
            "feature-values": features_value_ids,
            "page": page,
            "size": page_size,
        },
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()
