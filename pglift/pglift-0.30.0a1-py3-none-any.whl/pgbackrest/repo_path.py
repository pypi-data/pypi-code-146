import configparser
import logging
from typing import TYPE_CHECKING, List, Optional

from pgtoolkit import conf as pgconf

from .. import exceptions, hookimpl, postgresql, util
from ..models import interface, system
from ..settings import PgBackRestSettings, Settings
from ..task import task
from ..types import BackupType
from . import base, models
from . import register_if as base_register_if
from . import role
from .base import get_settings

if TYPE_CHECKING:
    import click

    from ..ctx import Context

PathRepository = PgBackRestSettings.PathRepository
logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    if not base_register_if(settings):
        return False
    s = get_settings(settings)
    return isinstance(s.repository, PathRepository)


@hookimpl
def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    logger.info("installing base pgbackrest configuration")
    global_configpath = base.base_configpath(s)
    global_configpath.parent.mkdir(parents=True, exist_ok=True)
    config = base_config(s)
    with global_configpath.open("w") as f:
        config.write(f)
    logger.info("creating pgbackrest repository path")
    repository_settings(s).path.mkdir(exist_ok=True, parents=True)


@hookimpl
def site_configure_uninstall(settings: Settings) -> None:
    logger.info("uninstalling base pgbackrest configuration")
    s = get_settings(settings)
    base.base_configpath(s).unlink(missing_ok=True)
    util.rmdir(s.configpath)
    # TODO: remove repository.path?


@hookimpl
def instance_configure(
    ctx: "Context",
    manifest: interface.Instance,
    config: pgconf.Configuration,
    creating: bool,
    upgrading_from: Optional[system.Instance],
) -> None:
    instance = system.PostgreSQLInstance.system_lookup(
        ctx, (manifest.name, manifest.version)
    )
    if instance.standby:
        return

    service_manifest = manifest.service_manifest(models.ServiceManifest)
    stanza = service_manifest.stanza or instance.qualname
    settings = get_settings(ctx.settings)
    service = models.Service(
        stanza=stanza, path=base.config_directory(settings) / f"{stanza}.conf"
    )

    if creating and upgrading_from is None and base.enabled(instance, settings):
        if not ctx.confirm(
            f"Stanza '{stanza}' already bound to another instance, continue by overwriting it?",
            False,
        ):
            raise exceptions.Cancelled("pgbackrest repository already exists")
        revert_init(ctx, service, settings)
        base.revert_setup(ctx, service, settings, config, instance.datadir)

    base.setup(ctx, service, settings, config, instance.datadir)

    if upgrading_from is not None:
        upgrade(ctx, service, settings)
    else:
        init(ctx, service, settings)

    if creating and postgresql.is_running(ctx, instance):
        password = None
        backup_role = role(ctx.settings, manifest)
        assert backup_role is not None
        if not backup_role.pgpass and backup_role.password is not None:
            password = backup_role.password.get_secret_value()
        base.check(ctx, instance, service, settings, password)


@hookimpl
def instance_drop(ctx: "Context", instance: system.Instance) -> None:
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    settings = get_settings(ctx.settings)
    nb_backups = len(base.backup_info(ctx, service, settings)["backup"])
    if not nb_backups or ctx.confirm(
        f"Confirm deletion of {nb_backups} backup(s) for instance {instance}?",
        True,
    ):
        revert_init(ctx, service, settings)
        base.revert_setup(ctx, service, settings, instance.config(), instance.datadir)


@hookimpl
def instance_cli(group: "click.Group") -> None:
    from .cli import instance_backup

    group.add_command(instance_backup)


def repository_settings(settings: PgBackRestSettings) -> PathRepository:
    assert isinstance(settings.repository, PathRepository)
    return settings.repository


def base_config(settings: "PgBackRestSettings") -> configparser.ConfigParser:
    cp = base.parser()
    cp.read_string(
        util.template("pgbackrest", "pgbackrest.conf").format(**dict(settings))
    )
    s = repository_settings(settings)
    cp["global"]["repo1-path"] = str(s.path)
    for opt, value in s.retention:
        cp["global"][f"repo1-retention-{opt}"] = str(value)
    return cp


@task("creating pgBackRest stanza {service.stanza}")
def init(
    ctx: "Context", service: models.Service, settings: "PgBackRestSettings"
) -> None:
    ctx.run(
        base.make_cmd(service.stanza, settings, "stanza-create", "--no-online"),
        check=True,
    )


@init.revert("deleting pgBackRest stanza {service.stanza}")
def revert_init(
    ctx: "Context", service: models.Service, settings: "PgBackRestSettings"
) -> None:
    stanza = service.stanza
    ctx.run(base.make_cmd(stanza, settings, "stop"), check=True)
    ctx.run(base.make_cmd(stanza, settings, "stanza-delete", "--force"), check=True)


def upgrade(
    ctx: "Context", service: models.Service, settings: "PgBackRestSettings"
) -> None:
    """Upgrade stanza"""
    stanza = service.stanza
    logger.info("upgrading pgBackRest stanza %s", stanza)
    ctx.run(
        base.make_cmd(stanza, settings, "stanza-upgrade", "--no-online"), check=True
    )


def backup_command(
    instance: "system.Instance",
    settings: "PgBackRestSettings",
    *,
    type: BackupType = BackupType.default(),
    start_fast: bool = True,
) -> List[str]:
    """Return the full pgbackrest command to perform a backup for ``instance``.

    :param type: backup type (one of 'full', 'incr', 'diff').

    Ref.: https://pgbackrest.org/command.html#command-backup
    """
    args = [
        f"--type={type.name}",
        "--log-level-console=info",
        "backup",
    ]
    if start_fast:
        args.insert(-1, "--start-fast")
    s = instance.service(models.Service)
    return base.make_cmd(s.stanza, settings, *args)


def backup(
    ctx: "Context",
    instance: "system.Instance",
    settings: "PgBackRestSettings",
    *,
    type: BackupType = BackupType.default(),
) -> None:
    """Perform a backup of ``instance``.

    :param type: backup type (one of 'full', 'incr', 'diff').

    Ref.: https://pgbackrest.org/command.html#command-backup
    """
    logger.info("backing up instance %s with pgBackRest", instance)
    if instance.standby:
        raise exceptions.InstanceStateError("backup should be done on primary instance")

    ctx.run(
        backup_command(instance, settings, type=type),
        check=True,
        env=ctx.settings.postgresql.libpq_environ(
            ctx, instance, ctx.settings.postgresql.backuprole.name
        ),
    )


def expire_command(
    service: models.Service, settings: "PgBackRestSettings"
) -> List[str]:
    """Return the full pgbackrest command to expire backups for ``instance``.

    Ref.: https://pgbackrest.org/command.html#command-expire
    """
    return base.make_cmd(service.stanza, settings, "--log-level-console=info", "expire")


def expire(
    ctx: "Context", instance: "system.Instance", settings: "PgBackRestSettings"
) -> None:
    """Expire a backup of ``instance``.

    Ref.: https://pgbackrest.org/command.html#command-expire
    """
    service = instance.service(models.Service)
    logger.info("expiring pgBackRest backups for stanza %s", service.stanza)
    ctx.run(expire_command(service, settings), check=True)
