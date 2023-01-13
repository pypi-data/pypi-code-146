import functools
import json
import socket
from datetime import timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

import attr
import pgtoolkit.conf
import yaml
from pydantic import BaseModel, Field, validator

from .. import types

if TYPE_CHECKING:
    from ..models import interface, system
    from ..settings import Settings


class _BaseModel(BaseModel):
    class Config:
        allow_mutation = False
        extra = "allow"
        validate_always = True
        validate_assignment = True


def bootstrap(manifest: "interface.Instance", settings: "Settings") -> Dict[str, Any]:
    """Return values for the "bootstrap" section of Patroni configuration."""
    patroni_settings = settings.patroni
    assert patroni_settings
    initdb_options = manifest.initdb_options(settings.postgresql.initdb)
    initdb: List[Union[str, Dict[str, str]]] = [
        {key: value}
        for key, value in initdb_options.dict(exclude_none=True).items()
        if key != "data_checksums"
    ]
    if initdb_options.data_checksums:
        initdb.append("data-checksums")
    pg_hba = manifest.pg_hba(settings).splitlines()
    pg_ident = manifest.pg_ident(settings).splitlines()
    return dict(
        dcs={"loop_wait": patroni_settings.loop_wait},
        initdb=initdb,
        pg_hba=pg_hba,
        pg_ident=pg_ident,
    )


def postgresql(
    instance: "system.BaseInstance",
    manifest: "interface.Instance",
    configuration: pgtoolkit.conf.Configuration,
    postgresql_connect_host: Optional[str],
    **args: Any,
) -> Dict[str, Any]:
    """Return values for the "postgresql" section of Patroni configuration.

    Any values from `**args` are used over default values that would be
    inferred but values from `manifest` still take precedence.
    """
    if "authentication" not in args:
        settings = instance._settings

        def r(role: "interface.Role") -> Dict[str, str]:
            d = {"username": role.name}
            if role.password:
                d["password"] = role.password.get_secret_value()
            return d

        args["authentication"] = {
            "superuser": r(manifest.surole(settings)),
            "replication": r(manifest.replrole(settings)),
        }
        args["authentication"]["rewind"] = args["authentication"]["superuser"]

    if postgresql_connect_host is not None:
        args["connect_address"] = types.Address.validate(
            f"{postgresql_connect_host}:{manifest.port}"
        )
    else:
        args["connect_address"] = types.Address.get(manifest.port)

    def s(entry: pgtoolkit.conf.Entry) -> Union[str, bool, int, float]:
        # Serialize pgtoolkit entry without quoting; specially needed to
        # timedelta.
        if isinstance(entry.value, timedelta):
            return entry.serialize().strip("'")
        return entry.value

    parameters = args.setdefault("parameters", {})
    parameters.update({k: s(e) for k, e in sorted(configuration.entries.items())})

    listen_addresses = parameters.get("listen_addresses", "*")
    args["listen"] = types.Address.validate(f"{listen_addresses}:{manifest.port}")

    args.setdefault("use_unix_socket", True)
    args.setdefault("use_unix_socket_repl", True)
    args.setdefault("pgpass", None)
    args.setdefault("data_dir", instance.datadir)
    args.setdefault("bin_dir", instance.bindir)
    if "pg_hba" not in args:
        args["pg_hba"] = manifest.pg_hba(settings).splitlines()
    if "pg_ident" not in args:
        args["pg_ident"] = manifest.pg_ident(settings).splitlines()

    return args


class RESTAPI(_BaseModel):
    connect_address: types.Address = Field(
        default_factory=functools.partial(types.Address.get, port=8008),
        description="IP address (or hostname) and port, to access the Patroni's REST API.",
    )
    listen: types.Address = Field(
        default=None,
        description="IP address (or hostname) and port that Patroni will listen to for the REST API.",
    )

    @validator("listen", always=True, pre=True)
    def __validate_listen_(cls, value: Optional[str], values: Dict[str, Any]) -> str:
        """Set 'listen' from 'connect_address' if unspecified.

        >>> RESTAPI(connect_address="localhost:8008")
        RESTAPI(connect_address='localhost:8008', listen='localhost:8008')
        >>> RESTAPI(connect_address="localhost:8008", listen="server:123")
        RESTAPI(connect_address='localhost:8008', listen='server:123')
        """
        if not value:
            value = values["connect_address"]
            assert isinstance(value, str)
        return value


class Patroni(_BaseModel):
    """A Patroni instance."""

    class PostgreSQL(_BaseModel):
        connect_address: types.Address
        listen: types.Address
        parameters: Dict[str, Any]

    scope: str = Field(description="Cluster name.")
    name: str = Field(description="Host name.")
    restapi: RESTAPI = Field(default_factory=RESTAPI)
    postgresql: PostgreSQL

    _P = TypeVar("_P", bound="Patroni")

    @classmethod
    def build(
        cls: Type[_P],
        postgresql_connect_host: Optional[str],
        instance: "system.BaseInstance",
        manifest: "interface.Instance",
        configuration: pgtoolkit.conf.Configuration,
        **args: Any,
    ) -> _P:
        if "bootstrap" not in args:
            args["bootstrap"] = bootstrap(manifest, instance._settings)
        args["postgresql"] = postgresql(
            instance,
            manifest,
            configuration,
            postgresql_connect_host,
            **args.pop("postgresql", {}),
        )
        return cls(**args)

    def yaml(self) -> str:
        data = json.loads(self.json(exclude_none=True))
        return yaml.dump(data, sort_keys=True)  # type: ignore[no-any-return]


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Service:
    """A Patroni service bound to a PostgreSQL instance."""

    cluster: str
    node: str


class ClusterMember(BaseModel):
    """An item of the list of members returned by Patroni API /cluster endpoint."""

    class Config:
        extra = "allow"
        frozen = True

    host: str
    name: str
    port: int
    role: str
    state: str


class ServiceManifest(types.ServiceManifest, service_name="patroni"):
    _cli_config: ClassVar[Dict[str, types.CLIConfig]] = {
        "cluster_members": {"hide": True},
    }
    _ansible_config: ClassVar[Dict[str, types.AnsibleConfig]] = {
        "cluster_members": {"hide": True},
    }

    # XXX Or simply use instance.qualname?
    cluster: str = Field(
        description="Name (scope) of the Patroni cluster.",
        readOnly=True,
    )
    node: str = Field(
        default_factory=socket.getfqdn,
        description="Name of the node (usually the host name).",
        readOnly=True,
    )
    restapi: RESTAPI = Field(
        default_factory=RESTAPI, description="REST API configuration"
    )
    postgresql_connect_host: Optional[str] = Field(
        default=None,
        description="Host or IP address through which PostgreSQL is externally accessible.",
    )
    cluster_members: List[ClusterMember] = Field(
        default=[],
        description="Members of the Patroni this instance is member of.",
        readOnly=True,
    )
