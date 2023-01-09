"""Module for reporting in JSON format."""
import logging
from enum import Enum
from typing import Any, Mapping, Optional, Union  # for type hinting

from pandas import DataFrame  # for type hinting
from pandas import Timestamp

from .._analysis.analyseraggregator import JsonAnalyserAggregator
from .._analysis.flow_analyser import FlowAnalyser  # for type hinting
from .._traffic.flow import Flow  # for type hinting
from .byteblowerreport import ByteBlowerReport
from .options import Layer2Speed

try:
    import simplejson as json
except ImportError:
    import json

# Type aliases
# Recursive content type:
_Content = Mapping[str, Union['_Content', str, int, float, bool]]


class ByteBlowerJsonReport(ByteBlowerReport):
    """Generate report in JSON format.

    Generates summary information of test status,
    test configuration and results from all flows.

    This report contains:

    * Global test status
    * Port configuration (**to-do**)
    * Correlated results

       * Aggregated results over all flows
         (supporting aggregation of *over time* data (**to-do**)
         and *summary* data)
    * Per-flow results (**to-do**)

       * Flow configuration
       * Results for all Analysers attached to the flow
    """

    _FILE_FORMAT: str = 'json'

    __slots__ = (
        '_layer2_speed',
        '_analyseraggregator',
        '_config',
        '_summary',
        '_flows',
    )

    def __init__(
            self,
            output_dir: Optional[str] = None,
            filename_prefix: str = 'byteblower',
            filename: Optional[str] = None,
            layer2_speed: Optional[Layer2Speed] = Layer2Speed.frame) -> None:
        """Create a ByteBlower JSON report generator.

        The report is stored under ``<output_dir>``. The default structure
        of the file name is

           ``<prefix>_<timestamp>.json``

        where:

        * ``<output_dir>``:  Configurable via ``output_dir``.
          Defaults to the current working directory.
        * ``<prefix>``: Configurable via ``filename_prefix``
        * ``<timestamp>``: Current time. Defined at construction time of the
          ``ByteBlowerReport`` Python object.

        :param output_dir: Override the directory where
           the report file is stored, defaults to ``None``
           (meaning that the "current directory" will be used)
        :type output_dir: str, optional
        :param filename_prefix: Prefix for the ByteBlower report file name,
           defaults to 'byteblower'
        :type filename_prefix: str, optional
        :param filename: Override the complete filename of the report,
           defaults to ``None``
        :type filename: str, optional
        :param layer2_speed: Configuration setting to select the layer 2
           speed reporting, defaults to :attr:`~.options.Layer2Speed.frame`
        :type layer2_speed: ~options.Layer2Speed, optional
        """
        super().__init__(output_dir=output_dir,
                         filename_prefix=filename_prefix,
                         filename=filename)
        self._layer2_speed = layer2_speed
        self._analyseraggregator = JsonAnalyserAggregator(
            layer2_speed=self._layer2_speed)
        self._reset_content()

    def add_flow(self, flow: Flow) -> None:
        """Add the flow info.

        :param flow: Flow to add the information for
        :type flow: Flow
        """
        aggregated_analyser: Optional[FlowAnalyser] = None
        sorted_analysers = self._analyseraggregator.order_by_support_level(
            flow._analysers)
        for analyser in sorted_analysers:
            if not analyser.has_passed:
                self._summary['status']['passed'] = False
            # NOTE - Avoid aggregating twice with the same Flow data
            if not aggregated_analyser:
                logging.debug('Aggregating supported analyser %s',
                              type(analyser).__name__)
                self._analyseraggregator.add_analyser(analyser)
                aggregated_analyser = analyser

    def render(self, api_version: str, port_list: DataFrame) -> None:
        """Render the report.

        :param port_list: Configuration of the ByteBlower Ports.
        :type port_list: DataFrame
        """
        # TODO - Render the config (from port_list)

        correlation_dict = self._summarize_aggregators()
        if correlation_dict:
            self._summary['aggregated'] = correlation_dict

        content = {
            'apiVersion': api_version,
            'config': self._config,
            'summary': self._summary,
            'flows': self._flows,
        }

        with open(self.report_url, 'w') as f:
            json.dump(content, f, default=_extra_encode_json)

    def clear(self) -> None:
        """Start with empty report contents."""
        self._analyseraggregator = JsonAnalyserAggregator(
            layer2_speed=self._layer2_speed)
        self._reset_content()

    def _reset_content(self) -> None:
        self._config: _Content = dict()
        self._summary: _Content = {
            'status': {
                'passed': True,
            },
        }
        self._flows: _Content = dict()

    def _summarize_aggregators(self) -> Optional[_Content]:
        # Check if we can do aggregation
        if not self._analyseraggregator.can_render():
            # Get the summary from the aggregator
            return
        return self._analyseraggregator.summarize()


def _extra_encode_json(o: Any) -> Any:
    if isinstance(o, Timestamp):
        return o.isoformat()

    if isinstance(o, Enum):
        return o.value

    # Let the base class default method raise the TypeError
    # return JSONEncoder.default(self, o)
    raise TypeError(f'Object of type {o.__class__.__name__} '
                    'is not JSON serializable')
