import logging
from datetime import datetime, timedelta
from typing import Optional, Union  # for type hinting

from .._analysis.bufferanalyser import BufferAnalyser
from .._endpoint.port import Port  # for type hinting
from .tcpflow import TCPCongestionAvoidanceAlgorithm, TcpFlow


class VideoFlow(TcpFlow):

    __slots__ = (
        '_segment_size',
        '_segment_duration',
        '_buffering_goal',
        '_bytes_per_ms',
        '_bufferanalyser',
        '_last_consume_time',
        '_ip_tos',
    )

    _CONFIG_ELEMENTS = TcpFlow._CONFIG_ELEMENTS + (
        "segment_size",
        "segment_duration",
        "buffering_goal",
    )

    def __init__(
        self,
        source: Port,
        destination: Port,
        name: Optional[str] = None,
        segment_size: int = 2 * 1000 * 1000,
        segment_duration: Union[timedelta, float] = timedelta(seconds=2.500),
        buffering_goal: Union[timedelta, float] = timedelta(seconds=60),
        play_goal: Union[timedelta, float] = timedelta(seconds=5),
        ip_tos: Optional[int] = None,
        # *args,
        **kwargs
    ) -> None:
        super().__init__(source, destination, name=name, **kwargs)
        # super().__init__(source, destination, *args, name=name, **kwargs)
        self._segment_size = segment_size
        if isinstance(segment_duration, timedelta):
            # Already timedelta
            self._segment_duration = segment_duration
        elif isinstance(segment_duration, (float, int)):
            # Convert to timedelta
            self._segment_duration = timedelta(seconds=segment_duration)
        else:
            raise ValueError(
                f'Invalid value for segment_duration: {segment_duration!r}'
            )
        if isinstance(buffering_goal, timedelta):
            # Already timedelta
            self._buffering_goal = buffering_goal
        elif isinstance(buffering_goal, (float, int)):
            # Convert to timedelta
            self._buffering_goal = timedelta(seconds=buffering_goal)
        else:
            raise ValueError(
                f'Invalid value for buffering_goal: {buffering_goal!r}'
            )
        if isinstance(play_goal, timedelta):
            # Already timedelta
            pass
        elif isinstance(play_goal, (float, int)):
            # Convert to timedelta
            play_goal = timedelta(seconds=play_goal)
        else:
            raise ValueError(
                f'Invalid value for buffering_goal: {play_goal!r}'
            )
        self._ip_tos = ip_tos
        self._bytes_per_ms = (
            self._segment_size / self._segment_duration.total_seconds() / 1000
        )  # video bitrate expressed in bytes/s
        bitrate = 8000 * self._bytes_per_ms
        logging.info(
            "Video bitrate will be {BITRATE} MBit/s".format(
                BITRATE=bitrate / 1000000.0
            )
        )
        buffering_goal_segments = (
            self._buffering_goal.total_seconds() /
            self._segment_duration.total_seconds()
        )

        buffering_goal_bytes = \
            int(buffering_goal_segments * self._segment_size)
        play_goal_bytes = int(
            play_goal.total_seconds() / self._segment_duration.total_seconds()
        ) * self._segment_size
        self._bufferanalyser = BufferAnalyser(
            buffering_goal_bytes, play_goal_bytes
        )
        self.add_analyser(self._bufferanalyser)
        self._last_consume_time: datetime = None

    @property
    def segment_size(self) -> int:
        return self._segment_size

    @property
    def segment_duration(self) -> timedelta:
        return self._segment_duration

    @property
    def buffering_goal(self) -> timedelta:
        return self._buffering_goal

    def apply(self, **kwargs) -> None:
        bb_tcp_server = self._set_tcp_server(
            server_port=self.source,
            receive_window_scaling=7,
            slow_start_threshold=1000000000,
            caa=TCPCongestionAvoidanceAlgorithm.sack_with_cubic
        )
        if bb_tcp_server is not None:
            # New HTTP server (not re-using existing one)
            bb_tcp_server.Start()
        self._last_consume_time = datetime.now()
        # Set the initial stats:
        self._bufferanalyser.updatestats()
        # ! FIXME - Is this required/wanted?
        return super().apply(**kwargs)

    def _elapsed_time_ms(self) -> float:
        now = datetime.now()
        difference: timedelta = now - self._last_consume_time
        self._last_consume_time = now
        return difference.total_seconds() * 1000

    def _download_segment(self) -> None:
        bb_tcp_client = self._add_client_session(
            client_port=self.destination,
            server_port=self.source,
            request_size=self._segment_size,
            receive_window_scaling=7,
            slow_start_threshold=1000000000,
            caa=TCPCongestionAvoidanceAlgorithm.sack_with_cubic,
            ip_tos=self._ip_tos
        )
        bb_tcp_client.RequestStart()

    def _segment_download_required(self) -> bool:
        return (
            self._bufferanalyser.size + self._segment_size <
            self._bufferanalyser.size_max
        )

    def process(self) -> None:
        try:
            bb_tcp_client = self._last_client_session()
        except ValueError:
            if self._segment_download_required():
                self._download_segment()
        else:
            # Wait maximum 10 milliseconds
            try:
                if bb_tcp_client.WaitUntilFinished(10000000):
                    # Destroy the http client
                    test_tcp_client = self._bb_tcp_clients.pop()
                    assert test_tcp_client == bb_tcp_client, \
                        'OOPS, clearing invalid TCP client'
                    self.destination.bb_port.ProtocolHttpClientRemove(
                        bb_tcp_client
                    )
                    self._bufferanalyser.buffer_fill(self._segment_size)

            except Exception as e:
                logging.error(
                    "No video statistics available. Unexpected error: %s", e
                )

        elapsed_bytes = self._elapsed_time_ms() * self._bytes_per_ms
        self._bufferanalyser.buffer_consume(elapsed_bytes)

        super().process()

    def updatestats(self) -> None:
        return super().updatestats()

    def analyse(self) -> None:
        """Pass or fail for this test."""
        self.updatestats()

        return super().analyse()
