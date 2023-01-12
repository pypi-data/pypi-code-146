import abc
from typing import Dict

from bin.commands.command import Command


class BaseCustomCommandDto(abc.ABC):
    @abc.abstractmethod
    def to_command(self, self_name: str) -> Dict[str, Command]:
        pass
