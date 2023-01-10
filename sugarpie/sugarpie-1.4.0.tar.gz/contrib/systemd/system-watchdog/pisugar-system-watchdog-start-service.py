"""
This module is meant to be launched by a systemd service.
It turns the PiSugar system watchdog on and then resets it until it is stopped.
It can be accompanied by its stop counterpart which turns off the system
watchdog.
"""
import sys
import time

from sugarpie.pisugar import Pisugar

pisugar = Pisugar()


def start_system_watchdog():
    """Ask the PiSugar to enable the system watchdog and reset it forever."""
    pisugar.switch_system_watchdog("on")

    while True:
        pisugar.reset_system_watchdog()
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(start_system_watchdog())
