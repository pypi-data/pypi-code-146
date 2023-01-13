import enum
from pathlib import Path
from typing import ClassVar, Dict, Final, List, Optional

import attr
import psycopg
import psycopg.conninfo
from pydantic import Field, SecretStr, validator

from .. import types
from ..settings import PrometheusSettings
from ..types import Port
from . import impl

default_port: Final = 9187
service_name: Final = "postgres_exporter"


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Service:
    """A Prometheus postgres_exporter service bound to a PostgreSQL instance."""

    __service_name__: ClassVar[str] = service_name

    name: str
    """Identifier for the service, usually the instance qualname."""

    settings: PrometheusSettings

    port: int
    """TCP port for the web interface and telemetry."""

    password: Optional[SecretStr]

    def __str__(self) -> str:
        return f"{self.__service_name__}@{self.name}"

    def args(self) -> List[str]:
        configpath = impl._configpath(self.name, self.settings)
        return impl._args(self.settings.execpath, configpath)

    def pidfile(self) -> Path:
        return impl._pidfile(self.name, self.settings)

    def env(self) -> Dict[str, str]:
        configpath = impl._configpath(self.name, self.settings)
        return impl._env(configpath)


class ServiceManifest(types.ServiceManifest, service_name="prometheus"):
    port: Port = Field(
        default=Port(default_port),
        description="TCP port for the web interface and telemetry of Prometheus",
    )
    password: Optional[SecretStr] = Field(
        default=None,
        description="Password of PostgreSQL role for Prometheus postgres_exporter.",
        exclude=True,
    )

    @validator("password")
    def __validate_password(cls, v: Optional[SecretStr]) -> Optional[SecretStr]:
        """Validate 'password' field.

        >>> ServiceManifest(password='without_space')  # doctest: +ELLIPSIS
        ServiceManifest(...)
        >>> ServiceManifest(password='with space')  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for ServiceManifest
        password
          password must not contain blank spaces (type=value_error)
        """
        # Avoid spaces as this will break postgres_exporter configuration.
        # See https://github.com/prometheus-community/postgres_exporter/issues/393
        if v is not None and " " in v.get_secret_value():
            raise ValueError("password must not contain blank spaces")
        return v


class PostgresExporter(types.Manifest):
    """Prometheus postgres_exporter service."""

    class State(types.AutoStrEnum):
        """Runtime state"""

        started = enum.auto()
        stopped = enum.auto()
        absent = enum.auto()

    _cli_config: ClassVar[Dict[str, types.CLIConfig]] = {
        "state": {"choices": [State.started.value, State.stopped.value]},
    }

    name: str = Field(description="locally unique identifier of the service")
    dsn: str = Field(description="connection string of target instance")
    password: Optional[SecretStr] = Field(description="connection password")
    port: int = Field(description="TCP port for the web interface and telemetry")
    state: State = Field(default=State.started, description="runtime state")

    @validator("name")
    def __validate_name_(cls, v: str) -> str:
        """Validate 'name' field.

        >>> PostgresExporter(name='without-slash', dsn="", port=12)  # doctest: +ELLIPSIS
        PostgresExporter(name='without-slash', ...)
        >>> PostgresExporter(name='with/slash', dsn="", port=12)
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for PostgresExporter
        name
          must not contain slashes (type=value_error)
        """
        # Avoid slash as this will break file paths during settings templating
        # (configpath, etc.)
        if "/" in v:
            raise ValueError("must not contain slashes")
        return v

    @validator("dsn")
    def __validate_dsn_(cls, value: str) -> str:
        try:
            psycopg.conninfo.conninfo_to_dict(value)
        except psycopg.ProgrammingError as e:
            raise ValueError(str(e)) from e
        return value
