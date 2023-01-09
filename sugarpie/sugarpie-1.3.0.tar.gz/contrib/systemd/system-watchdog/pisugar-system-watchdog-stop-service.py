"""
This module is meant to be launched by a systemd service.
It turns off the PiSugar system watchdog.
It can be accompanied by its start counterpart which turns on the
system watchdog.
"""
import sys

from sugarpie.pisugar import Pisugar

pisugar = Pisugar()


def stop_system_watchdog():
    """Ask PiSugar to disable the system watchdog."""
    pisugar.switch_system_watchdog("off")


if __name__ == "__main__":
    sys.exit(stop_system_watchdog())
