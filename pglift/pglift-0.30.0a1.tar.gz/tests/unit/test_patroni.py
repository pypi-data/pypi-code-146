import logging
from pathlib import Path
from typing import Type
from unittest.mock import patch

import pydantic
import pytest
import yaml
from click.testing import CliRunner

from pglift import exceptions, instances
from pglift.cli import CLIContext, Obj
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.patroni import (
    configure_postgresql,
    impl,
    install_systemd_unit_template,
    instance_env,
    models,
    uninstall_systemd_unit_template,
)
from pglift.patroni.cli import cli as cli
from pglift.settings import PatroniSettings, Settings, SystemdSettings

from . import click_result_traceback


@pytest.fixture
def patroni_settings(settings: Settings) -> PatroniSettings:
    assert settings.patroni
    return settings.patroni


@pytest.fixture
def instance_manifest(
    composite_instance_model: Type[interface.Instance],
) -> interface.Instance:
    return composite_instance_model.parse_obj(
        {
            "name": "test",
            "version": "11",
            "data_checksums": True,
            "settings": {
                "shared_buffers": "257MB",
                "effective_cache_size": "4 GB",
                "unix_socket_directories": "/tmp/tests",
                "log_connections": "on",
                "log_disconnections": "false",
                "log_checkpoints": True,
                "log_min_duration_statement": "3s",
                "shared_preload_libraries": "passwordcheck",
            },
            "surole_password": None,
            "replrole_password": "rrr",
            "patroni": {"cluster": "whatever"},
            "pgbackrest": {"stanza": "ha"},
        }
    )


@pytest.fixture
def instance(
    datadir: Path, patroni_settings: PatroniSettings, instance: system.Instance
) -> system.Instance:
    patroni_config = impl._configpath(instance.qualname, patroni_settings)
    patroni_config.parent.mkdir(parents=True, exist_ok=True)
    patroni_config.write_text((datadir / "patroni.yaml").read_text())
    patroni = models.Service(cluster="test-scope", node="pg1")
    instance.services.append(patroni)
    return instance


def test_available(settings: Settings) -> None:
    assert impl.available(settings)


def test_install_systemd_unit_template(
    settings: Settings, systemd_settings: SystemdSettings, patroni_execpath: Path
) -> None:
    install_systemd_unit_template(settings, systemd_settings)
    unit = systemd_settings.unit_path / "pglift-patroni@.service"
    assert unit.exists()
    lines = unit.read_text().splitlines()
    assert (
        f"ExecStart={patroni_execpath} {settings.prefix}/etc/patroni/%i.yaml" in lines
    )
    uninstall_systemd_unit_template(settings, systemd_settings)
    assert not unit.exists()


def test_patroni_incompatible_with_standby(
    composite_instance_model: Type[interface.Instance],
) -> None:
    with pytest.raises(pydantic.ValidationError):
        composite_instance_model.parse_obj(
            {
                "name": "invalid",
                "standby": {"primary_conninfo": "port=5444"},
                "patroni": {"cluster": "tests"},
            }
        )


@pytest.fixture
def patroni(
    ctx: Context,
    settings: Settings,
    instance: system.Instance,
    instance_manifest: interface.Instance,
) -> models.Patroni:
    m = instance_manifest._copy_validate(
        {
            "data_checksums": True,
            "surole_password": None,
            "replrole_password": "rrr",
        }
    )
    configuration = instances.configuration(ctx, instance_manifest, instance)
    with patch(
        "socket.gethostbyname",
        side_effect=AssertionError("gethostbyname unexpectedly called"),
    ):
        p = models.Patroni.build(
            "pghost.test",
            instance,
            m,
            configuration,
            scope="test-scope",
            name="pg1",
            restapi={"connect_address": "localhost:8080"},
            etcd3={
                "hosts": ["server:123"],
                "protocol": "https",
                "cacert": "/path/to/cacert.pem",
                "cert": "/path/to/host.pem",
                "key": "/path/to/host.key",
            },
            watchdog={
                "mode": "required",
                "device": "/dev/watchdog",
                "safety_margin": 5,
            },
        )
    return p


def test_yaml(patroni: models.Patroni, datadir: Path, write_changes: bool) -> None:
    patroni = patroni.copy(
        update={
            "postgresql": patroni.postgresql.copy(
                update={
                    "bin_dir": ".",
                    "data_dir": Path("test-datadir"),
                }
            ),
        }
    )
    doc = patroni.yaml()
    fpath = datadir / "patroni.yaml"
    if write_changes:
        fpath.write_text(doc)
    expected = fpath.read_text()
    assert doc == expected


def test_validate_config(
    patroni: models.Patroni,
    patroni_settings: PatroniSettings,
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING):
        impl.validate_config(patroni.yaml(), patroni_settings)
    (msg,) = caplog.messages
    assert msg.strip() == "invalid Patroni configuration: test test test"


def test_maybe_backup_config(
    instance: system.Instance,
    patroni_settings: "PatroniSettings",
    caplog: pytest.LogCaptureFixture,
) -> None:
    with patch.object(
        impl,
        "cluster_members",
        return_value=[
            models.ClusterMember(
                host="h", name="node", port=8097, role="leader", state="s"
            )
        ],
    ):
        with caplog.at_level("WARNING", logger="pglift.patroni"):
            impl.maybe_backup_config(
                instance.qualname, node="node", cluster="clu", settings=patroni_settings
            )
    assert (
        "'node' appears to be the last member of cluster 'clu', saving Patroni configuration file"
        in caplog.messages[0]
    )
    backuppath = next((patroni_settings.configpath.parent.glob("clu-node*.yaml")))
    backupconfig = yaml.safe_load(backuppath.read_text())
    assert backupconfig["etcd3"] == {
        "cacert": "/path/to/cacert.pem",
        "cert": "/path/to/host.pem",
        "hosts": ["server:123"],
        "key": "/path/to/host.key",
        "protocol": "https",
    }


def test_postgresql_service_name(ctx: Context, instance: system.Instance) -> None:
    assert ctx.hook.postgresql_service_name(ctx=ctx, instance=instance) == "patroni"


def test_postgresql_editable_conf(ctx: Context, instance: system.Instance) -> None:
    assert (
        ctx.hook.postgresql_editable_conf(ctx=ctx, instance=instance)
        == "\n".join(
            [
                "archive_command = '/usr/bin/pgbackrest --config-path=/cfg/pgbackrest --stanza=ha archive-push %p'",
                "archive_mode = on",
                "cluster_name = 'test'",
                "effective_cache_size = '4 GB'",
                "lc_messages = 'C'",
                "lc_monetary = 'C'",
                "lc_numeric = 'C'",
                "lc_time = 'C'",
                "log_checkpoints = on",
                "log_connections = on",
                "log_destination = 'stderr'",
                "log_disconnections = off",
                "log_min_duration_statement = '3s'",
                "logging_collector = on",
                "port = 5432",
                "shared_buffers = '257MB'",
                "shared_preload_libraries = 'passwordcheck, pg_qualstats, pg_stat_statements, pg_stat_kcache'",
                "unix_socket_directories = '/tmp/tests'",
                "wal_level = 'replica'",
            ]
        )
        + "\n"
    )


def test_configure_postgresql(
    ctx: Context,
    patroni_settings: PatroniSettings,
    instance_manifest: interface.Instance,
    instance: system.Instance,
) -> None:
    instance_manifest.settings["work_mem"] = "8MB"
    pgconfig = instances.configuration(ctx, instance_manifest, instance)
    patroni = impl.config(instance.qualname, patroni_settings)
    postgresql_parameters = patroni.postgresql.parameters.copy()
    assert "work_mem" not in postgresql_parameters
    postgresql_parameters["work_mem"] = "8MB"
    with patch.object(impl, "api_request") as api_request:
        changes = configure_postgresql(ctx, instance_manifest, pgconfig, instance)
    assert changes == {"work_mem": (None, "8MB")}
    (p, verb, endpoint), _ = api_request.call_args
    assert (verb, endpoint) == ("POST", "reload")
    assert p.postgresql.parameters == postgresql_parameters


def test_env(ctx: Context, instance: system.Instance, pg_version: str) -> None:
    assert instance_env(ctx, instance) == {
        "PATRONICTL_CONFIG_FILE": f"{ctx.settings.prefix}/etc/patroni/{pg_version}-test.yaml",
        "PATRONI_NAME": "pg1",
        "PATRONI_SCOPE": "test-scope",
    }


def test_api_request(patroni: models.Patroni) -> None:
    with patch("requests.request") as request:
        impl.api_request(patroni, "GET", "readiness")
    request.assert_called_once_with("GET", "http://localhost:8080/readiness")


def test_check_api_status(settings: Settings, instance: system.Instance) -> None:
    assert settings.patroni
    assert not impl.check_api_status(instance.qualname, settings.patroni)


def test_promote_postgresql(ctx: Context, instance: system.Instance) -> None:
    assert ctx.settings.patroni
    with pytest.raises(exceptions.UnsupportedError):
        ctx.hook.promote_postgresql(ctx=ctx, instance=instance)


def test_cli_patroni_logs(settings: Settings, instance: system.Instance) -> None:
    runner = CliRunner()
    ctx = CLIContext(settings=settings)
    obj = Obj(context=ctx)
    with patch.object(impl, "logs", return_value=["l1\n", "l2\n"]) as logs:
        result = runner.invoke(cli, ["-i", str(instance), "logs"], obj=obj)
    assert result.exit_code == 0, click_result_traceback(result)
    logs.assert_called_once_with(instance.qualname, ctx.settings.patroni)
    assert result.output == "l1\nl2\n"


def test_preserve_configuration_edits(
    ctx: Context,
    patroni_settings: PatroniSettings,
    instance: system.Instance,
    instance_manifest: interface.Instance,
) -> None:
    svc = models.ServiceManifest(cluster="test-scope", node="pg1")

    configpath = impl._configpath(instance.qualname, patroni_settings)
    config = yaml.safe_load(configpath.read_text())
    config["bootstrap"]["dcs"]["loop_wait"] = 42

    # Add an unmanaged "extra" field.
    config["restapi"]["verify_client"] = "required"

    # PostgreSQL settings only defined in actual Patroni configuration file
    # are preserved.
    assert "work_mem" not in config["postgresql"]["parameters"]
    config["postgresql"]["parameters"]["work_mem"] = "16MB"
    with configpath.open("w") as f:
        yaml.safe_dump(config, f)
    m = instance_manifest._copy_validate(update={"port": 5467})
    configuration = instances.configuration(ctx, m, instance)
    with impl.setup(
        ctx, instance, m, svc, patroni_settings, configuration, validate=True
    ) as patroni:
        p = patroni.dict()
        assert p["bootstrap"]["dcs"]["loop_wait"] == 42
        assert p["restapi"]["verify_client"] == "required"
        assert patroni.postgresql.parameters["work_mem"] == "16MB"
        assert patroni.postgresql.parameters["port"] == 5467
        assert patroni.postgresql.listen == "*:5467"
    config = yaml.safe_load(configpath.read_text())
    assert config["postgresql"]["parameters"]["work_mem"] == "16MB"

    # PostgreSQL settings from instance manifest take precedence over those
    # defined in actual Patroni configuration file.
    configuration["work_mem"] = "42kB"
    with impl.setup(
        ctx, instance, m, svc, patroni_settings, configuration, validate=True
    ) as patroni:
        assert patroni.postgresql.parameters["work_mem"] == "42kB"
    config = yaml.safe_load(configpath.read_text())
    assert config["postgresql"]["parameters"]["work_mem"] == "42kB"
