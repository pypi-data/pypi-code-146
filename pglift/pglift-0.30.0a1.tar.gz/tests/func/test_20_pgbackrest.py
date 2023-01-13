import json
import logging
from typing import Iterator, Optional, Tuple

import pytest
from tenacity import retry
from tenacity.before import before_log
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from pglift import postgresql, types
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.pgbackrest import base as pgbackrest
from pglift.pgbackrest import models, repo_path
from pglift.settings import PgBackRestSettings, Settings

from . import AuthType, execute, postgresql_stopped, reconfigure_instance
from .conftest import DatabaseFactory, Factory
from .pgbackrest import PgbackrestRepoHost


@pytest.fixture(scope="session", autouse=True)
def _pgbackrest_available(pgbackrest_available: bool) -> None:
    if not pgbackrest_available:
        pytest.skip("pgbackrest is not available")


def test_configure(
    ctx: Context,
    instance: system.Instance,
    instance_manifest: interface.Instance,
    tmp_port_factory: Iterator[int],
    postgresql_auth: AuthType,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
) -> None:
    instance_config = instance.config()
    assert instance_config
    instance_port = instance_config.port

    stanza = f"mystanza-{instance.name}"
    pgbackrest_settings = pgbackrest.get_settings(ctx.settings)
    stanza_configpath = pgbackrest_settings.configpath / "conf.d" / f"{stanza}.conf"
    assert stanza_configpath.exists()
    lines = stanza_configpath.read_text().splitlines()
    assert f"pg1-port = {instance_port}" in lines
    assert "pg1-user = backup" in lines

    if pgbackrest_repo_host is None:
        assert isinstance(
            pgbackrest_settings.repository, PgBackRestSettings.PathRepository
        )
        assert (
            pgbackrest_settings.repository.path / "archive" / stanza / "archive.info"
        ).exists()

        assert (pgbackrest_settings.logpath / f"{stanza}-stanza-create.log").exists()

    if postgresql_auth == AuthType.pgpass:
        lines = ctx.settings.postgresql.auth.passfile.read_text().splitlines()
        assert any(line.startswith(f"*:{instance.port}:*:backup:") for line in lines)

    pgconfigfile = instance.datadir / "postgresql.conf"
    pgconfig = pgconfigfile.read_text().splitlines()
    assert (
        f"archive_command = '{pgbackrest_settings.execpath}"
        f" --config-path={pgbackrest_settings.configpath}"
        f" --stanza={stanza} archive-push %p'"
        "  # command to use to archive a logfile segment"
    ) in pgconfig

    # If instance's configuration changes, pgbackrest configuration is
    # updated.
    config_before = stanza_configpath.read_text()
    new_port = next(tmp_port_factory)
    with reconfigure_instance(ctx, instance_manifest, port=new_port):
        config_after = stanza_configpath.read_text()
        assert config_after != config_before
        assert f"pg1-port = {new_port}" in config_after.splitlines()


def test_check(
    ctx: Context,
    instance: system.Instance,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    pgbackrest_password: Optional[str],
) -> None:
    """Run a 'pgbackrest check' on database host, when in remote repository setup."""
    if pgbackrest_repo_host is None:
        pytest.skip("not application for local repository")
    pgbackrest_settings = pgbackrest.get_settings(ctx.settings)
    service = instance.service(models.Service)
    with postgresql.running(ctx, instance):
        pgbackrest.check(
            ctx, instance, service, pgbackrest_settings, pgbackrest_password
        )
        pgbackrest_repo_host.run("check", f"--stanza={service.stanza}")
    r = pgbackrest.backup_info(ctx, service, pgbackrest_settings)
    assert r


@pytest.mark.usefixtures("surole_password")
def test_backup_restore(
    logger: logging.Logger,
    ctx: Context,
    settings: Settings,
    instance: system.Instance,
    database_factory: DatabaseFactory,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
) -> None:
    pgbackrest_settings = pgbackrest.get_settings(settings)
    stanza = f"mystanza-{instance.name}"

    assert list(pgbackrest.iter_backups(ctx, instance, pgbackrest_settings)) == []
    if pgbackrest_repo_host is None:
        assert isinstance(
            pgbackrest_settings.repository, PgBackRestSettings.PathRepository
        )
        repopath = pgbackrest_settings.repository.path
        latest_backup = repopath / "backup" / stanza / "latest"

        assert (repopath / "backup" / stanza / "backup.info").exists()
        assert not latest_backup.exists()

    database_factory("backrest")
    execute(
        ctx,
        instance,
        "CREATE TABLE t AS (SELECT 'created' as s)",
        dbname="backrest",
        fetch=False,
    )
    rows = execute(ctx, instance, "SELECT * FROM t", dbname="backrest")
    assert rows == [{"s": "created"}]

    if pgbackrest_repo_host is None:
        repo_path.backup(ctx, instance, pgbackrest_settings, type=types.BackupType.full)
        assert latest_backup.exists() and latest_backup.is_symlink()
        repo_path.expire(ctx, instance, pgbackrest_settings)
        # TODO: check some result from 'expire' command here.
        assert latest_backup.exists() and latest_backup.is_symlink()
    else:
        pgbackrest_repo_host.run("backup", "--stanza", stanza, "--type", "full")
        pgbackrest_repo_host.run("expire", "--stanza", stanza)
        # TODO: check latest_backup

    (backup1,) = list(pgbackrest.iter_backups(ctx, instance, pgbackrest_settings))
    assert backup1.type == "full"
    assert set(backup1.databases) & {"backrest", "postgres"}
    assert backup1.date_stop > backup1.date_start

    execute(
        ctx,
        instance,
        "INSERT INTO t(s) VALUES ('backup1')",
        dbname="backrest",
        fetch=False,
    )

    # Sleep 1s so that the previous backup gets sufficiently old to be picked
    # upon restore later on.
    execute(ctx, instance, "SELECT pg_sleep(1)", fetch=False)
    (record,) = execute(ctx, instance, "SELECT current_timestamp", fetch=True)
    before_drop = record["current_timestamp"]
    execute(
        ctx,
        instance,
        "INSERT INTO t(s) VALUES ('before-drop')",
        dbname="backrest",
        fetch=False,
    )

    execute(ctx, instance, "DROP DATABASE backrest", fetch=False)

    @retry(
        reraise=True,
        wait=wait_fixed(1),
        stop=stop_after_attempt(5),
        before=before_log(logger, logging.DEBUG),
    )
    def check_not_in_recovery() -> None:
        (r,) = execute(ctx, instance, "SELECT pg_is_in_recovery() as in_recovery")
        assert not r["in_recovery"], "instance still in recovery"

    # With no target (date or label option), restore *and* apply WALs, thus
    # getting back to the same state as before the restore, i.e. 'backrest'
    # database dropped.
    with postgresql_stopped(ctx, instance):
        pgbackrest.restore(ctx, instance, pgbackrest_settings)
    check_not_in_recovery()
    rows = execute(ctx, instance, "SELECT datname FROM pg_database")
    assert "backrest" not in [r["datname"] for r in rows]

    # With a date target, WALs are applied until that date.
    with postgresql_stopped(ctx, instance):
        pgbackrest.restore(ctx, instance, pgbackrest_settings, date=before_drop)
    check_not_in_recovery()
    rows = execute(ctx, instance, "SELECT datname FROM pg_database")
    assert "backrest" in [r["datname"] for r in rows]
    rows = execute(ctx, instance, "SELECT * FROM t", dbname="backrest")
    assert {r["s"] for r in rows} == {"created", "backup1"}

    # With a label target, WALs are not replayed, just restore instance state
    # at specified backup.
    with postgresql_stopped(ctx, instance):
        pgbackrest.restore(ctx, instance, pgbackrest_settings, label=backup1.label)
    check_not_in_recovery()
    rows = execute(ctx, instance, "SELECT datname FROM pg_database")
    assert "backrest" in [r["datname"] for r in rows]
    rows = execute(ctx, instance, "SELECT * FROM t", dbname="backrest")
    assert rows == [{"s": "created"}]


def test_upgrade(
    ctx: Context,
    settings: Settings,
    to_be_upgraded_instance: system.Instance,
    upgraded_instance: system.Instance,
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
) -> None:
    pgbackrest_settings = pgbackrest.get_settings(settings)
    # Upgraded instance use the stanza of the original instance.
    assert (
        pgbackrest_settings.configpath
        / "conf.d"
        / f"mystanza-{to_be_upgraded_instance.name}.conf"
    ).exists()
    assert not (
        pgbackrest_settings.configpath
        / "conf.d"
        / f"mystanza-{upgraded_instance.name}.conf"
    ).exists()

    if pgbackrest_repo_host is not None:
        stanza = f"mystanza-{to_be_upgraded_instance.name}"
        r = pgbackrest_repo_host.run("info", "--stanza", stanza, "--output", "json")
        (info,) = json.loads(r.stdout)
        assert not info["backup"]
        assert info["status"]["message"] == "no valid backups"

        with postgresql.running(ctx, upgraded_instance):
            pgbackrest_repo_host.run("backup", "--stanza", stanza)

        r = pgbackrest_repo_host.run("info", "--stanza", stanza, "--output", "json")
        (info,) = json.loads(r.stdout)
        assert info["backup"]
        assert info["status"]["message"] == "ok"


def test_instance_restore_from_backup(
    ctx: Context,
    instance: system.Instance,
    instance_factory: Factory[Tuple[interface.Instance, system.Instance]],
    settings: Settings,
    surole_password: Optional[str],
    pgbackrest_password: Optional[str],
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test a new primary instance can be created from a pgbackrest backup"""
    pgbackrest_settings = pgbackrest.get_settings(settings)
    stanza = f"mystanza-{instance.name}"
    if pgbackrest_repo_host is not None:
        pgbackrest_repo_host.run("backup", "--stanza", stanza, "--type", "full")
    else:
        repo_path.backup(ctx, instance, pgbackrest_settings, type=types.BackupType.full)
    caplog.clear()
    manifest, new_instance = instance_factory(
        ctx.settings,
        "primary_from_pgbackrest",
        surole_password=surole_password,
        pgbackrest={
            "password": pgbackrest_password,
            "restore": {"stanza": stanza},
        },
    )
    assert "creating instance from pgbackrest backup" in caplog.messages
    with postgresql.running(ctx, new_instance):
        replrole = manifest.replrole(settings)
        assert execute(
            ctx,
            new_instance,
            "SELECT * FROM pg_is_in_recovery()",
            role=replrole,
            dbname="template1",
        ) == [{"pg_is_in_recovery": False}]

    pgconfigfile = new_instance.datadir / "postgresql.conf"
    pgconfig = pgconfigfile.read_text().splitlines()
    new_stanza = f"mystanza-{new_instance.name}"
    assert (
        f"archive_command = '{pgbackrest_settings.execpath}"
        f" --config-path={pgbackrest_settings.configpath}"
        f" --stanza={new_stanza} archive-push %p'"
        "  # command to use to archive a logfile segment"
    ) in pgconfig


def test_standby_instance_restore_from_backup(
    ctx: Context,
    instance: system.Instance,
    instance_primary_conninfo: str,
    instance_factory: Factory[Tuple[interface.Instance, system.Instance]],
    replrole_password: str,
    settings: Settings,
    surole_password: Optional[str],
    pgbackrest_password: Optional[str],
    pgbackrest_repo_host: Optional[PgbackrestRepoHost],
) -> None:
    """Test a standby instance can be created from a pgbackrest backup"""
    # create slot on primary
    slot = "standby_restored"
    execute(
        ctx,
        instance,
        f"SELECT true FROM pg_create_physical_replication_slot('{slot}')",
        fetch=False,
    )
    stanza = f"mystanza-{instance.name}"
    if pgbackrest_repo_host is not None:
        pgbackrest_repo_host.run("backup", "--stanza", stanza, "--type", "full")
    else:
        pgbackrest_settings = pgbackrest.get_settings(settings)
        repo_path.backup(
            ctx,
            instance,
            pgbackrest_settings,
            type=types.BackupType.full,
        )
    manifest, standby = instance_factory(
        ctx.settings,
        "standby_from_pgbackrest",
        surole_password=surole_password,
        standby={
            "primary_conninfo": instance_primary_conninfo,
            "password": replrole_password,
            "slot": slot,
        },
        pgbackrest={
            "restore": {"stanza": stanza},
        },
    )
    with postgresql.running(ctx, standby):
        replrole = manifest.replrole(settings)
        assert execute(
            ctx,
            standby,
            "SELECT * FROM pg_is_in_recovery()",
            role=replrole,
            dbname="template1",
        ) == [{"pg_is_in_recovery": True}]
        assert execute(
            ctx,
            instance,
            "SELECT usename, state FROM pg_stat_replication",
        ) == [
            {
                "usename": "replication",
                "state": "streaming",
            }
        ]
