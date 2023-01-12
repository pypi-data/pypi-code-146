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


class ActivateVenvCommand(BinBaseModel, Command):
    exists_cmd: StrCommand
    activate_cmd: StrCommand

    @classmethod
    def from_venv(cls, venv: Venv) -> "ActivateVenvCommand":
        return cls(exists_cmd=venv.exists_cmd, activate_cmd=venv.activate_cmd)

    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) > 0:
            raise CommandFailedError.must_run_without_args("activate_venv")

        venv_exists = process.run(self.exists_cmd, capture_output=True).has_succeeded()
        if not venv_exists:
            process.log(f"{Emoji.FAILURE}  Activate venv")
            raise CommandFailedError.failed_with_reason("activate_venv", "venv not found")

        dummy_activate_result = process.run(self.activate_cmd, capture_output=True)
        if dummy_activate_result.has_failed():
            process.log(f"{Emoji.FAILURE}  Activate venv")
            raise CommandFailedError.command_failed("activate_venv")

        process.log(f"{Emoji.SUCCESS}  Activate venv")
        return process.with_venv(self.activate_cmd)

    def _get_short_description(self) -> str:
        return "Activates the virtual environment, fails when no virtual environment exist"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())
