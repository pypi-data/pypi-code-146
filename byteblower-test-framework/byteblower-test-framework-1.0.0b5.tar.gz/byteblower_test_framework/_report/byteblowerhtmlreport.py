"""Module for reporting in HTML format."""
import logging
from os.path import abspath, dirname, join
from typing import List, Optional  # for type hinting

from jinja2 import Environment, FileSystemLoader
from pandas import DataFrame  # for type hinting

from .._analysis.analyseraggregator import HtmlAnalyserAggregator
from .._analysis.flow_analyser import FlowAnalyser  # for type hinting
from .._traffic.flow import Flow  # for type hinting
from .byteblowerreport import ByteBlowerReport
from .helper import snake_to_title
from .options import Layer2Speed

_PACKAGE_DIRECTORY = dirname(abspath(__file__))

_FLOW_CONFIG_ROW_TMPL = \
    '<tr><th>{name}</th> <td>{value!s}</td></tr>'
_FLOW_PORT_INFO_TMPL = '{name} ({ip!s})'


class ByteBlowerHtmlReport(ByteBlowerReport):
    """Generate a report in HTML format.

    Generates summary information of test status,
    test configuration and results from all flows.

    This report contains:

    * A global PASS/FAIL result
    * Port configuration table
    * Correlated results

       * Aggregated results over all flows
         (supporting aggregation of *over time* graphs and *summary* table)
    * Per-flow results

       * Flow configuration
       * Results for all Analysers attached to the flow
    """

    _FILE_FORMAT: str = 'html'

    __slots__ = (
        '_title',
        '_test_passed',
        '_layer2_speed',
        '_env',
        '_template',
        '_test_section_template',
        '_flow_section_template',
        '_flows',
        '_analyseraggregator',
    )

    def __init__(
            self,
            output_dir: Optional[str] = None,
            filename_prefix: str = 'byteblower',
            filename: Optional[str] = None,
            layer2_speed: Optional[Layer2Speed] = Layer2Speed.frame) -> None:
        """Create a ByteBlower HTML report generator.

        The report is stored under ``<output_dir>``. The default structure
        of the file name is

           ``<prefix>_<timestamp>.html``

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
        self._title: str = 'ByteBlower report'
        self._test_passed: bool = True
        # Configure Jinja and ready the template
        self._env = Environment(loader=FileSystemLoader(
            searchpath=join(_PACKAGE_DIRECTORY, 'templates')))
        self._template = self._env.get_template('report.html')
        self._test_section_template = self._env.get_template(
            'test_section.html')
        self._flow_section_template = self._env.get_template(
            'flow_section.html')
        self._flows: List[str] = list()
        self._analyseraggregator = HtmlAnalyserAggregator(
            layer2_speed=self._layer2_speed)

    def add_flow(self, flow: Flow) -> None:
        """Add the flow info.

        :param flow: Flow to add the information for
        :type flow: Flow
        """
        self._render_flow(flow)
        aggregated_analyser: Optional[FlowAnalyser] = None
        sorted_analysers = self._analyseraggregator.order_by_support_level(
            flow._analysers)
        for analyser in sorted_analysers:
            if not analyser.has_passed:
                self._test_passed = False
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
        correlation_html = self._render_aggregators()

        with open(self.report_url, 'w') as f:
            if self._test_passed is True:
                pass_or_fail = '<font size="4" color="green">PASS</font>'
            else:
                pass_or_fail = '<font size="4" color="red">FAIL</font>'
            f.write(
                self._template.render(
                    title=self._title,
                    passorfail=pass_or_fail,
                    api_version=api_version,
                    ports=port_list.to_html(),
                    correlated=correlation_html,
                    flows=self._flows,
                ))

    def clear(self) -> None:
        """Start with empty report contents."""
        self._flows = list()
        self._analyseraggregator = HtmlAnalyserAggregator(
            layer2_speed=self._layer2_speed)

    # def _render_flow(self, name, type, source, destination, config, tests):
    def _render_flow(self, flow: Flow) -> None:
        tests = ''
        for analyser in flow._analysers:
            tests += self._render_test(analyser.type, analyser.has_passed,
                                       analyser.render())
        config = ""
        for k in flow._CONFIG_ELEMENTS:
            if k in ('analysers', 'source', 'destination', 'name', 'type'):
                continue
            config += _FLOW_CONFIG_ROW_TMPL.format(name=snake_to_title(k),
                                                   value=getattr(flow, k))

        source = _FLOW_PORT_INFO_TMPL.format(name=flow.source.name,
                                             ip=flow.source.ip)
        destination = _FLOW_PORT_INFO_TMPL.format(name=flow.destination.name,
                                                  ip=flow.destination.ip)
        self._flows.append(
            self._flow_section_template.render(
                name=flow.name,
                type=flow.type,
                source=source,
                destination=destination,
                config=config,
                tests=tests,
            ))

    def _render_test(self, test: str, has_passed: bool, log: str) -> str:
        """Render the log from the test scenario."""
        if has_passed:
            pass_or_fail = '<font size="3" color="green">PASS</font>'
        else:
            pass_or_fail = '<font size="3" color="red">FAIL</font>'
        return self._test_section_template.render(test=test,
                                                  passorfail=pass_or_fail,
                                                  log=log)

    def _render_aggregators(self) -> Optional[str]:
        # Check if we can do aggregation
        if not self._analyseraggregator.can_render():
            return
        # Render the aggregator
        return self._analyseraggregator.render()
