"""
This module implements the driver host used to manage all the external USB edges devices.
"""
# ============================ imports =========================================
import multiprocessing
import pyudev
from typing import List, Tuple, Dict
from txp.devices.drivers.driver import DriverState, StateReport
from txp.common.edge import EdgeDescriptor
from txp.devices.drivers.drivers_host import DriversHost
from txp.devices.drivers.usb.usb_video_driver import UsbVideoDriver
from txp.devices.drivers.usb.usb_base_driver import UsbDriver
from txp.devices.package_queue import PackageQueueProxy
from txp.common.edge.device_id import DeviceId
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# UsbDriversRegistry internal dictionary to map usb drivers string name to the
# concrete implementation.
# ==============================================================================
_UsbDriversRegistry: Dict = {
    UsbVideoDriver.__name__: UsbVideoDriver
}


# ==============================================================================
# UsbDriversHost
# ==============================================================================


class UsbDriversHost(DriversHost):
    """Concrete implementation of a DriversHost for USB devices."""
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
        super(UsbDriversHost, self).__init__(
            gateway_packages_queue,
            drivers_state_queue,
            self.usb_error_timeout,
            **kwargs,
        )
        log.info("USB driver host is ready.")

    def connect(self):
        """Connects external USB Hub"""
        for d in self.drivers:
            d.connect_device()

    def disconnect(self):
        """Disconnects USB Hub"""
        for d in self.drivers:
            d.disconnect_device()

    def discover_physical_ids(self) -> List[DeviceId]:
        """Returns all the USB edge devices currently connected.
        TODO: Just cameras are being discovered, so far there are not other USB edge devices.

        Returns:
            The List of DeviceId.
        """
        result = list()
        context = pyudev.Context()
        for device in context.list_devices(
            subsystem="video4linux", ID_V4L_CAPABILITIES=":capture:"
        ):
            result.append(device.get("ID_PATH"))
            log.info(
                f"USB Camera {device.get('ID_VENDOR_ID')}:{device.get('ID_MODEL_ID')} found from {device.get('ID_VENDOR')}"
            )

        return result

    def get_driver_host_name(self):
        return UsbDriver.device_name()

    def _add_drivers(self, edges: List[EdgeDescriptor]):
        """Adds the set of drivers for the specified edges in the host.

        Args:
            edges: List of EdgeDescriptor's for the drivers to be created in
                the host instance.
        """
        for descriptor in edges:
            edge_driver_param = descriptor.edge_parameters.get('usb_driver', None)
            if not edge_driver_param:
                log.error(f"'usb_driver' parameter not specified for edge {descriptor.logical_id} "
                          f"with type: {descriptor.device_kind}")
                log.warning(f"The edge {descriptor.logical_id} could not be created.")

            driver_class = _UsbDriversRegistry.get(edge_driver_param, None)
            if not driver_class:
                log.error(f"usb_driver '{edge_driver_param}' specified for {descriptor.logical_id}"
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
            log.error(
                "{} DEVICE IS NOT IN THE CURRENT  GATEWAY CONFIGURATION: {}".format(
                    self.get_driver_host_name(), physical_id
                )
            )

    def take_fix_error_action(self, serial):
        pass

    def _predicate_power_on(self, edge_logical_id: str) -> bool:
        return True
