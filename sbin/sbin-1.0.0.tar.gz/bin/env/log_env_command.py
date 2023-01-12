from typing import Any, Dict, List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.commands.errors import CommandFailedError
from bin.env.env import Env
from bin.models.bin_base_model import BinBaseModel
from bin.process.emoji import Emoji
from bin.process.helpable import Helpable
from bin.process.process import Process


class LogEnvCommand(Command, BinBaseModel):
    env: Env

    @classmethod
    def from_env(cls, env: Dict[str, Any]) -> "LogEnvCommand":
        return cls(env=Env(env))

    def _run(self, process: Process, args: List[str]) -> Process:
        if len(args) > 0:
            raise CommandFailedError.must_run_without_args("env")

        if len(self.env) == 0:
            process.log(f"{Emoji.THINKING_FACE}  no environment variables")
            return process

        to_log = ""
        for key in sorted(self.env.keys(), key=lambda k: k.lower()):
            to_log += f"{key}={self.env[key]}\n"

        process.log(to_log[:-1])
        return process

    def _get_short_description(self) -> str:
        return "Prints environment variables"

    def _get_help(self) -> Helpable:
        return CommandHelp.only_self(self._get_short_description())
