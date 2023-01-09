"""Module for the class that implements the controller for the PiSugar."""
import logging

from .constants import Constants
from .helpers import connection_to_i2c, pisugar_get_address, pisugar_set_bit

constants = Constants


class Pisugar:
    """Implements the various controls of the PiSugar."""

    def _set_system_watchdog_timeout(self, timeout=30) -> None:
        """Set the system watchdog timeout in seconds."""
        timeout //= 2  # the pisugar needs timeout divided by 2

        with connection_to_i2c() as i2c:
            i2c.write_byte_data(
                constants.PISUGAR_I2C_ADDRESS,
                constants.SYSTEM_WATCHDOG_TIMEOUT_ADDRESS,
                timeout,
            )

    def switch_system_watchdog(self, switch: str, timeout=30) -> None:
        """
        Turn the system watchdog on or off.
        Set the system watchdog timeout when turning on.

        Args:
            switch: A string, on or off.
            timeout: int, watchdog timeout in seconds.
        """
        if switch == "on":
            self._set_system_watchdog_timeout(timeout)
        pisugar_set_bit(
            constants.WATCHDOG_ADDRESS,
            constants.SYSTEM_WATCHDOG_SWITCH_BIT_INDEX,
            switch,
        )

    def reset_system_watchdog(self) -> None:
        """Tell the PiSugar to reset the system watchdog."""
        try:
            pisugar_set_bit(
                constants.WATCHDOG_ADDRESS,
                constants.SYSTEM_WATCHDOG_RESET_BIT_INDEX,
                "on",
            )
        except OSError:
            logging.error("This error is expected.", exc_info=True)

    def _set_boot_watchdog_max_retries(self, retries=5) -> None:
        """
        Set the maximum restarts of the system before stopping
        to retry to boot.
        """
        with connection_to_i2c() as i2c:
            i2c.write_byte_data(
                constants.PISUGAR_I2C_ADDRESS,
                constants.BOOT_WATCHDOG_MAX_RETRIES_ADDRESS,
                retries,
            )

    def switch_boot_watchdog(self, switch: str, retries=5) -> None:
        """
        Switch the boot watchdog on or off.

        The boot watchdog timeout is not configurable and
        is set to 1 minute and 30 seconds.

        Args:
            switch: A string, on or off.
            retries: int, maximum system restarts before stopping.
        """
        if switch == "on":
            self._set_boot_watchdog_max_retries(retries)
        pisugar_set_bit(
            constants.WATCHDOG_ADDRESS,
            constants.BOOT_WATCHDOG_SWITCH_BIT_INDEX,
            switch,
        )

    def reset_boot_watchdog(self) -> None:
        """Tell the PiSugar to reset the boot watchdog."""
        pisugar_set_bit(
            constants.WATCHDOG_ADDRESS,
            constants.BOOT_WATCHDOG_RESET_BIT_INDEX,
            "on",
        )

    def _set_switch_power_output_off_delay(self, delay: int) -> None:
        """
        Set the delay for the power output switch off.

        Args:
            delay: int, number of seconds to wait before cutting
            power. Must be in range 0-255.
        """
        with connection_to_i2c() as i2c:
            i2c.write_byte_data(
                constants.PISUGAR_I2C_ADDRESS,
                constants.POWER_OUTPUT_SWITCH_DELAY_ADDRESS,
                delay,
            )

    def switch_power_output_off(self, delay=0) -> None:
        """
        Switch off the power output to the Raspberry Pi.

        Turn off the 5 volts power to the Raspberry Pi,
        immediately or after an optional delay.
        The power output will be turned on again when the power
        button is pressed.

        Args:
            delay: int, number of seconds to wait before cutting
            power. Must be in range 0-255.
        """
        self._set_switch_power_output_off_delay(delay)
        pisugar_set_bit(
            constants.POWER_ADDRESS,
            constants.POWER_OUTPUT_SWITCH_BIT,
            "off",
        )

    def get_temperature(self) -> int:
        """
        Get the temperature of the PiSugar chip, in celsius.

        The range of temperatures is between -40 and 85 degrees
        celsius. This is a limitation of the PiSugar itself.
        """
        temperature = pisugar_get_address(constants.TEMPERATURE_ADDRESS)
        # The PiSugar returns 40 degrees as 0
        temperature = temperature - 40
        return temperature

    def get_firmware_version(self) -> str:
        """
        Get the PiSugar firmware version.

        It is extracted as ASCII encoded from the firmware
        version address and the subsequent adresses.

        Returns:
            string: the firmware version formatted like so vx.x.x

        Example:
            >>> pisugar.get_firmware_version()
            >>> v1.3.4
        """
        firmware_version = ""
        for i in range(0, constants.FIRMWARE_VERSION_LENGTH):
            character = pisugar_get_address(
                constants.FIRMWARE_VERSION_START_ADDRESS + i
            )
            if character != 0:
                character = chr(character)
                firmware_version = firmware_version + character
        return firmware_version
