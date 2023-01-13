from typing import Optional
from unittest.mock import patch

import psycopg
import pytest
from tenacity import retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from pglift import instances, postgresql
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.postgresql import Standby

from . import AuthType, execute
from .conftest import DatabaseFactory


def test_password(standby_instance: system.Instance, replrole_password: str) -> None:
    assert standby_instance.standby
    assert (
        standby_instance.standby.password
        and standby_instance.standby.password.get_secret_value() == replrole_password
    )


def test_primary_conninfo(standby_instance: system.Instance) -> None:
    assert standby_instance.standby
    assert standby_instance.standby.primary_conninfo


def test_slot(
    ctx: Context,
    instance: system.Instance,
    standby_manifest: interface.Instance,
    standby_instance: system.Instance,
) -> None:
    assert standby_manifest.standby
    slotname = standby_manifest.standby.slot
    assert standby_instance.standby
    assert standby_instance.standby.slot == slotname
    rows = execute(ctx, instance, "SELECT slot_name FROM pg_replication_slots")
    assert [r["slot_name"] for r in rows] == [slotname]


def test_pgpass(postgresql_auth: AuthType, standby_instance: system.Instance) -> None:
    if postgresql_auth != AuthType.pgpass:
        pytest.skip(f"not applicable for auth:{postgresql_auth}")
    settings = standby_instance._settings
    passfile = settings.postgresql.auth.passfile
    assert str(standby_instance.port) not in passfile.read_text()


def test_replication(
    pg_version: str,
    ctx: Context,
    instance: system.Instance,
    instance_manifest: interface.Instance,
    postgresql_auth: AuthType,
    surole_password: Optional[str],
    database_factory: DatabaseFactory,
    standby_instance: system.Instance,
) -> None:
    assert standby_instance.standby

    settings = instance._settings

    surole = instance_manifest.surole(settings)
    replrole = instance_manifest.replrole(settings)

    if surole.password:

        def get_stdby() -> Optional[Standby]:
            assert surole.password
            with patch.dict(
                "os.environ", {"PGPASSWORD": surole.password.get_secret_value()}
            ):
                return instances._get(ctx, standby_instance).standby

    else:

        def get_stdby() -> Optional[Standby]:
            return instances._get(ctx, standby_instance).standby

    class OutOfSync(AssertionError):
        pass

    @retry(
        retry=retry_if_exception_type(psycopg.OperationalError),
        wait=wait_fixed(2),
        stop=stop_after_attempt(5),
    )
    def assert_db_replicated() -> None:
        rows = execute(
            ctx,
            standby_instance,
            "SELECT * FROM t",
            role=replrole,
            dbname="test",
        )
        if rows[0]["i"] != 1:
            pytest.fail(f"table 't' not replicated; rows: {rows}")

    @retry(
        retry=retry_if_exception_type(OutOfSync),
        wait=wait_fixed(2),
        stop=stop_after_attempt(5),
    )
    def assert_replicated(expected: int) -> None:
        rlag = postgresql.replication_lag(standby_instance)
        assert rlag is not None
        row = execute(
            ctx,
            standby_instance,
            "SELECT * FROM t",
            role=replrole,
            dbname="test",
        )
        if row[0]["i"] != expected:
            assert rlag > 0
            raise OutOfSync
        if rlag > 0:
            raise OutOfSync
        if rlag != 0:
            pytest.fail(f"non-zero replication lag: {rlag}")

    assert postgresql.is_running(ctx, instance)
    assert postgresql.is_running(ctx, standby_instance)

    database_factory("test", owner=replrole.name)
    execute(
        ctx,
        instance,
        "CREATE TABLE t AS (SELECT 1 AS i)",
        dbname="test",
        fetch=False,
        role=replrole,
    )
    stdby = get_stdby()
    assert stdby is not None
    assert stdby.primary_conninfo == standby_instance.standby.primary_conninfo
    assert stdby.password == replrole.password
    assert stdby.slot == standby_instance.standby.slot
    assert stdby.replication_lag is not None
    if pg_version >= "12":
        assert stdby.wal_sender_state == "streaming"

    assert execute(
        ctx,
        standby_instance,
        "SELECT * FROM pg_is_in_recovery()",
        role=replrole,
        dbname="template1",
    ) == [{"pg_is_in_recovery": True}]

    assert_db_replicated()

    execute(
        ctx,
        instance,
        "UPDATE t SET i = 42",
        dbname="test",
        role=replrole,
        fetch=False,
    )

    assert_replicated(42)

    stdby = get_stdby()
    assert stdby is not None
    assert stdby.replication_lag == 0
    if pg_version >= "12":
        assert stdby.wal_sender_state == "streaming"
