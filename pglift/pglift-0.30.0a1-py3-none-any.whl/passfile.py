import logging
from copy import copy
from typing import TYPE_CHECKING

from pgtoolkit import pgpass

from . import hookimpl
from .models.interface import PresenceState

if TYPE_CHECKING:
    from pgtoolkit.conf import Configuration

    from .ctx import Context
    from .models import interface
    from .models.system import PostgreSQLInstance
    from .types import ConfigChanges

logger = logging.getLogger(__name__)


@hookimpl
def instance_configure(
    ctx: "Context",
    manifest: "interface.Instance",
    config: "Configuration",
    changes: "ConfigChanges",
    creating: bool,
) -> None:
    """Update passfile entry for PostgreSQL roles upon instance
    re-configuration (port change).
    """
    if creating or "port" not in changes:
        return
    old_port, port = changes["port"]
    if port is None:
        port = config.get("port", 5432)
    if old_port is None:
        old_port = 5432
    assert isinstance(old_port, int)
    assert isinstance(port, int), port
    if port == old_port:
        return

    passfile = ctx.settings.postgresql.auth.passfile
    with pgpass.edit(passfile) as f:
        for entry in f:
            if entry.matches(port=old_port):
                entry.port = port
                logger.info(
                    "updating entry for '%(username)s' in %(passfile)s (port changed: %(old_port)d->%(port)d)",
                    {
                        "username": entry.username,
                        "passfile": passfile,
                        "old_port": old_port,
                        "port": port,
                    },
                )


@hookimpl
def instance_drop(ctx: "Context", instance: "PostgreSQLInstance") -> None:
    """Remove password file (pgpass) entries for the instance being dropped."""
    passfile_path = ctx.settings.postgresql.auth.passfile
    if not passfile_path.exists():
        return
    with pgpass.edit(passfile_path) as passfile:
        logger.info(
            "removing entries matching port=%(port)s from %(passfile)s",
            {"port": instance.port, "passfile": passfile_path},
        )
        passfile.remove(port=instance.port)
    if not passfile.lines:
        logger.info(
            "removing now empty %(passfile)s",
            {"passfile": passfile_path},
        )
        passfile_path.unlink()


@hookimpl
def instance_upgrade(
    ctx: "Context", old: "PostgreSQLInstance", new: "PostgreSQLInstance"
) -> None:
    """Add pgpass entries matching 'old' instance for the 'new' one."""
    old_port = old.port
    new_port = new.port
    passfile = ctx.settings.postgresql.auth.passfile
    with pgpass.edit(passfile) as f:
        for entry in f:
            if entry.matches(port=old_port):
                new_entry = copy(entry)
                new_entry.port = new_port
                f.lines.append(new_entry)
                logger.info("added entry %s in %s", new_entry, passfile)


@hookimpl
def role_change(
    ctx: "Context", role: "interface.BaseRole", instance: "PostgreSQLInstance"
) -> bool:
    """Create / update or delete passfile entry matching ('role', 'instance')."""
    port = instance.port
    username = role.name
    password = None
    if role.password:
        password = role.password.get_secret_value()
    passfile = ctx.settings.postgresql.auth.passfile
    with pgpass.edit(passfile) as f:
        for entry in f:
            if entry.matches(username=username, port=port):
                if role.state == PresenceState.absent or not role.pgpass:
                    logger.info(
                        "removing entry for '%(username)s' in %(passfile)s (port=%(port)d)",
                        {"username": username, "passfile": passfile, "port": port},
                    )
                    f.lines.remove(entry)
                    return True
                elif password is not None and entry.password != password:
                    logger.info(
                        "updating password for '%(username)s' in %(passfile)s (port=%(port)d)",
                        {"username": username, "passfile": passfile, "port": port},
                    )
                    entry.password = password
                    return True
                return False
        else:
            if role.pgpass and password is not None:
                logger.info(
                    "adding an entry for '%(username)s' in %(passfile)s (port=%(port)d)",
                    {"username": username, "passfile": passfile, "port": port},
                )
                entry = pgpass.PassEntry("*", port, "*", username, password)
                f.lines.append(entry)
                f.sort()
                return True
            return False
