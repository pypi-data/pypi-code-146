import logging
import sys
from typing import TYPE_CHECKING, Optional

from . import exceptions, hookimpl, settings, systemd, types, util
from .models import system
from .pgbackrest import get_settings, repo_path

if TYPE_CHECKING:
    from .ctx import Context
    from .models import interface
    from .settings import Settings, SystemdSettings


logger = logging.getLogger(__name__)
service_name = "backup"
BACKUP_SERVICE_NAME = "pglift-backup@.service"
BACKUP_TIMER_NAME = "pglift-backup@.timer"


def register_if(settings: "Settings") -> bool:
    return (
        settings.service_manager == "systemd"
        and settings.scheduler == "systemd"
        and settings.pgbackrest is not None
        and repo_path.register_if(settings)
    )


@hookimpl
def install_systemd_unit_template(
    settings: "Settings",
    systemd_settings: "SystemdSettings",
    header: str = "",
    env: Optional[str] = None,
) -> None:
    logger.info("installing systemd template unit and timer for PostgreSQL backups")
    environment = ""
    if env:
        environment = f"\nEnvironment={env}\n"
    service_content = systemd.template(BACKUP_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        environment=environment,
        python=sys.executable,
    )
    systemd.install(
        BACKUP_SERVICE_NAME,
        util.with_header(service_content, header),
        systemd_settings.unit_path,
        logger=logger,
    )
    timer_content = systemd.template(BACKUP_TIMER_NAME)
    systemd.install(
        BACKUP_TIMER_NAME,
        util.with_header(timer_content, header),
        systemd_settings.unit_path,
        logger=logger,
    )


@hookimpl
def uninstall_systemd_unit_template(systemd_settings: "SystemdSettings") -> None:
    logger.info("uninstalling systemd template unit and timer for PostgreSQL backups")
    systemd.uninstall(BACKUP_SERVICE_NAME, systemd_settings.unit_path, logger=logger)
    systemd.uninstall(BACKUP_TIMER_NAME, systemd_settings.unit_path, logger=logger)


@hookimpl
def instance_configure(ctx: "Context", manifest: "interface.Instance") -> None:
    """Enable scheduled backup job for configured instance."""
    instance = system.Instance.system_lookup(ctx, (manifest.name, manifest.version))
    ctx.hook.schedule_service(ctx=ctx, service=service_name, name=instance.qualname)


@hookimpl
def instance_drop(ctx: "Context", instance: system.Instance) -> None:
    """Disable scheduled backup job when instance is being dropped."""
    ctx.hook.unschedule_service(
        ctx=ctx, service=service_name, name=instance.qualname, now=True
    )


@hookimpl
def instance_start(ctx: "Context", instance: system.Instance) -> None:
    """Start schedule backup job at instance startup."""
    ctx.hook.start_timer(ctx=ctx, service=service_name, name=instance.qualname)


@hookimpl
def instance_stop(ctx: "Context", instance: system.Instance) -> None:
    """Stop schedule backup job when instance is stopping."""
    ctx.hook.stop_timer(ctx=ctx, service=service_name, name=instance.qualname)


# This entry point is used by systemd 'postgresql-backup@' service.
def main() -> None:
    import argparse

    from .ctx import Context

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "instance", metavar="<version>-<name>", help="instance identifier"
    )

    def do_backup(
        ctx: "Context", instance: system.Instance, args: argparse.Namespace
    ) -> None:
        settings = get_settings(ctx.settings)
        return repo_path.backup(
            ctx, instance, settings, type=types.BackupType(args.type)
        )

    parser.set_defaults(func=do_backup)
    parser.add_argument(
        "--type",
        choices=[t.name for t in types.BackupType],
        default=types.BackupType.default().name,
    )

    args = parser.parse_args()
    ctx = Context(settings=settings.SiteSettings())
    try:
        instance = system.PostgreSQLInstance.from_qualname(ctx, args.instance)
    except ValueError as e:
        parser.error(str(e))
    except exceptions.InstanceNotFound as e:
        parser.exit(2, str(e))
    args.func(ctx, instance, args)


if __name__ == "__main__":  # pragma: nocover
    logging.basicConfig(level=logging.INFO)
    main()
