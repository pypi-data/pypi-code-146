import abc
from typing import Optional

from bin.process.process import Process


class Requirement(abc.ABC):
    @abc.abstractmethod
    def is_met(self, process: Process) -> bool:
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_help(self) -> Optional[str]:
        pass
