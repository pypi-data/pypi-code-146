from typing import List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.commands.errors import CommandFailedError
from bin.models.bin_base_model import BinBaseModel
from bin.process.emoji import Emoji
from bin.process.helpable import Helpable
from bin.process.process import Process
from bin.requirements.requirement import Requirement


class RequirementsCommand(BinBaseModel, Command):
    requirements: List[Requirement]

    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) > 0:
            raise CommandFailedError.must_run_without_args("requirements")

        nb_reqs = len(self.requirements)
        if nb_reqs == 0:
            process.log_warning(f"{Emoji.WARNING}  No requirements are defined")
            return process

        all_met = True
        for i, req in enumerate(self.requirements):
            if req.is_met(process):
                process.log(f"{Emoji.SUCCESS}  {i + 1}/{nb_reqs}  {req.get_name()}")
            else:
                all_met = False
                process.log(self.__failure_message(i, req))

        if not all_met:
            process.log_error("Unmet requirements")
            raise CommandFailedError.command_failed("requirements")

        process.log_success("All requirements are met")
        return process

    def _get_short_description(self) -> str:
        return "Makes sure you have all the project requirements installed"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())

    def __failure_message(self, i: int, requirement: Requirement) -> str:
        message = f"{Emoji.FAILURE}  {i+1}/{len(self.requirements)}  {requirement.get_name()}"
        if requirement.get_help():
            message += f"\n   {requirement.get_help()}"

        return message
