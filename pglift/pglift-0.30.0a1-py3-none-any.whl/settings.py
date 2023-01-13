import enum
import grp
import json
import os
import pwd
import shutil
import string
from pathlib import Path, PosixPath
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import yaml
from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    Field,
    FilePath,
    root_validator,
    validator,
)
from pydantic.fields import ModelField

from . import __name__ as pkgname
from . import exceptions, types, util

try:
    from pydantic.env_settings import SettingsSourceCallable
except ImportError:
    SettingsSourceCallable = Callable[[BaseSettings], Dict[str, Any]]  # type: ignore[misc]

if TYPE_CHECKING:
    from .ctx import Context
    from .models.system import BaseInstance


T = TypeVar("T", bound=BaseSettings)


def frozen(cls: Type[T]) -> Type[T]:
    cls.Config.frozen = True
    return cls


def default_prefix(uid: int) -> Path:
    """Return the default path prefix for 'uid'.

    >>> default_prefix(0)
    PosixPath('/')
    >>> default_prefix(42)  # doctest: +ELLIPSIS
    PosixPath('/home/.../.local/share/pglift')
    """
    if uid == 0:
        return Path("/")
    return util.xdg_data_home() / pkgname


def default_run_prefix(uid: int) -> Path:
    """Return the default run path prefix for 'uid'."""
    base = Path("/run") if uid == 0 else util.xdg_runtime_dir(uid)
    return base / pkgname


def default_systemd_unit_path(uid: int) -> Path:
    """Return the default systemd unit path for 'uid'.

    >>> default_systemd_unit_path(0)
    PosixPath('/etc/systemd/system')
    >>> default_systemd_unit_path(42)  # doctest: +ELLIPSIS
    PosixPath('/home/.../.local/share/systemd/user')
    """
    if uid == 0:
        return Path("/etc/systemd/system")
    return util.xdg_data_home() / "systemd" / "user"


def default_sysuser() -> Tuple[str, str]:
    pwentry = pwd.getpwuid(os.getuid())
    grentry = grp.getgrgid(pwentry.pw_gid)
    return pwentry.pw_name, grentry.gr_name


def string_format_variables(fmt: str) -> set[str]:
    return {v for _, v, _, _ in string.Formatter().parse(fmt) if v is not None}


def prefix_values(values: Dict[str, Any], prefixes: Dict[str, Path]) -> Dict[str, Any]:
    for key, child in values.items():
        if isinstance(child, PrefixedPath):
            values[key] = child.prefix(prefixes[child.key])
        elif isinstance(child, BaseSettings):
            child_values = {k: getattr(child, k) for k in child.__fields__}
            child_values = prefix_values(child_values, prefixes)
            values[key] = child.__class__(**child_values)
    return values


class PrefixedPath(PosixPath):
    basedir = Path("")
    key = "prefix"

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[..., "PrefixedPath"]]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Path, field: ModelField) -> "PrefixedPath":
        if not isinstance(value, cls):
            value = cls(value)
        # ensure all template variables used in default field value are also
        # used in user value.
        expected_variables = string_format_variables(str(field.default))
        if (
            expected_variables
            and string_format_variables(str(value)) != expected_variables
        ):
            raise ValueError(
                f"{value} template doesn't use expected variables: {', '.join(sorted(expected_variables))}"
            )
        return value

    def prefix(self, prefix: Union[str, Path]) -> Path:
        """Return the path prefixed if is not yet absolute.

        >>> PrefixedPath("documents").prefix("/home/alice")
        PosixPath('/home/alice/documents')
        >>> PrefixedPath("/root").prefix("/whatever")
        PosixPath('/root')
        """
        if self.is_absolute():
            return Path(self)
        assert Path(prefix).is_absolute(), (
            f"expecting an absolute prefix (got '{prefix}')",
        )
        return prefix / self.basedir / self


class ConfigPath(PrefixedPath):
    basedir = Path("etc")


class SSLPath(ConfigPath):
    basedir = ConfigPath.basedir / "ssl"


class RunPath(PrefixedPath):
    basedir = Path("")
    key = "run_prefix"


class DataPath(PrefixedPath):
    basedir = Path("srv")


class LogPath(PrefixedPath):
    basedir = Path("log")


class PostgreSQLVersion(types.StrEnum):
    """PostgreSQL version"""

    v15 = "15"
    v14 = "14"
    v13 = "13"
    v12 = "12"
    v11 = "11"


@frozen
class PostgreSQLVersionSettings(BaseSettings):
    """Version-specific settings for PostgreSQL."""

    version: PostgreSQLVersion
    bindir: Path


def _postgresql_bindir_version() -> Tuple[str, str]:
    usrdir = Path("/usr")
    for version in PostgreSQLVersion:
        # Debian packages
        if (usrdir / "lib" / "postgresql" / version).exists():
            return str(usrdir / "lib" / "postgresql" / "{version}" / "bin"), version

        # RPM packages from the PGDG
        if (usrdir / f"pgsql-{version}").exists():
            return str(usrdir / "pgsql-{version}" / "bin"), version
    else:
        raise EnvironmentError("no PostgreSQL installation found")


bindir: Optional[str]
try:
    bindir = _postgresql_bindir_version()[0]
except EnvironmentError:
    bindir = None


class AuthLocalMethod(types.AutoStrEnum):
    """Local authentication method"""

    trust = enum.auto()
    reject = enum.auto()
    md5 = enum.auto()
    password = enum.auto()
    scram_sha_256 = "scram-sha-256"
    gss = enum.auto()
    sspi = enum.auto()
    ident = enum.auto()
    peer = enum.auto()
    pam = enum.auto()
    ldap = enum.auto()
    radius = enum.auto()
    cert = enum.auto()


class AuthHostMethod(types.AutoStrEnum):
    """Host authentication method"""

    trust = enum.auto()
    reject = enum.auto()
    md5 = enum.auto()
    password = enum.auto()
    scram_sha_256 = "scram-sha-256"
    gss = enum.auto()
    sspi = enum.auto()
    ident = enum.auto()
    pam = enum.auto()
    ldap = enum.auto()
    radius = enum.auto()
    cert = enum.auto()


@frozen
class AuthSettings(BaseSettings):
    """PostgreSQL authentication settings."""

    class Config:
        env_prefix = "postgresql_auth_"

    local: AuthLocalMethod = Field(
        default="trust",
        description="Default authentication method for local-socket connections.",
    )

    host: AuthHostMethod = Field(
        default="trust",
        description="Default authentication method for local TCP/IP connections.",
    )

    passfile: Path = Field(
        default=Path.home() / ".pgpass", description="Path to .pgpass file."
    )

    password_command: Tuple[str, ...] = Field(
        default=(), description="An optional command to retrieve PGPASSWORD from"
    )


@frozen
class InitdbSettings(BaseSettings):
    """Settings for initdb step of a PostgreSQL instance."""

    class Config:
        env_prefix = "postgresql_initdb_"

    locale: Optional[str] = Field(
        default="C", description="Instance locale as used by initdb."
    )

    encoding: Optional[str] = Field(
        default="UTF8", description="Instance encoding as used by initdb."
    )

    data_checksums: Optional[bool] = Field(
        default=None, description="Use checksums on data pages."
    )


@frozen
class PostgreSQLSettings(BaseSettings):
    """Settings for PostgreSQL."""

    class Config:
        env_prefix = "postgresql_"

    bindir: Optional[str] = Field(
        default=bindir, description="Default PostgreSQL bindir, templated by version."
    )

    versions: Tuple[PostgreSQLVersionSettings, ...] = Field(
        default=(), description="Available PostgreSQL versions."
    )

    @validator("versions")
    def __set_versions_(
        cls, value: Tuple[PostgreSQLVersionSettings, ...], values: Dict[str, Any]
    ) -> Tuple[PostgreSQLVersionSettings, ...]:
        bindir = values["bindir"]
        pgversions = [v.version for v in value]
        versions = list(value)
        if bindir is not None:
            for version in PostgreSQLVersion:
                if version not in pgversions:
                    versions.append(
                        PostgreSQLVersionSettings(
                            version=version, bindir=bindir.format(version=version)
                        )
                    )
        versions.sort(key=lambda v: v.version)
        return tuple(versions)

    default_version: Optional[PostgreSQLVersion] = Field(
        default=None, description="Default PostgreSQL version to use, if unspecified."
    )

    initdb: InitdbSettings = InitdbSettings()

    auth: AuthSettings = AuthSettings()

    @frozen
    class Role(BaseSettings):
        name: str
        pgpass: bool = Field(
            default=False, description="Whether to store the password in .pgpass file."
        )

    @frozen
    class SuRole(Role):
        """Super-user role."""

        name: str = "postgres"

    surole: SuRole = Field(default=SuRole(), description="Instance super-user role.")

    replrole: str = Field(
        default="replication", description="Instance replication role."
    )

    @frozen
    class BackupRole(Role):
        """Backup role."""

        name: str = "backup"

    backuprole: BackupRole = Field(
        default=BackupRole(), description="Instance role used to backup."
    )

    datadir: DataPath = Field(
        default=DataPath("pgsql/{version}/{name}/data"),
        description="Path segment from instance base directory to PGDATA directory.",
    )

    waldir: DataPath = Field(
        default=DataPath("pgsql/{version}/{name}/wal"),
        description="Path segment from instance base directory to WAL directory.",
    )

    ssl_cert_directory: SSLPath = Field(
        default=SSLPath("postgresql"),
        description="Path to directory where SSL certificate for PostgreSQL will be installed.",
    )

    socket_directory: RunPath = Field(
        default=RunPath("postgresql"),
        description="Path to directory where postgres unix socket will be written.",
    )

    dumps_directory: DataPath = Field(
        default=DataPath("dumps/{version}-{name}"),
        description="Path to directory where database dumps are stored.",
    )

    dump_commands: Tuple[Tuple[str, ...], ...] = Field(
        default=(
            (
                "{bindir}/pg_dump",
                "-Fc",
                "-f",
                "{path}/{dbname}_{date}.dump",
                "-d",
                "{conninfo}",
            ),
        ),
        description="Commands used to dump a database",
    )

    restore_commands: Tuple[Tuple[str, ...], ...] = Field(
        default=(
            (
                "{bindir}/pg_restore",
                "-d",
                "{conninfo}",
                "{createoption}",
                "{path}/{dbname}_{date}.dump",
            ),
        ),
        description="Commands used to restore a database",
    )

    def libpq_environ(
        self,
        ctx: "Context",
        instance: "BaseInstance",
        role: str,
        *,
        base: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """Return a dict with libpq environment variables for authentication."""
        auth = self.auth
        if base is None:
            env = os.environ.copy()
        else:
            env = base.copy()
        env.setdefault("PGPASSFILE", str(self.auth.passfile))
        if auth.password_command and "PGPASSWORD" not in env:
            try:
                cmd = [
                    c.format(instance=instance, role=role)
                    for c in auth.password_command
                ]
            except ValueError as e:
                raise exceptions.SettingsError(
                    f"failed to format auth.password_command: {e}"
                ) from None
            password = ctx.run(cmd, check=True).stdout.strip()
            if password:
                env["PGPASSWORD"] = password
        return env


@frozen
class Etcd(BaseSettings):
    """Settings for Etcd (for Patroni)."""

    v2: bool = Field(default=False, description="Configure Patroni to use etcd v2.")

    hosts: List[types.Address] = Field(
        default=["127.0.0.1:2379"],
        description="List of etcd endpoint.",
    )

    protocol: Literal["http", "https"] = Field(
        default="http",
        description="http or https, if not specified http is used.",
    )

    cacert: Optional[FilePath] = Field(
        default=None,
        description="The CA certificate. If present it will enable validation.",
    )

    cert: Optional[FilePath] = Field(
        default=None,
        description="File with the client certificate.",
    )

    key: Optional[FilePath] = Field(
        default=None,
        description="File with the client key.",
    )

    @root_validator
    def __protocol_and_certificates(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Make sure protocol https is used when setting certificates.

        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile() as tmpfile:
        ...    tmpfile.flush()
        ...    Etcd(cacert=tmpfile.name)
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Etcd
        __root__
          'https' protocol is required when using certificates (type=value_error)
        >>> with tempfile.NamedTemporaryFile() as tmpfile:
        ...    tmpfile.flush()
        ...    Etcd(cert=tmpfile.name)
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Etcd
        __root__
          'https' protocol is required when using certificates (type=value_error)
        """
        if values["protocol"] == "http" and (values["cacert"] or values["cert"]):
            raise ValueError("'https' protocol is required when using certificates")
        return values


@frozen
class WatchDog(BaseSettings):
    """Settings for watchdog (for Patroni)."""

    mode: Literal["off", "automatic", "required"] = Field(
        default="off", description="watchdog mode."
    )

    device: Optional[FilePath] = Field(
        default=None,
        description="Path to watchdog.",
    )

    safety_margin: Optional[int] = Field(
        default=None,
        description=(
            "Number of seconds of safety margin between watchdog triggering"
            " and leader key expiration."
        ),
    )


@frozen
class PatroniSettings(BaseSettings):
    """Settings for Patroni."""

    class Config:
        env_prefix = "patroni_"

    execpath: FilePath = Field(
        default=Path("/usr/bin/patroni"),
        description="Path to patroni executable.",
    )

    configpath: ConfigPath = Field(
        default=ConfigPath("patroni/{name}.yaml"),
        description="Path to the config file.",
    )

    logpath: LogPath = Field(
        default=LogPath("patroni/{name}"),
        description="Path where log files are stored.",
    )

    pid_file: RunPath = Field(
        default=RunPath("patroni/{name}.pid"),
        description="Path to which Patroni process PID will be written.",
    )

    loop_wait: int = Field(
        default=10, description="Number of seconds the loop will sleep."
    )

    etcd: Etcd = Field(default_factory=Etcd, description="Etcd settings.")
    watchdog: WatchDog = Field(
        default_factory=WatchDog, description="Watchdog settings."
    )


@frozen
class PgBackRestSettings(BaseSettings):
    """Settings for pgBackRest."""

    class Config:
        env_prefix = "pgbackrest_"

    execpath: FilePath = Field(
        default=Path("/usr/bin/pgbackrest"),
        description="Path to the pbBackRest executable.",
    )

    configpath: ConfigPath = Field(
        default=ConfigPath("pgbackrest"),
        description="Base path for pgBackRest configuration files.",
    )

    class HostRepository(BaseSettings):
        """Remote repository host for pgBackRest."""

        class Cert(BaseSettings):
            """TLS certificate files."""

            cert: FilePath = Field(description="Certificate file.")
            key: FilePath = Field(description="Private key file.")

        host: str = Field(description="Host name of the remote repository.")
        host_port: Optional[int] = Field(
            default=None,
            description="Port for the TLS server of the remote repository.",
        )
        host_config: Optional[Path] = Field(
            default=None,
            description="pgBackRest configuration file path on the remote repository.",
        )
        ca_cert: FilePath = Field(description="Certificate Authority certificate.")
        cn: str = Field(description="Certificate Common Name of the remote repository.")
        certificate: Cert = Field(
            description="Certificate and (private) key files for the TLS server on site."
        )
        port: int = Field(default=8432, description="Port for the TLS server on site.")
        pid_file: RunPath = Field(
            default=RunPath("pgbackrest.pid"),
            description="Path to which pgbackrest server process PID will be written.",
        )

    class PathRepository(BaseSettings):
        """Remote repository (path) for pgBackRest."""

        class Retention(BaseSettings):
            """Retention settings."""

            archive: int = 2
            diff: int = 3
            full: int = 2

        path: DataPath = Field(
            description="Base directory path where backups and WAL archives are stored.",
        )
        retention: Retention = Field(
            default=Retention(), description="Retention options."
        )

    repository: Union[HostRepository, PathRepository] = Field(
        description="Repository definition, either as a (local) path-repository or as a host-repository."
    )

    logpath: LogPath = Field(
        default=LogPath("pgbackrest"),
        description="Path where log files are stored.",
    )

    spoolpath: DataPath = Field(
        default=DataPath("pgbackrest/spool"),
        description="Spool path.",
    )

    lockpath: RunPath = Field(
        default=RunPath("pgbackrest/lock"),
        description="Path where lock files are stored.",
    )


@frozen
class PrometheusSettings(BaseSettings):
    """Settings for Prometheus postgres_exporter"""

    class Config:
        env_prefix = "prometheus_"

    execpath: FilePath = Field(description="Path to the postgres_exporter executable.")

    role: str = Field(
        default="prometheus",
        description="Name of the PostgreSQL role for Prometheus postgres_exporter.",
    )

    configpath: ConfigPath = Field(
        default=ConfigPath("prometheus/postgres_exporter-{name}.conf"),
        description="Path to the config file.",
    )

    queriespath: ConfigPath = Field(
        default=ConfigPath("prometheus/postgres_exporter_queries-{name}.yaml"),
        description="Path to the queries file.",
    )

    pid_file: RunPath = Field(
        default=RunPath("prometheus/{name}.pid"),
        description="Path to which postgres_exporter process PID will be written.",
    )


@frozen
class PowaSettings(BaseSettings):
    """Settings for PoWA."""

    class Config:
        env_prefix = "powa_"

    dbname: str = Field(default="powa", description="Name of the PoWA database")

    role: str = Field(default="powa", description="Instance role used for PoWA.")


@frozen
class TemboardSettings(BaseSettings):
    """Settings for temBoard agent"""

    class Config:
        env_prefix = "temboard_"

    class Plugin(types.AutoStrEnum):
        activity = enum.auto()
        administration = enum.auto()
        dashboard = enum.auto()
        maintenance = enum.auto()
        monitoring = enum.auto()
        pgconf = enum.auto()
        statements = enum.auto()

    ui_url: AnyHttpUrl = Field(description="URL of the temBoard UI.")

    signing_key: FilePath = Field(
        description="Path to the public key for UI connection."
    )

    execpath: FilePath = Field(
        default=Path("/usr/bin/temboard-agent"),
        description="Path to the temboard-agent executable.",
    )

    role: str = Field(
        default="temboardagent",
        description="Name of the PostgreSQL roel for temBoard agent.",
    )

    configpath: ConfigPath = Field(
        default=ConfigPath("temboard-agent/temboard-agent-{name}.conf"),
        description="Path to the config file.",
    )

    pid_file: RunPath = Field(
        default=RunPath("temboard-agent/temboard-agent-{name}.pid"),
        description="Path to which temboard-agent process PID will be written.",
    )

    plugins: Tuple[Plugin, ...] = Field(
        default=(
            Plugin.monitoring,
            Plugin.dashboard,
            Plugin.activity,
        ),
        description="Plugins to load.",
    )

    ssl_cert_dir: SSLPath = Field(
        default=SSLPath("temboard-agent"),
        description="Path to directory where SSL certificate files will be written.",
    )

    home: DataPath = Field(
        default=DataPath("temboard-agent/{name}"),
        description="Path to agent home directory containing files used to store temporary data",
    )


@frozen
class SystemdSettings(BaseSettings):
    """Systemd settings."""

    class Config:
        env_prefix = "systemd_"

    unit_path: Path = Field(
        default=default_systemd_unit_path(os.getuid()),
        description="Base path where systemd units will be installed.",
    )

    user: bool = Field(
        default=True,
        description="Use the system manager of the calling user, by passing --user to systemctl calls.",
    )

    sudo: bool = Field(
        default=False,
        description="Run systemctl command with sudo; only applicable when 'user' is unset.",
    )

    @root_validator
    def __sudo_and_user(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values["user"] and values["sudo"]:
            raise ValueError("'user' mode cannot be used with 'sudo'")
        return values


def yaml_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """Load settings values 'settings.yaml' file if found in user or system
    config directory directory.
    """
    assert isinstance(settings, SiteSettings)
    path = settings.site_settings()
    if path is None:
        return {}
    settings = yaml.safe_load(path.read_text())
    if not isinstance(settings, dict):
        raise exceptions.SettingsError(
            f"failed to load site settings from {path}, expecting an object"
        )
    return settings


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """Load settings values from 'SETTINGS' environment variable.

    If this variable has a value starting with @, it is interpreted as a path
    to a JSON file. Otherwise, a JSON serialization is expected.
    """
    env_settings = os.getenv("SETTINGS")
    if not env_settings:
        return {}
    if env_settings.startswith("@"):
        config = Path(env_settings[1:])
        encoding = settings.__config__.env_file_encoding
        # May raise FileNotFoundError, which is okay here.
        env_settings = config.read_text(encoding)
    try:
        return json.loads(env_settings)  # type: ignore[no-any-return]
    except json.decoder.JSONDecodeError as e:
        raise exceptions.SettingsError(str(e))


@frozen
class Settings(BaseSettings):
    """Settings for pglift."""

    postgresql: PostgreSQLSettings = PostgreSQLSettings()
    patroni: Optional[PatroniSettings] = None
    pgbackrest: Optional[PgBackRestSettings] = None
    powa: Optional[PowaSettings] = None
    prometheus: Optional[PrometheusSettings] = None
    temboard: Optional[TemboardSettings] = None
    systemd: Optional[SystemdSettings] = None

    service_manager: Optional[Literal["systemd"]] = None
    scheduler: Optional[Literal["systemd"]] = None

    prefix: Path = Field(
        default=default_prefix(os.getuid()),
        description="Path prefix for configuration and data files.",
    )

    run_prefix: Path = Field(
        default=default_run_prefix(os.getuid()),
        description="Path prefix for runtime socket, lockfiles and PID files.",
    )

    logpath: LogPath = Field(
        default=LogPath(),
        description="Directory where temporary log files from command executions will be stored",
        title="CLI log directory",
    )

    sysuser: Tuple[str, str] = Field(
        default_factory=default_sysuser,
        help=(
            "(username, groupname) of system user running PostgreSQL; "
            "mostly applicable when operating PostgreSQL with systemd in non-user mode"
        ),
    )

    @validator("prefix", "run_prefix")
    def __validate_prefix_(cls, value: Path) -> Path:
        """Make sure path settings are absolute.

        >>> Settings(prefix='x')
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Settings
        prefix
          expecting an absolute path (type=value_error)
        """
        if not value.is_absolute():
            raise ValueError("expecting an absolute path")
        return value

    @root_validator(skip_on_failure=True)
    def __prefix_paths(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Prefix child settings fields with the global 'prefix'."""
        return prefix_values(
            values,
            {"prefix": values["prefix"], "run_prefix": values["run_prefix"]},
        )

    @validator("systemd")
    def __validate_systemd_(
        cls, v: Optional[SystemdSettings]
    ) -> Optional[SystemdSettings]:
        if v and shutil.which("systemctl") is None:
            raise ValueError("systemctl command not found, cannot use systemd setting")
        return v

    @root_validator(pre=True)
    def __set_service_manager_scheduler(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Set 'service_manager' and 'scheduler' to 'systemd' by default if systemd is enabled."""
        if values.get("systemd") is not None:
            values.setdefault("service_manager", "systemd")
            values.setdefault("scheduler", "systemd")
        return values

    @validator("service_manager", "scheduler")
    def __validate_service_manager_scheduler_(
        cls, v: Optional[Literal["systemd"]], values: Dict[str, Any]
    ) -> Optional[Literal["systemd"]]:
        """Make sure systemd is enabled globally when 'service_manager' or 'scheduler' are set

        >>> Settings(service_manager="systemd").service_manager
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Settings
        service_manager
          cannot use systemd, if 'systemd' is not enabled globally (type=value_error)
        """
        if values.get("systemd") is None and v is not None:
            raise ValueError("cannot use systemd, if 'systemd' is not enabled globally")
        return v


@frozen
class SiteSettings(Settings):
    """Settings loaded from site-sources.

    Load user or site settings from:
    - 'settings.yaml' if found in user or system configuration directory, and,
    - SETTINGS environment variable.
    """

    @staticmethod
    def site_settings() -> Optional[Path]:
        """Return content of 'settings.yaml' if found in site configuration
        directories.
        """
        for hdlr in (util.xdg_config, util.etc_config):
            fpath = hdlr("settings.yaml")
            if fpath is not None:
                return fpath
        return None

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                json_config_settings_source,
                yaml_settings_source,
            )
