"""
This module implements mcp9600 driver for a generic thermocouple.
"""
# ============================ imports =========================================

import threading
from typing import List
from txp.devices.drivers.driver import DriverState
from txp.common.edge import EdgeDescriptor

from txp.devices.package_queue import PackageQueueProxy
from txp.common.edge.perception_dimensions import TemperatureSignal
from txp.devices.drivers.driver import Driver
from txp.common.config import settings
import logging
import mcp9600
import queue

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# Thermocouple Driver Implementation.
# ==============================================================================


class Mcp9600Driver(Driver):
    """Implementation of the mcp9600 driver for a generic thermocouple.
    """

    def __init__(
            self,
            edge_descriptor: EdgeDescriptor,
            gateway_packages_queue: PackageQueueProxy,
            on_driver_state_changed: callable,
            host_clock_notification_queue: queue.Queue
    ):
        """
        Note: This Driver receives a thermocouple setup, which is added and passed down by the Gateway operative
        configuration. The physical_id is not used by the driver because is assumed tha the mcp9600 is always connected
        to the I2C bus.

        Args
            edge_descriptor: The Edge Descriptor for this Driver.
            gateway_packages_queue: The Gateway Package Queue to put produced packages.
            on_driver_state_changed: Function used to notify driver state changes.
        """
        Driver.__init__(self, edge_descriptor, gateway_packages_queue, on_driver_state_changed,
                        host_clock_notification_queue)

        self.tt = None

    def observation_pulse(self) -> int:
        return 5

    @classmethod
    def device_name(cls) -> str:
        return "Generic"

    @classmethod
    def is_virtual(cls) -> bool:
        return False

    def connect_device(self):
        """Connects to the mcp9600.
        """
        try:
            self.tt = mcp9600.MCP9600()
            self.on_driver_state_changed(
                self.logical_id, DriverState.CONNECTED
            )
        except:
            self.on_driver_state_changed(
                self.logical_id, DriverState.DISCONNECTED
            )

        #self.tt.set_thermocouple_type('K')

    def disconnect_device(self):
        """Disconnects the mcp9600 and release the handler.
        """
        log.info(f"Thermocouple disconnected: {self.logical_id}")
        self.on_driver_state_changed(
            self.logical_id, DriverState.DISCONNECTED
        )

    def _start_sampling_collect(
            self
    ) -> List["Signals"]:
        """Collects the signals from the camera and generates the packages for the gateway.

        This method should collect samples that belong to the defined Sampling Time.

        Args:
            sampling_time_finished: event to check when the sampling time has finished.
        Returns:
            A list of ImageSignal collected by the mcp9600.
        """
        signals = []

        temperature = self.tt.get_hot_junction_temperature()

        if temperature is not None:
            signal = TemperatureSignal.build_signal_from_value(
                temperature,
                0
            )
            signals.append(signal)
        else:
            log.error('Error reading thermocouple connected mcp9600 ')

        return signals

    def _stop_sampling_collect(self):
        """This method will stop the sampling collection in the driver implementation.
        """
        pass
