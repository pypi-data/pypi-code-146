import os
from contextlib import contextmanager
from datetime import timedelta
from typing import Dict, Generator, List

import httpx
from chaoslib.discovery.discover import (
    discover_activities,
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.types import (
    Configuration,
    DiscoveredActivities,
    Discovery,
    Secrets,
)
from logzero import logger

__version__ = "0.16.0"
__all__ = ["get_session", "discover", "parse_duration"]
RELIABLY_HOST = "app.reliably.com"


@contextmanager
def get_session(
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> Generator[httpx.Client, None, None]:
    c = configuration or {}
    verify_tls = c.get("reliably_verify_tls", True)
    with_http2 = True if verify_tls else False
    use_http = c.get("reliably_use_http", False)
    scheme = "http" if use_http else "https"
    auth_info = get_auth_info(configuration, secrets)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(auth_info["token"]),
    }

    with httpx.Client(verify=verify_tls, http2=with_http2) as client:
        client.headers = httpx.Headers(headers)
        client.base_url = httpx.URL(
            f"{scheme}://{auth_info['host']}/api/v1/organization"
        )
        yield client


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Reliably capabilities from this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-reliably")

    discovery = initialize_discovery_result(
        "chaostoolkit-reliably", __version__, "reliably"
    )
    discovery["activities"].extend(load_exported_activities())

    return discovery


###############################################################################
# Private functions
###############################################################################
def get_auth_info(
    configuration: Configuration = None, secrets: Secrets = None
) -> Dict[str, str]:
    reliably_host = None
    reliably_token = None

    reliably_host = secrets.get(
        "host", os.getenv("RELIABLY_HOST", RELIABLY_HOST)
    )

    reliably_token = secrets.get(
        "token", os.getenv("RELIABLY_TOKEN", reliably_token)
    )

    return {"host": reliably_host, "token": reliably_token}


def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions, probes and tolerances
    exposed by this extension.
    """
    activities = []
    activities.extend(
        discover_activities(
            "chaosreliably.activities.http.tolerances", "tolerance"
        )
    )
    activities.extend(discover_probes("chaosreliably.activities.http.probes"))
    activities.extend(
        discover_activities(
            "chaosreliably.activities.tls.tolerances", "tolerance"
        )
    )
    activities.extend(discover_probes("chaosreliably.activities.tls.probes"))
    activities.extend(
        discover_activities(
            "chaosreliably.activities.gh.tolerances", "tolerance"
        )
    )
    activities.extend(discover_probes("chaosreliably.activities.gh.probes"))

    return activities


def parse_duration(duration: str) -> timedelta:
    value = int(duration[:-1])
    unit = duration[-1]

    if unit == "s":
        return timedelta(seconds=value)
    elif unit == "m":
        return timedelta(minutes=value)
    elif unit == "d":
        return timedelta(days=value)
    elif unit == "w":
        return timedelta(weeks=value)

    return timedelta(weeks=1)
