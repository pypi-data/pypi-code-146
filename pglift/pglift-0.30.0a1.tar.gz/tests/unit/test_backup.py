import re

from pglift.backup import install_systemd_unit_template, uninstall_systemd_unit_template
from pglift.settings import Settings, SystemdSettings


def test_install_systemd_unit_template(
    settings: Settings, systemd_settings: SystemdSettings
) -> None:
    install_systemd_unit_template(settings, systemd_settings, env="X-DEBUG=no")
    service_unit = systemd_settings.unit_path / "pglift-backup@.service"
    assert service_unit.exists()
    service_lines = service_unit.read_text().splitlines()
    for line in service_lines:
        if line.startswith("ExecStart"):
            execstart = line.split("=", 1)[-1]
            assert re.match(r"^.+/python(3(.[0-9]*)?)? -m pglift.backup %i$", execstart)
            break
    else:
        raise AssertionError("ExecStart line not found")
    assert "Environment=X-DEBUG=no" in service_lines
    timer_unit = systemd_settings.unit_path / "pglift-backup@.timer"
    assert timer_unit.exists()
    timer_lines = timer_unit.read_text().splitlines()
    assert "OnCalendar=daily" in timer_lines
    uninstall_systemd_unit_template(systemd_settings)
