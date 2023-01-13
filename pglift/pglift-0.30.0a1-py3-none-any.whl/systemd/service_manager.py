from typing import TYPE_CHECKING, Literal, Optional

from .. import hookimpl
from . import daemon_reload, disable, enable, restart, start, stop

if TYPE_CHECKING:
    from ..ctx import Context
    from ..pm import PluginManager
    from ..settings import Settings


def register_if(settings: "Settings") -> bool:
    return settings.service_manager == "systemd"


def unit(service: str, qualname: Optional[str]) -> str:
    if qualname is not None:
        return f"pglift-{service}@{qualname}.service"
    else:
        return f"pglift-{service}.service"


@hookimpl
def enable_service(ctx: "Context", service: str, name: Optional[str]) -> Literal[True]:
    enable(ctx, unit(service, name))
    return True


@hookimpl
def disable_service(
    ctx: "Context", service: str, name: Optional[str], now: Optional[bool]
) -> Literal[True]:
    kwargs = {}
    if now is not None:
        kwargs["now"] = now
    disable(ctx, unit(service, name), **kwargs)
    return True


@hookimpl
def start_service(ctx: "Context", service: str, name: Optional[str]) -> Literal[True]:
    start(ctx, unit(service, name))
    return True


@hookimpl
def stop_service(ctx: "Context", service: str, name: Optional[str]) -> Literal[True]:
    stop(ctx, unit(service, name))
    return True


@hookimpl
def restart_service(ctx: "Context", service: str, name: Optional[str]) -> Literal[True]:
    restart(ctx, unit(service, name))
    return True


@hookimpl
def site_configure_install(
    settings: "Settings",
    pm: "PluginManager",
    header: str,
    env: Optional[str],
) -> None:
    systemd_settings = settings.systemd
    assert systemd_settings is not None
    pm.hook.install_systemd_unit_template(
        settings=settings, systemd_settings=systemd_settings, header=header, env=env
    )
    daemon_reload(systemd_settings)


@hookimpl
def site_configure_uninstall(settings: "Settings", pm: "PluginManager") -> None:
    systemd_settings = settings.systemd
    assert systemd_settings is not None
    pm.hook.uninstall_systemd_unit_template(
        settings=settings, systemd_settings=systemd_settings
    )
    daemon_reload(systemd_settings)
