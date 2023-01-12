#!/usr/bin/env python
"""CHIME/FRB Metrics API."""
import logging
from typing import Any, Dict, List, Optional, Union

from chime_frb_api.core import API
from chime_frb_api.core.json_type import JSON

log = logging.getLogger(__name__)


class Metrics:
    """CHIME/FRB Events API."""

    def __init__(self, API: API):
        """Initialize the Metrics API."""
        self.API = API

    def overview(self) -> list:
        """GET Metrics Configuration.

        Args:
            None

        Returns:
            JSON
        """
        return self.API.get(url="/v1/metrics/overview")

    def configure(
        self, description: str, category: str, names: List[str]
    ) -> Dict[str, Any]:
        """Configure a new category of metrics.

        Args:
            description: Small description of the metrics being tracked
                          e.g. L1 beams not sending packets
            category: Unique category to track the metrics under
                      e.g. deadbeams
            names: List of strings, mapping to metric names to be tracked
                   e.g. ["0","1000", "2000", "3000"]

        Returns:
            Returns the status of the configuration, nominal response should be
        """
        if not category:
            raise AttributeError("category is required")

        for name in names:
            assert type(name) == str, "names can only be strings"

        payload = {"description": description, "category": category, "names": names}
        return self.API.post(url="/v1/metrics/configure", json=payload)

    def reconfigure(self, category: str, names: List[str]) -> bool:
        """Reconfigure/Update an existing metrics category.

        Args:
            category: Name of the metric category
            names: A list of names (str) to be added

        Returns:
            dict
        """
        if not isinstance(category, str):
            raise ValueError("category must be a string")
        for name in names:
            assert type(name) == str, "names can only be strings"
        payload = {"category": category, "names": names}
        return self.API.patch(url="/v1/metrics/configure", json=payload)

    def add(
        self,
        timestamp: Optional[str] = None,
        category: Optional[str] = None,
        metrics: dict = {},
        patch: bool = False,
    ) -> Union[bool, Dict[str, Any]]:
        """Add Metrics.

        Args:
            timestamp: Timestamp in UTC, expected to be parsed by dateutil.parser.parse
            category: category the metrics belong to, e.g. deadbeams
            metrics: Metrics to posted, {metric_name: metric_value} format
            patch: When True, there will be an attempt patch the timestamp of the
                   most recently posted metric, rather than adding new entry
                   NOTE: When posting for the first time to a newly configured metric,
                   if patch cannot be set to True

        Returns:
            dict
        """
        if not category:
            raise AttributeError("category is required")
        assert type(metrics) == dict, "metrics needs to be dictionary"
        # Construct the payload
        payload: Dict[Any, Any] = {}
        if timestamp:
            payload["timestamp"] = timestamp
        payload["category"] = category
        payload["metrics"] = metrics
        # Patch or Post the metricss
        if patch:
            return self.API.patch(url="/v1/metrics", json=payload)
        else:
            return self.API.post(url="/v1/metrics", json=payload)

    def get_metrics(
        self, category: Optional[str] = None, metric: Optional[str] = None
    ) -> JSON:
        """Get Metrics.

        Args:
            category: Category the metrics belong to, e.g. deadbeams
            metric: Name of the metric to get, e.g. "1000"

        Returns:
            metrics: metrics are a list of dicts with the following key & values
        """
        if not category:
            raise AttributeError("category is required")
        url = f"/v1/metrics/{category}"
        if metric:
            url = f"{url}/{metric}"
        return self.API.get(url=url)

    def search(
        self,
        category: Optional[str] = None,
        metrics: Optional[List[str]] = None,
        timestamps: List[Any] = ["min", "max"],
        values: List[Any] = ["min", "max"],
    ) -> JSON:
        """Search Metrics.

        Args:
            category: Category the metrics belong to, e.g. deadbeams
            metric: List of metrics (str) to get, e.g. "1000"
            timestamps: Bounds of time range to search. Valid values are
                        "min", "max", dateutil.parser parseable str
                        e.g. ["min", "2019-01-3"], ["2019-01-3", "max"]
            values: Bounds of values to search in a lexicographical order
                    Valid values are dependent on the metrics being searched
                    e.g. [0, 1], ["30.0", "30.123"]

        Returns:
            metrics: List of python dicts conforming to a metric type
        """
        if not category:
            raise AttributeError("category is required")
        if not metrics:
            raise AttributeError("atleast 1 metric name is required")
        payload: Dict[Any, Any] = {}
        payload["category"] = category
        payload["metrics"] = metrics
        payload["values"] = values
        payload["timestamps"] = timestamps
        return self.API.post(url="/v1/metrics/search", json=payload)
