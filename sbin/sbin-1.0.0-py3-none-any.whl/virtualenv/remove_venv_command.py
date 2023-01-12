from typing import List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.commands.errors import CommandFailedError
from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.process.emoji import Emoji
from bin.process.helpable import Helpable
from bin.process.process import Process
from bin.virtualenv.venv import Venv


class RemoveVenvCommand(BinBaseModel, Command):
    exists_cmd: StrCommand
    remove_cmd: StrCommand

    @classmethod
    def from_venv(cls, venv: Venv) -> "RemoveVenvCommand":
        return cls(exists_cmd=venv.exists_cmd, remove_cmd=venv.remove_cmd)

    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) > 0:
            raise CommandFailedError.must_run_without_args("remove_venv")

        venv_exists = process.run(self.exists_cmd, capture_output=True).has_succeeded()
        if not venv_exists:
            process.log(f"{Emoji.SUCCESS}  Remove venv: no venv to remove")
            return process

        removal_result = process.run(self.remove_cmd, capture_output=True)
        if removal_result.has_failed():
            process.log(f"{Emoji.FAILURE}  Remove venv")
            raise CommandFailedError.command_failed("remove_venv")

        process.log(f"{Emoji.SUCCESS}  Remove venv")
        return process

    def _get_short_description(self) -> str:
        return "Deletes the virtual environment, noop when no virtual environment exist"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())
