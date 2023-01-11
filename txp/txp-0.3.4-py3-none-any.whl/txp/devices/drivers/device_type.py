"""
This module implements an enumerated registry of known devices and their
driver implementation.
"""
from enum import Enum

from txp.devices.drivers.arm_robot.thermal_robot import ThermalRobotDriver
from txp.devices.drivers.icomox.icomox_driver import IcomoxDriver
from txp.devices.drivers.icomox.icomox_driver_host import IcomoxDriversHost
from txp.devices.drivers.mock.mock_driver import MockDriver, MockDriversHost
from txp.devices.drivers.voyager.voyager_driver import VoyagerDriver
from txp.devices.drivers.voyager.voyager_driver_host import VoyagerDriversHost
from txp.devices.drivers.usb.usb_base_driver import UsbDriver
from txp.devices.drivers.usb.usb_driver_host import UsbDriversHost
from txp.devices.drivers.thermocouple.mcp9600_driver import Mcp9600Driver
from txp.devices.drivers.generic_driver_host import GenericDriversHost
from txp.devices.drivers.arm_robot.robot_driver import ArmRobotDriver
from txp.devices.drivers.arm_robot.robot_host import RobotDriversHost, ThermalArmHost
from txp.devices.drivers.driver import Driver
from txp.devices.drivers.drivers_host import DriversHost
from txp.devices.package_queue import PackageQueueProxy
from multiprocessing.managers import BaseManager
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Enumeration for the known communication device drivers.
# ==============================================================================
class DeviceType(Enum):
    """Enumeration registry for the different types of defined driver implementations.
    The _value_ for the enumeration is the name of the device defined by each driver
    with the class method device_name().

    The registry contains for each value:
        - The Driver class for the device.
        - The DriversHost class for the device.
        - Defined methods that helps with different use cases.

    """

    def __new__(cls, driver_class: Driver, devices_host_class: DriversHost):
        obj = object.__new__(cls)
        obj._value_ = driver_class.device_name()
        obj.driver = driver_class
        obj.host = devices_host_class

        return obj

    def build_host_process(self, process_manager: BaseManager, package_queue: PackageQueueProxy, drivers_state_queue,
                           **kwargs) -> DriversHost:
        """Builds a server process DriverHost instance using the provided
        process_manager.

        The others parameters after the process_manager, are the parameters expected by the
        constructor of a DriversHost class.

        Args:
            process_manager: The custom multiprocessing.managers.BaseManager that contains
                the DriversHost classes registered. The process_manager should had been started using
                the method start().
            package_queue: The Gateway's PackageQueue expected by each Drivers Host.
            **kwargs: The named kwargs expected by the DriversHost __init__ method.
            :param drivers_state_queue:
        """
        host_constructor = getattr(process_manager, self.host.__name__)
        try:
            host_instance_proxy = host_constructor(package_queue, drivers_state_queue, **kwargs)
        except Exception as ex:
            log.error(ex)

        return host_instance_proxy

    VOYAGER = (VoyagerDriver, VoyagerDriversHost)
    ICOMOX = (IcomoxDriver,IcomoxDriversHost)
    MOCK = (MockDriver, MockDriversHost)
    USB = (UsbDriver, UsbDriversHost)
    THERMOCOUPLE = (Mcp9600Driver, GenericDriversHost)
    ARMROBOT = (ArmRobotDriver, RobotDriversHost)
    THERMALROBOT = (ThermalRobotDriver, ThermalArmHost)
