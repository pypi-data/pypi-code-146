from typing import Any, Dict, List, Optional

from pydantic import root_validator

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp, CommandSummary
from bin.commands.errors import CommandNotFound
from bin.models.bin_base_model import BinBaseModel
from bin.process.helpable import Helpable
from bin.process.process import Process


class CommandTree(BinBaseModel, Command):
    self_cmd: Optional[Command]
    subcommands_tree: Dict[str, Command]

    @root_validator
    def must_contain_at_least_a_command(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        subcommands_tree = values.get("subcommands_tree", {})
        if len(subcommands_tree) == 0:
            raise ValueError("command tree must have at least 1 subcommand")

        return values

    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) == 0:
            return self.__run_self_cmd(process, args)

        subcommand_name = args[0]
        subcommand_args = args[1:]
        if subcommand_name in self.subcommands_tree:
            subcommand = self.subcommands_tree[subcommand_name]
            return subcommand.run(process, subcommand_args)

        return self.__run_self_cmd(process, args)

    def _get_short_description(self) -> str:
        if self.self_cmd is not None:
            return self.self_cmd._get_short_description()

        return "Only subcommands are available. Run them with --help to get more details"

    def _get_help(self) -> Helpable:
        summaries = [
            CommandSummary(command=cmd_name, help=cmd._get_short_description())
            for cmd_name, cmd in self.subcommands_tree.items()
        ]

        return CommandHelp(help=self._get_short_description(), summaries=summaries)

    def __run_self_cmd(self, process: Process, args: List[str]) -> Process:
        if self.self_cmd is None:
            raise CommandNotFound()

        return self.self_cmd.run(process, args)
