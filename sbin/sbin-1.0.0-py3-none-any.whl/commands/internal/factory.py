from typing import Dict, List

from bin.commands.command import Command
from bin.commands.command_help import CommandHelp
from bin.commands.internal.apply_env_command import ApplyEnvCommand
from bin.commands.internal.help_only_command import HelpOnlyCommand
from bin.commands.internal.mute_logs_command import MuteLogsCommand
from bin.commands.internal.noop_command import NoopCommand
from bin.commands.internal.unmute_logs_command import UnmuteLogsCommand
from bin.commands.internal.with_setup_command import WithSetupCommand


class InternalCommandFactory:
    @staticmethod
    def mute_logs() -> Command:
        return MuteLogsCommand()

    @staticmethod
    def unmute_logs() -> Command:
        return UnmuteLogsCommand()

    @staticmethod
    def noop() -> Command:
        return NoopCommand()

    @staticmethod
    def help_only(text: str) -> Command:
        return HelpOnlyCommand(short_description=text, help=CommandHelp.only_self(text))

    @staticmethod
    def wrap_with_env(env: Dict[str, str], cmd: Command) -> Command:
        if len(env) == 0:
            return cmd

        return InternalCommandFactory.with_setup([ApplyEnvCommand(env=env)], cmd)

    @staticmethod
    def with_setup(setup_cmds: List[Command], main_cmd: Command) -> Command:
        return WithSetupCommand(setup_cmds=setup_cmds, main_cmd=main_cmd)
