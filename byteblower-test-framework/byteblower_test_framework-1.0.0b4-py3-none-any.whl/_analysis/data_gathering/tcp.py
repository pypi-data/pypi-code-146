import logging
from datetime import datetime
from typing import List, Sequence  # for type hinting

# from byteblowerll.byteblower import HTTPResultDataList  # for type hinting
from byteblowerll.byteblower import HTTPResultData  # for type hinting
from byteblowerll.byteblower import HTTPResultHistory  # for type hinting
from byteblowerll.byteblower import DataRate, HTTPClient  # for type hinting

from ..storage.tcp import HttpData
from .data_gatherer import DataGatherer

_SECONDS_PER_NANOSECOND: int = 1000000000


class HttpDataGatherer(DataGatherer):

    __slots__ = (
        '_http_data',
        '_bb_tcp_clients',
        '_client_index',
    )

    def __init__(self, http_data: HttpData,
                 bb_tcp_clients: List[HTTPClient]) -> None:
        super().__init__()
        self._http_data = http_data
        self._bb_tcp_clients = bb_tcp_clients
        self._client_index = 0

    def updatestats(self) -> None:
        """
        Analyse the result.

        .. warning::
           What would be bad?

           - TCP sessions not going to ``Finished`` state.
        """
        # Let's analyse the result
        value_rx = 0
        value_tx = 0
        value_data_speed = 0
        interval_time = None
        intervals = set()
        # NOTE - Not analysing results for finished HTTP clients
        #        in a previous iteration of updatestats:
        # for client in self._bb_tcp_clients:
        for client in self._bb_tcp_clients[self._client_index:]:
            try:
                result_history: HTTPResultHistory = client.ResultHistoryGet()
                # Get interval result
                result_history.Refresh()
                # Cfr. HTTPResultDataList
                interval_results: Sequence[HTTPResultData] = \
                    result_history.IntervalGet()
                for result in interval_results[:-1]:
                    intervals.add(result.TimestampGet())
                    average_data_speed: DataRate = result.AverageDataSpeedGet()
                    value_rx += result.RxByteCountTotalGet()
                    value_tx += result.TxByteCountTotalGet()
                    value_data_speed += average_data_speed.ByteRateGet()
                    logging.debug('\tAdding extra bytes: %d',
                                  result.RxByteCountTotalGet())
                    # NOTE - Use the newest timestamp as the timestamp
                    #        for the results in the data storage
                    interval_time = datetime.fromtimestamp(
                        result.TimestampGet() / _SECONDS_PER_NANOSECOND)
                result_history.Clear()
            except Exception:
                logging.debug("Couldn't get result in HttpAnalyser")
        # NOTE - Don't analyse results for finished HTTP clients
        #        in a next iteration of updatestats:
        self._client_index = len(self._bb_tcp_clients)
        if self._client_index > 0:
            # ! FIXME - Shouldn't we check if HTTP client actually finished?
            self._client_index -= 1
        if interval_time is None:
            # No results in this iteration
            return
        if len(intervals) > 1:
            logging.warning('HttpDataGatherer: Got %d intervals: %r',
                            len(intervals), intervals)
            value_data_speed /= len(intervals)
        self._http_data.df_tcp.loc[interval_time] = (
            # value_tx,
            # value_rx,
            value_data_speed,
        )

    def summarize(self) -> None:
        """
        Store the final results.

        Stores the average data speed over the complete session.

        .. todo::
           This summary does not support multiple clients yet.
           It is only created for the last client.
        """
        # Take only the last client (if one available)
        # ! FIXME - Take average over multiple clients
        value_data_speed = None
        if len(self._bb_tcp_clients) > 1:
            logging.warning(
                'HttpAnalyser summary only supports one client for now.'
                ' The test used %d clients.', len(self._bb_tcp_clients))
        for client in self._bb_tcp_clients[-1:]:
            try:
                result_history: HTTPResultHistory = client.ResultHistoryGet()
                # Get interval result
                result_history.Refresh()
                # Cfr. HTTPResultDataList
                cumulative_results: Sequence[HTTPResultData] = \
                    result_history.CumulativeGet()
                # Take only the last snapshot (if one available)
                for result in cumulative_results[-1:]:
                    average_data_speed: DataRate = result.AverageDataSpeedGet()
                    value_data_speed = average_data_speed.ByteRateGet()
            except Exception as e:
                logging.warning("Couldn't get result in HttpAnalyser: %s", e)
        self._http_data._avg_data_speed = value_data_speed
