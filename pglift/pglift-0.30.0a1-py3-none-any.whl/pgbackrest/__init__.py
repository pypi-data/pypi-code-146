import logging
from typing import TYPE_CHECKING, Dict, Literal, Optional, Type

import pgtoolkit.conf as pgconf

from .. import hookimpl, util
from ..models import interface, system
from . import base, models
from .base import available as available
from .base import config_directory
from .base import get_settings as get_settings
from .base import iter_backups as iter_backups
from .base import restore as restore
from .models import ServiceManifest

if TYPE_CHECKING:
    import click

    from ..ctx import Context
    from ..settings import Settings

__all__ = ["available", "backup", "expire", "iter_backups", "restore"]

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


@hookimpl
def site_configure_install(settings: "Settings") -> None:
    logger.info("creating common pgbackrest directories")
    s = get_settings(settings)
    config_directory(s).mkdir(mode=0o750, exist_ok=True, parents=True)
    s.logpath.mkdir(exist_ok=True, parents=True)
    s.spoolpath.mkdir(exist_ok=True, parents=True)
    s.lockpath.mkdir(exist_ok=True, parents=True)


@hookimpl
def site_configure_uninstall(settings: "Settings") -> None:
    logger.info("deleting common pgbackrest directories")
    s = get_settings(settings)
    util.rmdir(config_directory(s))
    # TODO: remove logpath, spoolpath, lockpath?


@hookimpl
def system_lookup(
    ctx: "Context", instance: "system.PostgreSQLInstance"
) -> Optional[models.Service]:
    settings = get_settings(ctx.settings)
    return base.system_lookup(instance.datadir, settings)


@hookimpl
def get(
    ctx: "Context", instance: "system.Instance"
) -> Optional[models.ServiceManifest]:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(stanza=s.stanza)


@hookimpl
def instance_settings(
    ctx: "Context", manifest: "interface.Instance", instance: "system.BaseInstance"
) -> pgconf.Configuration:
    settings = get_settings(ctx.settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    stanza = service_manifest.stanza or instance.qualname
    return base.postgresql_configuration(stanza, settings)


@hookimpl
def interface_model() -> Type[models.ServiceManifest]:
    return models.ServiceManifest


@hookimpl
def initdb(
    ctx: "Context", manifest: "interface.Instance", instance: system.BaseInstance
) -> Optional[Literal[True]]:
    service_manifest = manifest.service_manifest(ServiceManifest)
    if service_manifest.restore is None:
        return None
    settings = get_settings(ctx.settings)
    logger.info("creating instance from pgbackrest backup")
    cmd = [
        str(settings.execpath),
        "--log-level-file=off",
        "--log-level-stderr=info",
        "--config-path",
        str(settings.configpath),
        "--stanza",
        service_manifest.restore.stanza,
        "--pg1-path",
        str(instance.datadir),
    ]
    if manifest.standby:
        cmd.append("--type=standby")
        # Double quote if needed (e.g. to escape white spaces in value).
        value = manifest.standby.full_primary_conninfo.replace("'", "''")
        cmd.extend(["--recovery-option", f"primary_conninfo={value}"])
        if manifest.standby.slot:
            cmd.extend(
                ["--recovery-option", f"primary_slot_name={manifest.standby.slot}"]
            )
    cmd.append("restore")
    ctx.run(cmd, check=True)
    return True


@hookimpl
def instance_env(ctx: "Context", instance: "system.Instance") -> Dict[str, str]:
    pgbackrest_settings = base.get_settings(ctx.settings)
    try:
        service = instance.service(models.Service)
    except ValueError:
        return {}
    return base.env_for(service, pgbackrest_settings)


@hookimpl
def rolename(settings: "Settings") -> str:
    return settings.postgresql.backuprole.name


@hookimpl
def role(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional["interface.Role"]:
    name = rolename(settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    password = None
    if service_manifest.password:
        password = service_manifest.password.get_secret_value()
    pgpass = settings.postgresql.backuprole.pgpass
    return interface.Role(
        name=name,
        password=password,
        login=True,
        superuser=True,
        pgpass=pgpass,
    )


@hookimpl
def cli() -> "click.Command":
    from .cli import pgbackrest

    return pgbackrest


@hookimpl
def instance_cli(group: "click.Group") -> None:
    from .cli import instance_backups, instance_restore

    group.add_command(instance_backups)
    group.add_command(instance_restore)
