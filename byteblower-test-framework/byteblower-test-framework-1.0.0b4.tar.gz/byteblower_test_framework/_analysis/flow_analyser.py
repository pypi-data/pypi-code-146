# import base64
import logging
from abc import ABC, abstractmethod, abstractproperty
# from io import BytesIO
from typing import List, Sequence  # for type hinting

from pandas import DataFrame  # for type hinting

from .._traffic.flow import Flow  # for type hinting


class FlowAnalyser(ABC):
    """Base class for a flow analyser implementation."""

    __slots__ = (
        '_flow',
        '_result',
        '_type',
        '_tags',
    )

    def __init__(self, type: str) -> None:
        """Create a flow analyser base.

        :param type: Descriptive type for the flow analyser implementation.
        :type type: str
        """
        self._flow: Flow = None
        self._result: bool = False
        # self._type: str = self.__class__.__name__
        self._type: str = type
        self._tags: List[str] = []

    def apply(self) -> None:
        """
        .. note::
           Virtual method.
        """
        pass

    def process(self) -> None:
        """
        .. note::
           Virtual method.
        """
        return

    def updatestats(self) -> None:
        """
        .. note::
           Virtual method.
        """
        pass

    def analyse(self) -> None:
        """
        .. note::
           Virtual method.
        """
        return

    @abstractmethod
    def render(self) -> str:
        """
        .. note::
           Virtual method.
        """

    def add_tag(self, new_tag: str) -> None:
        new_tag = new_tag.lower()
        if new_tag not in self._tags:
            self._tags.append(new_tag)

    # def add_fig(self, fig) -> str:
    #     io = BytesIO()
    #     fig.savefig(io, format="png")
    #     data = base64.encodestring(io.getvalue()).decode("utf-8")
    #     html = '<img src="data:image/png;base64,{}"/>'
    #     html = html.format(data)
    #     return html

    @property
    def type(self) -> str:
        return self._type

    @property
    def tags(self) -> Sequence[str]:
        return self._tags

    @property
    def has_passed(self) -> bool:
        """Return whether the test passed or not."""
        return self._result

    @abstractproperty
    def log(self) -> str:
        """Return the summary log text.

        .. note::
           Used for unit test report.

        :return: Summary log text.
        :rtype: str
        """
        raise NotImplementedError(f'{type(self)}: Analyser log.')

    @property
    def df_tx_bytes(self) -> DataFrame:
        """
        Return ``DataFrame`` of transmitted bytes per interval.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        raise NotImplementedError(f'{type(self)}: TX bytes data frame.')

    @property
    def df_rx_bytes(self) -> DataFrame:
        """
        Return ``DataFrame`` of received bytes per interval.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        raise NotImplementedError(f'{type(self)}: RX bytes data frame.')

    def _add_to_flow(self, flow: Flow) -> None:
        if self._flow is not None:
            raise ValueError(f'Already added to Flow {self._flow.name!r}')

        self._flow = flow
        for tag in flow._tags:
            self.add_tag(tag)
        logging.debug(self._tags)
        self._initialize()

    @abstractmethod
    def _initialize(self) -> None:
        pass

    def _set_result(self, result: bool) -> None:
        self._result = result
