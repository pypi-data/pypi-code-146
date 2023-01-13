import re
import stat
import sys
from typing import Any
from unittest.mock import patch

import pytest
from pgtoolkit.conf import parse as parse_pgconf

from pglift import exceptions, instances, postgresql
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.postgresql import (
    ctl,
    install_systemd_unit_template,
    uninstall_systemd_unit_template,
)
from pglift.settings import Settings, SystemdSettings
from pglift.types import ConfigChanges


def test_initdb_dirty(
    pg_version: str, settings: Settings, ctx: Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = interface.Instance(name="dirty", version=pg_version)
    i = system.BaseInstance("dirty", pg_version, settings)
    i.datadir.mkdir(parents=True)
    (i.datadir / "dirty").touch()
    calls = []
    with pytest.raises(exceptions.CommandError):
        with monkeypatch.context() as m:
            m.setattr("pglift.systemd.enable", lambda *a: calls.append(a))
            postgresql.initdb(ctx, manifest, i)
    assert not i.waldir.exists()
    if ctx.settings.service_manager == "systemd":
        assert not calls


@pytest.mark.parametrize("data_checksums", [True, False])
def test_initdb_force_data_checksums(
    ctx: Context, pg_version: str, data_checksums: bool
) -> None:
    settings = ctx.settings
    assert settings.postgresql.initdb.data_checksums is None
    manifest = interface.Instance(
        name="checksums", version=pg_version, data_checksums=data_checksums
    )
    initdb_options = manifest.initdb_options(settings.postgresql.initdb)
    assert bool(initdb_options.data_checksums) == data_checksums
    instance = system.BaseInstance.get(manifest.name, manifest.version, ctx)

    def fake_init(*a: Any, **kw: Any) -> None:
        instance.datadir.mkdir(parents=True)
        (instance.datadir / "postgresql.conf").touch()

    with patch("pgtoolkit.ctl.PGCtl.init", side_effect=fake_init) as init:
        postgresql.initdb(ctx, manifest, instance)
    expected = {
        "waldir": str(instance.waldir),
        "username": "postgres",
        "encoding": "UTF8",
        "auth_local": "peer",
        "auth_host": "password",
        "locale": "C",
    }
    if data_checksums:
        init.assert_called_once_with(instance.datadir, data_checksums=True, **expected)
    else:
        init.assert_called_once_with(instance.datadir, **expected)


def test_postgresql_service_name(ctx: Context, instance: system.Instance) -> None:
    assert ctx.hook.postgresql_service_name(ctx=ctx, instance=instance) == "postgresql"


def test_postgresql_editable_conf(ctx: Context, instance: system.Instance) -> None:
    assert ctx.hook.postgresql_editable_conf(ctx=ctx, instance=instance) == "\n".join(
        [
            "port = 999",
            "unix_socket_directories = /socks",
            "# backslash_quote = 'safe_encoding'",
        ]
    )


@pytest.mark.usefixtures("nohook")
def test_configuration_configure_postgresql(
    ctx: Context, instance: system.Instance, instance_manifest: interface.Instance
) -> None:
    def configuration_changes(m: interface.Instance) -> ConfigChanges:
        instances.configure_ssl(ctx, m.settings, instance.qualname, ssl_cert_directory)
        configuration = instances.configuration(ctx, m, instance)
        return postgresql.configure_postgresql(
            ctx=ctx, manifest=m, configuration=configuration, instance=instance
        )

    assert "ssl" not in instance_manifest.settings
    configdir = instance.datadir
    ssl_cert_directory = ctx.settings.postgresql.ssl_cert_directory
    postgresql_conf = configdir / "postgresql.conf"
    with postgresql_conf.open("w") as f:
        f.write("bonjour_name = 'overridden'\n")

    changes = configuration_changes(
        instance_manifest._copy_validate(
            {
                "settings": dict(
                    instance_manifest.settings,
                    max_connections=100,
                    shared_buffers="10 %",
                    effective_cache_size="5MB",
                ),
                "port": 5433,
            }
        )
    )
    old_shared_buffers, new_shared_buffers = changes.pop("shared_buffers")
    assert old_shared_buffers is None
    assert new_shared_buffers is not None and new_shared_buffers != "10 %"
    assert changes == {
        "bonjour_name": ("overridden", None),
        "cluster_name": (None, "test"),
        "effective_cache_size": (None, "5MB"),
        "lc_messages": (None, "C"),
        "lc_monetary": (None, "C"),
        "lc_numeric": (None, "C"),
        "lc_time": (None, "C"),
        "log_destination": (None, "stderr"),
        "logging_collector": (None, True),
        "max_connections": (None, 100),
        "port": (None, 5433),
        "shared_preload_libraries": (None, "passwordcheck"),
        "unix_socket_directories": (
            None,
            str(ctx.settings.postgresql.socket_directory),
        ),
    }

    postgresql_conf = configdir / "postgresql.conf"
    content = postgresql_conf.read_text()
    lines = content.splitlines()
    assert "port = 5433" in lines
    assert "cluster_name = 'test'" in lines
    assert re.search(r"shared_buffers = '\d+ [kMGT]?B'", content)
    assert "effective_cache_size" in content
    assert (
        f"unix_socket_directories = '{ctx.settings.prefix}/run/postgresql'" in content
    )

    with postgresql_conf.open() as f:
        config = parse_pgconf(f)
    assert config.port == 5433
    assert config.entries["bonjour_name"].commented
    assert config.cluster_name == "test"

    logdir = instance.datadir / "pglogs"
    assert not logdir.exists()
    changes = configuration_changes(
        instance_manifest._copy_validate(
            {
                "settings": dict(
                    instance_manifest.settings,
                    listen_address="*",
                    ssl=True,
                    log_directory="pglogs",
                ),
                "port": 5432,
            }
        )
    )
    old_effective_cache_size, new_effective_cache_size = changes.pop(
        "effective_cache_size"
    )
    assert old_effective_cache_size == "5MB"
    assert new_effective_cache_size != old_effective_cache_size
    old_shared_buffers1, new_shared_buffers1 = changes.pop("shared_buffers")
    assert old_shared_buffers1 == new_shared_buffers
    assert new_shared_buffers1 != old_shared_buffers1
    assert changes == {
        "listen_address": (None, "*"),
        "max_connections": (100, None),
        "port": (5433, 5432),
        "ssl": (None, True),
        "ssl_cert_file": (
            None,
            f"{ssl_cert_directory}/{instance.qualname}.crt",
        ),
        "ssl_key_file": (
            None,
            f"{ssl_cert_directory}/{instance.qualname}.key",
        ),
        "log_directory": (None, "pglogs"),
    }
    assert logdir.exists()

    # Same configuration, no change.
    mtime_before = postgresql_conf.stat().st_mtime
    changes = configuration_changes(
        instance_manifest._copy_validate(
            {
                "settings": dict(
                    instance_manifest.settings,
                    listen_address="*",
                    ssl=True,
                    log_directory="pglogs",
                ),
            }
        )
    )
    assert changes == {}
    mtime_after = postgresql_conf.stat().st_mtime
    assert mtime_before == mtime_after

    changes = configuration_changes(
        instance_manifest._copy_validate({"settings": {"ssl": True}})
    )
    lines = postgresql_conf.read_text().splitlines()
    assert "ssl = on" in lines
    crt = ssl_cert_directory / f"{instance.qualname}.crt"
    key = ssl_cert_directory / f"{instance.qualname}.key"
    assert crt.exists()
    assert key.exists()
    assert stat.filemode(crt.stat().st_mode) == "-rw-r--r--"
    assert stat.filemode(key.stat().st_mode) == "-rw-------"

    ssl = (cert_file, key_file) = (
        instance.datadir / "c.crt",
        instance.datadir / "k.key",
    )
    for fpath in ssl:
        fpath.touch()
    changes = configuration_changes(
        instance_manifest._copy_validate(
            {
                "settings": {
                    "ssl": True,
                    "ssl_key_file": str(key_file),
                    "ssl_cert_file": str(cert_file),
                }
            }
        )
    )
    assert changes == {
        "ssl_cert_file": (
            f"{ssl_cert_directory}/{instance.qualname}.crt",
            str(cert_file),
        ),
        "ssl_key_file": (
            f"{ssl_cert_directory}/{instance.qualname}.key",
            str(key_file),
        ),
    }
    lines = postgresql_conf.read_text().splitlines()
    assert "ssl = on" in lines
    assert f"ssl_cert_file = '{instance.datadir / 'c.crt'}'" in lines
    assert f"ssl_key_file = '{instance.datadir / 'k.key'}'" in lines
    for fpath in ssl:
        assert fpath.exists()

    # reconfigure default ssl certs
    changes = configuration_changes(
        instance_manifest._copy_validate({"settings": {"ssl": True}})
    )
    assert changes == {
        "ssl_cert_file": (
            str(cert_file),
            f"{ssl_cert_directory}/{instance.qualname}.crt",
        ),
        "ssl_key_file": (
            str(key_file),
            f"{ssl_cert_directory}/{instance.qualname}.key",
        ),
    }

    # disable ssl
    changes = configuration_changes(instance_manifest)
    assert changes == {
        "ssl": (True, None),
        "ssl_cert_file": (
            f"{ssl_cert_directory}/{instance.qualname}.crt",
            None,
        ),
        "ssl_key_file": (
            f"{ssl_cert_directory}/{instance.qualname}.key",
            None,
        ),
        "shared_preload_libraries": (None, "passwordcheck"),
    }


def test_configure_auth(
    ctx: Context, instance_manifest: interface.Instance, instance: system.Instance
) -> None:
    hba = instance.datadir / "pg_hba.conf"
    ident = instance.datadir / "pg_ident.conf"
    orig_hba = hba.read_text()
    orig_ident = ident.read_text()
    ctx.hook.configure_auth(
        settings=ctx.settings, instance=instance, manifest=instance_manifest
    )
    assert hba.read_text() != orig_hba
    assert ident.read_text() != orig_ident


def test_is_ready(ctx: Context, instance: system.Instance) -> None:
    assert not ctl.is_ready(ctx, instance)


def test_check_status(ctx: Context, instance: system.Instance) -> None:
    with pytest.raises(exceptions.InstanceStateError, match="instance is not_running"):
        postgresql.check_status(ctx, instance, postgresql.Status.running)
    postgresql.check_status(ctx, instance, postgresql.Status.not_running)


def test_start_foreground(ctx: Context, instance: system.Instance) -> None:
    with patch("os.execv") as execv:
        postgresql.start_postgresql(ctx, instance, foreground=True, wait=False)
    postgres = instance.bindir / "postgres"
    execv.assert_called_once_with(
        str(postgres), f"{postgres} -D {instance.datadir}".split()
    )


def test_install_systemd_unit_template(
    settings: Settings,
    systemd_settings: SystemdSettings,
) -> None:
    install_systemd_unit_template(
        settings,
        systemd_settings,
        env="SETTINGS=@settings.json",
        header="# Postgres managed by pglift",
    )
    unit = systemd_settings.unit_path / "pglift-postgresql@.service"
    assert unit.exists()
    lines = unit.read_text().splitlines()
    assert lines[0] == "# Postgres managed by pglift"
    assert "Environment=SETTINGS=@settings.json" in lines
    for line in lines:
        if line.startswith("ExecStart"):
            execstart = line.split("=", 1)[-1]
            assert execstart == f"{sys.executable} -m pglift postgres %i"
            break
    else:
        raise AssertionError("ExecStart line not found")
    uninstall_systemd_unit_template(systemd_settings)
    assert not unit.exists()


def test_replication_lag(
    instance: system.Instance, standby_instance: system.Instance
) -> None:
    with pytest.raises(TypeError, match="not a standby"):
        postgresql.replication_lag(instance)
