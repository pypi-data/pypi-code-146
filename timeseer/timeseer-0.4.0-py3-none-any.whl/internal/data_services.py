"""Python client for Timeseer Data Services."""

import time

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pyarrow as pa

from kukur import Metadata
from timeseer import SeriesSelector

from timeseer_client.internal import (
    JSONFlightClient,
    Statistic,
    TimeoutException,
    TimeseerClientException,
)


class DataServiceEvaluationFailedException(TimeseerClientException):
    """Thrown when a data service evaluation fails."""

    def __init__(self, name: str, view_name: str):
        super().__init__(f'evaluation for data service "{name}"/"{view_name}" failed')


class DataServices:
    """Data Services provide access to analysis results, time series data and statistics.

    Args:
        client: the Timeseer Client
    """

    __client: JSONFlightClient

    def __init__(self, client: JSONFlightClient):
        self.__client = client

    def list(self) -> List[str]:
        """Return a list containing all the data service names."""
        return self.__client.do_action("data_services/list", {})

    def wait_for_evaluation(
        self, data_service_name: str, series_set_name: str, *, timeout_seconds: int = 60
    ) -> None:
        """Wait until the evaluation of a data service is complete.

        Args:
            data_service_name: The name of the data service
            series_set_name: The name of the series set
            timeout_seconds: (optional, keyword only) The number of seconds to wait until the evaluation is complete

        Raises:
            DataServiceEvaluationFailedException when a failure is reported.
        """
        body = dict(
            dataServiceName=data_service_name,
            view=series_set_name,
        )
        while timeout_seconds > 0:
            job_state = self.__client.do_action("data_services/get_view_state", body)
            if job_state["completed"] == job_state["total"]:
                if job_state["failed"] > 0:
                    raise DataServiceEvaluationFailedException(
                        data_service_name, series_set_name
                    )
                return
            time.sleep(1)
            timeout_seconds = timeout_seconds - 1

        raise TimeoutException()

    def get_data(
        self,
        data_service_name: str,
        series_set_name: str,
        selector: SeriesSelector,
    ) -> pa.Table:
        """Get data from a given data service.

        Falls back to the data source when no data is present.

        Args:
            data_service_name: The name of the data service
            series_set_name: The name of the series set used in the data service
            selector: Return data for the time series selected by this selector.

        Returns::
            A pyarrow Table with three columns: 'ts', 'value' and 'quality'.
        """
        body = {
            "query": "data_services/get_data",
            "dataServiceName": data_service_name,
            "view": series_set_name,
            "selector": selector.to_data(),
        }
        return self.__client.do_get(body)

    def get_kpi_scores(
        self, data_service_name: str, series_set_name: str
    ) -> Dict[str, int]:
        """Get the kpi scores of a data service.

        Args:
            data_service_name: The name of the Data Service.
            series_set_name: The series set name.

        Returns::
            The score per KPI as a percentage.
        """
        body = {
            "dataServiceName": data_service_name,
            "view": series_set_name,
        }
        return self.__client.do_action("data_services/get_kpi_scores", body)

    def get_event_frames(  # pylint:disable=too-many-arguments
        self,
        data_service_name: str,
        series_set_name: str,
        selector: Optional[SeriesSelector] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        frame_type: Optional[Union[str, List[str]]] = None,
    ) -> pa.Table:
        """Get all event frames matching the given criteria.

        Args:
            data_service_name: The Data Service name to which the event frames are linked.
            view: The series set name to which the event frames are linked
            selector: the time series to which the event frames are linked.
            start_date: the start date of the range to find overlapping event frames in.
                Defaults to start date of the data service.
            end_date: the end date of the range to find overlapping event frames in.
                Defaults to end date of the data service.
            frame_type: the type or types of event frames to search for. Finds all types when empty.

        Returns::
            A pyarrow Table with 6 columns.
            The first column ('start_date') contains the start date.
            The second column ('end_date') contains the end date.
            The third column ('type') contains the type of the returned event frame as a string.
            The fourth column ('explanation') can contain the explanation for an event frame as a string.
            The fifth column ('status') can contain the status of an event frame as a string.
            Columns 6 contains possible multiple references for the event frame.
            The seventh column contains the uuid of the event frame.
        """

        query: Dict[str, Any] = {
            "query": "data_services/get_event_frames",
            "dataServiceName": data_service_name,
            "view": series_set_name,
            "selector": selector.to_data() if selector is not None else None,
            "startDate": start_date.isoformat() if start_date is not None else None,
            "endDate": end_date.isoformat() if end_date is not None else None,
        }

        if frame_type is not None:
            query["type"] = frame_type

        return self.__client.do_get(query)

    def get_statistics(
        self,
        data_service_name: str,
        series_set_name: Optional[str] = None,
        *,
        selector: Optional[SeriesSelector] = None,
    ) -> List[Statistic]:
        """Return statistics stored in a Data Service.

        One of series_set_name or series should be provided.

        Args:
            data_service_name: The name of the Data Service that contains the statistics.
            series_set_name: The name of the series set to return multivariate and calculated statistics for. (optional)
            selector: The time series to return statistics for. (optional, keyword-only)

        Returns::
            A list of `Statistic`s.
        """
        query: Dict[str, Any] = dict(
            dataServiceName=data_service_name,
        )

        if series_set_name is not None:
            if not isinstance(series_set_name, str):
                raise TypeError("`series_set_name` not an instance of `str`")
            query["view"] = series_set_name
        elif selector is not None:
            query["selector"] = selector.to_data()
        else:
            return []

        return [
            Statistic.from_data(data)
            for data in self.__client.do_action("data_services/get_statistics", query)
        ]

    def get_calculated_metadata(
        self, data_service_name: str, selector: SeriesSelector
    ) -> Metadata:
        """Return calculated metadata for a series.

        Args:
            data_service_name: The name of the Data Service that contains the calculated metadata.
            selector: The time series to return calculated metadata for.

        Returns::
            A `Metadata` object with the calculated metadata that's available.
        """
        query = dict(
            dataServiceName=data_service_name,
            selector=selector.to_data(),
        )
        return Metadata.from_data(
            self.__client.do_action("data_services/get_calculated_metadata", query),
            selector,
        )
