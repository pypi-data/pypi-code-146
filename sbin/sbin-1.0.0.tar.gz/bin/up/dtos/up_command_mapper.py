from typing import List

from bin.commands.command import Command
from bin.up.down_command import DownCommand
from bin.up.dtos import UpSubcommandDto
from bin.up.up_command import UpCommand


class UpCommandMapper:
    @staticmethod
    def to_up_command(dtos: List[UpSubcommandDto]) -> Command:
        subcommands = [d.to_up_subcommand() for d in dtos]

        return UpCommand(subcommands=[s for s in subcommands if s is not None])

    @staticmethod
    def to_down_command(dtos: List[UpSubcommandDto]) -> Command:
        subcommands = [d.to_down_subcommand() for d in dtos]

        return DownCommand(subcommands=[s for s in subcommands if s is not None])
