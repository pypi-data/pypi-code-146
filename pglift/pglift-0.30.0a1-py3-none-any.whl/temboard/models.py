from pathlib import Path
from typing import ClassVar, Final, List, Optional

import attr
from pydantic import Field, SecretStr

from .. import types
from ..settings import TemboardSettings
from . import impl

default_port: Final = 2345
service_name: Final = "temboard_agent"


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Service:
    """A temboard-agent service bound to a PostgreSQL instance."""

    __service_name__: ClassVar[str] = service_name

    name: str
    """Identifier for the service, usually the instance qualname."""

    settings: TemboardSettings

    port: int
    """TCP port for the temboard-agent API."""

    password: Optional[SecretStr]

    def __str__(self) -> str:
        return f"{self.__service_name__}@{self.name}"

    def args(self) -> List[str]:
        configpath = impl._configpath(self.name, self.settings)
        return impl._args(self.settings.execpath, configpath)

    def pidfile(self) -> Path:
        return impl._pidfile(self.name, self.settings)

    def env(self) -> None:
        return None


class ServiceManifest(types.ServiceManifest, service_name="temboard"):
    port: types.Port = Field(
        default=types.Port(default_port),
        description="TCP port for the temboard-agent API.",
    )
    password: Optional[SecretStr] = Field(
        default=None,
        description="Password of PostgreSQL role for temboard agent.",
        exclude=True,
    )
