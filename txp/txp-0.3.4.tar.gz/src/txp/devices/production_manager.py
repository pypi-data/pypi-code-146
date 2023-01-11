import multiprocessing
import threading
import time
from typing import List, Tuple, Dict, Union, Optional

from txp.common.edge import DeviceId
from txp.devices.drivers.arm_robot.arm_handler import ArmHandler
from txp.devices.drivers.arm_robot.robot_driver import ArmRobotDriver
from txp.devices.drivers.arm_robot.thermal_robot import ThermalRobotDriver
from txp.devices.drivers.voyager.voyager_driver_host import VoyagerDriversHost
from txp.devices.drivers.icomox.icomox_driver_host import IcomoxDriversHost
from txp.devices.gateway_states_enums import DevicePairingStatus
from txp.devices.drivers.mock.mock_driver import MockDriversHost
from txp.devices.drivers.icomox.icomox_driver import IcomoxDriver
from txp.devices.drivers.voyager.voyager_driver import VoyagerDriver
from txp.devices.drivers.mock.mock_driver import MockDriver
from txp.devices.drivers.drivers_host import DriversHost
from txp.devices.drivers.arm_robot.robot_host import RobotDriversHost
from txp.common.edge.common import EdgeType, EdgeDescriptor, VirtualSensorObject, VirtualEdgeInformation
from txp.devices.drivers.usb.camera.camera_handler_base import CameraHandlerBase, CameraType
from txp.common.config import settings
import logging
import dataclasses
import copy

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

MAX_NUMBER_OF_DEVICES_ALLOWED_IN_PRODUCTION = 1

# Hardcoded virtual sensor object for the Thermocouple of a ThermoArm
_thermo_arm_thermocuple_sensor: VirtualSensorObject = VirtualSensorObject(
    "I2C-0x44", CameraType.THERMOCOUPLE
)


@dataclasses.dataclass
class _VirtualProductionRecord:
    """Private class to track the virtual production process information."""
    virtual_camera: VirtualSensorObject = VirtualSensorObject()
    virtual_thermocamera: VirtualSensorObject = VirtualSensorObject()
    virtual_positions_produced: List[Tuple[EdgeDescriptor, str]] = dataclasses.field(default_factory=list)
    torque_enabled: bool = True  # By default the torque will be enabled
    position_captured: Tuple[int] = dataclasses.field(default_factory=tuple)  # the last position captured
    image_captured: Optional = None  # The last image captured in the virtual production
    thermographic_img_captured: Optional = None  # The last thermographic image captured in the virtual production
    captured_positions: List[Dict] = dataclasses.field(default_factory=list)  # The list of captured positions

    def virtual_camera_produced(self) -> bool:
        return bool(self.virtual_camera)  # No data in virtual camera implies not produced

    def virtual_thermocamera_produced(self) -> bool:
        return bool(self.virtual_thermocamera)  # No data in virtual thermocamera implies not produced

    def copy(self) -> "_VirtualProductionRecord":
        return copy.deepcopy(self)


class ProductionManager:
    """
    TODO: this class will be part of the device manager and connection methods wont be here. This is subject to change
    the purpose of this module is to speed up production interface.
    """
    _device_to_host_class = {
        IcomoxDriver.device_name(): IcomoxDriversHost,
        VoyagerDriver.device_name(): VoyagerDriversHost,
        MockDriver.device_name(): MockDriversHost
    }

    def __init__(self, gateway_packages_queue, devices: List[str]):
        state_queue = multiprocessing.Manager().Queue()
        self._is_device_available = False
        self._driver_hosts_deprecated_list: List[DriversHost] = []
        self._driver_hosts: Dict[str, DriversHost] = {}
        log.info(f"Production manager configured devices: {devices}")
        for device in devices:
            if device == RobotDriversHost.get_driver_host_name() or \
                device == ThermalRobotDriver.device_name():  # RobotDriversHost not required in production.
                continue
            host_instance = self._device_to_host_class[device](gateway_packages_queue, state_queue)
            self._driver_hosts[device] = host_instance

        self._available_devices = {}
        self._virtual_production: _VirtualProductionRecord = None
        self._normal_camera_handler: CameraHandlerBase = None
        self._thermographic_camera_handler: CameraHandlerBase = None
        self._arm_handler = ArmHandler()

    def _get_indexed_host(self, host_name):
        host = self._driver_hosts.get(host_name, None)
        if not host:
            log.error(f"ProductionManager requested to search an edge of kind: {host_name}, but the hosts was "
                      f"never configured")
        return host

    def start_listening_for_an_edge(self, device_kind: str):
        drivers_host = self._get_indexed_host(device_kind)
        drivers_host.connect()

    def get_hosted_device(self) -> Tuple[str, DeviceId]:
        """

        :return: a tuple with host name with the DeviceId associated. if not devices registerd
        returns empty tuple
        """
        if len(self._available_devices) > 0:
            item = self._available_devices.popitem()
            host_associated = item[0]
            device_id_associated = (item[1])[0]
            return (host_associated, device_id_associated)
        else:
            tuple()

    def is_device_available(self):
        return self._is_device_available

    def wait_for_device_to_connect(self, device_kind: str, timeout_in_minutes=10):
        """
        blocks for timeout minutes until a device is connected or it time out
        returns true when 1 devices is connected to the nerwork

        :rtype: boolean
        :exception: if there are more than 1 device connected a InvalidNumberOfDevices exception is thrown.
        """

        self._clear_devices()
        self._hast_timed_out = False

        t = threading.Thread(target=self._wait_for_device_to_connect_thread_body,
                             args=[device_kind, timeout_in_minutes])
        t.start()

        while (not self._hast_timed_out) and (not self._is_device_available):
            pass

        devices_ids_associated = list(self._available_devices.values())

        if devices_ids_associated:
            if len(self._available_devices) > MAX_NUMBER_OF_DEVICES_ALLOWED_IN_PRODUCTION or \
                    len(devices_ids_associated[0]) > MAX_NUMBER_OF_DEVICES_ALLOWED_IN_PRODUCTION:
                raise InvalidNumberOfDevices("Invalid number of devices in production", devices_ids_associated)

        return self._is_device_available

    def _wait_for_device_to_connect_thread_body(self, device_kind, timeout_minutes):
        self._is_device_available = False
        elapsedTime = 0
        while not self._is_device_available:
            time.sleep(6)
            drivers_host = self._get_indexed_host(device_kind)
            if not drivers_host:
                return

            physical_ids = drivers_host.discover_physical_ids()
            if len(physical_ids) > 0:
                if device_kind in self._available_devices.keys():
                    self._available_devices[device_kind].extend(physical_ids)
                else:
                    self._available_devices[device_kind] = physical_ids
                log.info(f"Devices found in Production for: {device_kind}")

            if len(self._available_devices) > 0:
                self._is_device_available = True
                break

            elapsedTime += 1
            if elapsedTime == timeout_minutes:
                self._hast_timed_out = True
                log.info("timeout waiting for a device")
                break

        log.info("wait for devices to connect finished")

    def stop_listening_for_devices(self, device_kind: str):
        driver_host = self._get_indexed_host(device_kind)
        if not driver_host:
            return
        driver_host.disconnect()

    def _clear_devices(self):
        if len(self._available_devices):
            self._available_devices.clear()

    # ========================= Virtual Production Methods =======================
    """
    The methods below provides an API for use in the production of a virtual edge device. 
    Currently, the virtual edge is bound to the production of the Arm Robot device. 
    By design, the implementation tries to:
        - Detect normal camera
        - Detect thermocamera 
        - Capture virtual positions from the Arm robot.
    """

    def prepare_virtual_production(self, actuator_descriptor: EdgeDescriptor):
        """Initializes internal attributes to track the virtual production process
        of virtualized edges through the ARM ROBOT"""

        if actuator_descriptor.get_virtual_sensors() is None or not actuator_descriptor.get_virtual_sensors():
            self._virtual_production = _VirtualProductionRecord()
        else:
            virtual_camera_sensor = list(filter(
                lambda virtual_sensor: virtual_sensor.camera_type == CameraType.NORMAL,
                actuator_descriptor.get_virtual_sensors()
            ))[0]
            thermocamera_virtual_sensor = list(filter(
                lambda virtual_sensor: virtual_sensor.camera_type == CameraType.THERMOGRAPHIC,
                actuator_descriptor.get_virtual_sensors()
            ))[0]

            if virtual_camera_sensor is None or thermocamera_virtual_sensor is None:
                self._virtual_production = _VirtualProductionRecord()
                return

            self._virtual_production = _VirtualProductionRecord(
                virtual_camera_sensor,
                thermocamera_virtual_sensor
            )

    def get_next_virtual_production_step(self) -> DevicePairingStatus:
        """Returns the next appropriate Status in the virtual production"""
        if not self._virtual_production.virtual_camera_produced():
            return DevicePairingStatus.RequestVirtualCameraConnection

        elif not self._virtual_production.virtual_thermocamera_produced():
            return DevicePairingStatus.RequestVirtualThermocameraConnection

        else:  # Cameras already paired. Only Arm robot configuration required
            if not self._normal_camera_handler:
                log.info("Production Manager creating camera handler for Normal Camera")
                self._normal_camera_handler = CameraHandlerBase(
                    self._virtual_production.virtual_camera.camera_type.__str__(),
                    self._virtual_production.virtual_camera.physical_id
                )
                self._normal_camera_handler.connect()

            if not self._thermographic_camera_handler:
                log.info("Production Manager creating camera handler for Thermographic Camera")
                self._thermographic_camera_handler = CameraHandlerBase(
                    str(self._virtual_production.virtual_thermocamera.camera_type.__str__()),
                    self._virtual_production.virtual_thermocamera.physical_id
                )
                self._thermographic_camera_handler.connect()

            return DevicePairingStatus.VirtualRequestNextStepFromUser

    def detect_virtual_camera(self) -> Union[
        "DevicePairingStatus.VirtualCameraProducedSuccessfully",
        "DevicePairingStatus.VirtualCameraConnectionError"
    ]:
        # Precondition: The user clicked and confirmed that the camera was connected.
        # It should be found.
        camera_id = CameraHandlerBase.detect_usb_camera()
        if not camera_id:
            log.error("Trying to pair virtual camera, but not camera usb device was found.")
            return DevicePairingStatus.VirtualCameraConnectionError

        self._virtual_production.virtual_camera = VirtualSensorObject(camera_id, CameraType.NORMAL)
        return DevicePairingStatus.VirtualCameraProducedSuccessfully

    def detect_virtual_thermocamera(self) -> Union[
        "DevicePairingStatus.VirtualThermocameraProducedSuccessfully",
        "DevicePairingStatus.VirtualCameraConnectionError"
    ]:
        # Precondition: The user clicked and confirmed that the camera was connected.
        # It should be found.
        camera_id = CameraHandlerBase.detect_usb_camera()
        if not camera_id:
            log.error("Trying to pair virtual thermographic camera, but not camera usb device was found.")
            return DevicePairingStatus.VirtualThermocameraConnectionError

        self._virtual_production.virtual_thermocamera = VirtualSensorObject(camera_id,
                                                                            CameraType.THERMOGRAPHIC)

        return DevicePairingStatus.VirtualThermocameraProducedSuccessfully

    def get_virtual_production_record(self) -> _VirtualProductionRecord:
        log.info("Creating copy of virtual production record")
        start_time = time.time()
        r = self._virtual_production.copy()
        end_time = time.time()
        log.info(f"Time Elapsed creating copy of virtual production record: {end_time-start_time}")
        return r

    def enable_torque(self) -> None:
        self._virtual_production.torque_enabled = True
        self._arm_handler.enable_torque()
        time.sleep(0.1)
        return

    def disable_torque(self) -> None:
        self._virtual_production.torque_enabled = False
        self._arm_handler.disable_torque()
        time.sleep(0.1)
        return

    def capture_virtual_pos(self) -> None:
        log.info("Capturing images from cameras / Converting to Bytes")
        start_time = time.time()
        self._virtual_production.image_captured = bytes(self._normal_camera_handler.get_image())
        self._virtual_production.thermographic_img_captured = bytes(self._thermographic_camera_handler \
                                                                    .get_image())
        end_time = time.time()
        log.info(f"Total time elapsed for capture and conversion:{end_time-start_time}")
        self._virtual_production.position_captured = self._arm_handler.get_positions().get_positions_tuple()

    def reject_captured_pos(self) -> None:
        self._virtual_production.position_captured = tuple()
        self._virtual_production.image_captured = None
        self._virtual_production.thermographic_img_captured = None

    def confirm_captured_pos(self, actuator_edge_descriptor: EdgeDescriptor, asset_associated: str) -> None:
        hashed_virtual_id: str = EdgeDescriptor.get_hashed_virtual_id(
            self._virtual_production.position_captured
        )

        virtual_logical_id: str = EdgeDescriptor.get_complete_virtual_id(
                actuator_edge_descriptor.logical_id, hashed_virtual_id
        )

        virtual_information = VirtualEdgeInformation(
            self._virtual_production.position_captured,
            hashed_virtual_id
        )

        virtual_descriptor = EdgeDescriptor(
            virtual_logical_id,
            actuator_edge_descriptor.device_kind,
            EdgeType.ON_OFF_DEVICE.__str__(),
            {},
            actuator_edge_descriptor.perceptions.copy()
        )

        virtual_descriptor.set_physical_id(actuator_edge_descriptor.logical_id)

        """This If statement assigns the right sensors depending on the driver type of the device.
        ArmRobotDriver -> Normal Camera and Thermocamera
        ThermalRobotDriver -> Normal Camera, Thermocamera and thermocouple
        """
        if virtual_descriptor.device_kind == ArmRobotDriver.device_name():
            virtual_descriptor.set_virtual_sensors([
                self._virtual_production.virtual_camera,
                self._virtual_production.virtual_thermocamera
            ])
        else:
            virtual_descriptor.set_virtual_sensors([
                self._virtual_production.virtual_camera,
                self._virtual_production.virtual_thermocamera,
                _thermo_arm_thermocuple_sensor
            ])

        virtual_descriptor.set_virtual_edge_information(virtual_information)

        self._virtual_production.virtual_positions_produced.append((virtual_descriptor, asset_associated))
        self._virtual_production.position_captured = tuple()
        self._virtual_production.image_captured = None

    def confirm_all_captured_pos(self, actuator_edge_descriptor: EdgeDescriptor) -> List[EdgeDescriptor]:
        actuator_edge_descriptor.set_physical_id(actuator_edge_descriptor.logical_id)
        if actuator_edge_descriptor.device_kind == ArmRobotDriver.device_name():
            actuator_edge_descriptor.set_virtual_sensors([
                self._virtual_production.virtual_camera,
                self._virtual_production.virtual_thermocamera
            ])
        else:
            actuator_edge_descriptor.set_virtual_sensors([
                self._virtual_production.virtual_camera,
                self._virtual_production.virtual_thermocamera,
                _thermo_arm_thermocuple_sensor
            ])
        log.debug("Sensors added to Actuator Edge Descriptor")
        return self._virtual_production.virtual_positions_produced

    def finish_virtual_production(self):
        self._normal_camera_handler.disconnect()
        self._thermographic_camera_handler.disconnect()
        self._arm_handler.enable_torque()
        self._normal_camera_handler = None
        self._thermographic_camera_handler = None
        self._virtual_production = None


class InvalidNumberOfDevices(Exception):
    """
    Exception raised when there are more than one devices connected to the network
    when in production operation mode

    """
    pass


class NotValidDeviceRegisred(Exception):
    """
    Exception raised when get device method is called to report error since there is no device available.

    """
    pass
