import abc
from typing import List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.commands.errors import CommandFailedError
from bin.models.bin_base_model import BinBaseModel
from bin.process.emoji import Emoji
from bin.process.helpable import Helpable
from bin.process.process import Process
from bin.up.up_subcommand import UpResult, UpSubcommand


class SetupCommandType(abc.ABC):
    @abc.abstractmethod
    def _type(self) -> str:
        pass


class UpCommand(BinBaseModel, Command, SetupCommandType):
    subcommands: List[UpSubcommand]

    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) > 0:
            raise CommandFailedError.must_run_without_args(self._type())

        if len(self.subcommands) == 0:
            process.log_warning(f"{Emoji.WARNING}  No steps are defined")
            return process

        for i, subcommand in enumerate(self.subcommands):
            up_result = subcommand.run(process)
            if not up_result.has_succeeded:
                process.log(self.__failed_result(i, up_result))
                process.log_error(f"{self._type().title()} failed")
                raise CommandFailedError.command_failed(self._type())

            process.log(self.__successful_result(i, up_result))

        process.log_success(f"{self._type().title()} ran successfully")
        return process

    def _get_short_description(self) -> str:
        return "Runs a bunch of commands in order to set up the project before running it"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())

    def _type(self) -> str:
        return "up"

    def __successful_result(self, i: int, result: UpResult) -> str:
        message = f"{Emoji.SUCCESS}  {i + 1}/{len(self.subcommands)}  "
        if result.details is not None:
            message += f"({result.details}) "

        return message + result.name

    def __failed_result(self, i: int, result: UpResult) -> str:
        message = f"{Emoji.FAILURE}  {i+1}/{len(self.subcommands)}  {result.name}"
        if result.details is not None:
            message += f"\n  {result.details}"

        return message
