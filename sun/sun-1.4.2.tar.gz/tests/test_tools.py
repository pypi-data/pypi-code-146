import subprocess
from sun.cli.tool import check_updates, daemon_status


def test_check_updates():
    message, packages = check_updates()
    if len(packages) == 0:
        assert message == 'No news is good news!'


def test_daemon_status():
    out = subprocess.getoutput('ps -a')
    if 'sun_daemon' in out:
        assert 'SUN is running...' == daemon_status()
    else:
        assert 'SUN not running' == daemon_status()
