from functools import partial
from typing import TYPE_CHECKING

import click

from .. import patroni
from ..cli.util import (
    Group,
    instance_identifier_option,
    pass_component_settings,
    pass_instance,
)
from . import impl

if TYPE_CHECKING:
    from ..models import system
    from ..settings import PatroniSettings

pass_patroni_settings = partial(pass_component_settings, patroni, "Patroni")


@click.group("patroni", cls=Group)
@instance_identifier_option
def cli(instance: "system.Instance") -> None:
    """Handle Patroni service for an instance."""


@cli.command("logs")
@pass_patroni_settings
@pass_instance
def logs(instance: "system.Instance", settings: "PatroniSettings") -> None:
    """Output Patroni logs."""
    for line in impl.logs(instance.qualname, settings):
        click.echo(line, nl=False)
