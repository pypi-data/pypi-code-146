import socket
from pathlib import Path

import port_for
import psycopg.conninfo
import pydantic
import pytest

from pglift import types
from pglift.ctx import Context
from pglift.models import interface
from pglift.prometheus import models as prometheus_models
from pglift.settings import Settings


def test_validate_ports() -> None:
    class S(pydantic.BaseModel):
        name: str
        port: types.Port

    class M(pydantic.BaseModel):
        p: types.Port
        s: S

    p1 = port_for.select_random()
    p2 = port_for.select_random()
    m = M.parse_obj({"p": p1, "s": {"name": "x", "port": p2}})
    interface.validate_ports(m)

    with socket.socket() as s1, socket.socket() as s2:
        s1.bind(("", p1))
        s1.listen()
        s2.bind(("", p2))
        s2.listen()
        with pytest.raises(pydantic.ValidationError) as cm:
            interface.validate_ports(m)
    assert f"{p1} already in use" in str(cm)
    assert f"{p2} already in use" in str(cm)


def test_instance_auth_options(
    settings: Settings, instance_manifest: interface.Instance
) -> None:
    assert instance_manifest.auth_options(
        settings.postgresql.auth
    ) == interface.Instance.Auth(local="peer", host="password")


def test_instance_pg_hba(
    settings: Settings,
    instance_manifest: interface.Instance,
    datadir: Path,
    write_changes: bool,
) -> None:
    actual = instance_manifest.pg_hba(settings)
    fpath = datadir / "pg_hba.conf"
    if write_changes:
        fpath.write_text(actual)
    expected = fpath.read_text()
    assert actual == expected


def test_instance_pg_ident(
    settings: Settings,
    instance_manifest: interface.Instance,
    datadir: Path,
    write_changes: bool,
) -> None:
    actual = instance_manifest.pg_ident(settings)
    fpath = datadir / "pg_ident.conf"
    if write_changes:
        fpath.write_text(actual)
    expected = fpath.read_text()
    assert actual == expected


def test_instance_initdb_options(
    settings: Settings, instance_manifest: interface.Instance
) -> None:
    initdb_settings = settings.postgresql.initdb
    assert instance_manifest.initdb_options(initdb_settings) == initdb_settings
    assert instance_manifest.copy(
        update={"locale": "X", "data_checksums": True}
    ).initdb_options(initdb_settings) == initdb_settings.copy(
        update={"locale": "X", "data_checksums": True}
    )
    assert instance_manifest.copy(update={"data_checksums": None}).initdb_options(
        initdb_settings.copy(update={"data_checksums": True})
    ) == initdb_settings.copy(update={"data_checksums": True})


def test_privileges_sorted() -> None:
    p = interface.Privilege(
        database="postgres",
        schema="main",
        object_type="table",
        object_name="foo",
        role="postgres",
        privileges=["select", "delete", "update"],
        column_privileges={"postgres": ["update", "delete", "reference"]},
    )
    assert p.dict() == {
        "column_privileges": {"postgres": ["delete", "reference", "update"]},
        "database": "postgres",
        "object_name": "foo",
        "object_type": "table",
        "privileges": ["delete", "select", "update"],
        "role": "postgres",
        "schema_": "main",
    }


def test_instance_composite_service(ctx: Context, pg_version: str) -> None:
    Instance = interface.Instance.composite(ctx.pm)
    with pytest.raises(ValueError, match="none is not an allowed value"):
        m = Instance.parse_obj(
            {"name": "test", "version": pg_version, "prometheus": None}
        )

    m = Instance.parse_obj(
        {"name": "test", "version": pg_version, "prometheus": {"port": 123}}
    )
    s = m.service_manifest(prometheus_models.ServiceManifest)
    assert s.port == 123

    class MyServiceManifest(types.ServiceManifest, service_name="notfound"):
        pass

    with pytest.raises(ValueError, match="notfound"):
        m.service_manifest(MyServiceManifest)


def test_role_state() -> None:
    assert interface.Role(name="exist").state.name == "present"
    assert interface.Role(name="notexist", state="absent").state.name == "absent"
    assert interface.RoleDropped(name="dropped").state.name == "absent"
    with pytest.raises(pydantic.ValidationError, match="unexpected value"):
        interface.RoleDropped(name="p", state="present")


def test_database_clone_from() -> None:
    with pytest.raises(pydantic.ValidationError, match="invalid or missing URL scheme"):
        interface.Database(name="cloned_db", clone_from="blob")

    db = interface.Database(
        name="cloned_db", clone_from="postgres://dba:pwd@server/base"
    )
    assert psycopg.conninfo.conninfo_to_dict(str(db.clone_from)) == {
        "dbname": "base",
        "host": "server",
        "password": "pwd",
        "user": "dba",
    }
