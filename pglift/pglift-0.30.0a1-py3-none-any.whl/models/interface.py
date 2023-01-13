import enum
import hashlib
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Final,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from pgtoolkit import conf as pgconf
from pgtoolkit.ctl import Status
from pydantic import (
    BaseModel,
    ByteSize,
    DirectoryPath,
    Field,
    PostgresDsn,
    SecretStr,
    ValidationError,
    create_model,
    fields,
    root_validator,
    validator,
)
from pydantic.error_wrappers import ErrorWrapper
from pydantic.utils import lenient_issubclass

from .. import settings as s
from .. import util
from ..postgresql import Standby
from ..types import (
    AnsibleConfig,
    AutoStrEnum,
    CLIConfig,
    Manifest,
    Port,
    ServiceManifest,
)

if TYPE_CHECKING:
    from ..pm import PluginManager

default_port: Final = 5432


def validate_ports(model: BaseModel) -> None:
    """Walk fields of 'model', checking those with type Port if their value is
    available.
    """

    def _validate(
        model: BaseModel, *, loc: Tuple[str, ...] = ()
    ) -> Iterator[ErrorWrapper]:
        cls = model.__class__
        for name, field in cls.__fields__.items():
            value = getattr(model, name)
            if value is None:
                continue
            ftype = field.outer_type_
            if lenient_issubclass(ftype, BaseModel):
                yield from _validate(value, loc=loc + (name,))
            elif lenient_issubclass(ftype, Port):
                assert isinstance(value, Port)
                if not value.available():
                    yield ErrorWrapper(
                        ValueError(f"port {value} already in use"), loc + (name,)
                    )

    errors = list(_validate(model))
    if errors:
        raise ValidationError(errors, model.__class__)


def validate_state_is_absent(
    value: Union[bool, str], values: Dict[str, Any], field: fields.ModelField
) -> Union[bool, str]:
    """Make sure state is absent.

    >>> r =  Role(name="bob",  drop_owned=True)
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Role
    drop_owned
      drop_owned can not be set if state is not absent (type=value_error)

    >>> r =  Role(name="bob",  reassign_owned="postgres")
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Role
    reassign_owned
      reassign_owned can not be set if state is not absent (type=value_error)

    >>> r =  Database(name="db1", force_drop=True)
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Database
    force_drop
      force_drop can not be set if state is not absent (type=value_error)
    """
    absent = PresenceState.absent
    if value and values["state"] != absent:
        raise ValueError(f"{field.name} can not be set if state is not {absent}")
    return value


class InstanceState(AutoStrEnum):
    """Instance state."""

    stopped = enum.auto()
    """stopped"""

    started = enum.auto()
    """started"""

    absent = enum.auto()
    """absent"""

    restarted = enum.auto()
    """restarted"""

    @classmethod
    def from_pg_status(cls, status: Status) -> "InstanceState":
        """Instance state from PostgreSQL status.

        >>> InstanceState.from_pg_status(Status.running)
        <InstanceState.started: 'started'>
        >>> InstanceState.from_pg_status(Status.not_running)
        <InstanceState.stopped: 'stopped'>
        >>> InstanceState.from_pg_status(Status.unspecified_datadir)
        <InstanceState.absent: 'absent'>
        """
        return cls(
            {
                status.running: cls.started,
                status.not_running: cls.stopped,
                status.unspecified_datadir: cls.absent,
            }[status]
        )


class PresenceState(AutoStrEnum):
    """Should the object be present or absent?"""

    present = enum.auto()
    absent = enum.auto()


class InstanceListItem(Manifest):

    name: str
    version: str
    port: int
    datadir: DirectoryPath
    status: str


class BaseInstance(Manifest):
    """PostgreSQL instance suitable for lookup"""

    name: str = Field(readOnly=True, description="Instance name.")
    version: Optional[s.PostgreSQLVersion] = Field(
        default=None, description="PostgreSQL version.", readOnly=True
    )

    @validator("name")
    def __validate_name_(cls, v: str) -> str:
        """Validate 'name' field.

        >>> Instance(name='without_dash')  # doctest: +ELLIPSIS
        Instance(name='without_dash', ...)
        >>> Instance(name='with-dash')
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        name
          instance name must not contain dashes (type=value_error)
        >>> Instance(name='with/slash')
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        name
          instance name must not contain slashes (type=value_error)
        """
        # Avoid dash as this will break systemd instance unit.
        if "-" in v:
            raise ValueError("instance name must not contain dashes")
        # Likewise, slash messes up with file paths.
        if "/" in v:
            raise ValueError("instance name must not contain slashes")
        return v


class BaseRole(Manifest):

    name: str = Field(readOnly=True, description="Role name.")
    state: PresenceState = Field(
        const=True,
        default=PresenceState.absent,
        description="Whether the role be present or absent.",
    )
    password: Optional[SecretStr] = Field(
        const=True, default=None, description="Role password.", exclude=True
    )
    pgpass: bool = Field(
        const=True,
        default=False,
        description="Whether to add an entry in password file for this role.",
    )


class _RoleExisting(BaseRole):
    """Base model for a role that exists (or should exist, after creation)."""

    _cli_config: ClassVar[Dict[str, CLIConfig]] = {
        "in_roles": {"name": "in_role"},
        "state": {"hide": True},
        "has_password": {"hide": True},
    }
    _ansible_config: ClassVar[Dict[str, AnsibleConfig]] = {
        "has_password": {"hide": True},
    }

    password: Optional[SecretStr] = Field(
        default=None, description="Role password.", exclude=True
    )
    has_password: bool = Field(
        default=False,
        description="True if the role has a password.",
        readOnly=True,
    )
    inherit: bool = Field(
        default=True,
        description="Let the role inherit the privileges of the roles it is a member of.",
    )
    login: bool = Field(default=False, description="Allow the role to log in.")
    superuser: bool = Field(
        default=False, description="Whether the role is a superuser."
    )
    replication: bool = Field(
        default=False, description="Whether the role is a replication role."
    )
    connection_limit: Optional[int] = Field(
        description="How many concurrent connections the role can make.",
    )
    validity: Optional[datetime] = Field(
        description="Date and time after which the role's password is no longer valid."
    )
    in_roles: List[str] = Field(
        default=[],
        description="List of roles to which the new role will be added as a new member.",
    )
    pgpass: bool = Field(
        default=False,
        description="Whether to add an entry in password file for this role.",
    )
    state: PresenceState = Field(
        default=PresenceState.present,
        description="Whether the role be present or absent.",
        exclude=True,
    )

    @validator("has_password", always=True)
    def __set_has_password(cls, value: bool, values: Dict[str, Any]) -> bool:
        """Set 'has_password' field according to 'password'.

        >>> r = Role(name="postgres")
        >>> r.has_password
        False
        >>> r = Role(name="postgres", password="P4zzw0rd")
        >>> r.has_password
        True
        >>> r = Role(name="postgres", has_password=True)
        >>> r.has_password
        True
        """
        return value or values["password"] is not None


class RoleDropped(BaseRole):
    """Model for a role that is being dropped."""

    drop_owned: bool = Field(
        default=False,
        description="Drop all PostgreSQL's objects owned by the role being dropped.",
        exclude=True,
    )
    reassign_owned: Optional[str] = Field(
        default=None,
        description="Reassign all PostgreSQL's objects owned by the role being dropped to the specified role name.",
        min_length=1,
        exclude=True,
    )

    @validator("reassign_owned")
    def __validate_reassign_owned(cls, value: str, values: Dict[str, Any]) -> str:
        """Validate reassign_owned fields.

        >>> r = RoleDropped(name="bob", drop_owned=True, reassign_owned="postgres")
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for RoleDropped
        reassign_owned
          drop_owned and reassign_owned are mutually exclusive (type=value_error)

        >>> r = RoleDropped(name="bob", reassign_owned="")
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for RoleDropped
        reassign_owned
          ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)
        >>> RoleDropped(name="bob", reassign_owned=None, drop_owned=True)  # doctest: +ELLIPSIS
        RoleDropped(name='bob', state=<PresenceState.absent: 'absent'>, ..., drop_owned=True, reassign_owned=None)
        """
        if value and values["drop_owned"]:
            raise ValueError("drop_owned and reassign_owned are mutually exclusive")
        return value


class Role(_RoleExisting, RoleDropped):
    """PostgreSQL role"""

    _cli_config: ClassVar[Dict[str, CLIConfig]] = _RoleExisting._cli_config.copy()
    _cli_config.update(
        {
            "drop_owned": {"hide": True},
            "reassign_owned": {"hide": True},
        }
    )

    _validate_drop_owned = validator("drop_owned", allow_reuse=True)(
        validate_state_is_absent
    )
    _validate_reassign_owned = validator("reassign_owned", allow_reuse=True)(
        validate_state_is_absent
    )


class BaseDatabase(Manifest):

    _cli_config: ClassVar[Dict[str, CLIConfig]] = {
        "state": {"hide": True},
    }
    name: str = Field(readOnly=True, description="Database name.", examples=["demo"])

    state: PresenceState = Field(
        const=True,
        default=PresenceState.absent,
        description="Database state.",
        examples=["present"],
    )


class _DatabaseExisting(BaseDatabase):
    """Base model for a database that exists (or should exist, after creation)."""

    _cli_config: ClassVar[Dict[str, CLIConfig]] = {
        "settings": {"hide": True},
        "state": {"hide": True},
        "extensions": {"name": "extension"},
    }
    _ansible_config: ClassVar[Dict[str, AnsibleConfig]] = {
        "settings": {"spec": {"type": "dict", "required": False}},
    }

    state: PresenceState = Field(
        default=PresenceState.present,
        description="Database state.",
        examples=["present"],
        exclude=True,
    )
    owner: Optional[str] = Field(
        description="The role name of the user who will own the database.",
        examples=["postgres"],
    )
    settings: Optional[Dict[str, Optional[pgconf.Value]]] = Field(
        default=None,
        description=(
            "Session defaults for run-time configuration variables for the database. "
            "Upon update, an empty (dict) value would reset all settings."
        ),
        examples=[{"work_mem": "5MB"}],
    )
    extensions: List[str] = Field(
        default=[],
        description="List of extensions to create in the database.",
        examples=[["unaccent"]],
    )
    clone_from: Optional[PostgresDsn] = Field(
        description="Data source name of the database to clone into this one, specified as a libpq connection URI.",
        readOnly=True,
        writeOnly=True,
        examples=["postgresql://app:password@dbserver:5455/appdb"],
    )


class DatabaseDropped(BaseDatabase):
    """Model for a database that is being dropped."""

    _cli_config: ClassVar[Dict[str, CLIConfig]] = {
        "force_drop": {"name": "force"},
    }

    force_drop: bool = Field(default=False, description="Force the drop.", exclude=True)


class Database(_DatabaseExisting, DatabaseDropped):
    """PostgreSQL database"""

    _cli_config: ClassVar[Dict[str, CLIConfig]] = _DatabaseExisting._cli_config.copy()
    _cli_config.update(
        {
            "force_drop": {"hide": True},
        }
    )

    _validate_force_drop = validator("force_drop", allow_reuse=True)(
        validate_state_is_absent
    )


class DatabaseDump(Manifest):
    id: str
    dbname: str
    date: datetime

    @root_validator(pre=True)
    def __generate_id_(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Identifier for the dump."""
        id = "_".join(
            [
                values["dbname"],
                hashlib.blake2b(
                    (values["dbname"] + str(values["date"])).encode("utf-8"),
                    digest_size=5,
                ).hexdigest(),
            ]
        )
        values["id"] = id
        return values


class Instance(BaseInstance):
    """PostgreSQL instance"""

    class Config(Manifest.Config):
        # Allow extra fields to permit plugins to populate an object with
        # their specific data, following (hopefully) what's defined by
        # the "composite" model (see composite()).
        extra = "allow"

    _cli_config: ClassVar[Dict[str, CLIConfig]] = {
        "status": {"hide": True},
        "state": {
            "choices": [InstanceState.started.value, InstanceState.stopped.value]
        },
        "pending_restart": {"hide": True},
        "restart_on_changes": {"hide": True},
        "settings": {"hide": True},
        "roles": {"hide": True},
        "databases": {"hide": True},
    }
    _ansible_config: ClassVar[Dict[str, AnsibleConfig]] = {
        "pending_restart": {"hide": True},
    }

    _T = TypeVar("_T", bound="Instance")

    @classmethod
    def composite(cls: Type[_T], pm: "PluginManager") -> Type[_T]:
        """Create a model class, based on this one, with extra fields based on
        interface models for satellite components defined in plugins.
        """
        fields = {}
        for m in pm.hook.interface_model():
            sname = m.__service__
            assert not m.__doc__
            sdesc = (
                f"Configuration for the {sname} service, if enabled in site settings."
            )
            if sname in fields:
                raise ValueError(f"duplicated '{sname}' service")
            for f in m.__fields__.values():
                assert isinstance(
                    f.required, bool  # ModelField.required defaults to Undefined.
                ), f"expecting a boolean for {f}.required"
                if f.required:
                    f = Field(default=None, description=sdesc)
                    m = Optional[m]
                    break
            else:
                f = Field(default=m(), description=sdesc)
            fields[sname] = m, f

        # XXX Spurious 'type: ignore' below.
        m = create_model(cls.__name__, __base__=cls, __module__=__name__, **fields)  # type: ignore[call-overload]
        # pydantic.create_model() uses type(), so this will confuse mypy which
        # cannot handle dynamic base class; hence the 'type: ignore'.
        return m  # type: ignore[no-any-return]

    port: Port = Field(
        default=Port(default_port),
        description=(
            "TCP port the postgresql instance will be listening to. "
            f"If unspecified, default to {default_port} unless a 'port' setting is found in 'settings'."
        ),
    )
    settings: Dict[str, Any] = Field(
        default={},
        description=("Settings for the PostgreSQL instance."),
        examples=[
            {
                "listen_addresses": "*",
                "shared_buffers": "1GB",
                "ssl": True,
                "ssl_key_file": "/etc/certs/db.key",
                "ssl_cert_file": "/etc/certs/db.key",
                "shared_preload_libraries": "pg_stat_statements",
            }
        ],
    )
    surole_password: Optional[SecretStr] = Field(
        default=None,
        description="Super-user role password.",
        readOnly=True,
        exclude=True,
    )
    replrole_password: Optional[SecretStr] = Field(
        default=None,
        description="Replication role password.",
        readOnly=True,
        exclude=True,
    )
    data_checksums: Optional[bool] = Field(
        default=None,
        description=(
            "Enable or disable data checksums. "
            "If unspecified, fall back to site settings choice."
        ),
    )
    locale: Optional[str] = Field(
        default=None, description="Default locale.", readOnly=True
    )
    encoding: Optional[str] = Field(
        default=None,
        description="Character encoding of the PostgreSQL instance.",
        readOnly=True,
    )

    class Auth(BaseModel):
        local: Optional[s.AuthLocalMethod] = Field(
            default=None,
            description="Authentication method for local-socket connections",
            readOnly=True,
        )
        host: Optional[s.AuthHostMethod] = Field(
            default=None,
            description="Authentication method for local TCP/IP connections",
            readOnly=True,
        )

    auth: Optional[Auth] = Field(default=None, exclude=True, writeOnly=True)

    standby: Optional[Standby] = Field(default=None, description="Standby information.")

    state: InstanceState = Field(
        default=InstanceState.started,
        description="Runtime state.",
    )
    databases: List["Database"] = Field(
        default=[],
        description="Databases defined in this instance (non-exhaustive list).",
        exclude=True,
        writeOnly=True,
    )
    roles: List["Role"] = Field(
        default=[],
        description="Roles defined in this instance (non-exhaustive list).",
        exclude=True,
        writeOnly=True,
    )

    pending_restart: bool = Field(
        default=False,
        description="Whether the instance needs a restart to account for settings changes.",
        readOnly=True,
    )
    restart_on_changes: bool = Field(
        default=False,
        description="Whether or not to automatically restart the instance to account for settings changes.",
        exclude=True,
        writeOnly=True,
    )

    @root_validator(pre=True)
    def __validate_port_(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that 'port' field and settings['port'] are consistent.

        If unspecified, 'port' is either set from settings value or from
        the default port value.

        >>> i = Instance(name="i")
        >>> i.port, "port" in i.settings
        (5432, False)
        >>> i = Instance(name="i", settings={"port": 5423})
        >>> i.port, i.settings["port"]
        (5423, 5423)
        >>> i = Instance(name="i", port=5454)
        >>> i.port, "port" in i.settings
        (5454, False)

        Otherwise, and if settings['port'] exists, make sure values are
        consistent and possibly cast the latter as an integer.

        >>> i = Instance(name="i", settings={"port": 5455})
        >>> i.port, i.settings["port"]
        (5455, 5455)
        >>> i = Instance(name="i", port=123, settings={"port": "123"})
        >>> i.port, i.settings["port"]
        (123, 123)
        >>> Instance(name="i", port=321, settings={"port": 123})
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        __root__
          'port' field and settings['port'] mismatch (type=value_error)
        >>> Instance(name="i", settings={"port": "abc"})
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        __root__
          invalid literal for int() with base 10: 'abc' (type=value_error)
        """
        config_port = None
        try:
            port = values["port"]
        except KeyError:
            try:
                config_port = int(values["settings"]["port"])
            except KeyError:
                pass
            else:
                values["port"] = Port(config_port)
        else:
            try:
                config_port = int(values["settings"]["port"])
            except KeyError:
                pass
            else:
                if config_port != port:
                    raise ValueError("'port' field and settings['port'] mismatch")
        if config_port is not None:
            values["settings"]["port"] = config_port
        return values

    @root_validator
    def __validate_standby_and_patroni_(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get("standby") and values.get("patroni"):
            raise ValueError("'patroni' and 'standby' fields are mutually exclusive")
        return values

    @validator("settings")
    def __validate_settings_(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        """Validate 'settings' field.

        >>> Instance(name="main", settings={"log_directory": 1})
        Traceback (most recent call last):
          ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        settings
          expecting a string for 'log_directory' setting (type=value_error)
        """
        try:
            if not isinstance(value["log_directory"], str):
                raise ValueError("expecting a string for 'log_directory' setting")
        except KeyError:
            pass
        return value

    _S = TypeVar("_S", bound=ServiceManifest)

    def service_manifest(self, stype: Type[_S]) -> _S:
        """Return satellite service manifest attached to this instance.

        :raises ValueError: if not found.
        """
        fname = stype.__service__
        try:
            s = getattr(self, fname)
        except AttributeError:
            raise ValueError(fname)
        if s is None:
            raise ValueError(fname)
        assert isinstance(
            s, stype
        ), f"expecting field {fname} to have type {stype} (got {type(s)})"
        return s

    def surole(self, settings: s.Settings) -> "Role":
        s = settings.postgresql.surole
        return Role(
            name=s.name,
            password=self.surole_password,
            pgpass=s.pgpass,
        )

    def replrole(self, settings: s.Settings) -> "Role":
        name = settings.postgresql.replrole
        return Role(
            name=name,
            password=self.replrole_password,
            login=True,
            replication=True,
            in_roles=["pg_read_all_stats"],
        )

    def auth_options(self, settings: s.AuthSettings) -> Auth:
        auth = self.auth
        local, host = settings.local, settings.host
        if auth:
            local = auth.local or local
            host = auth.host or host
        return Instance.Auth(local=local, host=host)

    def pg_hba(self, settings: s.Settings) -> str:
        surole = self.surole(settings)
        replrole = self.replrole(settings)
        auth = self.auth_options(settings.postgresql.auth)
        return util.template("postgresql", "pg_hba.conf").format(
            auth=auth,
            surole=surole.name,
            backuprole=settings.postgresql.backuprole.name,
            replrole=replrole.name,
        )

    def pg_ident(self, settings: s.Settings) -> str:
        surole = self.surole(settings)
        replrole = self.replrole(settings)
        return util.template("postgresql", "pg_ident.conf").format(
            surole=surole.name,
            backuprole=settings.postgresql.backuprole.name,
            replrole=replrole.name,
            sysuser=settings.sysuser[0],
        )

    def initdb_options(self, base: s.InitdbSettings) -> s.InitdbSettings:
        data_checksums: Union[None, Literal[True]] = {
            True: True,
            False: None,
            None: base.data_checksums or None,
        }[self.data_checksums]
        return s.InitdbSettings(
            locale=self.locale or base.locale,
            encoding=self.encoding or base.encoding,
            data_checksums=data_checksums,
        )


class InstanceBackup(Manifest):
    label: str
    size: ByteSize
    repo_size: ByteSize
    date_start: datetime
    date_stop: datetime
    type: Literal["incr", "diff", "full"]
    databases: List[str]


class Tablespace(BaseModel):
    name: str
    location: str
    size: ByteSize


class DetailedDatabase(Manifest):
    """PostgreSQL database (with details)"""

    name: str
    owner: str
    encoding: str
    collation: str
    ctype: str
    acls: List[str]
    size: ByteSize
    description: Optional[str]
    tablespace: Tablespace

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        tablespace = kwargs["tablespace"]
        if not isinstance(tablespace, Tablespace):
            assert isinstance(tablespace, str)
            try:
                kwargs["tablespace"] = Tablespace(
                    name=tablespace,
                    location=kwargs.pop("tablespace_location"),
                    size=kwargs.pop("tablespace_size"),
                )
            except KeyError as exc:
                raise TypeError(f"missing {exc} argument when 'tablespace' is a string")
        super().__init__(**kwargs)


class DefaultPrivilege(Manifest):
    """Default access privilege"""

    database: str
    schema_: str = Field(alias="schema")
    object_type: str
    role: str
    privileges: List[str]

    @validator("privileges")
    def __sort_privileges_(cls, value: List[str]) -> List[str]:
        return sorted(value)


class Privilege(DefaultPrivilege):
    """Access privilege"""

    object_name: str
    column_privileges: Dict[str, List[str]]

    @validator("column_privileges")
    def __sort_column_privileges_(
        cls, value: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        for v in value.values():
            v.sort()
        return value


class PGSetting(Manifest):
    """A column from pg_settings view."""

    _query: ClassVar[
        str
    ] = "SELECT name, setting, context, pending_restart FROM pg_settings"

    name: str
    setting: str
    context: str
    pending_restart: bool


class ApplyChangeState(AutoStrEnum):
    """A apply change state for object handled by pglift"""

    created = enum.auto()  #:
    changed = enum.auto()  #:
    dropped = enum.auto()  #:


class ApplyResult(Manifest):
    """
    ApplyResult allows to describe the result of a call to apply function
    (Eg: pglift.database.apply) to an object (Eg: database, instance,...).

    The `change_state` attribute of this class can be set to one of to those values:
      - :attr:`~ApplyChangeState.created` if the object has been created,
      - :attr:`~ApplyChangeState.changed` if the object has been changed,
      - :attr:`~ApplyChangeState.dropped` if the object has been dropped,
      - :obj:`None` if nothing happened to the object we manipulate (neither created,
        changed or dropped)
    """

    change_state: Optional[ApplyChangeState] = Field(
        description="Define the change applied (created, changed or dropped) to a manipulated object",
    )  #:


class InstanceApplyResult(ApplyResult):
    pending_restart: bool = Field(
        default=False,
        description="Whether the instance needs a restart to account for settings changes.",
    )
