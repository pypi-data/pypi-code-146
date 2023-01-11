"""
This module implements a DriversHost for the ArmRobotDriver.
"""

# ============================ imports =========================================
import multiprocessing
from typing import Tuple, List

from txp.devices.drivers.arm_robot.arm_controller import ArmController
from txp.devices.drivers.arm_robot.arm_handler import ArmHandler
from txp.devices.drivers.arm_robot.thermal_robot import ThermalRobotDriver
from txp.devices.drivers.driver import StateReport, DriverState
from txp.devices.drivers.drivers_host import DriversHost
from txp.common.edge import EdgeDescriptor
from txp.devices.package_queue import PackageQueueProxy

from txp.devices.drivers.arm_robot.robot_driver import ArmRobotDriver
from txp.common.edge import DeviceId
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# RobotDriversHost is the Host for mock drivers used in unit testing.
# ==============================================================================
class RobotDriversHost(DriversHost):
    # Value requested by the super class
    _driver_errored_timeout_seconds = 15

    def __init__(self, gateway_packages_queue: PackageQueueProxy,
                 drivers_state_queue: multiprocessing.Queue, **kwargs):
        """
        Args:
            gateway_packages_queue: The Gateway package queue to be used by Drivers
                to send collected GatewayPackages.
            drivers_state_queue: The queue provided by the Devices Manager to queue
                drivers states reports.
        """
        super(RobotDriversHost, self).__init__(gateway_packages_queue, drivers_state_queue,
                                               self._driver_errored_timeout_seconds)

        self._actuator_edge_decriptor: EdgeDescriptor = None
        self._drivers_edges_descriptor: List[EdgeDescriptor] = []
        self._arm_controller = None

    @staticmethod
    def get_driver_host_name():
        return ArmRobotDriver.device_name()

    def discover_physical_ids(self) -> List[DeviceId]:
        log.debug(f"{self.__class__.__name__} does not detect devices yet.")
        return []

    def connect(self):
        for driver in self.drivers:
            if driver._robotic_arm_controller is None:
                driver._robotic_arm_controller = self._arm_controller
            driver.connect_device()
            log.debug("connecting driver {}".format(driver.logical_id))

    def disconnect(self):
        if self._arm_controller is not None:
            self._arm_controller.disconnect()
            self._arm_controller = None
        for driver in self.drivers:
            driver.disconnect_device()

    def _add_drivers(self, edges: List[EdgeDescriptor]):
        for descriptor in edges:
            if descriptor.is_actuator_device():
                self._actuator_edge_decriptor = descriptor
                if self._arm_controller is None:
                    self._arm_controller = ArmController(descriptor)
                    log.info("{} arm controller instantiated".format(descriptor.logical_id))
            else:
                self._drivers_edges_descriptor.append(descriptor)
                log.info("{} instantiating virtual driver".format(descriptor.logical_id))
                driver = ArmRobotDriver(descriptor, self.gateway_package_queue,self._change_driver_state_callback,
                                        self._arm_controller, self._completed_driver_pulses_queue)
                self.drivers.append(driver)

    def _change_driver_state_callback(self, logical_id: str, driver_state: DriverState):
        driver = list(filter(lambda driver: driver.logical_id == logical_id, self.drivers)).pop()
        driver.update_driver_state(driver_state)
        self._add_drivers_state_to_queue(StateReport(driver.logical_id, driver_state,
                                                     driver_context=driver._driver_context))

    def is_actuator_device(self, logical_id: str) -> bool:
        return logical_id == self._actuator_edge_decriptor.logical_id

    def take_fix_error_action(self, serial):
        pass

    def _predicate_power_on(self, edge_logical_id: str) -> bool:
        return True


class ThermalArmHost(RobotDriversHost):
    def __init__(self, gateway_packages_queue: PackageQueueProxy,
                 drivers_state_queue: multiprocessing.Queue, **kwargs):
        super(ThermalArmHost, self).__init__(gateway_packages_queue, drivers_state_queue)

    @staticmethod
    def get_driver_host_name():
        return ThermalRobotDriver.device_name()

    def _add_drivers(self, edges: List[EdgeDescriptor]):
        for descriptor in edges:
            if descriptor.is_actuator_device():
                self._actuator_edge_decriptor = descriptor
                if self._arm_controller is None:
                    self._arm_controller = ArmController(descriptor)
                    log.info("{} arm controller instantiated".format(descriptor.logical_id))
            else:
                self._drivers_edges_descriptor.append(descriptor)
                log.info("{} instantiating virtual driver".format(descriptor.logical_id))
                driver = ThermalRobotDriver(descriptor, self.gateway_package_queue,self._change_driver_state_callback,
                                        self._arm_controller, self._completed_driver_pulses_queue)
                self.drivers.append(driver)

    def _predicate_power_on(self, edge_logical_id: str) -> bool:
        return True
