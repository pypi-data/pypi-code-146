from typing import Sequence  # for type hinting

from pandas import Timestamp  # for type hinting
from pandas import DataFrame

from .data_store import DataStore


class FrameCountData(DataStore):

    __slots__ = (
        '_df_tx',
        '_df_rx',
        '_total_tx_bytes',
        '_total_rx_bytes',
        '_total_tx_packets',
        '_total_rx_packets',
        '_timestamp_rx_first',
        '_timestamp_rx_last',
    )

    def __init__(self) -> None:
        self._df_tx = DataFrame(columns=[
            "Packets total",
            "Bytes total",
            "Packets interval",
            "Bytes interval",
        ])
        self._df_rx = DataFrame(columns=[
            "Packets total",
            "Bytes total",
            "Packets interval",
            "Bytes interval",
        ])
        self._total_tx_bytes: int = None
        self._total_rx_bytes: int = None
        self._total_tx_packets: int = None
        self._total_rx_packets: int = None
        self._timestamp_rx_first: Timestamp = None
        self._timestamp_rx_last: Timestamp = None

    @property
    def df_tx(self) -> DataFrame:
        return self._df_tx

    @property
    def df_rx(self) -> DataFrame:
        return self._df_rx

    @property
    def total_tx_bytes(self) -> int:
        return self._total_tx_bytes

    @property
    def total_rx_bytes(self) -> int:
        return self._total_rx_bytes

    @property
    def total_tx_packets(self) -> int:
        return self._total_tx_packets

    @property
    def total_rx_packets(self) -> int:
        return self._total_rx_packets

    @property
    def timestamp_rx_first(self) -> Timestamp:
        return self._timestamp_rx_first

    @property
    def timestamp_rx_last(self) -> Timestamp:
        return self._timestamp_rx_last


class LatencyData(DataStore):

    __slots__ = (
        '_df_latency',
        '_final_min_latency',
        '_final_max_latency',
        '_final_avg_latency',
        '_final_avg_jitter',
    )

    def __init__(self) -> None:
        self._df_latency = DataFrame(columns=[
            "Minimum",
            "Maximum",
            "Average",
            "Jitter",
        ])
        self._final_min_latency = None
        self._final_max_latency = None
        self._final_avg_latency = None
        self._final_avg_jitter = None

    @property
    def df_latency(self) -> DataFrame:
        return self._df_latency

    @property
    def final_min_latency(self) -> float:
        return self._final_min_latency

    @property
    def final_max_latency(self) -> float:
        return self._final_max_latency

    @property
    def final_avg_latency(self) -> float:
        return self._final_avg_latency

    @property
    def final_avg_jitter(self) -> float:
        return self._final_avg_jitter


class LatencyDistributionData(DataStore):

    __slots__ = (
        '_bucket_width',
        '_packet_count_buckets',
        '_final_min_latency',
        '_final_max_latency',
        '_final_avg_latency',
        '_final_avg_jitter',
        '_final_packet_count_valid',
        '_final_packet_count_invalid',
        '_final_packet_count_below_min',
        '_final_packet_count_above_max',
    )

    def __init__(self) -> None:
        self._bucket_width: int = None
        self._packet_count_buckets: Sequence[int] = None
        self._final_min_latency = None
        self._final_max_latency = None
        self._final_avg_latency = None
        self._final_avg_jitter = None
        self._final_packet_count_valid = None
        self._final_packet_count_invalid = None
        self._final_packet_count_below_min = None
        self._final_packet_count_above_max = None

    @property
    def bucket_width(self) -> int:
        """Return the bucket width in nanoseconds."""
        return self._bucket_width

    @property
    def packet_count_buckets(self) -> Sequence[int]:
        """Return the list of packet counts per bucket."""
        return self._packet_count_buckets

    @property
    def final_min_latency(self) -> float:
        return self._final_min_latency

    @property
    def final_max_latency(self) -> float:
        return self._final_max_latency

    @property
    def final_avg_latency(self) -> float:
        return self._final_avg_latency

    @property
    def final_avg_jitter(self) -> float:
        return self._final_avg_jitter

    @property
    def final_packet_count_valid(self) -> int:
        return self._final_packet_count_valid

    @property
    def final_packet_count_invalid(self) -> int:
        return self._final_packet_count_invalid

    @property
    def final_packet_count_below_min(self) -> int:
        return self._final_packet_count_below_min

    @property
    def final_packet_count_above_max(self) -> int:
        return self._final_packet_count_above_max
