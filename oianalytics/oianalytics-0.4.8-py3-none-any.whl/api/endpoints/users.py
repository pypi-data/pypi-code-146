from typing import Optional

import requests

from .. import _credentials

__all__ = ["get_users", "get_user_details"]


def get_users(
    page: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/users"
    response = requests.get(
        url=url, params={"page": page}, **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def get_user_details(
    user_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/users/{user_id}"
    response = requests.get(url=url, **api_credentials.auth_kwargs,)

    # Output
    response.raise_for_status()
    return response.json()
