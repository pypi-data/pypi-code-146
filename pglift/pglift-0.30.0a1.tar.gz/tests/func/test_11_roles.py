import datetime
import functools
import logging
from unittest.mock import patch

import psycopg
import pytest
from pydantic import SecretStr

from pglift import databases, db, exceptions, postgresql, roles
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.settings import PostgreSQLVersion

from . import AuthType, execute, role_in_pgpass
from .conftest import DatabaseFactory, RoleFactory


@pytest.fixture(scope="module", autouse=True)
def _postgresql_running(instance: system.Instance) -> None:
    ctx = Context(settings=instance._settings)
    if not postgresql.is_running(ctx, instance):
        pytest.fail("instance is not running")


def test_exists(
    ctx: Context, instance: system.Instance, role_factory: RoleFactory
) -> None:
    assert not roles.exists(ctx, instance, "absent")
    role_factory("present")
    assert roles.exists(ctx, instance, "present")


def test_create(ctx: Context, instance: system.Instance) -> None:
    role = interface.Role(name="nopassword")
    assert not roles.exists(ctx, instance, role.name)
    roles.create(ctx, instance, role)
    assert roles.exists(ctx, instance, role.name)
    assert not role.has_password

    role = interface.Role(
        name="password",
        password="scret",
        login=True,
        connection_limit=5,
        validity=datetime.datetime(2050, 1, 2, tzinfo=datetime.timezone.utc),
        in_roles=["pg_monitor"],
    )
    assert not roles.exists(ctx, instance, role.name)
    roles.create(ctx, instance, role)
    assert roles.exists(ctx, instance, role.name)
    assert role.has_password
    r = execute(
        ctx,
        instance,
        f"select rolpassword from pg_authid where rolname = '{role.name}'",
    )
    if instance.version >= PostgreSQLVersion.v14:
        assert r[0]["rolpassword"].startswith("SCRAM-SHA-256$4096:")
    else:
        assert r[0]["rolpassword"].startswith("md5")
    r = execute(ctx, instance, "select 1 as v", dbname="template1", role=role)
    assert r[0]["v"] == 1
    (record,) = execute(
        ctx,
        instance,
        f"select rolvaliduntil, rolconnlimit from pg_roles where rolname = '{role.name}'",
        dbname="template1",
        role=role,
    )
    assert record["rolvaliduntil"] == role.validity
    assert record["rolconnlimit"] == role.connection_limit
    r = execute(
        ctx,
        instance,
        """
        SELECT
            r.rolname AS role,
            ARRAY_AGG(m.rolname) AS member_of
        FROM
            pg_auth_members
            JOIN pg_authid m ON pg_auth_members.roleid = m.oid
            JOIN pg_authid r ON pg_auth_members.member = r.oid
        GROUP BY
            r.rolname
        """,
    )
    assert {"role": "password", "member_of": ["pg_monitor"]} in r

    nologin = interface.Role(name="nologin", password="passwd", login=False)
    roles.create(ctx, instance, nologin)
    with pytest.raises(
        psycopg.OperationalError, match='role "nologin" is not permitted to log in'
    ):
        execute(ctx, instance, "select 1", dbname="template1", role=nologin)


def test_apply(ctx: Context, instance: system.Instance) -> None:
    rolname = "applyme"
    _role_in_pgpass = functools.partial(
        role_in_pgpass, ctx.settings.postgresql.auth.passfile
    )

    role = interface.Role(name=rolname)
    assert not roles.exists(ctx, instance, role.name)
    assert (
        roles.apply(ctx, instance, role).change_state
        == interface.ApplyChangeState.created
    )
    assert roles.exists(ctx, instance, role.name)
    assert not role.has_password
    assert not _role_in_pgpass(role)
    assert roles.apply(ctx, instance, role).change_state is None  # no-op

    role = interface.Role(name=rolname, state="absent")
    assert roles.exists(ctx, instance, role.name)
    assert (
        roles.apply(ctx, instance, role).change_state
        == interface.ApplyChangeState.dropped
    )
    assert not roles.exists(ctx, instance, role.name)

    role = interface.Role(name=rolname, password=SecretStr("passw0rd"))
    assert (
        roles.apply(ctx, instance, role).change_state
        == interface.ApplyChangeState.created
    )
    assert role.has_password
    assert not _role_in_pgpass(role)

    role = interface.Role(
        name=rolname, login=True, password=SecretStr("passw0rd"), pgpass=True
    )
    assert (
        roles.apply(ctx, instance, role).change_state
        == interface.ApplyChangeState.changed
    )
    assert role.has_password
    assert _role_in_pgpass(role)
    with db.connect(
        ctx,
        instance,
        dbname="template1",
        user=rolname,
        password="passw0rd",
    ):
        pass

    pwchanged_role = role.copy(
        update={"password": SecretStr("changed"), "state": "present"}
    )
    assert (
        roles.apply(ctx, instance, pwchanged_role).change_state
        == interface.ApplyChangeState.changed
    )

    nopw_role = role.copy(update={"password": None, "state": "present"})
    assert roles.apply(ctx, instance, nopw_role).change_state is None

    role = interface.Role(
        name=rolname,
        login=True,
        password=SecretStr("passw0rd_changed"),
        pgpass=True,
        connection_limit=5,
    )
    assert (
        roles.apply(ctx, instance, role).change_state
        == interface.ApplyChangeState.changed
    )
    assert role.has_password
    assert _role_in_pgpass(role)
    assert roles.get(ctx, instance, rolname).connection_limit == 5
    with db.connect(
        ctx,
        instance,
        dbname="template1",
        user=rolname,
        password="passw0rd_changed",
    ):
        pass

    role = interface.Role(name=rolname, pgpass=False)
    assert (
        roles.apply(ctx, instance, role).change_state
        == interface.ApplyChangeState.changed
    )
    roles.apply(ctx, instance, role)
    assert not role.has_password
    assert not _role_in_pgpass(role)
    assert roles.get(ctx, instance, rolname).connection_limit is None


def test_alter_surole_password(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    postgresql_auth: AuthType,
    caplog: pytest.LogCaptureFixture,
) -> None:
    if postgresql_auth == AuthType.peer:
        pytest.skip(f"not applicable for auth:{postgresql_auth}")

    check_connect = functools.partial(
        db.connect,
        ctx,
        instance,
        user="postgres",
    )
    surole = roles.get(ctx, instance, "postgres")
    surole = surole.copy(
        update={
            "password": instance_manifest.surole(ctx.settings).password,
            "state": "present",
        }
    )
    role = surole.copy(
        update={"password": SecretStr("passw0rd_changed"), "state": "present"}
    )
    caplog.clear()
    with caplog.at_level(logging.WARNING, logger="pgflit.roles"):
        assert (
            roles.apply(ctx, instance, role).change_state
            == interface.ApplyChangeState.changed
        )
    if postgresql_auth == AuthType.password_command:
        assert (
            "failed to retrieve new role postgres, possibly due to password"
            in caplog.messages[0]
        )
    else:
        assert not caplog.messages
    try:
        with check_connect(password="passw0rd_changed"):
            pass
    finally:
        with patch.dict("os.environ", {"PGPASSWORD": "passw0rd_changed"}):
            assert (
                roles.apply(ctx, instance, surole).change_state
                == interface.ApplyChangeState.changed
            )
        with pytest.raises(
            psycopg.OperationalError, match="password authentication failed"
        ):
            with check_connect(password="passw0rd_changed"):
                pass
        with db.connect(ctx, instance):
            pass


def test_get(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    role_factory: RoleFactory,
) -> None:
    with pytest.raises(exceptions.RoleNotFound, match="absent"):
        roles.get(ctx, instance, "absent")

    postgres = roles.get(ctx, instance, "postgres")
    assert postgres is not None
    surole = instance_manifest.surole(ctx.settings)
    assert postgres.name == "postgres"
    if surole.password:
        assert postgres.has_password
        if surole.pgpass:
            assert postgres.pgpass is not None
        assert roles.get(ctx, instance, "postgres", password=False).password is None
    assert postgres.login
    assert postgres.superuser
    assert postgres.replication

    role_factory(
        "r1",
        "LOGIN NOINHERIT VALID UNTIL '2051-07-29T00:00+00:00' IN ROLE pg_monitor CONNECTION LIMIT 10",
    )
    r1 = roles.get(ctx, instance, "r1")
    assert r1.password is None
    assert not r1.inherit
    assert r1.login
    assert not r1.superuser
    assert not r1.replication
    assert r1.connection_limit == 10
    assert r1.in_roles == ["pg_monitor"]
    assert r1.validity == datetime.datetime(2051, 7, 29, tzinfo=datetime.timezone.utc)


def test_list(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    role_factory: RoleFactory,
) -> None:
    roles.apply(
        ctx,
        instance,
        interface.Role.parse_obj({"name": "r1", "pgpass": True, "password": "secret"}),
    )
    role_factory(
        "r2",
        "LOGIN NOINHERIT VALID UNTIL '2051-07-29T00:00+00:00' IN ROLE pg_monitor CONNECTION LIMIT 10",
    )
    rls = roles.list(ctx, instance)
    roles.drop(ctx, instance, interface.RoleDropped(name="r1"))
    assert {"r1", "r2"} & {r.name for r in rls}
    r1 = next(r for r in rls if r.name == "r1").dict(include={"has_password", "pgpass"})
    r2 = next(r for r in rls if r.name == "r2").dict()
    assert r1 == {"has_password": True, "pgpass": True}
    assert r2 == {
        "connection_limit": 10,
        "has_password": False,
        "in_roles": ["pg_monitor"],
        "inherit": False,
        "login": True,
        "name": "r2",
        "pgpass": False,
        "replication": False,
        "superuser": False,
        "validity": datetime.datetime(2051, 7, 29, 0, 0, tzinfo=datetime.timezone.utc),
    }


def test_alter(
    ctx: Context, instance: system.Instance, role_factory: RoleFactory
) -> None:
    role = interface.Role(
        name="alter",
        password="scret",
        login=True,
        connection_limit=5,
        validity=datetime.datetime(2050, 1, 2, tzinfo=datetime.timezone.utc),
        in_roles=["pg_read_all_stats", "pg_signal_backend"],
    )
    with pytest.raises(exceptions.RoleNotFound, match="alter"):
        roles.alter(ctx, instance, role)
    role_factory("alter", "IN ROLE pg_read_all_settings, pg_read_all_stats")
    roles.alter(ctx, instance, role)
    described = roles.get(ctx, instance, "alter").dict()
    expected = role.dict()
    assert described == expected


def test_drop(
    ctx: Context, instance: system.Instance, role_factory: RoleFactory
) -> None:
    with pytest.raises(exceptions.RoleNotFound, match="dropping_absent"):
        roles.drop(ctx, instance, interface.Role(name="dropping_absent"))
    role_factory("dropme")
    roles.drop(ctx, instance, interface.Role(name="dropme"))
    assert not roles.exists(ctx, instance, "dropme")


def test_drop_reassign_owned(
    ctx: Context, instance: system.Instance, database_factory: DatabaseFactory
) -> None:
    role1 = interface.Role(name="owner1", password="password", login=True)
    roles.create(ctx, instance, role1)
    assert roles.exists(ctx, instance, role1.name)

    role2 = interface.Role(name="owner2", password="password", login=True)
    roles.create(ctx, instance, role2)
    assert roles.exists(ctx, instance, role2.name)

    schema = "myschema"
    execute(ctx, instance, f"CREATE SCHEMA {schema}", fetch=False, dbname="postgres")
    execute(
        ctx,
        instance,
        f"GRANT ALL ON SCHEMA {schema} TO PUBLIC",
        fetch=False,
        dbname="postgres",
    )

    tablename = "myapp"
    execute(
        ctx,
        instance,
        f"CREATE TABLE {schema}.{tablename} (id INT)",
        fetch=False,
        dbname="postgres",
        role=role1,
    )
    r = execute(
        ctx,
        instance,
        f"SELECT tableowner FROM pg_catalog.pg_tables WHERE tablename = '{tablename}'",
        dbname="postgres",
        role=role1,
    )
    assert {"tableowner": role1.name} in r
    with pytest.raises(
        exceptions.DependencyError,
        match=r'role "owner1" cannot be dropped .* \(detail: owner of table myschema.myapp\)',
    ):
        roles.drop(ctx, instance, role1)

    role1 = role1._copy_validate(
        update={"reassign_owned": role2.name, "state": "absent"}
    )
    roles.apply(ctx, instance, role1)
    assert not roles.exists(ctx, instance, role1.name)
    r = execute(
        ctx,
        instance,
        f"SELECT tableowner FROM pg_catalog.pg_tables WHERE tablename = '{tablename}'",
    )
    assert {"tableowner": role2.name} in r

    database_factory("db_owned", owner=role2.name)

    role2 = role2._copy_validate(update={"drop_owned": True, "state": "absent"})
    roles.apply(ctx, instance, role2)
    assert not roles.exists(ctx, instance, role2.name)
    r = execute(
        ctx,
        instance,
        f"SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = '{tablename}')",
    )
    assert {"exists": False} in r
    assert not databases.exists(ctx, instance, "db_owned")
