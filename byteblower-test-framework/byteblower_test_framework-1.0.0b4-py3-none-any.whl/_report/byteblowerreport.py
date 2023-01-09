"""Module for abstract ByteBlower report interface definition."""
# NOTE: does not work on class property:
# from abc import abstractproperty
from abc import ABC, abstractmethod
from os import getcwd
from os.path import join
from time import gmtime, strftime
from typing import Optional  # for type hinting

from pandas import DataFrame  # for type hinting

from .._traffic.flow import Flow  # for type hinting


class ByteBlowerReport(ABC):
    """Abstract ByteBlower Report interface definition."""

    # @abstractproperty
    _FILE_FORMAT: str = ''

    __slots__ = (
        '_output_dir',
        '_filename',
    )

    def __init__(self,
                 output_dir: Optional[str] = None,
                 filename_prefix: str = 'byteblower',
                 filename: Optional[str] = None) -> None:
        """Create a ByteBlower report generator.

        The report is stored under ``<output_dir>``. The default structure
        of the file name is

           ``<prefix>_<timestamp>.<ext>``

        where:

        * ``<output_dir>``:  Configurable via ``output_dir``.
          Defaults to the current working directory.
        * ``<prefix>``: Configurable via ``filename_prefix``
        * ``<timestamp>``: Current time. Defined at construction time of the
          ``ByteBlowerReport`` Python object.
        * ``<ext>``: Output type specific file extension.

        :param output_dir: Override the directory where
           the report file is stored, defaults to ``None``
           (meaning that the "current directory" will be used)
        :type output_dir: str, optional
        :param filename: Override the complete filename of the report,
           defaults to ``None``
        :type filename: str, optional
        :param filename_prefix: Prefix for the ByteBlower report file name,
           defaults to 'byteblower'
        :type filename_prefix: str, optional
        """
        self._output_dir = output_dir or getcwd()
        self._filename: str = filename or '_'.join(
            (filename_prefix, strftime('%Y%m%d_%H%M%S', gmtime())))

    @property
    def report_url(self) -> str:
        """Return the name and location of the generated report.

        :return: Name and location of the generated report.
        :rtype: str
        """
        return self._report_path(self._FILE_FORMAT)

    @abstractmethod
    def add_flow(self, flow: Flow) -> None:
        """Add the flow info.

        :param flow: Flow to add the information for
        :type flow: Flow
        """
        raise NotImplementedError()

    @abstractmethod
    def render(self, api_version: str, port_list: DataFrame) -> None:
        """Render the report.

        :param port_list: Configuration of the ByteBlower Ports.
        :type port_list: DataFrame
        """
        raise NotImplementedError()

    @abstractmethod
    def clear(self) -> None:
        """Start with empty report contents."""
        raise NotImplementedError()

    def _report_path(self, file_format: str) -> str:
        """Return the complete path of the report file.

        :param file_format: File format of the file,
           defines the file extension.
        :type file_format: str
        :raises ValueError: When requesting an unsupported file format.
        :return: Path to the report file.
        :rtype: str
        """
        if file_format.lower() == 'html':
            return join(self._output_dir, self._filename + '.html')
        if file_format.lower() == 'xml':
            return join(self._output_dir, self._filename + '.xml')
        if file_format.lower() == 'json':
            return join(self._output_dir, self._filename + '.json')

        raise ValueError('Format not supported')
