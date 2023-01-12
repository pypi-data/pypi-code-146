from typing import List, Union

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.commands.errors import CommandFailedError
from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.process.helpable import Helpable
from bin.process.process import Process


class BasicCommand(BinBaseModel, Command):
    run_cmd: StrCommand
    short_description: str
    help: Helpable

    @staticmethod
    def no_help(run_cmd: Union[StrCommand, str]) -> "BasicCommand":
        return BasicCommand(
            run_cmd=run_cmd, short_description=f"Runs {run_cmd}", help=CommandHelp.only_self(f"Runs {run_cmd}")
        )

    def _run(self, process: Process, args: List[str]) -> Process:
        result = process.run(self.run_cmd, args)
        if result.has_failed():
            raise CommandFailedError.command_failed(self.run_cmd)

        return process

    def _get_short_description(self) -> str:
        return self.short_description

    def _get_help(self) -> Helpable:
        return self.help
