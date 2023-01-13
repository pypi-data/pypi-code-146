import configparser
import datetime
import json
import logging
import os
import re
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional

from dateutil.tz import gettz
from pgtoolkit import conf as pgconf

from .. import exceptions, util
from ..models import interface
from ..task import task
from .models import Service

if TYPE_CHECKING:
    from ..ctx import Context
    from ..models import system
    from ..settings import PgBackRestSettings, Settings

logger = logging.getLogger(__name__)


def available(settings: "Settings") -> Optional["PgBackRestSettings"]:
    return settings.pgbackrest


def get_settings(settings: "Settings") -> "PgBackRestSettings":
    """Return settings for pgbackrest

    Same as `available` but assert that settings are not None.
    Should be used in a context where settings for the plugin are surely
    set (for example in hookimpl).
    """
    assert settings.pgbackrest is not None
    return settings.pgbackrest


def enabled(
    instance: "system.PostgreSQLInstance", settings: "PgBackRestSettings"
) -> bool:
    return system_lookup(instance.datadir, settings) is not None


def base_configpath(settings: "PgBackRestSettings") -> Path:
    return settings.configpath / "pgbackrest.conf"


def config_directory(settings: "PgBackRestSettings") -> Path:
    return settings.configpath / "conf.d"


def make_cmd(stanza: str, settings: "PgBackRestSettings", *args: str) -> List[str]:
    return [
        str(settings.execpath),
        f"--config-path={settings.configpath}",
        f"--stanza={stanza}",
    ] + list(args)


parser = partial(configparser.ConfigParser, strict=True)

pgpath_rgx = re.compile(r"pg(\d+)-path")


def system_lookup(datadir: Path, settings: "PgBackRestSettings") -> Optional[Service]:
    d = config_directory(settings)
    for p in d.glob("*.conf"):
        cp = parser()
        with p.open() as f:
            cp.read_file(f)
        for stanza in cp.sections():
            for key, value in cp.items(stanza):
                m = pgpath_rgx.match(key)
                if m and value == str(datadir):
                    return Service(stanza=stanza, path=p, index=int(m.group(1)))
    return None


def backup_info(
    ctx: "Context",
    service: Service,
    settings: "PgBackRestSettings",
    *,
    backup_set: Optional[str] = None,
) -> Dict[str, Any]:
    """Call pgbackrest info command to obtain information about backups.

    Ref.: https://pgbackrest.org/command.html#command-info
    """
    args = []
    if backup_set is not None:
        args.append(f"--set={backup_set}")
    args.extend(["--output=json", "info"])
    r = ctx.run(make_cmd(service.stanza, settings, *args), check=True)
    infos = json.loads(r.stdout)
    try:
        return next(i for i in infos if i["name"] == service.stanza)
    except StopIteration:
        return {}


@task("setting up pgBackRest")
def setup(
    ctx: "Context",
    service: Service,
    settings: "PgBackRestSettings",
    instance_config: pgconf.Configuration,
    datadir: Path,
) -> None:
    """Setup pgBackRest"""
    base_config_path = base_configpath(settings)
    if not base_config_path.exists():
        raise exceptions.SystemError(
            f"Missing base config file {base_config_path} for pgbackrest. "
            "Did you forget to run 'pglift site-configure'?"
        )
    stanza = service.stanza
    stanza_confpath = service.path
    pg = f"pg{service.index}"
    cp = parser()
    if stanza_confpath.exists():
        with stanza_confpath.open() as f:
            cp.read_file(f)

    # Always use string values so that this would match with actual config (on
    # disk) that's parsed later on.
    config = {
        stanza: {
            f"{pg}-path": str(datadir),
            f"{pg}-port": str(instance_config.get("port", 5432)),
            f"{pg}-user": ctx.settings.postgresql.backuprole.name,
        },
    }
    unix_socket_directories = instance_config.get("unix_socket_directories")
    if unix_socket_directories:
        config[stanza][f"{pg}-socket-path"] = str(
            instance_config.unix_socket_directories
        )
    cp.read_dict(config)
    with stanza_confpath.open("w") as configfile:
        cp.write(configfile)


def postgresql_configuration(
    stanza: str, settings: "PgBackRestSettings"
) -> pgconf.Configuration:
    pgconfig = util.template("postgresql", "pgbackrest.conf").format(
        execpath=settings.execpath, configpath=settings.configpath, stanza=stanza
    )
    config = pgconf.Configuration()
    list(config.parse(pgconfig.splitlines()))
    return config


@setup.revert("deconfiguring pgBackRest")
def revert_setup(
    ctx: "Context",
    service: Service,
    settings: "PgBackRestSettings",
    instance_config: pgconf.Configuration,
    datadir: Path,
) -> None:
    """Un-setup pgBackRest.

    Remove options from 'stanza' section referencing instance's datadir, then
    possibly remove the configuration file if empty, and finally remove
    stanza's log files.
    """
    stanza = service.stanza
    stanza_confpath = service.path
    if stanza_confpath.exists():
        cp = parser()
        with stanza_confpath.open() as f:
            cp.read_file(f)
        for opt in cp.options(stanza):
            if opt.startswith(f"pg{service.index}-"):
                cp.remove_option(stanza, opt)
        with stanza_confpath.open("w") as f:
            cp.write(f)
        if not cp.options(stanza):
            stanza_confpath.unlink(missing_ok=True)
    if not stanza_confpath.exists():
        for logf in settings.logpath.glob(f"{stanza}-*.log"):
            logf.unlink(missing_ok=True)


def check(
    ctx: "Context",
    instance: "system.PostgreSQLInstance",
    service: Service,
    settings: "PgBackRestSettings",
    password: Optional[str],
) -> None:
    env = os.environ.copy()
    if password is not None:
        env["PGPASSWORD"] = password
    env = ctx.settings.postgresql.libpq_environ(
        ctx, instance, ctx.settings.postgresql.backuprole.name, base=env
    )
    ctx.run(make_cmd(service.stanza, settings, "check"), check=True, env=env)


def iter_backups(
    ctx: "Context", instance: "system.Instance", settings: "PgBackRestSettings"
) -> Iterator[interface.InstanceBackup]:
    """Yield information about backups on an instance."""
    service = instance.service(Service)
    backups = backup_info(ctx, service, settings)["backup"]

    def started_at(entry: Any) -> float:
        return entry["timestamp"]["start"]  # type: ignore[no-any-return]

    for backup in sorted(backups, key=started_at, reverse=True):
        info_set = backup_info(ctx, service, settings, backup_set=backup["label"])
        databases = [db["name"] for db in info_set["backup"][0]["database-ref"]]
        dtstart = datetime.datetime.fromtimestamp(backup["timestamp"]["start"])
        dtstop = datetime.datetime.fromtimestamp(backup["timestamp"]["stop"])
        yield interface.InstanceBackup(
            label=backup["label"],
            size=backup["info"]["size"],
            repo_size=backup["info"]["repository"]["size"],
            date_start=dtstart.replace(tzinfo=gettz()),
            date_stop=dtstop.replace(tzinfo=gettz()),
            type=backup["type"],
            databases=databases,
        )


def restore_command(
    instance: "system.Instance",
    settings: "PgBackRestSettings",
    *,
    date: Optional[datetime.datetime] = None,
    backup_set: Optional[str] = None,
) -> List[str]:
    """Return the pgbackrest restore for ``instance``.

    Ref.: https://pgbackrest.org/command.html#command-restore
    """
    args = [
        "--log-level-console=info",
        # The delta option allows pgBackRest to handle instance data/wal
        # directories itself, without the need to clean them up beforehand.
        "--delta",
        "--link-all",
    ]
    if date is not None and backup_set is not None:
        raise exceptions.UnsupportedError(
            "date and backup_set are not expected to be both specified"
        )
    elif date is not None:
        target = date.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        args += ["--target-action=promote", "--type=time", f"--target={target}"]
    elif backup_set is not None:
        args += ["--target-action=promote", "--type=immediate", f"--set={backup_set}"]
    args.append("restore")
    s = instance.service(Service)
    return make_cmd(s.stanza, settings, *args)


def restore(
    ctx: "Context",
    instance: "system.Instance",
    settings: "PgBackRestSettings",
    *,
    label: Optional[str] = None,
    date: Optional[datetime.datetime] = None,
) -> None:
    """Restore an instance, possibly only including specified databases.

    The instance must not be running.

    Ref.: https://pgbackrest.org/command.html#command-restore
    """
    logger.info("restoring instance %s with pgBackRest", instance)
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)

    cmd = restore_command(instance, settings, date=date, backup_set=label)
    ctx.run(cmd, check=True)


def env_for(service: "Service", settings: "PgBackRestSettings") -> Dict[str, str]:
    return {
        "PGBACKREST_CONFIG_PATH": str(settings.configpath),
        "PGBACKREST_STANZA": service.stanza,
    }
