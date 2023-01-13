import logging
import re
from pathlib import Path
from typing import List, NoReturn, Optional, Tuple

import pytest
from pgtoolkit import conf as pgconf
from pgtoolkit.ctl import Status

from pglift import databases, db, exceptions, instances, postgresql, systemd
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.settings import PostgreSQLVersion
from pglift.systemd import service_manager

from . import AuthType, check_connect, execute, reconfigure_instance
from .conftest import Factory


def test_directories(instance: system.Instance) -> None:
    assert instance.datadir.exists()
    assert instance.waldir.exists()
    assert (instance.waldir / "archive_status").is_dir()


def test_config(
    instance: system.Instance, instance_manifest: interface.Instance
) -> None:
    postgresql_conf = instance.datadir / "postgresql.conf"
    assert postgresql_conf.exists()
    pgconfig = pgconf.parse(postgresql_conf)
    assert {k for k, v in pgconfig.entries.items() if not v.commented} & set(
        instance_manifest.settings
    )


def test_psqlrc(instance: system.Instance) -> None:
    assert instance.psqlrc.read_text().strip().splitlines() == [
        f"\\set PROMPT1 '[{instance}] %n@%~%R%x%# '",
        "\\set PROMPT2 ' %R%x%# '",
    ]


def test_systemd(ctx: Context, instance: system.Instance) -> None:
    if ctx.settings.service_manager == "systemd":
        assert systemd.is_enabled(
            ctx, service_manager.unit("postgresql", instance.qualname)
        )


def test_reinit(
    ctx: Context,
    instance: system.PostgreSQLInstance,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Instance already exists, no-op.
    with monkeypatch.context() as m:

        def fail() -> NoReturn:
            raise AssertionError("unexpected called")

        m.setattr(postgresql, "pg_ctl", fail)
        instances.init(
            ctx, interface.Instance(name=instance.name, version=instance.version)
        )


def test_log_directory(instance: system.Instance, log_directory: Path) -> None:
    config = instance.config()
    assert isinstance(config.log_directory, str)
    instance_log_dir = Path(config.log_directory)
    assert instance_log_dir == log_directory
    assert instance_log_dir.exists()


def passfile_entries(passfile: Path, *, role: str = "postgres") -> List[str]:
    return [line for line in passfile.read_text().splitlines() if f":{role}:" in line]


def test_pgpass(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    postgresql_auth: AuthType,
    surole_password: Optional[str],
    pgbackrest_password: Optional[str],
) -> None:
    passfile = ctx.settings.postgresql.auth.passfile
    if postgresql_auth != AuthType.pgpass:
        pytest.skip(f"not applicable for auth:{postgresql_auth}")

    port = instance.port
    backuprole = ctx.settings.postgresql.backuprole.name

    assert passfile_entries(passfile) == [f"*:{port}:*:postgres:{surole_password}"]
    assert passfile_entries(passfile, role=backuprole) == [
        f"*:{port}:*:{backuprole}:{pgbackrest_password}"
    ]

    with reconfigure_instance(ctx, instance_manifest, port=port + 1):
        assert passfile_entries(passfile) == [
            f"*:{port+1}:*:postgres:{surole_password}"
        ]
        assert passfile_entries(passfile, role=backuprole) == [
            f"*:{port+1}:*:{backuprole}:{pgbackrest_password}"
        ]

    assert passfile_entries(passfile) == [f"*:{port}:*:postgres:{surole_password}"]
    assert passfile_entries(passfile, role=backuprole) == [
        f"*:{port}:*:{backuprole}:{pgbackrest_password}"
    ]


def test_connect(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    postgresql_auth: AuthType,
) -> None:
    check_connect(ctx, postgresql_auth, instance_manifest, instance)


def test_replrole(ctx: Context, instance: system.Instance) -> None:
    (row,) = execute(
        ctx,
        instance,
        # Simplified version of \du in psql.
        "SELECT rolsuper, rolcanlogin, rolreplication,"
        " ARRAY(SELECT b.rolname"
        "       FROM pg_catalog.pg_auth_members m"
        "       JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid)"
        "       WHERE m.member = r.oid) as memberof"
        " FROM pg_catalog.pg_roles r"
        " WHERE rolname = 'replication'",
    )
    assert row == {
        "rolsuper": False,
        "rolcanlogin": True,
        "rolreplication": True,
        "memberof": ["pg_read_all_stats"],
    }


def test_hba(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    postgresql_auth: AuthType,
) -> None:
    hba_path = instance.datadir / "pg_hba.conf"
    hba = hba_path.read_text().splitlines()
    auth_settings = ctx.settings.postgresql.auth
    auth_instance = instance_manifest.auth
    assert auth_instance is not None
    if postgresql_auth == AuthType.peer:
        assert "peer" in hba[0]
    assert (
        f"local   all             all                                     {auth_settings.local}"
        in hba
    )
    assert (
        f"host    all             all             127.0.0.1/32            {auth_instance.host}"
        in hba
    )


def test_ident(
    ctx: Context, instance: system.Instance, postgresql_auth: AuthType
) -> None:
    ident_path = instance.datadir / "pg_ident.conf"
    ident = ident_path.read_text().splitlines()
    assert ident[0] == "# MAPNAME       SYSTEM-USERNAME         PG-USERNAME"
    if postgresql_auth == AuthType.peer:
        assert re.match(r"^test\s+\w+\s+postgres$", ident[1])
    else:
        assert len(ident) == 1


def test_start_stop_restart_running_is_ready_stopped(
    ctx: Context, instance: system.Instance, caplog: pytest.LogCaptureFixture
) -> None:
    i = instance
    assert postgresql.status(ctx, i) == Status.running
    assert postgresql.is_ready(ctx, i)
    use_systemd = ctx.settings.service_manager == "systemd"
    if use_systemd:
        assert systemd.is_active(ctx, service_manager.unit("postgresql", i.qualname))

    instances.stop(ctx, i)
    try:
        assert postgresql.status(ctx, i) == Status.not_running
        assert not postgresql.is_ready(ctx, i)
        if use_systemd:
            assert not systemd.is_active(
                ctx, service_manager.unit("postgresql", i.qualname)
            )
        # Stopping a non-running instance is a no-op.
        caplog.clear()
        with caplog.at_level(logging.WARNING, logger="pglift"):
            instances.stop(ctx, i)
        assert f"instance {instance} is already stopped" in caplog.records[0].message
    finally:
        instances.start(ctx, i)

    assert postgresql.status(ctx, i) == Status.running
    assert postgresql.is_ready(ctx, i)
    if use_systemd:
        assert systemd.is_active(ctx, service_manager.unit("postgresql", i.qualname))

    assert postgresql.status(ctx, i) == Status.running
    assert postgresql.is_ready(ctx, i)
    if not use_systemd:
        # FIXME: systemctl restart would fail with:
        #   Start request repeated too quickly.
        #   Failed with result 'start-limit-hit'.
        instances.restart(ctx, i)
        assert postgresql.status(ctx, i) == Status.running
        assert postgresql.is_ready(ctx, i)
    instances.reload(ctx, i)
    assert postgresql.status(ctx, i) == Status.running
    assert postgresql.is_ready(ctx, i)

    assert postgresql.status(ctx, i) == Status.running
    with instances.stopped(ctx, i):
        assert postgresql.status(ctx, i) == Status.not_running
        with instances.stopped(ctx, i):
            assert postgresql.status(ctx, i) == Status.not_running
            assert not postgresql.is_ready(ctx, i)
        with instances.running(ctx, i):
            assert postgresql.status(ctx, i) == Status.running
            assert postgresql.is_ready(ctx, i)
            with instances.running(ctx, i):
                assert postgresql.status(ctx, i) == Status.running
            with instances.stopped(ctx, i):
                assert postgresql.status(ctx, i) == Status.not_running
                assert not postgresql.is_ready(ctx, i)
            assert postgresql.status(ctx, i) == Status.running
            assert postgresql.is_ready(ctx, i)
        assert postgresql.status(ctx, i) == Status.not_running
    assert postgresql.status(ctx, i) == Status.running
    assert postgresql.is_ready(ctx, i)


def test_apply(
    ctx: Context,
    pg_version: str,
    tmp_path: Path,
    instance_factory: Factory[Tuple[interface.Instance, system.Instance]],
    caplog: pytest.LogCaptureFixture,
) -> None:
    i = system.BaseInstance.get("test_apply", pg_version, ctx)
    assert postgresql.status(ctx, i) == Status.unspecified_datadir
    im, i = instance_factory(
        ctx.settings,
        name="test_apply",
        settings={
            "unix_socket_directories": str(tmp_path),
            "ssl": True,
        },
        restart_on_changes=False,
        roles=[{"name": "bob"}],
        databases=[
            {"name": "db1"},
            {"name": "db2", "owner": "bob", "extensions": ["unaccent"]},
        ],
        pgbackrest={"stanza": "test_apply_stanza"},
    )
    assert i.port == im.port
    pgconfig = i.config()
    assert pgconfig
    assert pgconfig.ssl

    result_apply = instances.apply(ctx, im)
    assert result_apply.change_state is None  # no-op

    assert postgresql.status(ctx, i) == Status.not_running
    im = im._copy_validate({"state": "started"})
    result_apply = instances.apply(ctx, im)
    assert result_apply.change_state == interface.ApplyChangeState.changed
    assert postgresql.status(ctx, i) == Status.running
    with db.connect(ctx, i) as conn:
        assert not instances.pending_restart(conn)

    with postgresql.running(ctx, i):
        assert databases.exists(ctx, i, "db1")
        assert databases.exists(ctx, i, "db2")
        db2 = databases.get(ctx, i, "db2")
        assert db2.extensions == ["unaccent"]
        assert db2.owner == "bob"

    newconfig = im.settings.copy()
    newconfig["listen_addresses"] = "*"  # requires restart
    newconfig["autovacuum"] = False  # requires reload
    im = im._copy_validate({"settings": newconfig})
    with caplog.at_level(logging.DEBUG, logger="pgflit"):
        result_apply = instances.apply(ctx, im)
        assert result_apply.change_state == interface.ApplyChangeState.changed
    assert (
        f"instance {i} needs restart due to parameter changes: listen_addresses"
        in caplog.messages
    )
    assert postgresql.status(ctx, i) == Status.running
    with db.connect(ctx, i) as conn:
        assert instances.pending_restart(conn)

    im = im._copy_validate({"state": "stopped"})
    result_apply = instances.apply(ctx, im)
    assert result_apply.change_state == interface.ApplyChangeState.changed
    assert postgresql.status(ctx, i) == Status.not_running

    im = im._copy_validate({"state": "absent"})
    assert instances.apply(ctx, im).change_state == interface.ApplyChangeState.dropped
    with pytest.raises(exceptions.InstanceNotFound):
        i.exists()
    assert postgresql.status(ctx, i) == Status.unspecified_datadir


def test_get(
    ctx: Context,
    instance: system.Instance,
    log_directory: Path,
    pgbackrest_available: bool,
    powa_available: bool,
) -> None:
    im = instances.get(ctx, instance)
    assert im is not None
    assert im.name == "test"
    config = im.settings
    assert im.port == instance.port
    assert im.data_directory == instance.datadir  # type: ignore[attr-defined]
    assert im.wal_directory == instance.waldir  # type: ignore[attr-defined]
    # Pop host-dependent values.
    del config["effective_cache_size"]
    del config["shared_buffers"]
    spl = "passwordcheck"
    if powa_available:
        spl += ", pg_qualstats, pg_stat_statements, pg_stat_kcache"
    socket_directory = str(ctx.settings.postgresql.socket_directory).format(
        instance=instance
    )
    expected_config = {
        "cluster_name": "test",
        "lc_messages": "C",
        "lc_monetary": "C",
        "lc_numeric": "C",
        "lc_time": "C",
        "log_destination": "stderr",
        "log_directory": str(log_directory),
        "logging_collector": True,
        "shared_preload_libraries": spl,
        "unix_socket_directories": socket_directory,
    }
    if pgbackrest_available:
        del config["archive_command"]
        expected_config["archive_mode"] = True
        expected_config["wal_level"] = "replica"
    assert config == expected_config
    assert im.data_checksums is False
    assert im.state.name == "started"
    assert not im.pending_restart


def test_list(ctx: Context, instance: system.Instance) -> None:
    not_instance_dir = Path(
        str(ctx.settings.postgresql.datadir).format(
            version="12", name="notAnInstanceDir"
        )
    )
    not_instance_dir.mkdir(parents=True)
    try:
        ilist = list(instances.list(ctx))

        for i in ilist:
            assert i.status == Status.running.name
            # this also ensure instance name is not notAnInstanceDir
            assert i.name == "test"

        for i in ilist:
            if (i.version, i.name) == (instance.version, instance.name):
                break
        else:
            assert False, f"Instance {instance.version}/{instance.name} not found"

        iv = next(instances.list(ctx, version=instance.version))
        assert iv == i
    finally:
        not_instance_dir.rmdir()


def test_upgrade(
    ctx: Context, pg_version: str, upgraded_instance: system.Instance
) -> None:
    assert upgraded_instance.name == "upgraded"
    assert upgraded_instance.version == pg_version
    assert postgresql.status(ctx, upgraded_instance) == Status.not_running
    with postgresql.running(ctx, upgraded_instance):
        assert databases.exists(ctx, upgraded_instance, "postgres")


def test_upgrade_pgpass(
    ctx: Context,
    postgresql_auth: AuthType,
    upgraded_instance: system.Instance,
    surole_password: Optional[str],
    pgbackrest_password: Optional[str],
) -> None:
    passfile = ctx.settings.postgresql.auth.passfile
    if postgresql_auth != AuthType.pgpass:
        pytest.skip(f"not applicable for auth:{postgresql_auth}")
    backuprole = ctx.settings.postgresql.backuprole.name
    port = upgraded_instance.port
    assert f"*:{port}:*:postgres:{surole_password}" in passfile_entries(passfile)
    assert f"*:{port}:*:{backuprole}:{pgbackrest_password}" in passfile_entries(
        passfile, role=backuprole
    )


def test_server_settings(ctx: Context, instance: system.Instance) -> None:
    with db.connect(ctx, instance) as conn:
        pgsettings = instances.settings(conn)
    port = next(p for p in pgsettings if p.name == "port")
    assert port.setting == str(instance.port)
    assert not port.pending_restart
    assert port.context == "postmaster"


def test_logs(ctx: Context, instance: system.Instance) -> None:
    logs = list(instances.logs(ctx, instance))
    assert any(
        "database system is ready to accept connections" in line for line in logs
    )


def test_get_locale(
    ctx: Context, instance_manifest: interface.Instance, instance: system.Instance
) -> None:
    assert postgresql.is_running(ctx, instance)
    with db.connect(ctx, instance) as conn:
        assert instances.get_locale(conn) == "C"
    with reconfigure_instance(ctx, instance_manifest, lc_numeric=""):
        with db.connect(ctx, instance) as conn:
            assert instances.get_locale(conn) is None


def test_data_checksums(
    ctx: Context,
    pg_version: str,
    instance_factory: Factory[Tuple[interface.Instance, system.Instance]],
    caplog: pytest.LogCaptureFixture,
) -> None:
    manifest, instance = instance_factory(ctx.settings, "datachecksums")

    with postgresql.running(ctx, instance):
        assert execute(ctx, instance, "SHOW data_checksums") == [
            {"data_checksums": "off"}
        ]

    # explicitly enabled
    manifest = manifest._copy_validate({"data_checksums": True})
    if pg_version <= PostgreSQLVersion.v11:
        with pytest.raises(
            exceptions.UnsupportedError,
            match=r"^PostgreSQL <= 11 doesn't have pg_checksums to enable data checksums$",
        ):
            instances.apply(ctx, manifest)
        return

    with caplog.at_level(logging.INFO, logger="pglift.instances"):
        result_apply = instances.apply(ctx, manifest)
        assert result_apply.change_state == interface.ApplyChangeState.changed
    with postgresql.running(ctx, instance):
        assert execute(ctx, instance, "SHOW data_checksums") == [
            {"data_checksums": "on"}
        ]
    assert "enabling data checksums" in caplog.messages
    caplog.clear()

    assert instances._get(ctx, instance).data_checksums

    # not explicitly disabled so still enabled
    result_apply = instances.apply(
        ctx, manifest._copy_validate({"data_checksums": None})
    )
    assert result_apply.change_state is None
    with postgresql.running(ctx, instance):
        assert execute(ctx, instance, "SHOW data_checksums") == [
            {"data_checksums": "on"}
        ]

    # explicitly disabled
    with caplog.at_level(logging.INFO, logger="pglift.instances"):
        result_apply = instances.apply(
            ctx, manifest._copy_validate({"data_checksums": False})
        )
        assert result_apply.change_state == interface.ApplyChangeState.changed
    with postgresql.running(ctx, instance):
        assert execute(ctx, instance, "SHOW data_checksums") == [
            {"data_checksums": "off"}
        ]
    assert "disabling data checksums" in caplog.messages
    caplog.clear()
    assert instances._get(ctx, instance).data_checksums is False

    # re-enabled with instance running
    with postgresql.running(ctx, instance):
        with pytest.raises(
            exceptions.InstanceStateError,
            match="could not alter data_checksums on a running instance",
        ):
            instances.apply(ctx, manifest._copy_validate({"data_checksums": True}))
    assert instances._get(ctx, instance).data_checksums is False
