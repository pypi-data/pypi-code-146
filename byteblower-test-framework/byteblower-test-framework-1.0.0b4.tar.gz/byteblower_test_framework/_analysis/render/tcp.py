from ..data_analysis.tcp import HttpDataAnalyser
from ..plotting import GenericChart
from .renderer import Renderer


class HttpRenderer(Renderer):

    __slots__ = ('_data_analyser', )

    def __init__(self, data_analyser: HttpDataAnalyser) -> None:
        super().__init__()
        self._data_analyser = data_analyser

    def render(self) -> str:
        analysis_log = self._data_analyser.log

        # Get the data
        # df_tx = self._data_analyser.df_tx
        # df_rx = self._data_analyser.df_rx
        df_dataspeed = self._data_analyser.df_dataspeed

        # Set the summary
        result = self._verbatim(analysis_log)

        # Build the graph
        chart = GenericChart("HTTP statistics",
                             x_axis_options={"type": "datetime"},
                             chart_options={"zoomType": "x"})
        # chart.add_series(list(df_tx.itertuples(index=True)), "line", "TX",
        #                  "Data count", "bytes")
        # chart.add_series(list(df_rx.itertuples(index=True)), "line", "RX",
        #                  "Data count", "bytes")
        chart.add_series(list(df_dataspeed.itertuples(index=True)), "line",
                         "AVG dataspeed", "Dataspeed", "bytes/s")
        result += chart.plot()

        return result
