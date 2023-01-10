"""Definition of Timeseries access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class TimeseriesOperations:
    """Interfaces for accessing Timeseries API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def get_table(self, timeseries: str) -> Dict:
        """Execute getTimeseriesTable API operation"""

        endpoint = "account/services/timeseries/{timeseries}".format(
            timeseries=timeseries
        )
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_timeseries_table", **self._service.kwargs)

    def delete_table(self, timeseries: str) -> Dict:
        """Execute deleteTimeseriesTable API operation"""

        endpoint = "account/services/timeseries/{timeseries}".format(
            timeseries=timeseries
        )
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "delete_timeseries_table", **self._service.kwargs)

    def update_table(self, timeseries: str, **kwargs: Any) -> Dict:
        """Execute updateTimeseriesTable API operation"""

        endpoint = "account/services/timeseries/{timeseries}".format(
            timeseries=timeseries
        )
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "defaults" in kwargs:
            body["defaults"] = kwargs["defaults"]
        if "retention" in kwargs:
            body["retention"] = kwargs["retention"]
        if "chunk" in kwargs:
            body["chunk"] = kwargs["chunk"]
        if "dimensions" in kwargs:
            body["dimensions"] = kwargs["dimensions"]
        if "measurements" in kwargs:
            body["measurements"] = kwargs["measurements"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "update_timeseries_table", **self._service.kwargs)

    def get_tables(self) -> Dict:
        """Execute getTimeseriesTables API operation"""

        endpoint = "account/services/timeseries"
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(resp, "get_timeseries_table", **self._service.kwargs)

    def update_access(self, **kwargs: Any) -> Dict:
        """Execute updateTimeseriesAccess API operation"""

        endpoint = "account/services/timeseries"
        endpoint = urllib.parse.quote(endpoint)

        body = {}
        if "users" in kwargs:
            body["users"] = kwargs["users"]

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(
            resp, "update_timeseries_access", **self._service.kwargs
        )

    def create_table(self, **kwargs: Any) -> Dict:
        """Execute createTimeseriesTable API operation"""

        endpoint = "account/services/timeseries"
        endpoint = urllib.parse.quote(endpoint)

        body = {"timeseries": kwargs["timeseries"]}

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "create_timeseries_table", **self._service.kwargs)

    def truncate_table(self, timeseries: str) -> Dict:
        """Execute truncateTimeseriesTable API operation"""

        endpoint = "account/services/timeseries/{timeseries}/data".format(
            timeseries=timeseries
        )
        endpoint = urllib.parse.quote(endpoint)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
        )

        return process_response(
            resp, "truncate_timeseries_table", **self._service.kwargs
        )
