import logging
import socket
import subprocess
import tempfile
import time
import urllib.parse
from contextlib import contextmanager
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Iterator, List, Optional, Tuple

import pgtoolkit.conf
import requests
import tenacity
import yaml
from tenacity.before_sleep import before_sleep_log
from tenacity.retry import retry_if_exception_type
from tenacity.wait import wait_exponential, wait_fixed

from .. import cmd, conf, exceptions, postgresql
from ..models import interface, system
from ..task import task
from .models import ClusterMember, Patroni, ServiceManifest

if TYPE_CHECKING:
    from ..ctx import Context
    from ..settings import PatroniSettings, Settings
    from ..types import ConfigChanges

logger = logging.getLogger(__name__)


def available(settings: "Settings") -> Optional["PatroniSettings"]:
    return settings.patroni


def get_settings(settings: "Settings") -> "PatroniSettings":
    """Return settings for patroni

    Same as `available` but assert that settings are not None.
    Should be used in a context where settings for the plugin are surely
    set (for example in hookimpl).
    """
    assert settings.patroni is not None
    return settings.patroni


def enabled(qualname: str, settings: "PatroniSettings") -> bool:
    return _configpath(qualname, settings).exists()


def _configpath(qualname: str, settings: "PatroniSettings") -> Path:
    return Path(str(settings.configpath).format(name=qualname))


def _pidfile(qualname: str, settings: "PatroniSettings") -> Path:
    return Path(str(settings.pid_file).format(name=qualname))


def _logpath(qualname: str, settings: "PatroniSettings") -> Path:
    return Path(str(settings.logpath).format(name=qualname))


def config(qualname: str, settings: "PatroniSettings") -> Patroni:
    fpath = _configpath(qualname, settings)
    if not fpath.exists():
        raise exceptions.FileNotFoundError(
            f"Patroni configuration for {qualname} node not found"
        )
    with fpath.open() as f:
        data = yaml.safe_load(f)
    return Patroni.parse_obj(data)


def validate_config(content: str, settings: "PatroniSettings") -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".yaml") as f:
        f.write(content)
        f.seek(0)
        try:
            subprocess.run(  # nosec B603
                [str(settings.execpath), "--validate-config", f.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logger.warning("invalid Patroni configuration: %s", e.stdout.strip())


def write_config(
    ctx: "Context",
    name: str,
    config: Patroni,
    settings: "PatroniSettings",
    *,
    validate: bool = False,
) -> None:
    """Write Patroni YAML configuration to disk after validation."""
    content = config.yaml()
    if validate:
        validate_config(content, settings)
    path = _configpath(name, settings)
    path.parent.mkdir(mode=0o750, exist_ok=True, parents=True)
    path.write_text(content)
    path.chmod(0o600)


def maybe_backup_config(
    qualname: str, *, node: str, cluster: str, settings: "PatroniSettings"
) -> None:
    """Make a backup of Patroni YAML configuration for 'qualname' instance
    alongside the original file, if 'node' is the last member in 'cluster'.
    """
    configpath = _configpath(qualname, settings)
    members = cluster_members(qualname, settings)
    if len(members) == 1 and members[0].name == node:
        backuppath = configpath.parent / f"{cluster}-{node}-{time.time()}.yaml"
        logger.warning(
            "'%s' appears to be the last member of cluster '%s', "
            "saving Patroni configuration file to %s",
            node,
            cluster,
            backuppath,
        )
        backuppath.write_text(
            f"# Backup of Patroni configuration for instance '{qualname}'\n"
            + configpath.read_text()
        )


def postgresql_changes(
    qualname: str, patroni: Patroni, settings: "PatroniSettings"
) -> "ConfigChanges":
    """Return changes to PostgreSQL parameters w.r.t. to actual Patroni configuration."""
    configpath = _configpath(qualname, settings)
    config_before = {}
    if configpath.exists():
        config_before = config(qualname, settings).postgresql.parameters
    # Round-trip dump/load in order to get the suppress serialization effects
    # (e.g. timedelta to / from str).
    config_after = yaml.safe_load(patroni.yaml())["postgresql"]["parameters"]
    return conf.changes(config_before, config_after)


def api_request(
    patroni: Patroni, method: str, path: str, *args: Any, **kwargs: Any
) -> requests.Response:
    url = urllib.parse.urlunparse(("http", patroni.restapi.listen, path, "", "", ""))
    try:
        r = requests.request(method, url, *args, **kwargs)
    except requests.ConnectionError as exc:
        raise exc from None
    r.raise_for_status()
    return r


@contextmanager
def setup(
    ctx: "Context",
    instance: "system.BaseInstance",
    manifest: "interface.Instance",
    service: "ServiceManifest",
    settings: "PatroniSettings",
    configuration: pgtoolkit.conf.Configuration,
    *,
    validate: bool = False,
) -> Iterator[Patroni]:
    """Context manager setting up Patroni for instance *in memory*, yielding
    the Patroni object, and writing to disk upon successful exit.
    """
    logger.info("setting up Patroni service")
    logpath = _logpath(instance.qualname, settings)
    logpath.mkdir(exist_ok=True, parents=True)
    p = _configpath(instance.qualname, settings)
    if p.exists():
        with p.open() as f:
            args = yaml.safe_load(f)
    else:
        args = {}
    args.setdefault("scope", service.cluster)
    args.setdefault("name", service.node)
    args.setdefault("log", {"dir": logpath})
    etcd = "etcd" if settings.etcd.v2 else "etcd3"
    args.setdefault(etcd, settings.etcd.copy(exclude={"v2"}))
    args.setdefault("restapi", service.restapi)
    args.setdefault("watchdog", settings.watchdog)
    patroni = Patroni.build(
        service.postgresql_connect_host, instance, manifest, configuration, **args
    )
    yield patroni
    write_config(ctx, instance.qualname, patroni, settings, validate=validate)


@tenacity.retry(
    retry=(
        retry_if_exception_type(exceptions.InstanceNotFound)
        | retry_if_exception_type(exceptions.InstanceStateError)
        | retry_if_exception_type(requests.ConnectionError)
        | retry_if_exception_type(requests.HTTPError)
    ),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=before_sleep_log(logger, logging.DEBUG),
)
def wait_ready(
    ctx: "Context",
    instance: "system.BaseInstance",
    patroni: Patroni,
    settings: "PatroniSettings",
    bootstrap_logs: IO[str],
) -> None:
    """Wait for Patroni to bootstrap by checking that (1) the postgres
    instance exists, (2) that it's up and running and, (3) that Patroni REST
    API is ready.

    At each retry, log new lines found in Patroni logs to our logger.
    """
    for line in bootstrap_logs:
        logger.debug("%s: %s", settings.execpath, line.rstrip())
    pginstance = system.PostgreSQLInstance.system_lookup(ctx, instance)
    if not postgresql.is_ready(ctx, pginstance):
        raise exceptions.InstanceStateError(f"{instance} not ready")
    api_request(patroni, "GET", "readiness")


@task("bootstraping PostgreSQL with Patroni")
def init(
    ctx: "Context",
    instance: "system.BaseInstance",
    patroni: Patroni,
    settings: "PatroniSettings",
) -> None:
    """Call patroni for bootstrap."""
    start_timeout = 5  # delay for Patroni bootstrap before checking instance status.
    logf = _logpath(instance.qualname, settings) / "patroni.log"
    logger.info("Patroni logs can be found at %s", logf)
    with start_background(
        ctx,
        instance.qualname,
        settings,
        timeout=start_timeout,
    ) as (_, f):
        wait_ready(ctx, instance, patroni, settings, f)
    logger.info("instance %s successfully created by Patroni", instance)


@init.revert("deconfiguring Patroni service")
def revert_init(
    ctx: "Context",
    instance: "system.BaseInstance",
    patroni: Patroni,
    settings: "PatroniSettings",
) -> None:
    delete(ctx, instance.qualname, patroni.name, patroni.scope, settings)


def delete(
    ctx: "Context",
    qualname: str,
    node: str,
    cluster_name: str,
    settings: "PatroniSettings",
) -> None:
    """Remove Patroni configuration for 'instance'."""
    if check_api_status(qualname, settings):
        maybe_backup_config(
            qualname, node=node, cluster=cluster_name, settings=settings
        )
    stop(ctx, qualname, settings)
    _configpath(qualname, settings).unlink(missing_ok=True)
    (_logpath(qualname, settings) / "patroni.log").unlink(missing_ok=True)


def start(
    ctx: "Context",
    name: str,
    settings: "PatroniSettings",
    *,
    foreground: bool = False,
) -> None:
    logger.info("starting Patroni %s", name)
    if foreground:
        configpath = _configpath(name, settings)
        args = [str(settings.execpath), str(configpath)]
        cmd.execute_program(args)
    else:
        pidfile = _pidfile(name, settings)
        if cmd.status_program(pidfile) == cmd.Status.running:
            logger.debug("Patroni '%s' is already running", name)
            return
        with start_background(ctx, name, settings):
            pass


@contextmanager
def start_background(
    ctx: "Context", name: str, settings: "PatroniSettings", **kwargs: Any
) -> Iterator[Tuple["cmd.Program", IO[str]]]:
    """Context manager to start Patroni in the background using
    :class:`~pglift.cmd.Program`.

    :param kwargs: extra arguments passed to :class:`~pglift.cmd.Program`.
    """
    pidfile = _pidfile(name, settings)
    configpath = _configpath(name, settings)
    args = [str(settings.execpath), str(configpath)]
    with cmd.Program(args, pidfile, capture_output=True, **kwargs) as p:
        with logstream(name, settings) as f:
            if not check_api_status(name, settings):
                for line in f:
                    logger.warning("%s: %s", args[0], line.rstrip())
                if ctx.confirm("Patroni failed to start, abort?", default=False):
                    raise exceptions.Cancelled(f"Patroni {name} start cancelled")
            yield p, f


def stop(ctx: "Context", name: str, settings: "PatroniSettings") -> None:
    logger.info("stopping Patroni %s", name)
    pidfile = _pidfile(name, settings)
    if cmd.status_program(pidfile) == cmd.Status.not_running:
        logger.debug("Patroni '%s' is already stopped", name)
        return
    cmd.terminate_program(pidfile)
    logger.info("waiting for Patroni REST API to stop")
    wait_api_down(name, settings)


def restart(
    ctx: "Context",
    instance: "system.BaseInstance",
    settings: "PatroniSettings",
    timeout: int = 3,
) -> None:
    logger.info("restarting Patroni %s", instance.qualname)
    patroni = config(instance.qualname, settings)
    api_request(patroni, "POST", "restart", json={"timeout": timeout})


def reload(
    ctx: "Context", instance: "system.BaseInstance", settings: "PatroniSettings"
) -> None:
    logger.info("reloading Patroni %s", instance.qualname)
    patroni = config(instance.qualname, settings)
    api_request(patroni, "POST", "reload")


def cluster_members(qualname: str, settings: "PatroniSettings") -> List[ClusterMember]:
    """Return the list of members of the Patroni cluster which 'instance' is member of."""
    patroni = config(qualname, settings)
    r = api_request(patroni, "GET", "cluster")
    return [ClusterMember(**item) for item in r.json()["members"]]


def cluster_leader(qualname: str, settings: "PatroniSettings") -> Optional[str]:
    for m in cluster_members(qualname, settings):
        if m.role == "leader":
            return m.name
    return None


def check_api_status(
    name: str, settings: "PatroniSettings", *, logger: Optional[logging.Logger] = logger
) -> bool:
    """Return True if the REST API of Patroni with 'name' is listening."""
    patroni = config(name, settings)
    api_address = patroni.restapi.listen
    if logger:
        logger.debug(
            "checking status of REST API for Patroni %s at %s", name, api_address
        )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex((api_address.host, api_address.port)) == 0:
            return True
    if logger:
        logger.error("REST API for Patroni %s not listening at %s", name, api_address)
    return False


@tenacity.retry(
    retry=retry_if_exception_type(exceptions.Error),
    wait=wait_fixed(1),
    before_sleep=before_sleep_log(logger, logging.DEBUG),
)
def wait_api_down(name: str, settings: "PatroniSettings") -> None:
    if check_api_status(name, settings, logger=None):
        raise exceptions.Error("Patroni REST API still running")


@contextmanager
def logstream(name: str, settings: "PatroniSettings") -> Iterator[IO[str]]:
    logf = _logpath(name, settings) / "patroni.log"
    if not logf.exists():
        raise exceptions.FileNotFoundError(f"no Patroni logs found at {logf}")
    with logf.open() as f:
        yield f


def logs(name: str, settings: "PatroniSettings") -> Iterator[str]:
    with logstream(name, settings) as f:
        yield from f
