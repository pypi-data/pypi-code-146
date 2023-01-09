import logging

from ..data_analysis.frameblasting import (
    FrameCountAnalyser,
    LatencyAnalyser,
    LatencyCDFAnalyser,
    MosAnalyser,
)
from ..plotting import GenericChart
from .renderer import Renderer


class FrameCountRenderer(Renderer):

    __slots__ = ('_data_analyser', )

    def __init__(self, data_analyser: FrameCountAnalyser) -> None:
        super().__init__()
        self._data_analyser = data_analyser

    def render(self) -> str:
        analysis_log = self._data_analyser.log

        # Get the data
        df_tx = self._data_analyser.df_tx_bytes
        df_rx = self._data_analyser.df_rx_bytes

        # Set the summary
        result = self._verbatim(analysis_log)

        # Build the graph
        chart = GenericChart("Throughput",
                             x_axis_options={"type": "datetime"},
                             chart_options={"zoomType": "x"})
        chart.add_series(list(df_tx.itertuples(index=True)), "line", "TX",
                         "Dataspeed", "byte/s")
        chart.add_series(list(df_rx.itertuples(index=True)), "line", "RX",
                         "Dataspeed", "byte/s")
        result += chart.plot()

        return result


class LatencyFrameCountRenderer(Renderer):

    __slots__ = (
        '_framecount_analyser',
        '_latency_analyser',
    )

    def __init__(self, framecount_analyser: FrameCountAnalyser,
                 latency_analyser: LatencyAnalyser) -> None:
        super().__init__()
        self._framecount_analyser = framecount_analyser
        self._latency_analyser = latency_analyser

    def render(self) -> str:
        analysis_log = '\n'.join(
            (self._framecount_analyser.log, self._latency_analyser.log))

        # Get the data
        df_rx = self._framecount_analyser.df_rx_bytes
        df_latency_min = self._latency_analyser.df_latency_min
        df_latency_max = self._latency_analyser.df_latency_max
        df_latency_avg = self._latency_analyser.df_latency_avg
        df_latency_jitter = self._latency_analyser.df_latency_jitter

        # Set the summary
        result = self._verbatim(analysis_log)

        # Build the graph
        chart = GenericChart("Flow results",
                             x_axis_options={"type": "datetime"},
                             chart_options={"zoomType": "x"})
        chart.add_series(list(df_rx.itertuples(index=True)), "line", "RX",
                         "Dataspeed", "byte/s")
        chart.add_series(list(df_latency_min.itertuples(index=True)), "line",
                         "Minimum", "Latency", "Milliseconds")
        chart.add_series(list(df_latency_max.itertuples(index=True)), "line",
                         "Maximum", "Latency", "Milliseconds")
        chart.add_series(list(df_latency_avg.itertuples(index=True)), "line",
                         "Average", "Latency", "Milliseconds")
        chart.add_series(list(df_latency_jitter.itertuples(index=True)),
                         "line", "Jitter", "Latency", "Milliseconds")
        result += chart.plot()

        return result


class LatencyCDFRenderer(Renderer):

    __slots__ = (
        '_framecount_analyser',
        '_latency_cdf_analyser',
    )

    def __init__(self, framecount_analyser: FrameCountAnalyser,
                 latency_cdf_analyser: LatencyCDFAnalyser) -> None:
        super().__init__()
        self._framecount_analyser = framecount_analyser
        self._latency_cdf_analyser = latency_cdf_analyser

    def render(self) -> str:
        analysis_log = '\n'.join(
            (self._framecount_analyser.log, self._latency_cdf_analyser.log))

        # Get the data
        df = self._latency_cdf_analyser.df_latency
        df["Latency"] = df["Latency"] / (1000 * 1000.0)
        df = df.set_index("Latency")
        logging.debug(df)

        # Set the summary
        result = self._verbatim(analysis_log)

        rxpacketstotal = self._latency_cdf_analyser.packet_count_valid
        if not rxpacketstotal:
            return result

        # Build the graph
        chart = GenericChart(
            "Latency CCDF",
            x_axis_title="Latency [ms]",
            chart_options={"zoomType": "x"},
            x_axis_options={"labels": {
                "format": "{value} ms"
            }},
        )

        chart.add_series(
            list(df.itertuples(index=True)),
            "line",
            "",
            "",
            "",
            y_axis_options={
                # "reversed": "true",
                "labels": {
                    "formatter":
                    "function() {"
                    " let str = 'P';"
                    " str += (100.0 - this.value);"
                    " return str }"
                },
                "type": "logarithmic",
                "tickInterval": 1,
                "minorTickInterval": 0.1,
                "endOnTick": "true",
                "gridLineWidth": 1,
                "max": 100.0,
                "min": 0.1,
            },
        )
        result += chart.plot()

        return result


class MosRenderer(Renderer):

    __slots__ = ('_analyser', )

    def __init__(self, analyser: MosAnalyser) -> None:
        super().__init__()
        self._analyser = analyser

    def render(self) -> str:
        analysis_log = self._analyser.log

        # Get the data
        df_tx = self._analyser.df_tx_bytes
        df_rx = self._analyser.df_rx_bytes
        has_rx = self._analyser.has_rx
        df_latency_min = self._analyser.df_latency_min
        df_latency_max = self._analyser.df_latency_max
        df_latency_avg = self._analyser.df_latency_avg
        df_latency_jitter = self._analyser.df_latency_jitter

        # Set the summary
        result = self._verbatim(analysis_log)

        if not has_rx:
            return result

        # Build the graph
        chart = GenericChart("Flow results",
                             x_axis_options={"type": "datetime"},
                             chart_options={"zoomType": "x"})
        chart.add_series(list(df_tx.itertuples(index=True)), "line", "TX",
                         "Dataspeed", "byte/s")
        chart.add_series(list(df_rx.itertuples(index=True)), "line", "RX",
                         "Dataspeed", "byte/s")
        chart.add_series(list(df_latency_min.itertuples(index=True)), "line",
                         "Minimum", "Latency", "Milliseconds")
        chart.add_series(list(df_latency_max.itertuples(index=True)), "line",
                         "Maximum", "Latency", "Milliseconds")
        chart.add_series(list(df_latency_avg.itertuples(index=True)), "line",
                         "Average", "Latency", "Milliseconds")
        chart.add_series(list(df_latency_jitter.itertuples(index=True)),
                         "line", "Jitter", "Latency", "Milliseconds")
        result += chart.plot()

        return result
