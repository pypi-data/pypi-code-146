import re
from typing import List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.commands.errors import CommandFailedError
from bin.models.bin_base_model import BinBaseModel
from bin.process.helpable import Helpable
from bin.process.process import Process

VERSION_REGEX = re.compile(r"Version: (\d+\.\d+\.\d+)")


class VersionCommand(BinBaseModel, Command):
    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) > 0:
            raise CommandFailedError.must_run_without_args("version")

        result = process.run("pip show sbin", capture_output=True)
        if result.has_failed():
            raise CommandFailedError.command_failed("version")

        found = VERSION_REGEX.findall(result.stdout)
        if len(found) == 0:
            raise CommandFailedError.failed_with_reason("version", "unable to find version")

        process.log(f"sbin {found[0]}")
        return process

    def _get_short_description(self) -> str:
        return "sbin version"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())
