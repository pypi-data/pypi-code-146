from .._traffic.tcpflow import TcpFlow  # for type hinting
from .data_analysis.tcp import HttpDataAnalyser
from .data_gathering.tcp import HttpDataGatherer
from .flow_analyser import FlowAnalyser
from .render.tcp import HttpRenderer
from .storage.tcp import HttpData


class HttpAnalyser(FlowAnalyser):
    """Analyse HTTP and TCP statistics over time.

    The analyser currently only provides the HTTP goodput over time
    and the average HTTP goodput over the duration of the test.

    .. todo::
       There is no specific analysis performed and the test
       will always pass.

    This analyser is intended for use with a :class:`~.traffic.HTTPFlow`.

    Supports:

    * Analysis of a single flow

    .. warning::
        Does not support aggregation data from multiple flows
        (via :class:`~.analysis.AnalyserAggregator`).
    """

    __slots__ = (
        '_http_data',
        '_data_gatherer',
        '_data_analyser',
        '_renderer',
    )

    def __init__(self):
        """Create the HTTP and TCP statistics over time analyser."""
        super().__init__("HTTP analyser")
        self._http_data = HttpData()
        self._data_gatherer = None
        self._data_analyser = None
        self._renderer = None

    @property
    def flow(self) -> TcpFlow:
        """Return Flow implementation.

        Useful for correct type hinting.
        """
        return self._flow

    def _initialize(self) -> None:
        self._data_gatherer = HttpDataGatherer(self._http_data,
                                               self.flow._bb_tcp_clients)
        self._data_analyser = HttpDataAnalyser(self._http_data)
        self._renderer = HttpRenderer(self._data_analyser)

    def apply(self) -> None:
        self._data_gatherer.prepare()

    def process(self) -> None:
        self._data_gatherer.process()

    def updatestats(self) -> None:
        """Analyse the result.

        What would be bad?

        * TCP sessions not going to Finished
        """
        # Let's analyse the result
        self._data_gatherer.updatestats()

    def analyse(self) -> None:
        # Currently, no pass/fail criteria.
        self._data_gatherer.summarize()
        self._data_analyser.analyse()
        self._set_result(self._data_analyser.has_passed)

    @property
    def log(self) -> str:
        """Return the summary log text.

        .. note::
           Used for unit test report.

        :return: Summary log text.
        :rtype: str
        """
        return self._data_analyser.log

    def render(self) -> str:
        return self._renderer.render()
