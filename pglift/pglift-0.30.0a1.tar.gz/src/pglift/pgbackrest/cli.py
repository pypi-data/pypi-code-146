from datetime import datetime
from functools import partial
from typing import TYPE_CHECKING, Optional, Tuple

import click

from .. import postgresql, types
from ..cli.instance import instance_identifier
from ..cli.util import (
    Command,
    OutputFormat,
    instance_identifier_option,
    output_format_option,
    pass_component_settings,
    pass_ctx,
    print_json_for,
    print_table_for,
)
from . import base, models, repo_path

if TYPE_CHECKING:
    from ..ctx import Context
    from ..models import system
    from ..settings import PgBackRestSettings

pass_pgbackrest_settings = partial(pass_component_settings, base, "pgbackrest")


@click.command(
    "pgbackrest",
    hidden=True,
    cls=Command,
    context_settings={"ignore_unknown_options": True},
)
@instance_identifier_option
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
@pass_pgbackrest_settings
@pass_ctx
def pgbackrest(
    ctx: "Context",
    settings: "PgBackRestSettings",
    instance: "system.Instance",
    command: Tuple[str, ...],
) -> None:
    """Proxy to pgbackrest operations on an instance"""
    s = instance.service(models.Service)
    cmd = base.make_cmd(s.stanza, settings, *command)
    ctx.run(cmd, capture_output=False, check=True)


@click.command("backup", cls=Command)
@instance_identifier(nargs=1)
@click.option(
    "--type",
    "backup_type",
    type=click.Choice([t.name for t in types.BackupType]),
    default=types.BackupType.default().name,
    help="Backup type",
    callback=lambda ctx, param, value: types.BackupType(value),
)
@pass_pgbackrest_settings
@pass_ctx
def instance_backup(
    ctx: "Context",
    settings: "PgBackRestSettings",
    instance: "system.Instance",
    backup_type: types.BackupType,
) -> None:
    """Back up PostgreSQL INSTANCE"""
    repo_path.backup(ctx, instance, settings, type=backup_type)


@click.command("restore", cls=Command)
@instance_identifier(nargs=1)
@click.option("--label", help="Label of backup to restore")
@click.option("--date", type=click.DateTime(), help="Date of backup to restore")
@pass_pgbackrest_settings
@pass_ctx
def instance_restore(
    ctx: "Context",
    settings: "PgBackRestSettings",
    instance: "system.Instance",
    label: Optional[str],
    date: Optional[datetime],
) -> None:
    """Restore PostgreSQL INSTANCE"""
    postgresql.check_status(ctx, instance, postgresql.Status.not_running)
    if label is not None and date is not None:
        raise click.BadArgumentUsage(
            "--label and --date arguments are mutually exclusive"
        )
    base.restore(ctx, instance, settings, label=label, date=date)


@click.command("backups", cls=Command)
@output_format_option
@instance_identifier(nargs=1)
@pass_pgbackrest_settings
@pass_ctx
def instance_backups(
    ctx: "Context",
    settings: "PgBackRestSettings",
    instance: "system.Instance",
    output_format: OutputFormat,
) -> None:
    """List available backups for INSTANCE"""
    backups = base.iter_backups(ctx, instance, settings)
    if output_format == OutputFormat.json:
        print_json_for((i.dict(by_alias=True) for i in backups))
    else:
        print_table_for(
            (i.dict(by_alias=True) for i in backups),
            title=f"Available backups for instance {instance}",
        )
