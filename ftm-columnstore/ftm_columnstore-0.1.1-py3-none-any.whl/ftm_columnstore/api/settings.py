from os import environ as env
from typing import Any, Dict, List, Optional

from normality import stringify


def env_str(name: str, default: Optional[str] = None) -> Optional[str]:
    """Ensure the env returns a string even on Windows (#100)."""
    value = stringify(env.get(name))
    return default if value is None else value


VERSION = "0.0.1"
AUTHOR = "Simon Wörpel"
HOME_PAGE = "https://followthemoney.store"
EMAIL = "simon.woerpel@gmail.com"
CONTACT = {"name": AUTHOR, "url": HOME_PAGE, "email": EMAIL}
DOMAIN = "https://followthemoney.store"

TITLE = env_str("API_TITLE") or "followthemoney.store API"
DESCRIPTION = """
The yente API provides endpoints that help you determine if any of the people or
companies mentioned in your data are subject to international sanctions, known
to be involved in criminal activity, or if they are politically exposed people.

`yente` is the open source basis for the OpenSanctions SaaS API. Its matching
and entity retrieval functionality is identical to the hosted API, but it does
not include functionality for metered accounting of API requests.

In this service, there is support for the following operations:

* A simple text-based search for interactive applications (``/search``),
* A query-by-example endpoint for KYC-style tasks (``/match``),
* Support for getting graph data for a particular entity (``/entities``),
* Support for the OpenRefine Reconciliation API (``/reconcile``).

The API uses JSON for data transfer and does not support authentication or access
control.

Further reading:

* [Self-hosted OpenSanctions](https://www.opensanctions.org/docs/self-hosted/)
* [Install and deployment](https://github.com/opensanctions/yente/blob/main/README.md)
* Intro to the [entity data model](https://www.opensanctions.org/docs/entities/)
* Tutorial: [Using the matching API to do KYC-style checks](https://www.opensanctions.org/articles/2022-02-01-matching-api/)
* [Data dictionary](https://opensanctions.org/reference/)
"""

TAGS: List[Dict[str, Any]] = [
    {
        "name": "Matching",
        "description": "Endpoints for conducting a user-facing entity search or"
        "matching a local data store against the given dataset.",
        "externalDocs": {
            "description": "Data dictionary",
            "url": "https://opensanctions.org/reference/",
        },
    },
    {
        "name": "System information",
        "description": "Service metadata endpoints for health checking and getting "
        "the application metadata to be used in client applications.",
    },
    {
        "name": "Data access",
        "description": "Endpoints for fetching data from the API, either related to "
        "individual entities, or for bulk data access in various forms.",
        "externalDocs": {
            "description": "Data dictionary",
            "url": "https://opensanctions.org/reference/",
        },
    },
    {
        "name": "Reconciliation",
        "description": "The Reconciliation Service provides four separate endpoints"
        "that work in concert to implement the data matching API used by OpenRefine, "
        "Wikidata and several other services and utilities.",
        "externalDocs": {
            "description": "W3C Community API specification",
            "url": "https://reconciliation-api.github.io/specs/latest/",
        },
    },
    {
        "name": "Geocoding",
        "description": "Geocode ftm entities using ftm-geocode",
        "externalDocs": {
            "description": "ftm-geocode on github",
            "url": "https://github.com/simonwoerpel/ftm-geocode",
        },
    },
]

EXPOSE_DATASETS = env_str("API_EXPOSE_DATASETS") or "luanda_leaks"  # test dataset
