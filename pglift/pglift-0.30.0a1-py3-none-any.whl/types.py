import enum
import json
import re
import socket
import subprocess
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypedDict,
    TypeVar,
    Union,
)

import psycopg.errors
import yaml
from pgtoolkit import conf as pgconf
from pydantic import BaseModel, ConstrainedStr, SecretStr

from ._compat import TypeAlias

if TYPE_CHECKING:
    CompletedProcess = subprocess.CompletedProcess[str]
    Popen = subprocess.Popen[str]
else:
    CompletedProcess = subprocess.CompletedProcess
    Popen = subprocess.Popen


class StrEnum(str, enum.Enum):
    def __str__(self) -> str:
        assert isinstance(self.value, str)
        return self.value


@enum.unique
class AutoStrEnum(StrEnum):
    """Enum base class with automatic values set to member name.

    >>> class State(AutoStrEnum):
    ...     running = enum.auto()
    ...     stopped = enum.auto()
    >>> State.running
    <State.running: 'running'>
    >>> State.stopped
    <State.stopped: 'stopped'>
    """

    def _generate_next_value_(name, *args: Any) -> str:  # type: ignore[override]
        return name


class CommandRunner(Protocol):
    def __call__(
        self,
        args: Sequence[str],
        *,
        check: bool = False,
        **kwargs: Any,
    ) -> CompletedProcess:
        ...


ConfigChanges: TypeAlias = Dict[
    str, Tuple[Optional[pgconf.Value], Optional[pgconf.Value]]
]


class BackupType(AutoStrEnum):
    """Backup type."""

    full = enum.auto()
    """full backup"""
    incr = enum.auto()
    """incremental backup"""
    diff = enum.auto()
    """differential backup"""

    @classmethod
    def default(cls) -> "BackupType":
        return cls.incr


PostgreSQLStopMode = Literal["smart", "fast", "immediate"]


class Role(Protocol):
    name: str
    password: Optional[SecretStr]


class NoticeHandler(Protocol):
    def __call__(self, diag: psycopg.errors.Diagnostic) -> Any:
        ...


class AnsibleArgSpec(TypedDict, total=False):
    required: bool
    type: str
    default: Any
    choices: List[str]
    description: List[str]
    no_log: bool
    elements: str
    options: Dict[str, Any]


class CLIConfig(TypedDict, total=False):
    """Configuration for CLI generation of a manifest field."""

    name: str
    hide: bool
    choices: List[str]


class AnsibleConfig(TypedDict, total=False):
    hide: bool
    choices: List[str]
    spec: AnsibleArgSpec


class Port(int):
    """Port field type."""

    P = TypeVar("P", bound="Port")

    @classmethod
    def __get_validators__(cls: Type[P]) -> Iterator[Callable[..., P]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type[P], value: Any) -> P:
        return cls(value)

    def available(self) -> bool:
        """Return True if this port is free to use."""
        port = int(self)
        for family, socktype, proto, canonname, sockaddr in socket.getaddrinfo(
            None, port, 0, socket.SOCK_STREAM, 0, socket.AI_PASSIVE
        ):
            with socket.socket(family, socktype, proto) as s:
                if s.connect_ex(sockaddr) == 0:
                    return False
        return True


class Manifest(BaseModel):
    """Base class for manifest data classes."""

    _cli_config: ClassVar[Dict[str, CLIConfig]] = {}
    _ansible_config: ClassVar[Dict[str, AnsibleConfig]] = {}

    class Config:
        allow_mutation = False
        extra = "forbid"
        validate_always = True
        validate_assignment = True

    _M = TypeVar("_M", bound="Manifest")

    @classmethod
    def parse_yaml(cls: Type[_M], value: Union[str, IO[str]]) -> _M:
        """Parse from a YAML stream."""
        data = yaml.safe_load(value)
        return cls.parse_obj(data)

    def yaml(self, **kwargs: Any) -> str:
        """Return a YAML serialization of this manifest."""
        data = json.loads(self.json(by_alias=True, **kwargs))
        return yaml.dump(data, sort_keys=False, explicit_start=True)  # type: ignore[no-any-return]

    def _copy_validate(self: _M, update: Dict[str, Any]) -> _M:
        """Like .copy(), but with validation (and default value setting).

        (Internal method, mostly useful for test purpose.)
        """
        return self.__class__.validate(dict(self.dict(by_alias=True), **update))


class ServiceManifest(Manifest):
    __service__: ClassVar[str]

    def __init_subclass__(cls, *, service_name: str, **kwargs: Any) -> None:
        """Set a __name__ to subclasses.

        >>> class MyS(ServiceManifest, service_name="my"):
        ...     x: str
        >>> s = MyS(x=1)
        >>> s.__class__.__service__
        'my'
        """
        super().__init_subclass__(**kwargs)
        cls.__service__ = service_name


class Runnable(Protocol):
    __service_name__: ClassVar[str]

    @property
    def name(self) -> Optional[str]:
        ...

    def args(self) -> List[str]:
        ...

    def pidfile(self) -> Path:
        ...

    def env(self) -> Optional[Dict[str, str]]:
        ...


class Address(ConstrainedStr):
    r"""Network address type <host or ip>:<port>.

    >>> class Cfg(BaseModel):
    ...     addr: Address
    >>> cfg = Cfg(addr="server:123")
    >>> cfg.addr
    'server:123'
    >>> cfg.addr.host, cfg.addr.port
    ('server', 123)

    >>> Cfg(addr="server")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Cfg
    addr
      string does not match regex "(?P<host>[^\s:?#]+):(?P<port>\d+)" (type=value_error.str.regex; pattern=...)
    >>> Cfg(addr="server:ab")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Cfg
    addr
      string does not match regex "(?P<host>[^\s:?#]+):(?P<port>\d+)" (type=value_error.str.regex; pattern=...)
    """

    __slots__ = ("host", "port")

    regex = re.compile(r"(?P<host>[^\s:?#]+):(?P<port>\d+)")

    A = TypeVar("A", bound="Address")

    def __new__(cls: Type[A], value: str, *, host: str, port: int) -> A:
        return str.__new__(cls, value)

    def __init__(self, value: str, *, host: str, port: int) -> None:
        str.__init__(value)
        self.host = host
        self.port = port

    @classmethod
    def validate(cls: Type[A], value: str) -> A:
        value = super().validate(value)
        m = cls.regex.match(value)
        assert m  # True, per parent validation.
        host, port = m.group("host"), m.group("port")
        return cls(value, host=host, port=int(port))

    @classmethod
    def get(cls: Type[A], port: int) -> A:
        host = socket.gethostbyname(socket.gethostname())
        if host.startswith("127."):  # loopback addresses
            host = socket.getfqdn()
        return cls.validate(f"{host}:{port}")
