import configparser
import io
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest
from pgtoolkit.conf import Configuration, parse

from pglift import exceptions, types
from pglift.ctx import Context
from pglift.models import interface
from pglift.models.system import Instance
from pglift.pgbackrest import base as pgbackrest
from pglift.pgbackrest import (
    models,
    repo_host,
    repo_path,
    site_configure_install,
    site_configure_uninstall,
)
from pglift.settings import PgBackRestSettings, Settings


@pytest.fixture
def pgbackrest_settings(settings: Settings) -> PgBackRestSettings:
    assert settings.pgbackrest is not None
    return settings.pgbackrest


def test_site_configure(
    settings: Settings, pgbackrest_settings: PgBackRestSettings
) -> None:
    assert not pgbackrest_settings.configpath.exists()

    site_configure_install(settings)
    assert pgbackrest_settings.configpath.exists()
    assert pgbackrest_settings.lockpath.exists()
    assert pgbackrest_settings.spoolpath.exists()

    repo_path.site_configure_install(settings)
    assert (pgbackrest_settings.configpath / "pgbackrest.conf").exists()
    config = (
        (pgbackrest_settings.configpath / "pgbackrest.conf").read_text().splitlines()
    )
    assert isinstance(pgbackrest_settings.repository, PgBackRestSettings.PathRepository)
    assert f"repo1-path = {pgbackrest_settings.repository.path}" in config
    assert "repo1-retention-full = 2" in config
    assert pgbackrest_settings.repository.path.exists()

    leftover = pgbackrest_settings.configpath / "conf.d" / "x.conf"
    leftover.touch()
    site_configure_uninstall(settings)
    assert leftover.exists()
    assert pgbackrest_settings.configpath.exists()

    leftover.unlink()

    repo_path.site_configure_uninstall(settings)
    assert pgbackrest_settings.repository.path.exists()
    site_configure_uninstall(settings)
    assert not (pgbackrest_settings.configpath / "pgbackrest.conf").exists()


def test_setup(
    tmp_path: Path, ctx: Context, pgbackrest_settings: PgBackRestSettings
) -> None:
    stanza_path1 = tmp_path / "1.conf"
    datadir1 = tmp_path / "pgdata1"
    service1 = models.Service(stanza="unittests", path=stanza_path1)
    conf = Configuration()
    with pytest.raises(exceptions.SystemError, match="Missing base config file"):
        pgbackrest.setup(ctx, service1, pgbackrest_settings, conf, datadir1)

    pgbackrest_settings.logpath.mkdir(parents=True)
    logfile = pgbackrest_settings.logpath / "unittests-123.log"
    logfile.touch()

    baseconfig = pgbackrest.base_configpath(pgbackrest_settings)
    baseconfig.parent.mkdir(parents=True)
    baseconfig.touch()
    pgbackrest.setup(ctx, service1, pgbackrest_settings, conf, datadir1)

    datadir2 = tmp_path / "pgdata2"
    service2 = models.Service(stanza="unittests", path=stanza_path1, index=2)
    pgbackrest.setup(
        ctx,
        service2,
        pgbackrest_settings,
        parse(io.StringIO("port=5433\nunix_socket_directories=/tmp\n")),
        datadir2,
    )
    assert stanza_path1.read_text().rstrip() == (
        "[unittests]\n"
        f"pg1-path = {datadir1}\n"
        "pg1-port = 5432\n"
        "pg1-user = backup\n"
        f"pg2-path = {datadir2}\n"
        "pg2-port = 5433\n"
        "pg2-user = backup\n"
        "pg2-socket-path = /tmp"
    )

    stanza_path3 = tmp_path / "3.conf"
    datadir3 = tmp_path / "pgdata3"
    service3 = models.Service(stanza="unittests2", path=stanza_path3)
    pgbackrest.setup(ctx, service3, pgbackrest_settings, conf, datadir3)
    assert stanza_path3.exists()

    pgbackrest.revert_setup(ctx, service1, pgbackrest_settings, conf, datadir1)
    assert stanza_path1.exists()
    assert stanza_path3.exists()
    assert str(datadir1) not in stanza_path1.read_text()
    assert logfile.exists()
    pgbackrest.revert_setup(ctx, service2, pgbackrest_settings, conf, datadir2)
    assert not stanza_path1.exists()
    assert not logfile.exists()
    assert stanza_path3.exists()
    pgbackrest.revert_setup(ctx, service3, pgbackrest_settings, conf, datadir3)
    assert not stanza_path3.exists()


def test_make_cmd(settings: Settings, pgbackrest_settings: PgBackRestSettings) -> None:
    assert pgbackrest.make_cmd("42-test", pgbackrest_settings, "stanza-upgrade") == [
        "/usr/bin/pgbackrest",
        f"--config-path={settings.prefix}/etc/pgbackrest",
        "--stanza=42-test",
        "stanza-upgrade",
    ]


def test_backup_info(
    ctx: Context,
    settings: Settings,
    pgbackrest_settings: PgBackRestSettings,
    tmp_path: Path,
) -> None:
    with patch.object(ctx, "run") as run:
        run.return_value.stdout = "[]"
        assert (
            pgbackrest.backup_info(
                ctx,
                models.Service(stanza="testback", path=tmp_path / "mystanza.conf"),
                pgbackrest_settings,
                backup_set="foo",
            )
            == {}
        )
    run.assert_called_once_with(
        [
            "/usr/bin/pgbackrest",
            f"--config-path={settings.prefix}/etc/pgbackrest",
            "--stanza=testback",
            "--set=foo",
            "--output=json",
            "info",
        ],
        check=True,
    )


def test_backup_command(
    instance: Instance, settings: Settings, pgbackrest_settings: PgBackRestSettings
) -> None:
    assert repo_path.backup_command(
        instance, pgbackrest_settings, type=types.BackupType.full
    ) == [
        "/usr/bin/pgbackrest",
        f"--config-path={settings.prefix}/etc/pgbackrest",
        "--stanza=mystanza",
        "--type=full",
        "--log-level-console=info",
        "--start-fast",
        "backup",
    ]


def test_expire_command(
    instance: Instance, settings: Settings, pgbackrest_settings: PgBackRestSettings
) -> None:
    s = instance.service(models.Service)
    assert repo_path.expire_command(s, pgbackrest_settings) == [
        "/usr/bin/pgbackrest",
        f"--config-path={settings.prefix}/etc/pgbackrest",
        "--stanza=mystanza",
        "--log-level-console=info",
        "expire",
    ]


def test_restore_command(
    instance: Instance, settings: Settings, pgbackrest_settings: PgBackRestSettings
) -> None:
    with pytest.raises(exceptions.UnsupportedError):
        pgbackrest.restore_command(
            instance, pgbackrest_settings, date=datetime.now(), backup_set="sunset"
        )

    assert pgbackrest.restore_command(instance, pgbackrest_settings) == [
        "/usr/bin/pgbackrest",
        f"--config-path={settings.prefix}/etc/pgbackrest",
        "--stanza=mystanza",
        "--log-level-console=info",
        "--delta",
        "--link-all",
        "restore",
    ]

    assert pgbackrest.restore_command(
        instance,
        pgbackrest_settings,
        date=datetime(2003, 1, 1).replace(tzinfo=timezone.utc),
    ) == [
        "/usr/bin/pgbackrest",
        f"--config-path={settings.prefix}/etc/pgbackrest",
        "--stanza=mystanza",
        "--log-level-console=info",
        "--delta",
        "--link-all",
        "--target-action=promote",
        "--type=time",
        "--target=2003-01-01 00:00:00.000000+0000",
        "restore",
    ]

    assert pgbackrest.restore_command(
        instance,
        pgbackrest_settings,
        backup_set="x",
    ) == [
        "/usr/bin/pgbackrest",
        f"--config-path={settings.prefix}/etc/pgbackrest",
        "--stanza=mystanza",
        "--log-level-console=info",
        "--delta",
        "--link-all",
        "--target-action=promote",
        "--type=immediate",
        "--set=x",
        "restore",
    ]


def test_standby_backup(
    ctx: Context, pgbackrest_settings: PgBackRestSettings, standby_instance: Instance
) -> None:
    with pytest.raises(
        exceptions.InstanceStateError,
        match="^backup should be done on primary instance",
    ):
        repo_path.backup(ctx, standby_instance, pgbackrest_settings)


def test_standby_restore(
    ctx: Context, pgbackrest_settings: PgBackRestSettings, standby_instance: Instance
) -> None:
    with pytest.raises(
        exceptions.InstanceReadOnlyError,
        match=f"^{standby_instance.version}/standby is a read-only standby",
    ):
        pgbackrest.restore(ctx, standby_instance, pgbackrest_settings)


def test_instance_configure_cancelled_if_repo_exists(
    ctx: Context, instance: Instance, instance_manifest: interface.Instance
) -> None:
    settings = ctx.settings.pgbackrest
    assert settings is not None
    with patch.object(pgbackrest, "enabled", return_value=True) as enabled:
        with pytest.raises(exceptions.Cancelled):
            repo_path.instance_configure(
                ctx=ctx,
                manifest=instance_manifest,
                config=Configuration(),
                creating=True,
                upgrading_from=None,
            )
    assert enabled.call_count == 1


def test_env_for(
    instance: Instance,
    settings: Settings,
    pgbackrest_settings: PgBackRestSettings,
) -> None:
    service = instance.service(models.Service)
    assert pgbackrest.env_for(service, pgbackrest_settings) == {
        "PGBACKREST_CONFIG_PATH": f"{settings.prefix}/etc/pgbackrest",
        "PGBACKREST_STANZA": "mystanza",
    }


def test_system_lookup(
    pgbackrest_settings: PgBackRestSettings, instance: Instance
) -> None:
    stanza_config = pgbackrest.config_directory(pgbackrest_settings) / "mystanza.conf"

    stanza_config.write_text("\nempty\n")
    with pytest.raises(configparser.MissingSectionHeaderError):
        pgbackrest.system_lookup(instance.datadir, pgbackrest_settings)

    stanza_config.write_text("\n[asection]\n")
    assert pgbackrest.system_lookup(instance.datadir, pgbackrest_settings) is None

    other_config = stanza_config.parent / "aaa.conf"
    other_config.write_text(f"[mystanza]\npg42-path = {instance.datadir}\n")
    s = pgbackrest.system_lookup(instance.datadir, pgbackrest_settings)
    assert s is not None and s.path == other_config and s.index == 42
    other_config.unlink()

    stanza_config.write_text(f"[mystanza]\npg1-path = {instance.datadir}\n")
    s = pgbackrest.system_lookup(instance.datadir, pgbackrest_settings)
    assert s is not None and s.stanza == "mystanza" and s.index == 1


def test_repo_host_base_config(tmp_path: Path) -> None:
    ca_file = tmp_path / "ca.crt"
    ca_file.touch()
    crt = tmp_path / "pgbackrest.crt"
    crt.touch()
    key = tmp_path / "pgbackrest.key"
    key.touch(mode=0o600)
    settings = PgBackRestSettings.parse_obj(
        {
            "repository": {
                "host": "backup-srv",
                "host_port": 8433,
                "host_config": "/conf/pgbackrest.conf",
                "ca_cert": ca_file,
                "cn": "pghost",
                "certificate": {"cert": crt, "key": key},
            }
        }
    )
    cp = repo_host.base_config(settings)
    s = io.StringIO()
    cp.write(s)
    assert s.getvalue().strip().splitlines() == [
        "[global]",
        "lock-path = pgbackrest/lock",
        "log-path = pgbackrest",
        "spool-path = pgbackrest/spool",
        "repo1-host-type = tls",
        "repo1-host = backup-srv",
        "repo1-host-port = 8433",
        "repo1-host-config = /conf/pgbackrest.conf",
        f"repo1-host-ca-file = {ca_file}",
        f"repo1-host-cert-file = {crt}",
        f"repo1-host-key-file = {key}",
    ]
    cp = repo_host.server_config(settings)
    s = io.StringIO()
    cp.write(s)
    assert s.getvalue().strip().splitlines() == [
        "[global]",
        "lock-path = pgbackrest/lock",
        "log-path = pgbackrest",
        "tls-server-address = *",
        "tls-server-auth = pghost=*",
        f"tls-server-ca-file = {ca_file}",
        f"tls-server-cert-file = {crt}",
        f"tls-server-key-file = {key}",
        "tls-server-port = 8432",
    ]
