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


class CreateVenvCommand(BinBaseModel, Command):
    exists_cmd: StrCommand
    create_cmd: StrCommand

    @classmethod
    def from_venv(cls, venv: Venv) -> "CreateVenvCommand":
        return cls(exists_cmd=venv.exists_cmd, create_cmd=venv.create_cmd)

    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) > 0:
            raise CommandFailedError.must_run_without_args("create_venv")

        venv_exists = process.run(self.exists_cmd, capture_output=True).has_succeeded()
        if venv_exists:
            process.log(f"{Emoji.SUCCESS}  Create venv: already exists")
            return process

        creation_result = process.run(self.create_cmd, capture_output=True)
        if creation_result.has_failed():
            process.log(f"{Emoji.FAILURE}  Create venv")
            raise CommandFailedError.command_failed("create_venv")

        process.log(f"{Emoji.SUCCESS}  Create venv")
        return process

    def _get_short_description(self) -> str:
        return "Creates the virtual environment, noop when it already exists"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())
