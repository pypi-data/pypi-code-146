"""
This module implements the driver host used to manage voyager 3 devices through
the USB smartmesh dongle.
"""
# ============================ imports =========================================
import multiprocessing
from typing import Tuple, List

from txp.devices.drivers.driver import StateReport, DriverState
from txp.devices.drivers.drivers_host import DriversHost
from txp.common.edge import EdgeDescriptor
from txp.devices.package_queue import PackageQueueProxy

from txp.devices.drivers.voyager.smartmesh_dongle import SmartMeshDongle
from txp.devices.drivers.voyager.voyager_driver import VoyagerDriver
from txp.common.edge import DeviceId
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# VoyagerDriversHost
# ==============================================================================
class VoyagerDriversHost(DriversHost):
    """Concrete implementation of a DriversHost for Voyager edge_descriptors.

    This class is executed as a separated process, and it's responsible for:
        - Start the SmartMeshDongle as smartmesh manager for the motes registered.
        - Host the configured Voyager Drivers for the connected device.
    """
    voyager_driver_errored_timeout_seconds = 240

    def __init__(self, gateway_packages_queue: PackageQueueProxy,drivers_state_queue: multiprocessing.Queue,**kwargs):
        """
        Args:
            gateway_packages_queue: The Gateway package queue to be used by Drivers
                to send collected GatewayPackages.
            **kwargs: named parameters specific to this VoyagerDriversHost implementation.
        """
        super(VoyagerDriversHost, self).__init__(gateway_packages_queue,drivers_state_queue,self.voyager_driver_errored_timeout_seconds,**kwargs)
        log.info("Initialization process of a VoyagerDriversHost")
        self._smartmesh_manager = SmartMeshDongle(self._change_driver_state)

        # Detect the SmartMesh device.
        try:
            log.info("Detecting SmartMesh manager device")
            detected = self._smartmesh_manager.detect()
            if detected:
                log.info("SmartMesh manager device detected.")
            else:
                log.info("SmartMesh manager device not detected.")
        except Exception as e:
            log.error(f"Exception detecting SmartMesh device: {e}")

    def connect(self):
        """Connects the Voyager 3 Dongle unit"""
        try:
            self._smartmesh_manager.connect()
        except Exception as e:
            log.error(f"Exception connecting smartmesh devices: {e}")

        if not self._smartmesh_manager.connected:
            raise Exception("Host failed to initiailze connection with the device.")

    def disconnect(self):
        """Disconnects the Voyager 3 dongle unit"""
        self._smartmesh_manager.disconnect()

    def discover_physical_ids(self) -> List[DeviceId]:
        """Returns the set of found DeviceId in the smartmesh network.

        Returns:
            The List of DeviceId.
        """
        result = list()

        for mac in self._smartmesh_manager.operational_macs:
            dev_id = DeviceId("", SmartMeshDongle.pretty_mac(mac))
            result.append(dev_id)

        print(result)

        return result

    def get_driver_host_name(self):
        return VoyagerDriver.device_name()

    def _add_drivers(self, edges: List[EdgeDescriptor]):
        """Adds the set of drivers for the specified edges in the host.

        Args:
            edges: List of EdgeDescriptor's for the drivers to be created in
                the host instance.
        """
        for descriptor in edges:
            driver = VoyagerDriver(descriptor, self.gateway_package_queue, self._smartmesh_manager,
                                   self._on_driver_state_changed, self._completed_driver_pulses_queue)
            self.drivers.append(driver)

    #TODO: this has to be changed. This method will be putted in base class and physical_id in this case is named mac will be standardized for both drivers since thi code
    # is being repeated in both hosts. same internal content.
    def _change_driver_state(self, mac: Tuple, driver_state):
        drivers = list(filter(lambda driver : driver.mac == mac,self.drivers))
        if len(drivers) > 0:
            driver = drivers.pop()
            if driver_state == DriverState.DISCONNECTED:
                driver.stop_sampling_windows()
            driver.update_driver_state(driver_state)
            self._add_drivers_state_to_queue(StateReport(driver.logical_id, driver_state))
        else:
            log.error("{} DEVICE IS NOT IN THE CURRENT  GATEWAY CONFIGURATION. ILLEGAL CONNECTION FROM SERIAL {}".format(self.get_driver_host_name(),mac))

    def take_fix_error_action(self, serial):
        pass

    def _predicate_power_on(self, edge_logical_id: str) -> bool:
        return True

