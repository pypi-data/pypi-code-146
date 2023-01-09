"This modules defines the PiSugar constants."
from dataclasses import dataclass


@dataclass(frozen=True)
class Constants:
    """
    Adresses and bit indexes found in the PiSugar
    documentation.
    Bit indexes start with 0, on the least significant bit.
    """

    RPI_I2C_BUS = 1
    PISUGAR_I2C_ADDRESS = 0x57
    WATCHDOG_ADDRESS = 0x06
    SYSTEM_WATCHDOG_SWITCH_BIT_INDEX = 7
    SYSTEM_WATCHDOG_RESET_BIT_INDEX = 5
    SYSTEM_WATCHDOG_TIMEOUT_ADDRESS = 0x07
    BOOT_WATCHDOG_RESET_BIT_INDEX = 3
    BOOT_WATCHDOG_SWITCH_BIT_INDEX = 4
    BOOT_WATCHDOG_MAX_RETRIES_ADDRESS = 0x0A
    POWER_ADDRESS = 0x02
    POWER_OUTPUT_SWITCH_BIT = 5
    POWER_OUTPUT_SWITCH_DELAY_ADDRESS = 0x09
    TEMPERATURE_ADDRESS = 0x04
