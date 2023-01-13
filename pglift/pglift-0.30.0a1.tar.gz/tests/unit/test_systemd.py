import logging
from pathlib import Path
from unittest.mock import patch

import pytest

from pglift import systemd
from pglift.settings import Settings, SystemdSettings


def test_executeas() -> None:
    with patch("shutil.which", return_value=True) as which:
        s = Settings.parse_obj({"systemd": {"user": True}})
    which.assert_called_once_with("systemctl")
    assert systemd.executeas(s) == ""

    with patch("shutil.which", return_value=True) as which:
        s = Settings.parse_obj(
            {"systemd": {"user": False}, "sysuser": ["postgres", "pgsql"]}
        )
    which.assert_called_once_with("systemctl")
    assert systemd.executeas(s) == "User=postgres\nGroup=pgsql"


def test_systemctl() -> None:
    settings = SystemdSettings()
    assert systemd.systemctl(settings, "user") == ["systemctl", "--user", "user"]

    settings = SystemdSettings(user=False)
    assert systemd.systemctl(settings, "root") == ["systemctl", "--system", "root"]

    settings = SystemdSettings(user=False, sudo=True)
    assert systemd.systemctl(settings, "sudoer") == [
        "sudo",
        "systemctl",
        "--system",
        "sudoer",
    ]


def test_install_uninstall(tmp_path: Path) -> None:
    logger = logging.getLogger(__name__)
    systemd.install("foo", "ahah", tmp_path, logger=logger)
    unit_path = tmp_path / "foo"
    mtime = unit_path.stat().st_mtime
    assert unit_path.read_text() == "ahah"
    systemd.install("foo", "ahah", tmp_path, logger=logger)
    assert unit_path.stat().st_mtime == mtime
    with pytest.raises(FileExistsError, match="not overwriting"):
        systemd.install("foo", "ahahah", tmp_path, logger=logger)
    systemd.uninstall("foo", tmp_path, logger=logger)
    assert not unit_path.exists()
    systemd.uninstall("foo", tmp_path, logger=logger)  # no-op
