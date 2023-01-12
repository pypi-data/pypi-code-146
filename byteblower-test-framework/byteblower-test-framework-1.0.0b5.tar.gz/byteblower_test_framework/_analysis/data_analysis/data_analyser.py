"""Contains the data analyser interface definition."""


class DataAnalyser(object):
    """Data analyser interface definition."""

    __slots__ = (
        '_result',
        '_log',
    )

    def __init__(self) -> None:
        """Make a new data analyser."""
        self._result: bool = False
        self._log: str = ''

    def analyse(self) -> None:
        """
        Analyse the gathered data.

        .. note::
           Virtual method.
        """
        pass

    @property
    def has_passed(self) -> bool:
        """Return whether the test passed or not."""
        return self._result

    @property
    def log(self) -> str:
        """Return the analysis summary log."""
        return self._log

    def _set_result(self, result: bool) -> None:
        self._result = result

    def _set_log(self, log: str) -> None:
        self._log = log
