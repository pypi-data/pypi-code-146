import logging
from abc import ABC, abstractmethod
from typing import (  # for type hinting
    Any,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

from pandas import Timestamp  # for type hinting
from pandas import DataFrame

from .._report.options import Layer2Speed, layer2_speed_info
from .._traffic.frame import ETHERNET_FCS_LENGTH
from .flow_analyser import FlowAnalyser  # for type hinting
from .framelossanalyser import BaseFrameLossAnalyser
from .latencyanalyser import (
    BaseLatencyCDFFrameLossAnalyser,
    BaseLatencyFrameLossAnalyser,
)
from .plotting import GenericChart

# Type aliases
_FrameCountAnalysers = (BaseFrameLossAnalyser, )
_OverTimeLatencyAnalysers = (BaseLatencyFrameLossAnalyser, )
# NOTE: CDF analyser does not support "over time" results (yet):
_OverTimeSupportedAnalysersList = _FrameCountAnalysers \
    + _OverTimeLatencyAnalysers
_SummaryLatencyAnalysers = (
    BaseLatencyFrameLossAnalyser,
    BaseLatencyCDFFrameLossAnalyser,  # only supported for summarizing
)
_SummarySupportedAnalysersList = _FrameCountAnalysers \
    + _SummaryLatencyAnalysers
_OverTimeOrSummarySupportedAnalysersList = _SummarySupportedAnalysersList
_SUPPORT_LEVEL = (
    BaseLatencyCDFFrameLossAnalyser,  # Frame count & Latency; summary only
    BaseFrameLossAnalyser,  # Frame count; summary & over time
    BaseLatencyFrameLossAnalyser,  # Frame count & Latency; summary & over time
)
# NOTE: Required Python 3.11 or later:
# SupportedAnalysers = Union[*_OverTimeSupportedAnalysersList]
#: :class:`~.flowanalyser.FlowAnalyser` implementations which are supported in
#: the :class:`AnalyserAggregator`.
PossiblySupportedAnalysers = Union[BaseFrameLossAnalyser,
                                   BaseLatencyFrameLossAnalyser,
                                   BaseLatencyCDFFrameLossAnalyser]
# JsonAnalyserAggregator support all analysers
# (it only supports summary results for now)
_SummarySupportedAnalysers = PossiblySupportedAnalysers
# Recursive content type
# ! FIXME - Causes error while generating Sphinx documentation
#         * exception: maximum recursion depth exceeded
#  Content = Mapping[str, Union['Content', str, int, float, bool]]
RecursiveContent = Any  # Woraround to avoid recursion depth error
Content = Mapping[str, Union[RecursiveContent, str, int, float, bool]]


class AnalyserAggregator(ABC):

    # (minimum) number of analysers required for aggregation
    _ANALYSER_COUNT = 2

    __slots__ = (
        '_analysers',
        '_layer2_speed',
    )

    def __init__(self, layer2_speed: Layer2Speed) -> None:
        # This will store the analysers based on their tags.
        # For each of these tags, we will aggregate the resuls
        self._analysers: Mapping[str,
                                 List[PossiblySupportedAnalysers]] = dict()
        self._layer2_speed = layer2_speed

    @abstractmethod
    def supports_analyser(self, analyser: FlowAnalyser) -> bool:
        """Return whether the flow analyser is supported."""
        raise NotImplementedError()

    def order_by_support_level(
        self, analyser_list: List[PossiblySupportedAnalysers]
    ) -> List[PossiblySupportedAnalysers]:
        """Order a list of flow analysers by aggregation support level.

        The flow analysers are ordered by the highest level of support they
        provide for aggregating results. "*Result aggregation support*" covers
        both results over time and summarization.

        :param analyser_list: List of flow analysers to order
        :type analyser_list: List[PossiblySupportedAnalysers]
        :return: List of ordered flow analysers
        :rtype: List[PossiblySupportedAnalysers]
        """
        supported_analyser_list = (analyser for analyser in analyser_list
                                   if self.supports_analyser(analyser))

        def support_level(analyser: PossiblySupportedAnalysers) -> int:
            for level, analyser_type in enumerate(_SUPPORT_LEVEL):
                if isinstance(analyser, analyser_type):
                    return level + 1
            return 0

        sorted_analyser_list = sorted(supported_analyser_list,
                                      key=support_level,
                                      reverse=True)
        return sorted_analyser_list

    def add_analyser(self, analyser: PossiblySupportedAnalysers) -> None:
        for tag in analyser.tags:
            logging.info('%s: Adding analyser %s to tag %s',
                         type(self).__name__, analyser, tag)
            if tag in self._analysers:
                self._analysers[tag].append(analyser)
            else:
                self._analysers[tag] = [analyser]

    def can_render(self) -> bool:
        # Check if we have something to render
        return any((len(analysers) >= self._ANALYSER_COUNT
                    for analysers in self._analysers.values()))

    @staticmethod
    def _parse_key(key: str) -> str:
        if key.endswith('analyser'):
            key = key.rpartition('_')[0]
        return key


class HtmlAnalyserAggregator(AnalyserAggregator):

    def supports_analyser(self, analyser: FlowAnalyser) -> bool:
        """Return whether the flow analyser is supported."""
        return isinstance(analyser, _OverTimeOrSummarySupportedAnalysersList)

    def render(self) -> str:
        # Render our aggregate result
        result = '<h3>Aggregated results</h3>\n'\
            f'<pre>\n{layer2_speed_info(self._layer2_speed)}\n</pre>\n'
        result_charts = ''
        logging.debug('I should render something')

        df_summary = DataFrame(columns=[
            'TX frames',
            'RX frames',
            'Frame loss (%)',
            'TX Bytes',
            'RX Bytes',
            'Byte loss (%)',
            'Duration',
            'Average throughput [kbps]',
            'Status',
        ])

        for key, analysers in self._analysers.items():
            if len(analysers) < self._ANALYSER_COUNT:
                continue

            logging.debug('I can aggregate on %s', key)
            title = AnalyserAggregator._parse_key(key)
            title = title.replace('_', ' ').upper()
            logging.info('Title: %s', title)

            # Summary results

            (
                test_passed,
                total_rx_packets,
                total_tx_packets,
                total_rx_bytes,
                total_tx_bytes,
                timestamp_rx_first,
                timestamp_rx_last,
                latency_results,
            ) = _summarize_analysers(analysers, self._layer2_speed)

            total_packets_loss = total_tx_packets - total_rx_packets
            if total_tx_packets:
                total_packets_relative_loss = \
                    total_packets_loss / total_tx_packets
                total_packets_relative_loss_str = \
                    f'{total_packets_relative_loss:.2f}%'
            else:
                total_packets_relative_loss_str = 'n/a'
            total_bytes_loss = total_tx_bytes - total_rx_bytes
            if total_tx_bytes:
                total_bytes_relative_loss = \
                    total_bytes_loss / total_tx_bytes
                total_bytes_relative_loss_str = \
                    f'{total_bytes_relative_loss:.2f}%'
            else:
                total_bytes_relative_loss_str = 'n/a'
            duration = timestamp_rx_last - timestamp_rx_first
            if duration:
                avg_rx_throughput = \
                    total_rx_bytes / duration.total_seconds() * 8 / 1024
            else:
                avg_rx_throughput = 'n/a'
            df_summary.loc[title] = (
                total_tx_packets,
                total_rx_packets,
                f'{total_packets_loss} ({total_packets_relative_loss_str})',
                total_tx_bytes,
                total_rx_bytes,
                f'{total_bytes_loss} ({total_bytes_relative_loss_str})',
                duration,
                f'{avg_rx_throughput:.2f}',
                'PASSED' if test_passed else 'FAILED',
            )

            # TODO - Add latency summary results

            # Over-time results

            if _analyser_frame_count_over_time(analysers[0]):
                df_tx = analysers[0].df_tx_bytes[['Bytes interval']]
                df_rx = analysers[0].df_rx_bytes[['Bytes interval']]
            else:
                df_tx = DataFrame(columns=['Bytes interval'])
                df_rx = DataFrame(columns=['Bytes interval'])

            for analyser in analysers[1:]:
                if not _analyser_frame_count_over_time(analyser):
                    continue

                logging.debug('Adding extra elements to sum')
                if analyser._layer2_speed != self._layer2_speed:
                    logging.warning('Layer2 speed reporting option mismatch'
                                    ' between analyser and aggregator.'
                                    ' You will see unexpected results!')
                df_tx = df_tx.add(analyser.df_tx_bytes[['Bytes interval']],
                                  fill_value=0)
                df_rx = df_rx.add(analyser.df_rx_bytes[['Bytes interval']],
                                  fill_value=0)

            if df_tx.empty and df_rx.empty:
                continue

            chart = GenericChart('Aggregate Throughput',
                                 x_axis_options={"type": "datetime"},
                                 chart_options={"zoomType": "x"})
            if not df_tx.empty:
                chart.add_series(list(df_tx.itertuples(index=True)), 'line',
                                 'TX', 'Dataspeed', 'byte/s')
            if not df_rx.empty:
                chart.add_series(list(df_rx.itertuples(index=True)), 'line',
                                 'RX', 'Dataspeed', 'byte/s')

            result_charts += f'<h4>{title}</h4>'
            result_charts += chart.plot()

        # Compose the aggregated results:
        result += df_summary.to_html()
        result += result_charts

        return result


class JsonAnalyserAggregator(AnalyserAggregator):

    def supports_analyser(self, analyser: FlowAnalyser) -> bool:
        """Return whether the flow analyser is supported."""
        return isinstance(analyser, _SummarySupportedAnalysersList)

    # Also "aggregate" for a single Analyser (DUT)
    _ANALYSER_COUNT = 1

    def summarize(self) -> Content:
        """Summarize our aggregate result.

        :raises RuntimeError: When we have aggregated result name clashes.
        :return: Dictionary with summary result.
        :rtype: Content
        """
        summary: Content = {
            'layer2_speed': self._layer2_speed,
        }
        logging.debug('I should summarize something')

        for key, analysers in self._analysers.items():
            if len(analysers) < self._ANALYSER_COUNT:
                continue

            logging.debug('I can aggregate on %s', key)
            summary_key = AnalyserAggregator._parse_key(key)
            # Convert to 'camelCase', from dash- and/or space-separated string:
            summary_key = _to_camel_case(summary_key)
            logging.info('Summary key: %r', summary_key)
            if summary_key in summary:
                logging.warning('Overwriting summary results in %r by %r',
                                summary_key, key)
                raise RuntimeError('Overwriting summary results'
                                   f' for {summary_key!r} analysers')

            (
                test_passed,
                total_rx_packets,
                total_tx_packets,
                total_rx_bytes,
                total_tx_bytes,
                timestamp_rx_first,
                timestamp_rx_last,
                latency_results,
            ) = _summarize_analysers(analysers, self._layer2_speed)

            test_summary = {
                'status': {
                    'passed': test_passed,
                },
                'sent': {
                    'bytes': total_tx_bytes,
                    'packets': total_tx_packets,
                },
                'received': {
                    'bytes': total_rx_bytes,
                    'packets': total_rx_packets,
                },
            }

            if latency_results:
                (
                    final_min_latency,
                    final_max_latency,
                    final_avg_latency,
                    final_avg_jitter,
                ) = latency_results
                test_summary['latency'] = {
                    'minimum': final_min_latency,
                    'maximum': final_max_latency,
                    'average': final_avg_latency,
                    'jitter': final_avg_jitter,
                }

            summary[summary_key] = test_summary

        return summary


def _summarize_analysers(
    analysers: List[PossiblySupportedAnalysers], layer2_speed: Layer2Speed
) -> Tuple[bool, int, int, int, int, Timestamp, Timestamp, Optional[Tuple[
        float, float, float, float]]]:
    test_passed = analysers[0].has_passed
    total_rx_packets = analysers[0].total_rx_packets
    total_tx_packets = analysers[0].total_tx_packets
    total_rx_bytes = analysers[0].total_rx_bytes
    total_tx_bytes = analysers[0].total_tx_bytes
    timestamp_rx_first = analysers[0].timestamp_rx_first
    timestamp_rx_last = analysers[0].timestamp_rx_last
    has_latency = False
    final_min_latency: Optional[float] = None
    final_max_latency: Optional[float] = None
    final_avg_latency: float = 0
    final_avg_jitter: float = 0

    if _analyser_has_latency_summary(analysers[0]):
        has_latency = True
        final_min_latency = analysers[0].final_min_latency
        final_max_latency = analysers[0].final_max_latency
        final_avg_latency = analysers[0].final_avg_latency
        final_avg_jitter = analysers[0].final_avg_jitter

    for analyser in analysers[1:]:
        logging.debug('Adding extra counters to sum')
        test_passed = test_passed and analyser.has_passed
        rx_packets = analyser.total_rx_packets
        tx_packets = analyser.total_tx_packets
        rx_bytes = analyser.total_rx_bytes
        tx_bytes = analyser.total_tx_bytes
        ts_rx_first = analyser.timestamp_rx_first
        ts_rx_last = analyser.timestamp_rx_last

        if _analyser_has_latency_summary(analyser):
            logging.debug('Adding extra latency to sum')
            has_latency = True
            min_latency = analyser.final_min_latency
            max_latency = analyser.final_max_latency
            avg_latency = analyser.final_avg_latency
            avg_jitter = analyser.final_avg_jitter
            if (final_min_latency is None or min_latency < final_min_latency):
                final_min_latency = min_latency
            if (final_max_latency is None or max_latency > final_max_latency):
                final_max_latency = max_latency
            # Update weighted average latency and jitter:
            final_avg_latency = ((final_avg_latency * total_rx_packets +
                                  avg_latency * rx_packets) /
                                 (total_rx_packets + rx_packets))
            final_avg_jitter = ((final_avg_jitter * total_rx_packets +
                                 avg_jitter * rx_packets) /
                                (total_rx_packets + rx_packets))

        total_rx_packets += rx_packets
        total_tx_packets += tx_packets
        total_rx_bytes += rx_bytes
        total_tx_bytes += tx_bytes
        if timestamp_rx_first < ts_rx_first:
            timestamp_rx_first = ts_rx_first
        if ts_rx_last > timestamp_rx_last:
            timestamp_rx_last = ts_rx_last

    if layer2_speed == Layer2Speed.frame:
        pass
    elif layer2_speed == Layer2Speed.frame_with_fcs:
        # NOTE - These calculations are correct when no data received too

        total_tx_bytes += ETHERNET_FCS_LENGTH * total_tx_packets
        total_rx_bytes += ETHERNET_FCS_LENGTH * total_rx_packets
    else:
        raise ValueError(f'Unsupported Layer 2 speed: {layer2_speed}')

    if has_latency:
        latency_results = (
            final_min_latency,
            final_max_latency,
            final_avg_latency,
            final_avg_jitter,
        )
    else:
        latency_results = None

    return (
        test_passed,
        total_rx_packets,
        total_tx_packets,
        total_rx_bytes,
        total_tx_bytes,
        timestamp_rx_first,
        timestamp_rx_last,
        latency_results,
    )


def _analyser_frame_count_over_time(
        analyser: _SummarySupportedAnalysers) -> bool:
    return isinstance(analyser, _OverTimeSupportedAnalysersList)


def _analyser_has_latency_summary(
        analyser: _SummarySupportedAnalysers) -> bool:
    return isinstance(analyser, _SummaryLatencyAnalysers)


def _to_camel_case(key: str) -> str:
    """Convert to ``camelCase``, from dash- and/or space-separated string.

    :param key: Key to convert
    :type key: str
    :return: Key in camelCase format.
    :rtype: str
    """
    keys = key.split(' ')
    keys = [k.split('_') for k in keys]
    keys = [k.title() for kk in keys for k in kk]
    keys[0] = keys[0].lower()
    return ''.join(keys)
