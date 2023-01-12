import abc
from typing import List

from bin.process.helpable import Helpable
from bin.process.process import Process


class Command(abc.ABC):
    """
    This abstract class implements the template pattern in order for --help to work
    with all available commands. In order for the Template pattern to make sense, all
    concretions must implement both Command#_run and Command#_get_help protected methods
    """

    def run(self, process: Process, args: List[str]) -> Process:
        if self.__should_run_help(args):
            process.log_help(self._get_help())
            return process

        return self._run(process, args)

    @abc.abstractmethod
    def _run(self, process: Process, args: List[str]) -> Process:
        pass

    @abc.abstractmethod
    def _get_short_description(self) -> str:
        pass

    @abc.abstractmethod
    def _get_help(self) -> Helpable:
        pass

    def __should_run_help(self, args: List[str]) -> bool:
        return len(args) > 0 and args[0] in ("-h", "--help")
