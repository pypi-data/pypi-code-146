import logging
from typing import TYPE_CHECKING, Optional, Type

from .. import hookimpl, systemd, util
from ..models import interface
from . import impl, models
from .impl import apply as apply
from .impl import available as available
from .impl import get_settings
from .impl import start as start
from .impl import stop as stop
from .models import PostgresExporter as PostgresExporter
from .models import ServiceManifest

if TYPE_CHECKING:
    import click
    from pgtoolkit.conf import Configuration

    from ..ctx import Context
    from ..models import system
    from ..settings import Settings, SystemdSettings

__all__ = ["PostgresExporter", "apply", "available", "start", "stop"]

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


@hookimpl
def system_lookup(
    ctx: "Context", instance: "system.PostgreSQLInstance"
) -> Optional[models.Service]:
    settings = get_settings(ctx.settings)
    return impl.system_lookup(ctx, instance.qualname, settings)


@hookimpl
def interface_model() -> Type[models.ServiceManifest]:
    return models.ServiceManifest


@hookimpl
def get(
    ctx: "Context", instance: "system.Instance"
) -> Optional[models.ServiceManifest]:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(port=s.port, password=s.password)


SYSTEMD_SERVICE_NAME = "pglift-postgres_exporter@.service"


@hookimpl
def install_systemd_unit_template(
    settings: "Settings", systemd_settings: "SystemdSettings", header: str = ""
) -> None:
    logger.info("installing systemd template unit for Prometheus postgres_exporter")
    s = get_settings(settings)
    configpath = str(s.configpath).replace("{name}", "%i")
    content = systemd.template(SYSTEMD_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        configpath=configpath,
        execpath=s.execpath,
    )
    systemd.install(
        SYSTEMD_SERVICE_NAME,
        util.with_header(content, header),
        systemd_settings.unit_path,
        logger=logger,
    )


@hookimpl
def uninstall_systemd_unit_template(
    settings: "Settings", systemd_settings: "SystemdSettings"
) -> None:
    logger.info("uninstalling systemd template unit for Prometheus postgres_exporter")
    systemd.uninstall(SYSTEMD_SERVICE_NAME, systemd_settings.unit_path, logger=logger)


@hookimpl
def instance_configure(
    ctx: "Context", manifest: "interface.Instance", config: "Configuration"
) -> None:
    """Install postgres_exporter for an instance when it gets configured."""
    settings = get_settings(ctx.settings)
    impl.setup_local(ctx, manifest, settings, config)


@hookimpl
def instance_start(ctx: "Context", instance: "system.Instance") -> None:
    """Start postgres_exporter service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    impl.start(ctx, service)


@hookimpl
def instance_stop(ctx: "Context", instance: "system.Instance") -> None:
    """Stop postgres_exporter service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    impl.stop(ctx, service)


@hookimpl
def instance_drop(ctx: "Context", instance: "system.Instance") -> None:
    """Uninstall postgres_exporter from an instance being dropped."""
    settings = get_settings(ctx.settings)
    impl.revert_setup(ctx, instance.qualname, settings)


@hookimpl
def role(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional[interface.Role]:
    service_manifest = manifest.service_manifest(ServiceManifest)
    password = None
    if service_manifest.password:
        password = service_manifest.password.get_secret_value()
    assert settings.prometheus is not None
    return interface.Role(
        name=settings.prometheus.role,
        password=password,
        login=True,
        in_roles=["pg_monitor"],
    )


@hookimpl
def cli() -> "click.Group":
    from .cli import postgres_exporter

    return postgres_exporter
