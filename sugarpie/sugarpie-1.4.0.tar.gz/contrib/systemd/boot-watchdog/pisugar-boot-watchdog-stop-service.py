"""
This module is meant to be launched by a systemd service.
It turns off the PiSugar boot watchdog.
It can be accompanied by its start counterpart which turns on the
boot watchdog.
"""
import sys

from sugarpie.pisugar import Pisugar

pisugar = Pisugar()


def stop_boot_watchdog():
    """Ask PiSugar to disable the boot watchdog."""
    pisugar.switch_boot_watchdog("off")


if __name__ == "__main__":
    sys.exit(stop_boot_watchdog())
