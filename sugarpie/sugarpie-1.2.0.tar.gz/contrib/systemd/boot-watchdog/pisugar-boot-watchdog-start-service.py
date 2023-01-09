"""
This module is meant to be launched by a systemd service.
It turns the PiSugar boot watchdog on and then resets it on boot.
It can be accompanied by its stop counterpart which turns off the boot
watchdog.
"""
import sys

from sugarpie.pisugar import Pisugar

pisugar = Pisugar()


def start_boot_watchdog():
    """
    Reset the boot watchdog, in case it was already on during the present
    boot. If it was off, then resetting it has no effect anyway.
    Then ask the PiSugar to enable the boot watchdog to make sure it is ready
    for the next boot. If it was already on, then it will stay on.
    """
    pisugar.reset_boot_watchdog()
    pisugar.switch_boot_watchdog("on")


if __name__ == "__main__":
    sys.exit(start_boot_watchdog())
