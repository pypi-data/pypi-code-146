from typing import List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.env.env import Env
from bin.models.bin_base_model import BinBaseModel
from bin.process.helpable import Helpable
from bin.process.process import Process


class ApplyEnvCommand(Command, BinBaseModel):
    env: Env

    def _run(self, process: Process, args: List[str]) -> Process:
        return process.apply_env(self.env.provide())

    def _get_short_description(self) -> str:
        return "inner command"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self("inner command")
