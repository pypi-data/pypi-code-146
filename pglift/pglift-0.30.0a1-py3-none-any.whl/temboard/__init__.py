import logging
from typing import TYPE_CHECKING, Optional, Type

from .. import hookimpl, systemd, util
from ..models import interface, system
from . import impl, models
from .impl import available as available
from .impl import get_settings

if TYPE_CHECKING:
    from pgtoolkit.conf import Configuration

    from ..ctx import Context
    from ..settings import Settings, SystemdSettings

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
        return models.ServiceManifest(port=s.port)


SYSTEMD_SERVICE_NAME = "pglift-temboard_agent@.service"


@hookimpl
def install_systemd_unit_template(
    settings: "Settings", systemd_settings: "SystemdSettings", header: str = ""
) -> None:
    logger.info("installing systemd template unit for Temboard Agent")
    s = get_settings(settings)
    configpath = str(s.configpath).replace("{name}", "%i")
    content = systemd.template(SYSTEMD_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        configpath=configpath,
        execpath=str(s.execpath),
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
    logger.info("uninstalling systemd template unit for Temboard Agent")
    systemd.uninstall(SYSTEMD_SERVICE_NAME, systemd_settings.unit_path, logger=logger)


@hookimpl
def instance_configure(
    ctx: "Context", manifest: "interface.Instance", config: "Configuration"
) -> None:
    """Install temboard agent for an instance when it gets configured."""
    settings = get_settings(ctx.settings)
    impl.setup(ctx, manifest, settings, config)


@hookimpl
def instance_start(ctx: "Context", instance: "system.Instance") -> None:
    """Start temboard agent service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    impl.start(ctx, service)


@hookimpl
def instance_stop(ctx: "Context", instance: "system.Instance") -> None:
    """Stop temboard agent service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    impl.stop(ctx, service)


@hookimpl
def instance_drop(ctx: "Context", instance: "system.Instance") -> None:
    """Uninstall temboard from an instance being dropped."""
    settings = get_settings(ctx.settings)
    manifest = interface.Instance(name=instance.name, version=instance.version)
    impl.revert_setup(ctx, manifest, settings, instance.config())


@hookimpl
def rolename(settings: "Settings") -> str:
    assert settings.temboard
    return settings.temboard.role


@hookimpl
def role(settings: "Settings", manifest: "interface.Instance") -> "interface.Role":
    name = rolename(settings)
    service_manifest = manifest.service_manifest(models.ServiceManifest)
    password = None
    if service_manifest.password:
        password = service_manifest.password.get_secret_value()
    return interface.Role(
        name=name,
        password=password,
        login=True,
        superuser=True,
    )
