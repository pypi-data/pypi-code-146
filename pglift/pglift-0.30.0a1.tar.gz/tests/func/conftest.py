import logging
import pathlib
import platform
import shutil
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    TypeVar,
)
from unittest.mock import patch

import pgtoolkit.conf
import psycopg.conninfo
import pydantic
import pytest
from pydantic.utils import deep_update

from pglift import _install, instances, plugin_manager, postgresql
from pglift.backup import BACKUP_SERVICE_NAME, BACKUP_TIMER_NAME
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.pgbackrest import base as pgbackrest
from pglift.pgbackrest import models as pgbackrest_models
from pglift.postgresql import POSTGRESQL_SERVICE_NAME
from pglift.settings import PostgreSQLSettings, Settings

from . import AuthType, execute
from .pgbackrest import CA, Certificate, PgbackrestRepoHost


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--pg-auth",
        choices=[t.value for t in AuthType],
        default=AuthType.peer.value,
        help="Run tests with PostgreSQL authentication method (default: %(default)s)",
    )
    parser.addoption(
        "--systemd",
        action="store_true",
        default=False,
        help="Run tests with systemd as service manager/scheduler",
    )
    if shutil.which("pgbackrest") is not None:
        parser.addoption(
            "--pgbackrest-repo-host",
            action="store_true",
            default=False,
            help="Use a dedicated repository host for pgbackrest",
        )


def pytest_report_header(config: Any) -> List[str]:
    systemd = config.option.systemd
    pg_auth = config.option.pg_auth
    pgbackrest_repo_host = config.getoption("pgbackrest_repo_host", False)
    return [
        f"auth method: {pg_auth}",
        f"systemd: {systemd}",
        f"pgbackrest repo host: {pgbackrest_repo_host}",
    ]


def pytest_configure(config: Any) -> None:
    config.addinivalue_line(
        "markers", "standby: mark test as concerning standby instance"
    )


@pytest.fixture(autouse=True)
def journalctl(systemd_requested: bool) -> Iterator[None]:
    journalctl = shutil.which("journalctl")
    if not systemd_requested or journalctl is None:
        yield
        return
    proc = subprocess.Popen([journalctl, "--user", "-f", "-n0"])
    yield
    proc.kill()


@pytest.fixture(scope="package")
def systemd_available() -> bool:
    try:
        subprocess.run(
            ["systemctl", "--user", "status"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return True


@pytest.fixture(scope="package")
def powa_available(no_plugins: bool, pg_bindir: Tuple[pathlib.Path, str]) -> bool:
    if no_plugins:
        return False
    pg_config = pg_bindir[0] / "pg_config"
    result = subprocess.run(
        [pg_config, "--pkglibdir"], stdout=subprocess.PIPE, check=True, text=True
    )
    pkglibdir = pathlib.Path(result.stdout.strip())
    return (
        (pkglibdir / "pg_qualstats.so").exists()
        and (pkglibdir / "pg_stat_kcache.so").exists()
        and (pkglibdir / "powa.so").exists()
    )


@pytest.fixture(scope="package")
def systemd_requested(request: Any, systemd_available: bool) -> bool:
    value = request.config.option.systemd
    assert isinstance(value, bool)
    if value and not systemd_available:
        raise pytest.UsageError("systemd is not available on this system")
    return value


@pytest.fixture(scope="package")
def postgresql_auth(request: Any) -> AuthType:
    return AuthType(request.config.option.pg_auth)


@pytest.fixture(scope="package")
def ca(tmp_path_factory: pytest.TempPathFactory) -> CA:
    return CA.make(tmp_path_factory.mktemp("ca-certs"), "pglift-tests-ca")


@pytest.fixture(scope="package")
def pgbackrest_repo_host(
    request: Any,
    pgbackrest_available: bool,
    ca: CA,
    tmp_path_factory: pytest.TempPathFactory,
    tmp_port_factory: Iterator[int],
    logger: logging.Logger,
) -> Iterator[Optional[PgbackrestRepoHost]]:
    if not request.config.option.pgbackrest_repo_host:
        yield None
        return

    assert pgbackrest_available
    path = tmp_path_factory.mktemp("pgbackrest-repo")
    ssl_path = path / "ssl"
    ssl_path.mkdir()
    logpath = path / "logs"
    logpath.mkdir()
    server_cn = client_cn = socket.getfqdn()
    server_keyfile, server_certfile = Certificate.make(
        ca.crt, ca.key, cn=server_cn
    ).install(ssl_path)
    with PgbackrestRepoHost(
        client_configpath=path / "pgbackrest.conf",
        server_configpath=path / "server.conf",
        logpath=logpath,
        port=next(tmp_port_factory),
        path=path / "backups",
        server_cn=server_cn,
        client_cn=client_cn,
        ca_file=ca.crt,
        server_certfile=server_certfile,
        server_keyfile=server_keyfile,
        logger=logger,
    ) as r:
        yield r


@pytest.fixture(scope="package")
def site_config(
    site_config: Callable[..., str], postgresql_auth: AuthType
) -> Iterator[Callable[..., Optional[str]]]:
    if postgresql_auth == AuthType.peer:

        datadir = pathlib.Path(__file__).parent / "data" / "peer"
    else:
        datadir = pathlib.Path(__file__).parent / "data" / "base"

    def test_site_config(*args: str) -> Optional[str]:
        """Lookup for configuration files in local data director first."""
        fpath = datadir.joinpath(*args)
        if fpath.exists():
            return fpath.read_text()
        return site_config(*args)

    with patch("pglift.util.site_config", new=test_site_config) as fn:
        yield fn


@pytest.fixture(scope="package")
def postgresql_settings(
    tmp_path_factory: pytest.TempPathFactory,
    postgresql_auth: AuthType,
    surole_password: Optional[str],
    pgbackrest_password: Optional[str],
) -> PostgreSQLSettings:
    """Factory to create a PostgreSQLSettings instance with distinct files
    (.pgpass or password_command file) from other instances.
    """
    passfile = tmp_path_factory.mktemp("home") / ".pgpass"
    if postgresql_auth == AuthType.pgpass:
        passfile.touch(mode=0o600)
    auth: Dict[str, Any] = {
        "local": "password",
        "passfile": str(passfile),
    }
    surole: Dict[str, Any] = {"name": "postgres"}
    backuprole: Dict[str, Any] = {"name": "backup"}
    if postgresql_auth == AuthType.peer:
        pass
    elif postgresql_auth == AuthType.password_command:
        passcmdfile = tmp_path_factory.mktemp("home") / "passcmd"
        auth["password_command"] = [str(passcmdfile), "{instance}", "{role}"]
        with passcmdfile.open("w") as f:
            f.write(
                dedent(
                    f"""\
                    #!/bin/sh
                    instance=$1
                    role=$2
                    if [ ! "$instance" ]
                    then
                        echo "no instance given!!" >&2
                        exit 1
                    fi
                    if [ ! "$role" ]
                    then
                        echo "no role given!!" >&2
                        exit 1
                    fi
                    if [ "$role" = {surole["name"]} ]
                    then
                        echo "retrieving password for $role for $instance..." >&2
                        echo {surole_password}
                        exit 0
                    fi
                    if [ "$role" = {backuprole["name"]} ]
                    then
                        echo "retrieving password for $role for $instance..." >&2
                        echo {pgbackrest_password}
                        exit 0
                    fi
                    """
                )
            )
        passcmdfile.chmod(0o700)
    elif postgresql_auth == AuthType.pgpass:
        surole["pgpass"] = True
        backuprole["pgpass"] = True
    else:
        raise AssertionError(f"unexpected {postgresql_auth}")
    return PostgreSQLSettings.parse_obj(
        {
            "auth": auth,
            "surole": surole,
            "backuprole": backuprole,
        }
    )


@pytest.fixture(scope="package")
def settings(
    tmp_path_factory: pytest.TempPathFactory,
    postgresql_settings: PostgreSQLSettings,
    systemd_requested: bool,
    systemd_available: bool,
    patroni_execpath: Optional[pathlib.Path],
    etcd_host: str,
    pgbackrest_available: bool,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    ca: CA,
    prometheus_execpath: Optional[pathlib.Path],
    powa_available: bool,
    temboard_execpath: Optional[pathlib.Path],
    tmp_port_factory: Iterator[int],
) -> Settings:
    prefix = tmp_path_factory.mktemp("prefix")
    (prefix / "run" / "postgresql").mkdir(parents=True)
    obj = {
        "prefix": str(prefix),
        "run_prefix": str(tmp_path_factory.mktemp("run")),
        "postgresql": postgresql_settings.dict(),
    }
    if systemd_requested:
        obj.update({"systemd": {}})

    if obj.get("service_manager") == "systemd" and not systemd_available:
        pytest.skip("systemd not functional")

    if patroni_execpath:
        obj["patroni"] = {
            "execpath": str(patroni_execpath),
            "loop_wait": 1,
            "etcd": {"hosts": [etcd_host]},
        }

    if pgbackrest_available:
        if pgbackrest_repo_host is not None:
            keyfile, crtfile = Certificate.make(
                ca.crt, ca.key, cn=pgbackrest_repo_host.client_cn
            ).install(tmp_path_factory.mktemp("pgbackrest-certs"))
            obj["pgbackrest"] = {
                "repository": {
                    "host": socket.getfqdn(),
                    "host_port": pgbackrest_repo_host.port,
                    "host_config": pgbackrest_repo_host.client_configpath,
                    "ca_cert": ca.crt,
                    "cn": pgbackrest_repo_host.server_cn,
                    "certificate": {"cert": crtfile, "key": keyfile},
                    "port": next(tmp_port_factory),
                },
            }
        else:
            obj["pgbackrest"] = {
                "repository": {"path": tmp_path_factory.mktemp("backups")},
            }

    if prometheus_execpath:
        obj["prometheus"] = {"execpath": prometheus_execpath}

    if powa_available:
        obj["powa"] = {}

    if temboard_execpath:
        temboard_signing_key = prefix / "etc" / "temboard-agent" / "signing-public.pem"
        obj["temboard"] = {
            "execpath": temboard_execpath,
            "ui_url": "https://0.0.0.0:8888",
            "signing_key": temboard_signing_key,
        }
        temboard_signing_key.parent.mkdir(parents=True)
        temboard_signing_key.write_text(
            "-----BEGIN PUBLIC KEY-----\n"
            "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChaZFhzRuFgNDLgAJ2+WQsVQ75\n"
            "G9UswuVxTfltxP4mc+ou8lyj7Ck73+M3HkFE2r623g6DZcNYCXqpyNpInsBo68kD\n"
            "IDgwHKaQBTPyve0VhNjkJyqoKIC6AJKv/wixEwsHUm/rNU8cXnY7WCNGjCV+JrEm\n"
            "ekHBWP1X4hFfPKcvvwIDAQAB\n"
            "-----END PUBLIC KEY-----"
        )

    try:
        s = Settings.parse_obj(obj)
    except pydantic.ValidationError as exc:
        pytest.skip(
            "; ".join(
                f"unsupported setting(s) {' '.join(map(str, e['loc']))}: {e['msg']}"
                for e in exc.errors()
            )
        )

    return s


@pytest.fixture
def ctx(settings: Settings) -> Context:
    return Context(settings=settings)


@pytest.fixture(scope="package")
def require_systemd_scheduler(settings: Settings) -> None:
    if settings.scheduler != "systemd":
        pytest.skip("not applicable for scheduler method other than 'systemd'")


@pytest.fixture(scope="package")
def require_pgbackrest(settings: Settings) -> None:
    if not settings.pgbackrest:
        pytest.skip("not applicable if pgbackrest is not activated")


@pytest.fixture(autouse=True)
def _hook_logger(ctx: Context, logger: logging.Logger) -> None:
    hook_level = logging.DEBUG - 1
    logging.addLevelName(hook_level, "HOOK")
    logger.setLevel(hook_level)

    def before(
        hook_name: str, hook_impls: Sequence[Any], kwargs: Dict[str, Any]
    ) -> None:
        if not hook_impls:
            return

        def p(value: Any) -> str:
            s = str(value)
            if len(s) >= 20:
                s = f"{s[:17]}..."
            return s

        logger.log(
            hook_level,
            "calling hook %s(%s) with implementations: %s",
            hook_name,
            ", ".join(f"{k}={p(v)}" for k, v in kwargs.items()),
            ", ".join(i.plugin_name for i in hook_impls),
        )

    def after(
        outcome: Any, hook_name: str, hook_impls: Sequence[Any], kwargs: Dict[str, Any]
    ) -> None:
        if not hook_impls:
            return
        logger.log(hook_level, "outcome of %s: %s", hook_name, outcome.get_result())

    ctx.pm.add_hookcall_monitoring(before, after)


@pytest.fixture(scope="package", autouse=True)
def _installed(
    settings: Settings,
    systemd_requested: bool,
    tmp_path_factory: pytest.TempPathFactory,
    override_systemd_unit_start_limit: Iterator[None],
) -> Iterator[None]:
    tmp_path = tmp_path_factory.mktemp("config")

    if systemd_requested:
        assert settings.service_manager == "systemd"

    custom_settings = tmp_path / "settings.json"
    custom_settings.write_text(settings.json())
    _install.do(
        settings,
        env=f"SETTINGS=@{custom_settings}",
        header=f"# ** Test run on {platform.node()} at {datetime.now().isoformat()} **",
    )
    yield
    _install.undo(settings)


@pytest.fixture(scope="package")
def override_systemd_unit_start_limit(systemd_requested: bool) -> Iterator[None]:
    """Override the systemd configuration for the instance to prevent
    errors when too many starts happen in a short amount of time
    """
    if not systemd_requested:
        yield
        return
    units = [
        POSTGRESQL_SERVICE_NAME,
        BACKUP_SERVICE_NAME,
        BACKUP_TIMER_NAME,
    ]
    overrides_dir = Path("~/.config/systemd/user").expanduser()
    overrides = [overrides_dir / f"{unit}.d" / "override.conf" for unit in units]
    for override in overrides:
        override.parent.mkdir(parents=True, exist_ok=True)
        content = """
        [Unit]
        StartLimitIntervalSec=0
        """
        override.write_text(dedent(content))

    yield

    for override in overrides:
        shutil.rmtree(override.parent)


@pytest.fixture(scope="package")
def surole_password(postgresql_auth: AuthType) -> Optional[str]:
    if postgresql_auth == AuthType.peer:
        return None
    return "s3kret p@Ssw0rd!"


@pytest.fixture(scope="package")
def replrole_password(settings: Settings) -> str:
    return "r3pl p@Ssw0rd!"


@pytest.fixture(scope="package")
def prometheus_password() -> str:
    # TODO: use a password with blanks when
    # https://github.com/prometheus-community/postgres_exporter/issues/393 is fixed
    return "prom3th3us-p@Ssw0rd!"


@pytest.fixture(scope="package")
def temboard_password() -> str:
    return "tembo@rd p@Ssw0rd!"


@pytest.fixture(scope="package")
def powa_password() -> str:
    return "P0w4 p@Ssw0rd!"


@pytest.fixture(scope="package")
def pgbackrest_password(postgresql_auth: AuthType) -> Optional[str]:
    if postgresql_auth == AuthType.peer:
        return None
    return "b4ckup p@Ssw0rd!"


@pytest.fixture(scope="package")
def log_directory(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    return tmp_path_factory.mktemp("postgres-logs")


T_co = TypeVar("T_co", covariant=True)


class Factory(Protocol[T_co]):
    def __call__(self, s: Settings, name: str, state: str = ..., **kwargs: Any) -> T_co:
        ...


@pytest.fixture(scope="package")
def instance_manifest_factory(
    pg_version: str,
    surole_password: Optional[str],
    replrole_password: str,
    pgbackrest_password: Optional[str],
    prometheus_password: str,
    temboard_password: str,
    powa_password: str,
    log_directory: pathlib.Path,
    tmp_port_factory: Iterator[int],
) -> Factory[interface.Instance]:
    def factory(
        s: Settings, name: str, state: str = "stopped", **kwargs: Any
    ) -> interface.Instance:
        port = next(tmp_port_factory)
        services = {}
        if s.prometheus:
            services["prometheus"] = {
                "port": next(tmp_port_factory),
                "password": prometheus_password,
            }
        if s.powa:
            services["powa"] = {"password": powa_password}
        if s.temboard:
            services["temboard"] = {
                "password": temboard_password,
                "port": next(tmp_port_factory),
            }
        if s.pgbackrest:
            services["pgbackrest"] = {
                "password": pgbackrest_password,
                "stanza": f"mystanza-{name}",
            }
        m = {
            "name": name,
            "version": pg_version,
            "state": state,
            "port": port,
            "auth": {
                "host": "trust",
            },
            "settings": {
                "log_directory": str(log_directory),
                "shared_preload_libraries": "passwordcheck",
            },
            "surole_password": surole_password,
            "replrole_password": replrole_password,
            "restart_on_changes": True,
            **services,
        }
        m = deep_update(m, kwargs)
        pm = plugin_manager(s)
        return interface.Instance.composite(pm).parse_obj(m)

    return factory


@pytest.fixture(scope="package")
def instance_manifest(
    settings: Settings,
    instance_manifest_factory: Factory[interface.Instance],
) -> interface.Instance:
    return instance_manifest_factory(settings, "test", state="started")


@pytest.fixture
def instance_factory(
    instance_manifest_factory: Factory[interface.Instance],
) -> Iterator[Factory[Tuple[interface.Instance, system.Instance]]]:
    values: Dict[str, Tuple[system.Instance, Context]] = {}

    def factory(
        s: Settings, name: str, state: str = "stopped", **kwargs: Any
    ) -> Tuple[interface.Instance, system.Instance]:
        assert name not in values, f"{name} already used"
        m = instance_manifest_factory(s, name, state=state, **kwargs)
        ctx = Context(settings=s)
        result = instances.apply(ctx, m)
        assert result.change_state == interface.ApplyChangeState.created
        i = system.Instance.system_lookup(ctx, (m.name, m.version))
        values[name] = i, ctx
        return m, i

    yield factory

    for i, ctx in values.values():
        _drop_instance_if_exists(i, ctx)


@pytest.fixture(scope="package")
def instance(
    settings: Settings,
    instance_manifest: interface.Instance,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    pgbackrest_password: Optional[str],
) -> Iterator[system.Instance]:
    ctx = Context(settings=settings)
    assert instances.apply(ctx, instance_manifest)
    instance = system.Instance.system_lookup(
        ctx, (instance_manifest.name, instance_manifest.version)
    )
    if settings.pgbackrest and pgbackrest_repo_host is not None:
        svc = instance.service(pgbackrest_models.Service)
        pgbackrest_repo_host.add_stanza(svc.stanza, instance)
        pgbackrest.check(ctx, instance, svc, settings.pgbackrest, pgbackrest_password)
    # Limit postgresql.conf to uncommented entries to reduce pytest's output
    # due to --show-locals.
    postgresql_conf = instance.datadir / "postgresql.conf"
    postgresql_conf.write_text(
        "\n".join(
            line
            for line in postgresql_conf.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
    )
    yield instance
    _drop_instance_if_exists(instance, ctx)


@pytest.fixture(scope="package")
def instance_primary_conninfo(settings: Settings, instance: system.Instance) -> str:
    return psycopg.conninfo.make_conninfo(
        host=settings.postgresql.socket_directory,
        port=instance.port,
        user=settings.postgresql.replrole,
    )


@pytest.fixture(scope="package")
def standby_manifest(
    settings: Settings,
    replrole_password: str,
    instance_primary_conninfo: str,
    instance_manifest_factory: Factory[interface.Instance],
) -> interface.Instance:
    return instance_manifest_factory(
        settings,
        "standby",
        state="started",
        surole_password=None,
        standby={
            "primary_conninfo": instance_primary_conninfo,
            "password": replrole_password,
            "slot": "standby",
        },
    )


@pytest.fixture(scope="package")
def standby_instance(
    settings: Settings,
    standby_manifest: interface.Instance,
    instance: system.Instance,
) -> Iterator[system.Instance]:
    ctx = Context(settings=settings)
    assert postgresql.is_running(ctx, instance)
    standby = standby_manifest.standby
    assert standby is not None
    execute(
        ctx,
        instance,
        f"SELECT true FROM pg_create_physical_replication_slot('{standby.slot}')",
        fetch=False,
    )
    instances.apply(ctx, standby_manifest)
    stdby_instance = system.Instance.system_lookup(
        ctx, (standby_manifest.name, standby_manifest.version)
    )
    yield stdby_instance
    _drop_instance_if_exists(stdby_instance, ctx)


@pytest.fixture(scope="package")
def to_be_upgraded_manifest(
    settings: Settings, instance_manifest_factory: Factory[interface.Instance]
) -> interface.Instance:
    return instance_manifest_factory(settings, "to_be_upgraded")


@pytest.fixture(scope="package")
def to_be_upgraded_instance(
    settings: Settings,
    to_be_upgraded_manifest: interface.Instance,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    pgbackrest_password: Optional[str],
) -> Iterator[system.Instance]:
    m = to_be_upgraded_manifest
    ctx = Context(settings=settings)
    assert instances.apply(ctx, m)
    instance = system.Instance.system_lookup(ctx, (m.name, m.version))
    if settings.pgbackrest and pgbackrest_repo_host is not None:
        svc = instance.service(pgbackrest_models.Service)
        with postgresql.running(ctx, instance):
            pgbackrest_repo_host.add_stanza(svc.stanza, instance)
            pgbackrest.check(
                ctx, instance, svc, settings.pgbackrest, pgbackrest_password
            )
    yield instance
    _drop_instance_if_exists(instance, ctx)


@pytest.fixture(scope="package")
def upgraded_instance(
    settings: Settings,
    to_be_upgraded_instance: system.Instance,
    tmp_port_factory: Iterator[int],
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    pgbackrest_password: Optional[str],
) -> Iterator[system.Instance]:
    ctx = Context(settings=settings)
    port = next(tmp_port_factory)
    instance = instances.upgrade(
        ctx,
        to_be_upgraded_instance,
        name="upgraded",
        version=to_be_upgraded_instance.version,
        port=port,
        _instance_model=interface.Instance.composite(ctx.pm),
    )
    if settings.pgbackrest and pgbackrest_repo_host is not None:
        svc = instance.service(pgbackrest_models.Service)
        assert svc == to_be_upgraded_instance.service(pgbackrest_models.Service)
        with pgbackrest_repo_host.edit_config() as cfg:
            cfg[svc.stanza]["pg1-path"] = str(instance.datadir)
            cfg[svc.stanza]["pg1-port"] = str(port)
        with postgresql.running(ctx, instance):
            pgbackrest_repo_host.run(
                "stanza-upgrade", "--stanza", svc.stanza, "--no-online"
            )
            pgbackrest.check(
                ctx, instance, svc, settings.pgbackrest, pgbackrest_password
            )
    yield instance
    _drop_instance_if_exists(instance, ctx)


def _drop_instance(instance: system.Instance) -> pgtoolkit.conf.Configuration:
    config = instance.config()
    _drop_instance_if_exists(instance)
    return config


def _drop_instance_if_exists(
    instance: system.Instance, ctx: Optional[Context] = None
) -> None:
    if ctx is None:
        ctx = Context(settings=instance._settings)
    if instances.exists(ctx, instance.name, instance.version):
        # Do a new system_lookup() in order to get the list of services refreshed.
        instance = system.Instance.system_lookup(ctx, instance)
        instances.drop(ctx, instance)


@pytest.fixture(scope="package")
def instance_dropped(instance: system.Instance) -> pgtoolkit.conf.Configuration:
    return _drop_instance(instance)


@pytest.fixture(scope="package")
def standby_instance_dropped(
    standby_instance: system.Instance,
) -> pgtoolkit.conf.Configuration:
    return _drop_instance(standby_instance)


@pytest.fixture(scope="package")
def to_be_upgraded_instance_dropped(
    to_be_upgraded_instance: system.Instance,
) -> pgtoolkit.conf.Configuration:
    return _drop_instance(to_be_upgraded_instance)


@pytest.fixture(scope="package")
def upgraded_instance_dropped(
    upgraded_instance: system.Instance,
) -> pgtoolkit.conf.Configuration:
    return _drop_instance(upgraded_instance)


class RoleFactory(Protocol):
    def __call__(self, name: str, options: str = "") -> None:
        ...


@pytest.fixture()
def role_factory(ctx: Context, instance: system.Instance) -> Iterator[RoleFactory]:
    rolnames = set()

    def factory(name: str, options: str = "") -> None:
        if name in rolnames:
            raise ValueError(f"'{name}' name already taken")
        execute(ctx, instance, f"CREATE ROLE {name} {options}", fetch=False)
        rolnames.add(name)

    yield factory

    for name in rolnames:
        execute(ctx, instance, f"DROP ROLE IF EXISTS {name}", fetch=False)


class DatabaseFactory(Protocol):
    def __call__(self, name: str, *, owner: Optional[str] = None) -> None:
        ...


@pytest.fixture()
def database_factory(
    ctx: Context, instance: system.Instance
) -> Iterator[DatabaseFactory]:
    datnames = set()

    def factory(name: str, *, owner: Optional[str] = None) -> None:
        if name in datnames:
            raise ValueError(f"'{name}' name already taken")
        sql = f"CREATE DATABASE {name}"
        if owner:
            sql += f" OWNER {owner}"
        execute(ctx, instance, sql, fetch=False)
        datnames.add(name)

    yield factory

    for name in datnames:
        execute(
            ctx,
            instance,
            f"DROP DATABASE IF EXISTS {name}",
            fetch=False,
        )
