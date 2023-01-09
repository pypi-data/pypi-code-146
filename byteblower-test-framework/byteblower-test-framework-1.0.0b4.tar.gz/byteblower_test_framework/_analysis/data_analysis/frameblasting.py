import logging

from pandas import DataFrame, Timestamp, concat  # for type hinting

from ..._report.options import Layer2Speed, layer2_speed_info
from ..._traffic.frame import ETHERNET_FCS_LENGTH
from ..storage.trigger import (
    FrameCountData,
    LatencyData,
    LatencyDistributionData,
)
from .data_analyser import DataAnalyser

__all__ = (
    'FrameCountAnalyser',
    'LatencyAnalyser',
    'LatencyCDFAnalyser',
    'MosAnalyser',
)


class FrameCountAnalyser(DataAnalyser):

    __slots__ = (
        '_data',
        '_df_tx_bytes',
        '_df_rx_bytes',
        '_layer2_speed',
        '_max_loss_percentage',
    )

    def __init__(self, data: FrameCountData, layer2_speed: Layer2Speed,
                 max_loss_percentage: float) -> None:
        super().__init__()
        self._data = data
        self._df_tx_bytes: DataFrame = None
        self._df_rx_bytes: DataFrame = None
        self._layer2_speed = layer2_speed
        self._max_loss_percentage = max_loss_percentage

    def analyse(self) -> None:
        """Fail the test if the packet loss > ``max_loss_percentage``."""
        df_tx_bytes = self._data.df_tx[["Bytes interval"]]
        df_rx_bytes = self._data.df_rx[["Bytes interval"]]

        total_tx_bytes = self._data.total_tx_bytes
        total_rx_bytes = self._data.total_rx_bytes

        if self._layer2_speed == Layer2Speed.frame:
            self._df_tx_bytes = df_tx_bytes
            self._df_rx_bytes = df_rx_bytes
        elif self._layer2_speed == Layer2Speed.frame_with_fcs:
            # NOTE - These calculations are correct when no data received too

            # NOTE - Create a copy to avoid SettingWithCopyWarning !
            #
            #     pandas/core/indexing.py:1951: SettingWithCopyWarning:
            #     A value is trying to be set on a copy of a slice from a DataFrame.  # noqa: E501
            #     Try using .loc[row_indexer,col_indexer] = value instead

            #     See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy  # noqa: E501
            #     self.obj[selected_item_labels] = value
            self._df_tx_bytes = df_tx_bytes.copy()
            self._df_tx_bytes["Bytes interval"] = \
                self._data.df_tx["Bytes interval"] + (
                    ETHERNET_FCS_LENGTH * self._data.df_tx["Packets interval"])

            self._df_rx_bytes = df_rx_bytes.copy()
            self._df_rx_bytes["Bytes interval"] = \
                self._data.df_rx["Bytes interval"] + (
                    ETHERNET_FCS_LENGTH * self._data.df_rx["Packets interval"])

            total_tx_bytes += \
                (ETHERNET_FCS_LENGTH * self._data.total_tx_packets)
            total_rx_bytes += \
                (ETHERNET_FCS_LENGTH * self._data.total_rx_packets)
        else:
            raise ValueError(
                f'Unsupported Layer 2 speed: {self._layer2_speed}')

        self._set_result(True)
        loss = total_tx_bytes - total_rx_bytes
        relativeloss = 100.0
        if total_tx_bytes != 0:
            relativeloss *= loss / total_tx_bytes
        self._set_log(f"{layer2_speed_info(self._layer2_speed)}\n"
                      f"{total_tx_bytes} bytes transmitted"
                      f", {total_rx_bytes} bytes received."
                      f" Loss is {loss} bytes, or {relativeloss}%")
        if relativeloss > self._max_loss_percentage:
            self._set_result(False)

    @property
    def df_tx_bytes(self) -> DataFrame:
        """Return ``DataFrame`` of transmitted bytes per interval."""
        return self._df_tx_bytes

    @property
    def df_rx_bytes(self) -> DataFrame:
        """Return ``DataFrame`` of received bytes per interval."""
        return self._df_rx_bytes

    @property
    def total_tx_bytes(self) -> int:
        """Return total transmitted number of bytes.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.total_tx_bytes

    @property
    def total_rx_bytes(self) -> int:
        """Return total received number of bytes.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.total_rx_bytes

    @property
    def total_tx_packets(self) -> int:
        """Return total transmitted number of packets.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.total_tx_packets

    @property
    def total_rx_packets(self) -> int:
        """Return total received number of packets.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.total_rx_packets

    @property
    def timestamp_rx_first(self) -> Timestamp:
        """Return the timestamp of the first received packet.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.timestamp_rx_first

    @property
    def timestamp_rx_last(self) -> Timestamp:
        """Return the timestamp of the last received packet.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.timestamp_rx_last


class LatencyAnalyser(DataAnalyser):

    __slots__ = (
        '_data',
        '_df_latency_min',
        '_df_latency_max',
        '_df_latency_avg',
        '_df_latency_jitter',
        '_max_threshold_latency',
    )

    def __init__(self, data: LatencyData,
                 max_threshold_latency: float) -> None:
        super().__init__()
        self._data = data
        self._df_latency_min: DataFrame = None
        self._df_latency_max: DataFrame = None
        self._df_latency_avg: DataFrame = None
        self._df_latency_jitter: DataFrame = None
        self._max_threshold_latency = max_threshold_latency

    def analyse(self) -> None:
        self._df_latency_min = self._data.df_latency[["Minimum"]]
        self._df_latency_max = self._data.df_latency[["Maximum"]]
        self._df_latency_avg = self._data.df_latency[["Average"]]
        self._df_latency_jitter = self._data.df_latency[["Jitter"]]

        final_min_latency = self._data.final_min_latency
        final_max_latency = self._data.final_max_latency
        final_avg_latency = self._data.final_avg_latency
        final_avg_jitter = self._data.final_avg_jitter

        self._set_log(f"{final_min_latency} ms mininum latency"
                      f", {final_max_latency} ms maximum latency"
                      f", {final_avg_latency} ms average latency"
                      f", {final_avg_jitter} ms average jitter.")

        self._set_result(True)
        if (final_max_latency is None
                or final_max_latency > self._max_threshold_latency):
            # NOTE - If we did not receive any data,
            #        we will not have latency values.
            self._set_result(False)

    @property
    def df_latency_min(self) -> DataFrame:
        return self._df_latency_min

    @property
    def df_latency_max(self) -> DataFrame:
        return self._df_latency_max

    @property
    def df_latency_avg(self) -> DataFrame:
        return self._df_latency_avg

    @property
    def df_latency_jitter(self) -> DataFrame:
        return self._df_latency_jitter

    @property
    def final_min_latency(self) -> float:
        """Return the minimum latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_min_latency

    @property
    def final_max_latency(self) -> float:
        """Return the maximum latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_max_latency

    @property
    def final_avg_latency(self) -> float:
        """Return the average latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_avg_latency

    @property
    def final_avg_jitter(self) -> float:
        """Return the average jitter in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_avg_jitter


class LatencyCDFAnalyser(DataAnalyser):

    __slots__ = (
        '_data',
        '_df_latency',
        '_max_threshold_latency',
        '_quantile',
    )

    def __init__(self, data: LatencyDistributionData,
                 max_threshold_latency: float, quantile: float) -> None:
        super().__init__()
        self._data = data
        self._df_latency: DataFrame = None
        self._max_threshold_latency = max_threshold_latency
        self._quantile = quantile

    def analyse(self) -> None:
        bucket_width = self._data.bucket_width
        packet_count_buckets = self._data.packet_count_buckets

        self._df_latency = DataFrame(columns=["Latency", "CDF"])

        final_min_latency = self._data.final_min_latency
        final_max_latency = self._data.final_max_latency
        final_avg_latency = self._data.final_avg_latency
        final_avg_jitter = self._data.final_avg_jitter
        final_packet_count_valid = self._data.final_packet_count_valid
        # final_packet_count_invalid = self._data.final_packet_count_invalid
        final_packet_count_below_min = self._data.final_packet_count_below_min
        final_packet_count_above_max = self._data.final_packet_count_above_max

        # Build percentiles
        percentiles = list()
        i = 0.00
        incr = 10.0
        while i <= 100.00:
            i += incr
            logging.debug("Adding percentile %s", i)
            percentiles.append(i)
            # I know this seems strange, but comparing floats is very tricky.
            # This doesn't work:
            # if ( 100.0 - i ) < incr
            # See  https://stackoverflow.com/questions/3049101/floating-point-equality-in-python-and-in-general  # noqa: E501
            if (100.0 - i - incr) < (incr / 10):
                incr /= 10
                if incr < 0.01:
                    break

        # Process latency
        self._set_result(True)
        if final_packet_count_valid == 0:
            self._set_log("No packets received. Test has failed.")
            self._set_result(False)
            return

        log = [
            f"Latency is below {self._max_threshold_latency} ms"
            " for all percentile values."
        ]
        for percentile in percentiles:
            # Let's calculate the latency
            percentile_factor = percentile / 100.0
            if (final_packet_count_above_max / final_packet_count_valid >
                (1.0 - percentile_factor) and percentile <= self._quantile):
                if self.has_passed:
                    self._set_result(False)
                    log = [
                        "Latency is larger"
                        f" than {self._max_threshold_latency} ms"
                        f" for quantile {percentile}"
                    ]
            # The user will need to know the latency percentile.
            threshold = percentile_factor * final_packet_count_valid
            cumul = 0
            for x in range(0, len(packet_count_buckets)):
                cumul += packet_count_buckets[x]
                if cumul > threshold:
                    df_latency_update = DataFrame({
                        'Latency': [(x + 1) * bucket_width],
                        'CDF': [100.0 - percentile]
                    })

                    self._df_latency = concat(
                        [self._df_latency, df_latency_update],
                        ignore_index=True)

                    if not self.has_passed:
                        log.append("\tLatency for quantile {} is {}ms.".format(
                            percentile, (x + 1) * bucket_width / 1000000.0))
                    break

        if (final_max_latency is None
                or final_max_latency > self._max_threshold_latency):
            # NOTE - If we did not receive any data,
            #        we will not have latency values.
            self._set_result(False)

        # Add latency summary information to the log
        summary_log = list()
        summary_log.append(f"Minimum latency: {final_min_latency} ms")
        summary_log.append(f"Maximum latency: {final_max_latency} ms")
        summary_log.append(f"Average latency: {final_avg_latency} ms")
        summary_log.append(f"Latency jitter: {final_avg_jitter} ms")
        summary_log.append("Number of packets below minimum latency"
                           f": {final_packet_count_below_min}")
        summary_log.append("Number of packets above maximum latency"
                           f": {final_packet_count_above_max}")

        self._set_log('\n'.join((*summary_log, *log)))

    @property
    def packet_count_valid(self) -> int:
        """Return number of valid received packets."""
        return self._data.final_packet_count_valid

    @property
    def df_latency(self) -> DataFrame:
        return self._df_latency

    @property
    def final_min_latency(self) -> float:
        """Return the minimum latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_min_latency

    @property
    def final_max_latency(self) -> float:
        """Return the maximum latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_max_latency

    @property
    def final_avg_latency(self) -> float:
        """Return the average latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_avg_latency

    @property
    def final_avg_jitter(self) -> float:
        """Return the average jitter in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_avg_jitter


class MosAnalyser(DataAnalyser):

    __slots__ = (
        '_data_framecount',
        '_data_latency',
        '_layer2_speed',
        '_df_tx_bytes',
        '_df_rx_bytes',
        '_df_latency_min',
        '_df_latency_max',
        '_df_latency_avg',
        '_df_latency_jitter',
        '_minimum_mos',
    )

    def __init__(self, data_framecount: FrameCountData,
                 data_latency: LatencyData, layer2_speed: Layer2Speed,
                 minimum_mos: float) -> None:
        super().__init__()
        self._data_framecount = data_framecount
        self._data_latency = data_latency
        self._df_tx_bytes: DataFrame = None
        self._df_rx_bytes: DataFrame = None
        self._df_latency_min: DataFrame = None
        self._df_latency_max: DataFrame = None
        self._df_latency_avg: DataFrame = None
        self._df_latency_jitter: DataFrame = None
        self._layer2_speed = layer2_speed
        self._minimum_mos = minimum_mos

    def analyse(self) -> None:
        df_tx_bytes = self._data_framecount.df_tx[["Bytes interval"]]
        df_rx_bytes = self._data_framecount.df_rx[["Bytes interval"]]
        self._df_latency_min = self._data_latency.df_latency[["Minimum"]]
        self._df_latency_max = self._data_latency.df_latency[["Maximum"]]
        self._df_latency_avg = self._data_latency.df_latency[["Average"]]
        self._df_latency_jitter = self._data_latency.df_latency[["Jitter"]]

        total_tx_bytes = self._data_framecount.total_tx_bytes
        total_rx_bytes = self._data_framecount.total_rx_bytes
        final_min_latency = self._data_latency.final_min_latency
        final_max_latency = self._data_latency.final_max_latency
        final_avg_latency = self._data_latency.final_avg_latency
        final_avg_jitter = self._data_latency.final_avg_jitter

        if self._layer2_speed == Layer2Speed.frame:
            self._df_tx_bytes = df_tx_bytes
            self._df_rx_bytes = df_rx_bytes
        elif self._layer2_speed == Layer2Speed.frame_with_fcs:
            # NOTE - These calculations are correct when no data received too

            # NOTE - Create a copy to avoid SettingWithCopyWarning !
            #
            #     pandas/core/indexing.py:1951: SettingWithCopyWarning:
            #     A value is trying to be set on a copy of a slice from a DataFrame.  # noqa: E501
            #     Try using .loc[row_indexer,col_indexer] = value instead

            #     See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy  # noqa: E501
            #     self.obj[selected_item_labels] = value
            self._df_tx_bytes = df_tx_bytes.copy()
            self._df_tx_bytes["Bytes interval"] = \
                self._data_framecount.df_tx["Bytes interval"] + (
                    ETHERNET_FCS_LENGTH * self._data_framecount.df_tx[
                        "Packets interval"])

            self._df_rx_bytes = df_rx_bytes.copy()
            self._df_rx_bytes["Bytes interval"] = \
                self._data_framecount.df_rx["Bytes interval"] + (
                    ETHERNET_FCS_LENGTH * self._data_framecount.df_rx[
                        "Packets interval"])

            total_tx_bytes += \
                (ETHERNET_FCS_LENGTH * self._data_framecount.total_tx_packets)
            total_rx_bytes += \
                (ETHERNET_FCS_LENGTH * self._data_framecount.total_rx_packets)
        else:
            raise ValueError(
                f'Unsupported Layer 2 speed: {self._layer2_speed}')

        loss = total_tx_bytes - total_rx_bytes
        relativeloss = 100.0
        if total_tx_bytes != 0:
            relativeloss *= loss / total_tx_bytes

        if not total_rx_bytes:
            # No packets received, so we can't calculate a MOS value.
            self._set_log(f"{layer2_speed_info(self._layer2_speed)}\n"
                          f"{total_tx_bytes} bytes transmitted"
                          f", {total_rx_bytes} bytes received."
                          f" Loss is {loss} bytes, or {relativeloss}%.\n"
                          "No packets received. Test has failed."
                          " MOS calculation is skipped.")
            self._set_result(False)
            return

        # Calculate MOS
        mos_score = calculate_mos(relativeloss, final_avg_latency,
                                  final_avg_jitter)

        self._set_log(f"{layer2_speed_info(self._layer2_speed)}\n"
                      f"{total_tx_bytes} bytes transmitted"
                      f", {total_rx_bytes} bytes received."
                      f" Loss is {loss} bytes, or {relativeloss}%.\n"
                      f"{final_min_latency} ms mininum latency"
                      f", {final_max_latency} ms maximum latency"
                      f", {final_avg_latency} ms average latency"
                      f", {final_avg_jitter} ms average jitter.\n"
                      f"Average MOS is {mos_score}.")

        self._set_result(True)
        if mos_score < self._minimum_mos:
            self._set_result(False)

    @property
    def has_rx(self) -> bool:
        """Return if this analyser received data.

        :return: Whether data was received.
        :rtype: bool
        """
        return self._data_framecount.total_rx_bytes > 0

    @property
    def df_tx_bytes(self) -> DataFrame:
        """Return DataFrame of transmitted bytes per interval."""
        return self._df_tx_bytes

    @property
    def df_rx_bytes(self) -> DataFrame:
        """Return DataFrame of received bytes per interval."""
        return self._df_rx_bytes

    @property
    def df_latency_min(self) -> DataFrame:
        return self._df_latency_min

    @property
    def df_latency_max(self) -> DataFrame:
        return self._df_latency_max

    @property
    def df_latency_avg(self) -> DataFrame:
        return self._df_latency_avg

    @property
    def df_latency_jitter(self) -> DataFrame:
        return self._df_latency_jitter


def calculate_mos(relative_loss: float, avg_latency: float,
                  avg_jitter: float) -> float:
    """Calculate MOS.

    :param relative_loss: Relative packet loss
    :type relative_loss: float
    :param avg_latency: Average latency in milliseconds
    :type avg_latency: float
    :param avg_jitter: Average jitter in milliseconds
    :type avg_jitter: float
    :return: MOS value (1.0 - 5.0)
    :rtype: float
    """
    # G.107, 7.1 Calculation of the transmission rating factor, R
    #   R = Ro - Is - Id - Ie-eff + A
    # where
    #   Ro: basic signal-to-noise ratio, including noise sources
    #       such as circuit noise and room noise.
    #   Is: combination of all impairments which occur more or less
    #       simultaneously with the voice signal.
    #   Id: impairments caused by delay
    #   Ie-eff: Effective equipment impairment factor represents
    #           impairments caused by low bit-rate codecs.
    #           It also includes impairment due to randomly
    #           distributed packet losses.
    #   A: Advantage factor allows for compensation of impairment factors
    #      when the user benefits from other types of access to the user.
    # Where (G.107, 7.7 Default values):
    #   TODO: Where does this 93.2 come from?
    #   Ro - Is = 93.2
    #   Ie = 0
    #   Ppl = 0 [no packet loss]
    #   Bpl = *** [See G.113]
    #   BurstR = 1 [random packet loss, not bursty]
    #   => Ie-eff = 0
    #   A = 0
    # From G.113, Appendix I, Provisional planning values for the
    #      equipment impairment factor, Ie, and packet-loss robustness
    #      factor, Bpl:
    #   Ie = 0 [PCM, G.711, 10ms]
    #   Bpl = 4.3/25.1 [G.711; random packet loss]
    effective_latency = avg_latency + (avg_jitter * 2) + 10
    if effective_latency < 160:
        r_value = 93.2 - (effective_latency / 40)
    else:
        r_value = 93.2 - (effective_latency - 120) / 10
    r_value = r_value - (relative_loss * 2.5)
    r_value = clamp(r_value, 0, 100)
    mos_score = 1 + (0.035 * r_value) + (0.000007 * r_value) * (
        r_value - 60) * (100 - r_value)
    return mos_score


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))
