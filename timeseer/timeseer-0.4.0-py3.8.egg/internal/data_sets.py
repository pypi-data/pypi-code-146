"""Python client for Timeseer Data Sets."""

from typing import List, Tuple

from kukur import Metadata
from pyarrow import Table

from timeseer_client.internal import JSONFlightClient


class DataSets:
    """Data Sets are fixed collections of time series and their data in a specific time range.

    Args:
        client: the Timeseer Client
    """

    __client: JSONFlightClient

    def __init__(self, client: JSONFlightClient):
        self.__client = client

    def list(self) -> List[str]:
        """Return a list containing all the data set names."""
        return self.__client.do_action("data_sets/list", {})

    def remove_data(self, name: str):
        """Removes all data in a data set

        Args:
            name: The name of the data set.
        """
        body = {"name": name}
        self.__client.do_action("data_sets/remove_data", body)

    def upload_data(
        self,
        many_series: List[Tuple[Metadata, Table]],
    ):
        """Upload time series data to a Data Set.

        The 'source' field in the SeriesSelector in Metadata determines the name of the data set.

        Data is provided as a pyarrow.Table of two or three columns:
            The first column with name 'ts' contains Arrow timestamps.
            The second column with name 'value' contains the values as a number or string.
            The optional third column with name 'quality' contains a quality flag (0 is BAD, 1 is GOOD)

        Arguments:
            many_series: a list of tuple of metadata and data.
        """
        for metadata, table in many_series:
            metadata_json = metadata.to_data()
            self.__client.do_put(dict(metadata=metadata_json), table)
