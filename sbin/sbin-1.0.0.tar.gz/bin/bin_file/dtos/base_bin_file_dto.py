import abc
from typing import Any, Dict, Type

from bin.commands.command import Command


class BaseBinFileDto(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def parse_obj_explicitly(cls: Type["BaseBinFileDto"], data: Dict[str, Any]) -> "BaseBinFileDto":
        """
        The purpose of this method is to raise pretty errors instead of pydantic default ValidationError

        raises CommandParseError with pretty message when Dto.parse_obj(data) fails

        returns Dto.parse_obj(data) when data is correct
        """

    @abc.abstractmethod
    def to_command(self) -> Command:
        pass
