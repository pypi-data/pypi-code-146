import os
import platform


def execute_cmd(cmd: str):
    return os.system(cmd)


def restart_os():
    cmd = 'shutdown -r -f -t 0' if platform.system().lower() == 'windows' else 'reboot'
    return execute_cmd(cmd)
