from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Type

import pluggy
from pgtoolkit.conf import Configuration

from . import __name__ as pkgname
from ._compat import TypeAlias

if TYPE_CHECKING:
    import click

    from .ctx import Context
    from .models import interface, system
    from .models.system import BaseInstance, Instance, PostgreSQLInstance
    from .pm import PluginManager
    from .postgresql import Standby
    from .settings import Settings, SystemdSettings
    from .types import ConfigChanges, ServiceManifest

hookspec = pluggy.HookspecMarker(pkgname)

FirstResult: TypeAlias = Optional[Literal[True]]


@hookspec  # type: ignore[misc]
def site_configure_install(
    settings: "Settings", pm: "PluginManager", header: str, env: Optional[str]
) -> None:
    """Global configuration hook."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def site_configure_uninstall(settings: "Settings", pm: "PluginManager") -> None:
    """Global configuration hook."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def install_systemd_unit_template(
    settings: "Settings",
    systemd_settings: "SystemdSettings",
    header: str,
    env: Optional[str],
) -> None:
    """Install systemd unit templates."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def uninstall_systemd_unit_template(
    settings: "Settings", systemd_settings: "SystemdSettings"
) -> None:
    """Uninstall systemd unit templates."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def cli() -> "click.Command":
    """Return command-line entry point as click Command (or Group) for the plugin."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def instance_cli(group: "click.Group") -> None:
    """Extend 'group' with extra commands from the plugin."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def system_lookup(ctx: "Context", instance: "PostgreSQLInstance") -> Optional[Any]:
    """Look up for the satellite service object on system that matches specified instance."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def get(ctx: "Context", instance: "Instance") -> Optional["ServiceManifest"]:
    """Return the description the satellite service bound to specified instance."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def interface_model() -> Type["ServiceManifest"]:
    """The interface model for satellite component provided plugin."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def instance_settings(
    ctx: "Context", manifest: "interface.Instance", instance: "BaseInstance"
) -> Configuration:
    """Called before the PostgreSQL instance settings is written."""
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def standby_model(
    ctx: "Context",
    instance: "system.Instance",
    standby: "system.Standby",
    running: bool,
) -> Optional["Standby"]:
    """The interface model holding standby information, if 'instance' is a
    plain standby.

    Only one implementation should be invoked so call order and returned value
    matter.

    An implementation may raise a ValueError to interrupt hook execution.
    """
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def instance_configure(
    ctx: "Context",
    manifest: "interface.Instance",
    config: Configuration,
    changes: "ConfigChanges",
    creating: bool,
    upgrading_from: Optional["Instance"],
) -> None:
    """Called when the PostgreSQL instance got (re-)configured."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def instance_drop(ctx: "Context", instance: "Instance") -> None:
    """Called when the PostgreSQL instance got dropped."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def instance_start(ctx: "Context", instance: "Instance") -> None:
    """Called when the PostgreSQL instance got started."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def instance_stop(ctx: "Context", instance: "Instance") -> None:
    """Called when the PostgreSQL instance got stopped."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def instance_env(ctx: "Context", instance: "Instance") -> Dict[str, str]:
    """Return environment variables for instance defined by the plugin."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def instance_upgrade(
    ctx: "Context", old: "PostgreSQLInstance", new: "PostgreSQLInstance"
) -> None:
    """Called when 'old' PostgreSQL instance got upgraded as 'new'."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def role_change(
    ctx: "Context", role: "interface.BaseRole", instance: "PostgreSQLInstance"
) -> bool:
    """Called when 'role' changed in 'instance' (be it a create, an update or a deletion).

    Return True if any change happened during hook invocation.
    """
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def rolename(settings: "Settings") -> str:
    """Return the name of role used by a plugin."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def role(settings: "Settings", manifest: "interface.Instance") -> "interface.Role":
    """Return the role used by a plugin, to be created at instance creation."""
    raise NotImplementedError


@hookspec  # type: ignore[misc]
def database(
    settings: "Settings", manifest: "interface.Instance"
) -> "interface.Database":
    """Return the database used by a plugin, to be created at instance creation."""
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def initdb(
    ctx: "Context", manifest: "interface.Instance", instance: "BaseInstance"
) -> FirstResult:
    """Initialize a PostgreSQL database cluster.

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def postgresql_editable_conf(ctx: "Context", instance: "BaseInstance") -> Optional[str]:
    """Return the content of editable postgresql.conf.

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def configure_postgresql(
    ctx: "Context",
    manifest: "interface.Instance",
    configuration: Configuration,
    instance: "BaseInstance",
) -> Optional["ConfigChanges"]:
    """Configure PostgreSQL and return 'changes' to postgresql.conf.

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def configure_auth(
    settings: "Settings", instance: "BaseInstance", manifest: "interface.Instance"
) -> Optional[bool]:
    """Configure authentication for PostgreSQL (pg_hba.conf, pg_ident.conf).

    Only one implementation should be invoked so call order and returned value
    matter.

    If returning True, PostgreSQL should be restarted by the caller.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def start_postgresql(
    ctx: "Context", instance: "PostgreSQLInstance", foreground: bool, wait: bool
) -> FirstResult:
    """Start PostgreSQL for specified 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def stop_postgresql(
    ctx: "Context",
    instance: "PostgreSQLInstance",
    mode: str,
    wait: bool,
    deleting: bool,
) -> FirstResult:
    """Stop PostgreSQL for specified 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def restart_postgresql(
    ctx: "Context", instance: "Instance", mode: str, wait: bool
) -> FirstResult:
    """Restart PostgreSQL for specified 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def reload_postgresql(ctx: "Context", instance: "Instance") -> FirstResult:
    """Reload PostgreSQL configuration for 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def promote_postgresql(ctx: "Context", instance: "PostgreSQLInstance") -> FirstResult:
    """Promote PostgreSQL for 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def postgresql_service_name(ctx: "Context", instance: "BaseInstance") -> str:
    """Return the system service name (e.g.  postgresql).

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def enable_service(ctx: "Context", service: str, name: Optional[str]) -> FirstResult:
    """Enable a service

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def disable_service(
    ctx: "Context", service: str, name: Optional[str], now: Optional[bool]
) -> FirstResult:
    """Disable a service

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def start_service(ctx: "Context", service: str, name: Optional[str]) -> FirstResult:
    """Start a service for a plugin

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def stop_service(ctx: "Context", service: str, name: Optional[str]) -> FirstResult:
    """Stop a service for a plugin

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def restart_service(ctx: "Context", service: str, name: Optional[str]) -> FirstResult:
    """Restart a service for a plugin

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def schedule_service(ctx: "Context", service: str, name: str) -> FirstResult:
    """Schedule a job through timer

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def unschedule_service(
    ctx: "Context", service: str, name: str, now: Optional[bool]
) -> FirstResult:
    """Unchedule a job

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def start_timer(ctx: "Context", service: str, name: str) -> FirstResult:
    """Start a timer

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError


@hookspec(firstresult=True)  # type: ignore[misc]
def stop_timer(ctx: "Context", service: str, name: str) -> FirstResult:
    """Stop a timer

    Only one implementation should be invoked so call order and returned value
    matter.
    """
    raise NotImplementedError
