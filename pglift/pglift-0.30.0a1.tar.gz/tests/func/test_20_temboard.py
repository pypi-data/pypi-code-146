import json
from pathlib import Path
from typing import Iterator, Optional

import pytest
import requests
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from pglift import instances, postgresql, systemd
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.systemd import service_manager
from pglift.temboard import impl as temboard
from pglift.temboard import models

from . import reconfigure_instance


@pytest.fixture(scope="session", autouse=True)
def _temboard_available(temboard_execpath: Optional[Path]) -> None:
    if not temboard_execpath:
        pytest.skip("temboard not available")


def test_configure(
    ctx: Context,
    temboard_password: str,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    tmp_port_factory: Iterator[int],
) -> None:
    temboard_settings = temboard.get_settings(ctx.settings)
    configpath = Path(str(temboard_settings.configpath).format(name=instance.qualname))
    assert configpath.exists()
    lines = configpath.read_text().splitlines()
    assert "user = temboardagent" in lines
    assert f"port = {instance.port}" in lines
    assert f"password = {temboard_password}" in lines

    home_dir = Path(str(temboard_settings.home).format(name=instance.qualname))
    assert home_dir.exists()

    assert temboard._ssl_cert_file(instance.qualname, temboard_settings).exists()
    assert temboard._ssl_key_file(instance.qualname, temboard_settings).exists()

    new_port = next(tmp_port_factory)
    with reconfigure_instance(ctx, instance_manifest, port=new_port):
        lines = configpath.read_text().splitlines()
        assert f"port = {new_port}" in lines


@retry(reraise=True, wait=wait_fixed(2), stop=stop_after_attempt(5))
def request_agent(port: int) -> requests.Response:
    return requests.get(f"https://0.0.0.0:{port}/discover", verify=False)


def test_start_stop(ctx: Context, instance: system.Instance) -> None:
    service = instance.service(models.Service)
    port = service.port
    if ctx.settings.service_manager == "systemd":
        assert systemd.is_enabled(
            ctx, service_manager.unit("temboard_agent", instance.qualname)
        )

    if ctx.settings.service_manager == "systemd":
        assert systemd.is_active(
            ctx, service_manager.unit("temboard_agent", instance.qualname)
        )
    try:
        r = request_agent(port)
    except requests.ConnectionError as e:
        raise AssertionError(f"HTTPS connection failed: {e}") from None
    r.raise_for_status()
    assert r.ok
    output = r.text
    output_json = json.loads(output)
    assert output_json["postgres"]["port"] == instance.port

    with instances.stopped(ctx, instance):
        if ctx.settings.service_manager == "systemd":
            assert not systemd.is_active(
                ctx, service_manager.unit("temboard_agent", instance.qualname)
            )
        with pytest.raises(requests.ConnectionError):
            request_agent(port)


def test_standby(
    ctx: Context,
    temboard_password: str,
    standby_instance: system.Instance,
) -> None:
    temboard_settings = temboard.get_settings(ctx.settings)
    service = standby_instance.service(models.Service)
    port = service.port
    assert service.password and service.password.get_secret_value() == temboard_password
    configpath = Path(
        str(temboard_settings.configpath).format(name=standby_instance.qualname)
    )
    assert configpath.exists()
    assert postgresql.is_running(ctx, standby_instance)

    if ctx.settings.service_manager == "systemd":
        assert systemd.is_active(
            ctx,
            service_manager.unit("temboard_agent", standby_instance.qualname),
        )
    try:
        r = request_agent(port)
    except requests.ConnectionError as e:
        raise AssertionError(f"HTTPS connection failed: {e}") from None
    r.raise_for_status()
    assert r.ok
    output = r.text
    output_json = json.loads(output)
    assert output_json["postgres"]["port"] == standby_instance.port
