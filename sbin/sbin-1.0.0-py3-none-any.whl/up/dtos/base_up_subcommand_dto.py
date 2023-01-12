import abc
from typing import Optional

from bin.up.up_subcommand import UpSubcommand


class BaseUpSubcommandDto(abc.ABC):
    @abc.abstractmethod
    def to_up_subcommand(self) -> Optional[UpSubcommand]:
        pass

    @abc.abstractmethod
    def to_down_subcommand(self) -> Optional[UpSubcommand]:
        pass
