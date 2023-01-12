from typing import List

from bin.commands.command import Command
from bin.commands.errors import CommandNotFound
from bin.models.bin_base_model import BinBaseModel
from bin.process.helpable import Helpable
from bin.process.process import Process


class HelpOnlyCommand(BinBaseModel, Command):
    short_description: str
    help: Helpable

    def _run(self, process: Process, args: List[str]) -> Process:
        raise CommandNotFound()

    def _get_short_description(self) -> str:
        return self.short_description

    def _get_help(self) -> Helpable:
        return self.help
