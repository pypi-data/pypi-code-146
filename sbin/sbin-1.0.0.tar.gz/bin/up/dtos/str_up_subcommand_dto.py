from typing import Optional

from bin.models.str_command import StrCommand
from bin.up.dtos.base_up_subcommand_dto import BaseUpSubcommandDto
from bin.up.simple_up_subcommand import SimpleUpSubcommand
from bin.up.up_subcommand import UpSubcommand


class StrUpSubcommandDto(StrCommand, BaseUpSubcommandDto):
    @classmethod
    def validate(cls, v: str) -> "StrUpSubcommandDto":
        StrCommand.validate(v)

        return StrUpSubcommandDto(v)

    def to_up_subcommand(self) -> Optional[UpSubcommand]:
        return SimpleUpSubcommand(name=self, run_cmd=self)

    def to_down_subcommand(self) -> Optional[UpSubcommand]:
        return None
