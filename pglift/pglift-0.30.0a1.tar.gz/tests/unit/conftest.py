import pathlib
from pathlib import Path
from typing import Any, Callable, Iterator, List, Optional, Type
from unittest.mock import patch

import pydantic
import pytest

from pglift.ctx import Context
from pglift.models import interface
from pglift.models.system import Instance
from pglift.pgbackrest import models as pgbackrest_models
from pglift.prometheus import impl as prometheus_mod
from pglift.prometheus import models as prometheus_models
from pglift.settings import Settings, SystemdSettings
from pglift.temboard import impl as temboard_mod
from pglift.temboard import models as temboard_models


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--write-changes",
        action="store_true",
        default=False,
        help="Write-back changes to test data.",
    )


@pytest.fixture
def write_changes(request: Any) -> bool:
    value = request.config.option.write_changes
    assert isinstance(value, bool)
    return value


@pytest.fixture
def prometheus_execpath(tmp_path: Path) -> Path:
    execpath = tmp_path / "postgres_exporter"
    execpath.touch(0o700)
    execpath.write_text("#!/bin/sh\nexit 1\n")
    return execpath


@pytest.fixture
def temboard_execpath(tmp_path: Path) -> Path:
    execpath = tmp_path / "temboard-agent"
    execpath.touch(0o700)
    execpath.write_text("#!/bin/sh\nexit 1\n")
    return execpath


@pytest.fixture
def patroni_execpath(tmp_path: Path) -> Path:
    execpath = tmp_path / "patroni"
    execpath.touch(0o700)
    execpath.write_text(
        "\n".join(
            [
                "#!/bin/sh",
                'if [ "$1" = "--validate-config" ]',
                "then",
                "  echo 'test test test'",
                "fi",
                "exit 1",
            ]
        )
    )
    return execpath


@pytest.fixture
def systemd_settings(tmp_path: Path) -> SystemdSettings:
    return SystemdSettings.parse_obj({"unit_path": str(tmp_path / "systemd")})


@pytest.fixture
def settings(
    tmp_path: Path,
    patroni_execpath: Path,
    prometheus_execpath: Path,
    temboard_execpath: Path,
    systemd_settings: SystemdSettings,
) -> Settings:
    passfile = tmp_path / "pgass"
    passfile.touch()
    signing_key = tmp_path / "signing-public.pem"
    signing_key.touch()
    obj = {
        "prefix": str(tmp_path),
        "run_prefix": str(tmp_path / "run"),
        "postgresql": {
            "auth": {
                "local": "peer",
                "host": "password",
                "passfile": str(passfile),
            }
        },
        "systemd": systemd_settings,
        "service_manager": None,
        "scheduler": None,
        "patroni": {"execpath": patroni_execpath},
        "pgbackrest": {
            "repository": {"path": tmp_path / "backups"},
        },
        "prometheus": {"execpath": prometheus_execpath},
        "temboard": {
            "execpath": temboard_execpath,
            "ui_url": "https://0.0.0.0:8888",
            "signing_key": str(signing_key),
        },
        "powa": {},
    }
    with patch("shutil.which", return_value=True) as which:
        settings = Settings.parse_obj(obj)
    which.assert_called_once_with("systemctl")
    return settings


@pytest.fixture
def ctx(settings: Settings) -> Context:
    return Context(settings=settings)


@pytest.fixture
def nohook(ctx: Context) -> Iterator[None]:
    unregistered = ctx.pm.unregister_all()
    yield
    for plugin in unregistered:
        ctx.pm.register(plugin)


@pytest.fixture
def composite_instance_model(ctx: Context) -> Type[interface.Instance]:
    return interface.Instance.composite(ctx.pm)


@pytest.fixture
def instance_manifest(
    composite_instance_model: Type[interface.Instance], pg_version: str
) -> interface.Instance:
    return composite_instance_model(
        name="test",
        version=pg_version,
        surole_password=pydantic.SecretStr("p0st.g're$"),
        replrole_password=pydantic.SecretStr("repl1&c"),
        settings={"shared_preload_libraries": "passwordcheck"},
    )


def _instance(
    name: str, version: str, postgresql_conf: str, settings: Settings
) -> Instance:
    # Services are looked-up in reverse order of plugin registration.
    services: List[Any] = []

    assert settings.temboard is not None
    temboard_port = 2345
    temboard = temboard_models.Service(
        name=f"{version}-{name}",
        settings=settings.temboard,
        port=temboard_port,
        password=pydantic.SecretStr("dorade"),
    )
    services.append(temboard)

    assert settings.prometheus is not None
    prometheus_port = 9817
    prometheus = prometheus_models.Service(
        name=f"{version}-{name}",
        settings=settings.prometheus,
        port=prometheus_port,
        password=pydantic.SecretStr("truite"),
    )
    services.append(prometheus)

    assert settings.pgbackrest is not None
    pgbackrest = pgbackrest_models.Service(
        stanza="mystanza",
        path=settings.pgbackrest.configpath / "conf.d" / "mystanza.conf",
    )
    services.append(pgbackrest)

    instance = Instance(
        name=name,
        version=version,
        settings=settings,
        services=services,
    )
    instance.datadir.mkdir(parents=True)
    (instance.datadir / "PG_VERSION").write_text(instance.version)
    (instance.datadir / "postgresql.conf").write_text(postgresql_conf)
    (instance.datadir / "pg_hba.conf").write_text(
        "# pg_hba.conf\nlocal all postgres peer\n"
    )
    (instance.datadir / "pg_ident.conf").write_text("# pg_ident.conf\nmymap test dba\n")

    prometheus_config = prometheus_mod._configpath(
        instance.qualname, settings.prometheus
    )
    prometheus_config.parent.mkdir(parents=True, exist_ok=True)
    prometheus_config.write_text(
        f"DATA_SOURCE_NAME=dbname=postgres port={instance.port} host={settings.postgresql.socket_directory} user=monitoring sslmode=disable password=truite\n"
        f"PG_EXPORTER_WEB_LISTEN_ADDRESS=:{prometheus.port}"
    )

    temboard_config = temboard_mod._configpath(instance.qualname, settings.temboard)
    temboard_config.parent.mkdir(parents=True, exist_ok=True)
    temboard_config.write_text(
        "\n".join(
            [
                "[temboard]",
                f"port = {temboard.port}",
                "ui_url = https://0.0.0.0:8888",
                "[postgresql]",
                f"port = {instance.port}",
                f"host = {settings.postgresql.socket_directory}",
                "user = temboardagent",
                "password = dorade",
            ]
        )
    )

    stanza_config = pgbackrest.path
    stanza_config.parent.mkdir(parents=True, exist_ok=True)
    stanza_config.write_text(
        "\n".join(
            [
                "[mystanza]",
                f"pg1-path = {instance.datadir}",
                f"pg1-port = {instance.port}",
                "pg1-user = backup",
            ]
        )
    )

    return instance


@pytest.fixture
def postgresql_conf() -> str:
    return "\n".join(
        [
            "port = 999",
            "unix_socket_directories = /socks",
            "# backslash_quote = 'safe_encoding'",
        ]
    )


@pytest.fixture
def instance(pg_version: str, postgresql_conf: str, settings: Settings) -> Instance:
    return _instance("test", pg_version, postgresql_conf, settings)


@pytest.fixture
def instance2(pg_version: str, postgresql_conf: str, settings: Settings) -> Instance:
    return _instance("test2", pg_version, postgresql_conf, settings)


@pytest.fixture
def standby_instance(
    pg_version: str, postgresql_conf: str, settings: Settings
) -> Instance:
    instance = _instance("standby", pg_version, postgresql_conf, settings)
    (
        instance.datadir
        / ("standby.signal" if int(pg_version) >= 12 else "recovery.conf")
    ).write_text("")
    (instance.datadir / "postgresql.auto.conf").write_text(
        "primary_conninfo = 'host=/tmp port=4242 user=pg'\n"
        "primary_slot_name = aslot\n"
    )
    return instance


@pytest.fixture
def meminfo(tmp_path: Path) -> Path:
    fpath = tmp_path / "meminfo"
    fpath.write_text(
        "\n".join(
            [
                "MemTotal:        6022056 kB",
                "MemFree:         3226640 kB",
                "MemAvailable:    4235060 kB",
                "Buffers:          206512 kB",
            ]
        )
    )
    return fpath


@pytest.fixture(scope="package")
def site_config(
    site_config: Callable[..., Optional[str]]
) -> Iterator[Callable[..., Optional[str]]]:
    def test_site_config(*args: str) -> Optional[str]:
        """Lookup for configuration files in local data director first."""
        datadir = pathlib.Path(__file__).parent / "data"
        fpath = datadir.joinpath(*args)
        if fpath.exists():
            return fpath.read_text()
        return site_config(*args)

    with patch("pglift.util.site_config", new=test_site_config) as fn:
        yield fn
