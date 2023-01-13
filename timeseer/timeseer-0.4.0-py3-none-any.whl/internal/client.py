"""Timeseer Client provides the low-level connection to Timeseer."""

import json

from typing import Any, Dict, List, Optional, Union, Tuple

import pyarrow as pa
import pyarrow.flight as fl

from kukur import Metadata
from kukur.client import Client as KukurClient

from timeseer import SeriesSelector
from timeseer_client.internal.flows import (
    evaluate_flow,
    wait_for_flow_evaluation,
)


class Client(KukurClient):
    """Client connects to Timeseer using Arrow Flight."""

    def upload_data(
        self,
        metadata_or_data: Union[Metadata, List[Tuple[Metadata, pa.Table]]],
        table: Optional[pa.Table] = None,
        *,
        analyze=True,
        block=True,
    ):
        """Upload time series data to Timeseer.

        This requires a configured 'flight-upload' source in Timeseer.

        There are two ways to call this method.

        One requires two arguments:
            metadata: any known metadata about the time series. This will be merged with the metadata
                already known by Timeseer depending on the source configuration. The source of the series should match
                the source name of a 'flight-upload' source.
            table: a pyarrow.Table of two columns.
                The first column with name 'ts' contains Arrow timestamps.
                The second column with name 'value' contains the values as a number or string.

        The second accepts a list of tuples of the same arguments. This allows uploading multiple time series at the
        same time.

        When `analyze` is `True`, start a flow evaluation.
        When `block` is `True`, block execution until the flow evaluation is done.
        """
        if table is not None:
            assert isinstance(metadata_or_data, Metadata)
            self._upload_data_single(metadata_or_data, table, analyze, block)
        else:
            assert not isinstance(metadata_or_data, Metadata)
            self._upload_data_multiple(metadata_or_data, analyze, block)

    def _upload_data_single(
        self, metadata: Metadata, table: pa.Table, analyze: bool, block: bool
    ):
        self._upload_data_multiple([(metadata, table)], analyze, block)

    def _upload_data_multiple(
        self, many_series: List[Tuple[Metadata, pa.Table]], analyze: bool, block: bool
    ):
        client = self._get_client()
        selectors = []
        for metadata, table in many_series:
            metadata_json = metadata.to_data()
            selector = SeriesSelector.from_tags(
                metadata.series.source, metadata.series.tags, metadata.series.field
            )
            selectors.append(selector)
            descriptor = fl.FlightDescriptor.for_command(
                json.dumps(
                    dict(
                        metadata=metadata_json,
                    )
                )
            )
            writer, reader = client.do_put(descriptor, table.schema)
            writer.write_table(table)
            writer.done_writing()
            buf: pa.Buffer = reader.read()
            response: Dict = json.loads(buf.to_pybytes())
            writer.close()

        if "flowName" in response:
            if analyze:
                evaluate_flow(
                    self, response["flowName"], limitations=selectors, block=block
                )
        elif block and "flow_evaluation_group_id" in response:
            wait_for_flow_evaluation(self, response)

    def do_action(self, name: str, data: Any) -> Any:
        """Perform an Arrow Flight action with the given data provided as JSON.

        Args:
            name: The name of the action to perform.
            data: The json-convertible data to provide to the action.

        Returns:
            An action specific return values or nothing.
        """
        response = self._get_client().do_action((name, json.dumps(data).encode()))
        if response is not None:
            results = list(response)
            if len(results) > 0:
                return json.loads(results[0].body.to_pybytes())
        return None

    def do_get(self, data: Any) -> pa.Table:
        """Do an Arrow Flight GET request to return an Arrow table.

        Args:
            data: The json-convertible data for the Flight ticket.

        Returns:
            A PyArrow Table.
        """
        ticket = fl.Ticket(json.dumps(data))
        return self._get_client().do_get(ticket).read_all()

    def do_put(self, data: Any, table: pa.Table) -> Any:
        """Do an Arrow Flight PUT request to upload an Arrow table.

        Args:
            data: The json-convertible data for the Flight descriptor.
            table: The pyarrow.Table to PUT.

        Returns:
            The json-converted result of the PUT operation.
        """
        descriptor = fl.FlightDescriptor.for_command(json.dumps(data))
        writer, reader = self._get_client().do_put(descriptor, table.schema)
        writer.write_table(table)
        writer.done_writing()
        buf: pa.Buffer = reader.read()
        response: Dict = json.loads(buf.to_pybytes())
        writer.close()
        return response
