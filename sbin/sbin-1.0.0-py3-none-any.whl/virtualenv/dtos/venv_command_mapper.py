from typing import Dict

from bin.commands.command import Command
from bin.custom_commands.command_tree import CommandTree
from bin.virtualenv.activate_venv_command import ActivateVenvCommand
from bin.virtualenv.create_venv_command import CreateVenvCommand
from bin.virtualenv.dtos import VenvDto
from bin.virtualenv.remove_venv_command import RemoveVenvCommand


class VenvCommandMapper:
    @staticmethod
    def to_create_venv_command(dto: VenvDto) -> Command:
        return CreateVenvCommand.from_venv(dto.to_venv())

    @staticmethod
    def to_activate_venv_command(dto: VenvDto) -> Command:
        return ActivateVenvCommand.from_venv(dto.to_venv())

    @staticmethod
    def to_command_dict(name: str, dto: VenvDto) -> Dict[str, Command]:
        venv = dto.to_venv()
        rm_command = RemoveVenvCommand.from_venv(venv)
        subcommands = {
            "create": CreateVenvCommand.from_venv(venv),
            "activate": ActivateVenvCommand.from_venv(venv),
            "remove": rm_command,
            "rm": rm_command,
        }

        return {name: CommandTree(subcommands_tree=subcommands)}
