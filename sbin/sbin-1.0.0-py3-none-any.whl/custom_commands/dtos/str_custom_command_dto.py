from typing import Dict

from bin.commands.command import Command
from bin.custom_commands.basic_command import BasicCommand
from bin.custom_commands.dtos.base_custom_command_dto import BaseCustomCommandDto
from bin.models.str_command import StrCommand


class StrCustomCommandDto(StrCommand, BaseCustomCommandDto):
    @classmethod
    def validate(cls, v: str) -> "StrCustomCommandDto":
        StrCommand.validate(v)

        return StrCustomCommandDto(v)

    def to_command(self, self_name: str) -> Dict[str, Command]:
        return {self_name: BasicCommand.no_help(self)}
