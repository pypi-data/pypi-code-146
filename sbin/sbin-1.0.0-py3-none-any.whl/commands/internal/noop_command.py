from typing import List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.models.bin_base_model import BinBaseModel
from bin.process.helpable import Helpable
from bin.process.process import Process


class NoopCommand(Command, BinBaseModel):
    def _run(self, process: Process, _: List[str]) -> Process:
        return process

    def _get_short_description(self) -> str:
        return "Noop command"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())
