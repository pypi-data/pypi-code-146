import logging

import click

from com.enovation.enov import enov


class EnovGroup(click.Group):
    """
    The com.enovation framework comes with a default click group and commands. Later, this click application can be
    extended with client specific commands.

    To merge both universes (aka group enov and commands, and client specific commands), we use this base class, to
    instantiate the client specific click application.
    """
    _logger: logging.Logger = logging.getLogger(__name__)

    def __init__(
            self,
            str_name: str,
            lst_commands: list[click.Command] = None,
    ):
        super(EnovGroup, self).__init__(
            name=str_name,
            callback=enov.callback,
            params=enov.params,
            chain=enov.chain,
            help=enov.help,
            commands=enov.commands
        )

        if lst_commands is not None:
            self.add_commands(lst_commands)

    def add_commands(self, lst_commands: list[click.Command]):
        for i_cmd in lst_commands:
            self.add_command(i_cmd)
