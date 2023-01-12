from typing import Dict

from bin.commands.command import Command
from bin.custom_commands.command_tree import CommandTree
from bin.custom_commands.dtos import CustomCommandsDto
from bin.custom_commands.dtos.command_tree_dto import CommandTreeDto


class CustomCommandsMapper:
    @staticmethod
    def to_command_dict(dto: CustomCommandsDto) -> Dict[str, Command]:
        if len(dto) == 0:
            return {}

        tmp_name = "__root__"
        command_tree = CommandTreeDto(subcommands=dto).to_command(tmp_name).get("__root__")
        if not isinstance(command_tree, CommandTree):
            return {}

        return command_tree.subcommands_tree
