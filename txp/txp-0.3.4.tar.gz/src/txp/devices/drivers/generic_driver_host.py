"""
This module implements a generic driver host for devices attached physically to the gateway.
"""
# ============================ imports =========================================
import multiprocessing
from typing import List, Tuple, Dict
from txp.devices.drivers.driver import DriverState, StateReport
from txp.common.edge import EdgeDescriptor
from txp.devices.drivers.drivers_host import DriversHost
from txp.devices.drivers.thermocouple.mcp9600_driver import Mcp9600Driver
from txp.devices.package_queue import PackageQueueProxy
from txp.common.edge.device_id import DeviceId
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# _GeneralDriversRegistry internal dictionary to map usb drivers string name to the
# concrete implementation.
# ==============================================================================
_GeneralDriversRegistry: Dict = {
    Mcp9600Driver.__name__: Mcp9600Driver
}

# ==============================================================================
# GenericDriversHost
# ==============================================================================


class GenericDriversHost(DriversHost):
    """Concrete implementation of a GenericDriversHost for gateway peripherals."""

    usb_error_timeout = 10

    def __init__(
        self,
        gateway_packages_queue: PackageQueueProxy,
        drivers_state_queue: multiprocessing.Queue,
        **kwargs,
    ):
        """
        Args:
            gateway_packages_queue: The Gateway package queue to be used by Drivers
                to send collected GatewayPackages.
            **kwargs: named parameters specific to this UsbDriversHost implementation.
        """
        super(GenericDriversHost, self).__init__(
            gateway_packages_queue,
            drivers_state_queue,
            self.usb_error_timeout,
            **kwargs,
        )
        log.info("Generic driver host is ready.")

    def connect(self):
        """Connects custom drivers"""
        for d in self.drivers:
            d.connect_device()

    def disconnect(self):
        """Disconnects custom drivers"""
        for d in self.drivers:
            d.disconnect_device()

    def discover_physical_ids(self) -> List[DeviceId]:
        """Returns and empty.

        Returns:
            The List empty.
        """
        log.warning("This is a generic host for gateway peripherals which does not need to be produced (I2C, SPI,etc).")
        return list()

    def get_driver_host_name(self):
        return "Generic"

    def _add_drivers(self, edges: List[EdgeDescriptor]):
        """Adds the set of drivers for the specified edges in the host.

        Args:
            edges: List of EdgeDescriptor's for the drivers to be created in
                the host instance.
        """
        for descriptor in edges:
            edge_driver_param = descriptor.edge_parameters.get('custom_driver', None)

            if not edge_driver_param:
                log.error(f"'custom_driver' parameter not specified for edge {descriptor.logical_id} "
                          f"with type: {descriptor.device_kind}")
                log.warning(f"The edge {descriptor.logical_id} could not be created.")

            driver_class = _GeneralDriversRegistry.get(edge_driver_param, None)

            if not driver_class:
                log.error(f"custom_driver '{edge_driver_param}' specified for {descriptor.logical_id}"
                          f"is unknown to the {self.__class__.__name__}")
                return

            driver = driver_class(
                descriptor, self.gateway_package_queue, self._on_driver_state_changed,
                self._completed_driver_pulses_queue
            )
            log.debug(f'Driver created with {edge_driver_param} implementation for {descriptor.logical_id}')
            self.drivers.append(driver)

    def _change_driver_state(self, physical_id: Tuple, driver_state):
        drivers = list(
            filter(lambda driver: driver.physical_id == physical_id, self.drivers)
        )
        if len(drivers) > 0:
            driver = drivers.pop()
            if driver_state == DriverState.DISCONNECTED:
                driver.stop_sampling_windows()
            driver.update_driver_state(driver_state)
            self._add_drivers_state_to_queue(
                StateReport(driver.logical_id, driver_state)
            )
        else:
            log.error("DEVICE IS NOT IN THE CURRENT GATEWAY CONFIGURATION: {}".format(physical_id))

    def take_fix_error_action(self, serial):
        pass

    def _predicate_power_on(self, edge_logical_id: str) -> bool:
        return True
