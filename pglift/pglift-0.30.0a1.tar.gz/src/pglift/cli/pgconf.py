from typing import Any, Dict, Iterable, Optional, Tuple

import click
import pgtoolkit.conf

from .. import instances
from ..ctx import Context
from ..models import system
from ..types import ConfigChanges
from .util import Group, instance_identifier_option, pass_ctx, pass_instance


@click.group(cls=Group)
@instance_identifier_option
def cli(instance: system.Instance) -> None:
    """Manage configuration of a PostgreSQL instance."""


def show_configuration_changes(
    changes: ConfigChanges, parameters: Optional[Iterable[str]] = None
) -> None:
    for param, (old, new) in changes.items():
        click.secho(f"{param}: {old} -> {new}", err=True, fg="green")
    if parameters is None:
        return
    unchanged = set(parameters) - set(changes)
    if unchanged:
        click.secho(
            f"changes in {', '.join(map(repr, sorted(unchanged)))} not applied",
            err=True,
            fg="red",
        )
        click.secho(
            " hint: either these changes have no effect (values already set) "
            "or specified parameters are already defined in an un-managed file "
            "(e.g. 'postgresql.conf')",
            err=True,
            fg="blue",
        )


@cli.command("show")
@click.argument("parameter", nargs=-1)
@pass_instance
@pass_ctx
def pgconf_show(ctx: Context, instance: system.Instance, parameter: Tuple[str]) -> None:
    """Show configuration (all parameters or specified ones).

    Only uncommented parameters are shown when no PARAMETER is specified. When
    specific PARAMETERs are queried, commented values are also shown.
    """
    config = instance.config()
    for entry in config.entries.values():
        if parameter:
            if entry.name in parameter:
                if entry.commented:
                    click.echo(f"# {entry.name} = {entry.serialize()}")
                else:
                    click.echo(f"{entry.name} = {entry.serialize()}")
        elif not entry.commented:
            click.echo(f"{entry.name} = {entry.serialize()}")


def validate_configuration_parameters(
    context: click.Context, param: click.Parameter, value: Tuple[str]
) -> Dict[str, str]:
    items = {}
    for v in value:
        try:
            key, val = v.split("=", 1)
        except ValueError:
            raise click.BadParameter(v)
        items[key] = val
    return items


@cli.command("set")
@click.argument(
    "parameters",
    metavar="<PARAMETER>=<VALUE>...",
    nargs=-1,
    callback=validate_configuration_parameters,
    required=True,
)
@pass_instance
@pass_ctx
def pgconf_set(
    ctx: Context, instance: system.Instance, parameters: Dict[str, Any]
) -> None:
    """Set configuration items."""
    manifest = instances._get(ctx, instance)
    manifest.settings.update(parameters)
    changes = instances.configure(ctx, manifest)
    show_configuration_changes(changes, parameters.keys())


@cli.command("remove")
@click.argument("parameters", nargs=-1, required=True)
@pass_instance
@pass_ctx
def pgconf_remove(
    ctx: Context, instance: system.Instance, parameters: Tuple[str]
) -> None:
    """Remove configuration items."""
    manifest = instances._get(ctx, instance)
    for p in parameters:
        try:
            del manifest.settings[p]
        except KeyError:
            raise click.ClickException(f"'{p}' not found in managed configuration")
    changes = instances.configure(ctx, manifest)
    show_configuration_changes(changes, parameters)


@cli.command("edit")
@pass_instance
@pass_ctx
def pgconf_edit(ctx: Context, instance: system.Instance) -> None:
    """Edit managed configuration."""
    actual_config = ctx.hook.postgresql_editable_conf(ctx=ctx, instance=instance)
    edited = click.edit(text=actual_config)
    if edited is None:
        click.echo("no change", err=True)
        return
    config = pgtoolkit.conf.parse_string(edited)
    values = config.as_dict()
    manifest = instances._get(ctx, instance)
    manifest.settings.clear()
    manifest.settings.update(values)
    changes = instances.configure(ctx, manifest)
    show_configuration_changes(changes)
