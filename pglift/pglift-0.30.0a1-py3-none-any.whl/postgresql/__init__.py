import contextlib
import logging
import os
import shutil
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Union

import pgtoolkit.conf as pgconf
from pgtoolkit.ctl import Status as Status  # noqa: F401

from .. import cmd, conf, db, hookimpl, systemd, util
from .ctl import check_status as check_status  # noqa: F401
from .ctl import is_ready as is_ready  # noqa: F401
from .ctl import is_running as is_running
from .ctl import pg_ctl
from .ctl import replication_lag as replication_lag
from .ctl import status as status  # noqa: F401
from .ctl import wait_ready as wait_ready
from .ctl import wal_sender_state
from .models import Standby as Standby

if TYPE_CHECKING:
    from ..ctx import Context
    from ..models import interface, system
    from ..settings import Settings, SystemdSettings
    from ..types import ConfigChanges, PostgreSQLStopMode

logger = logging.getLogger(__name__)
POSTGRESQL_SERVICE_NAME = "pglift-postgresql@.service"


@hookimpl(trylast=True)
def postgresql_service_name() -> str:
    return "postgresql"


@hookimpl(trylast=True)
def standby_model(
    ctx: "Context",
    instance: "system.Instance",
    standby: "system.Standby",
    running: bool,
) -> Standby:
    values: Dict[str, Any] = {
        "primary_conninfo": standby.primary_conninfo,
        "slot": standby.slot,
        "password": standby.password,
    }
    if running:
        values["replication_lag"] = replication_lag(instance)
    values["wal_sender_state"] = wal_sender_state(instance)
    return Standby.parse_obj(values)


@hookimpl(trylast=True)
def postgresql_editable_conf(instance: "system.PostgreSQLInstance") -> str:
    return "".join(instance.config(managed_only=True).lines)


def init_replication(
    ctx: "Context", instance: "system.BaseInstance", standby: "Standby"
) -> None:
    with tempfile.TemporaryDirectory() as _tmpdir:
        tmpdir = Path(_tmpdir)
        # pg_basebackup will also copy config files from primary datadir.
        # So to have expected configuration at this stage we have to backup
        # postgresql.conf & pg_hba.conf (created by prior pg_ctl init) and
        # restore after pg_basebackup finishes.
        keep = {"postgresql.conf", "pg_hba.conf"}
        for name in keep:
            shutil.copyfile(instance.datadir / name, tmpdir / name)
        ctx.rmtree(instance.datadir)
        ctx.rmtree(instance.waldir)
        cmd = [
            str(instance.bindir / "pg_basebackup"),
            "--pgdata",
            str(instance.datadir),
            "--write-recovery-conf",
            "--checkpoint=fast",
            "--no-password",
            "--progress",
            "--verbose",
            "--dbname",
            standby.primary_conninfo,
            "--waldir",
            str(instance.waldir),
        ]

        if standby.slot:
            cmd += ["--slot", standby.slot]

        env = None
        if standby.password:
            env = os.environ.copy()
            env["PGPASSWORD"] = standby.password.get_secret_value()
        ctx.run(cmd, check=True, env=env)
        for name in keep:
            shutil.copyfile(tmpdir / name, instance.datadir / name)


@hookimpl(trylast=True)
def initdb(
    ctx: "Context", manifest: "interface.Instance", instance: "system.BaseInstance"
) -> Literal[True]:
    """Initialize the PostgreSQL database cluster with plain initdb."""
    assert instance.bindir.exists()  # Per BaseInstance.get().
    pgctl = pg_ctl(instance.bindir, ctx=ctx)

    settings = ctx.settings
    surole = manifest.surole(settings)
    opts: Dict[str, Union[str, Literal[True]]] = {
        "waldir": str(instance.waldir),
        "username": surole.name,
    }
    opts.update(
        {
            f"auth_{m}": v.value
            for m, v in manifest.auth_options(settings.postgresql.auth).dict().items()
        }
    )
    opts.update(
        manifest.initdb_options(settings.postgresql.initdb).dict(exclude_none=True)
    )

    if surole.password:
        with tempfile.NamedTemporaryFile("w") as pwfile:
            pwfile.write(surole.password.get_secret_value())
            pwfile.flush()
            pgctl.init(instance.datadir, pwfile=pwfile.name, **opts)
    else:
        pgctl.init(instance.datadir, **opts)

    if manifest.standby:
        init_replication(ctx=ctx, instance=instance, standby=manifest.standby)

    return True


@hookimpl(trylast=True)
def configure_postgresql(
    ctx: "Context",
    manifest: "interface.Instance",
    configuration: pgconf.Configuration,
    instance: "system.BaseInstance",
) -> "ConfigChanges":
    postgresql_conf = pgconf.parse(instance.datadir / "postgresql.conf")
    config_before = postgresql_conf.as_dict()
    conf.update(postgresql_conf, **configuration.as_dict())
    config_after = postgresql_conf.as_dict()
    changes = conf.changes(config_before, config_after)

    if changes:
        postgresql_conf.save()

    return changes


@hookimpl(trylast=True)
def configure_auth(
    settings: "Settings",
    instance: "system.BaseInstance",
    manifest: "interface.Instance",
) -> Literal[True]:
    """Configure authentication for the PostgreSQL instance."""
    logger.info("configuring PostgreSQL authentication")
    hba_path = instance.datadir / "pg_hba.conf"
    hba = manifest.pg_hba(settings)
    hba_path.write_text(hba)

    ident_path = instance.datadir / "pg_ident.conf"
    ident = manifest.pg_ident(settings)
    ident_path.write_text(ident)
    return True


@hookimpl(trylast=True)
def start_postgresql(
    ctx: "Context",
    instance: "system.PostgreSQLInstance",
    foreground: bool,
    wait: bool,
    run_hooks: bool = True,
    **runtime_parameters: str,
) -> Literal[True]:
    logger.info("starting PostgreSQL cluster %s", instance.qualname)

    ctx.settings.postgresql.socket_directory.mkdir(parents=True, exist_ok=True)
    if not foreground and run_hooks:
        if ctx.hook.start_service(
            ctx=ctx,
            service=ctx.hook.postgresql_service_name(ctx=ctx, instance=instance),
            name=instance.qualname,
        ):
            if wait:
                wait_ready(ctx, instance)
            return True

    postgres = instance.bindir / "postgres"
    command = [str(postgres), "-D", str(instance.datadir)]
    for name, value in runtime_parameters.items():
        command.extend(["-c", f"{name}={value}"])
    if foreground:
        cmd.execute_program(command)
    else:
        with cmd.Program(command, pidfile=None):
            if wait:
                wait_ready(ctx, instance)
    return True


@hookimpl(trylast=True)
def stop_postgresql(
    ctx: "Context",
    instance: "system.PostgreSQLInstance",
    mode: "PostgreSQLStopMode",
    wait: bool,
    run_hooks: bool = True,
) -> Literal[True]:
    logger.info("stopping PostgreSQL cluster %s", instance.qualname)

    if run_hooks:
        if ctx.hook.stop_service(
            ctx=ctx,
            service=ctx.hook.postgresql_service_name(ctx=ctx, instance=instance),
            name=instance.qualname,
        ):
            return True

    pg_ctl(instance.bindir, ctx=ctx).stop(instance.datadir, mode=mode, wait=wait)
    return True


@hookimpl(trylast=True)
def restart_postgresql(
    ctx: "Context",
    instance: "system.PostgreSQLInstance",
    mode: "PostgreSQLStopMode",
    wait: bool,
) -> Literal[True]:
    logger.info("restarting PostgreSQL")
    stop_postgresql(ctx, instance, mode=mode, wait=wait)
    start_postgresql(ctx, instance, foreground=False, wait=wait)
    return True


@hookimpl(trylast=True)
def reload_postgresql(ctx: "Context", instance: "system.Instance") -> Literal[True]:
    logger.info(f"reloading PostgreSQL configuration for {instance.qualname}")
    with db.connect(ctx, instance) as cnx:
        cnx.execute("SELECT pg_reload_conf()")
    return True


@hookimpl(trylast=True)
def promote_postgresql(ctx: "Context", instance: "system.Instance") -> Literal[True]:
    logger.info("promoting PostgreSQL instance")
    pgctl = pg_ctl(instance.bindir, ctx=ctx)
    ctx.run(
        [str(pgctl.pg_ctl), "promote", "-D", str(instance.datadir)],
        check=True,
    )
    return True


@contextlib.contextmanager
def running(ctx: "Context", instance: "system.PostgreSQLInstance") -> Iterator[None]:
    """Context manager to temporarily start a PostgreSQL instance."""
    if is_running(ctx, instance):
        yield
        return

    start_postgresql(
        ctx,
        instance,
        foreground=False,
        wait=True,
        run_hooks=False,
        # Keep logs to stderr, uncollected, to get meaningful errors on our side.
        logging_collector="off",
        log_destination="stderr",
    )
    try:
        yield
    finally:
        stop_postgresql(ctx, instance, mode="fast", wait=True, run_hooks=False)


@hookimpl
def install_systemd_unit_template(
    settings: "Settings",
    systemd_settings: "SystemdSettings",
    header: str,
    env: Optional[str],
) -> None:
    logger.info("installing systemd template unit for PostgreSQL")
    environment = ""
    if env:
        environment = f"\nEnvironment={env}\n"
    if getattr(sys, "frozen", False):
        execpath = sys.executable
    else:
        execpath = f"{sys.executable} -m pglift"
    content = systemd.template(POSTGRESQL_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        execpath=execpath,
        environment=environment,
    )
    systemd.install(
        POSTGRESQL_SERVICE_NAME,
        util.with_header(content, header),
        systemd_settings.unit_path,
        logger=logger,
    )


@hookimpl
def uninstall_systemd_unit_template(systemd_settings: "SystemdSettings") -> None:
    logger.info("uninstalling systemd template unit for PostgreSQL")
    systemd.uninstall(
        POSTGRESQL_SERVICE_NAME, systemd_settings.unit_path, logger=logger
    )
