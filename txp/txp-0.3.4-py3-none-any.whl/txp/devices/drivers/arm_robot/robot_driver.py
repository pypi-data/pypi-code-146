"""
This module contains the concrete driver implementation for the Arm Robot device.
"""

# =================== imports ==============================================
import queue
import threading
import time
import logging
from typing import Dict, Tuple, List, Callable

from txp.devices.drivers.arm_robot.arm_controller import ArmController, ArmControllerError
from txp.devices.drivers.arm_robot.arm_handler import ArmHandler
from txp.devices.drivers.usb.camera.camera_handler_base import CameraHandlerBase, CameraType
from txp.devices.drivers.driver import Driver, EdgeParameterNotFoundError, DriverState
from txp.common.edge import EdgeDescriptor, VirtualSensorObject, VirtualEdgeInformation
from txp.devices.package_queue import PackageQueueProxy
import datetime

from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Robot driver implementation
# ==============================================================================
class ArmRobotDriver(Driver):
    """Implementation of the Arm Robot driver used with the NVIDIA Jetson computer.

    The ArmRobotDriver is the main unit composed of different physical sensors
    and a set of positions which are interpreted as Virtual Edges that captures
    the perceptions of those edges.
    """

    def __init__(
            self,
            edge_descriptor: EdgeDescriptor,
            gateway_packages_queue: PackageQueueProxy,
            on_driver_state_changed: Callable,
            robotic_arm_controller: ArmController,
            host_clock_notification_queue: queue.Queue
    ):
        """
        Args:
            edge_descriptor: The EdgeDescriptor for this driver that contains all the
                information for the configured sensors and the virtual positions.
            gateway_packages_queue: The Gateway Package Queue to put produced packages.
            on_driver_state_changed: Function used to notify driver state changes in the
                upper layers.
            robotic_arm_handler: The Robotic arm controller shared across all the ArmRobotDriver
                instances
        """
        super(ArmRobotDriver, self).__init__(edge_descriptor, gateway_packages_queue,
                                             on_driver_state_changed, host_clock_notification_queue)

        # Validations of the received descriptor
        self._validate_edge_descriptor(edge_descriptor)

        if not self._validate_position_and_virtual_id(edge_descriptor):
            raise ValueError("The received virtual positions do not match the received virtual IDs")

        if not self._validate_cameras(edge_descriptor.get_virtual_sensors()):
            raise ValueError("Unknown camera devices in the configuration for Virtual Edge")

        self._robotic_arm_controller: ArmController = robotic_arm_controller

        self._virtual_information: VirtualEdgeInformation = edge_descriptor.get_virtual_edge_information()

    def _add_position_not_reached_context(self):
        self._driver_context = {
            "error": ArmControllerError.POSITION_NOT_REACHED,
            "reported_time": str(datetime.datetime.now())
        }

    def _add_images_taken_context(self):
        self._driver_context = {
            "info": f"{self.logical_id} Successfully captured position images.",
            "reported_time": str(datetime.datetime.now())
        }

    def _add_images_no_taken_context(self):
        self._driver_context = {
            "error": ArmControllerError.IMAGE_NOT_TAKEN,
            "reported_time": str(datetime.datetime.now())
        }

    def observation_pulse(self) -> int:
        """The observation pulse for Virtual Drivers.

        Note: this time interval doesn't really represent the
        driver's clock value. The reason is that, currently by design
        simplification, the WindowPolicyManager will expect 1 sample
        per virtual edge on each sampling window.

        TODO: The driver could change it's observation pulse value given
            the current sampling window, in order to reflect that design
            simplification.

        """
        return 20

    @property
    def parent_logical_id(self) -> str:
        return EdgeDescriptor.split_virtual_id(self.logical_id)[0]

    @property
    def get_virtual_id_hash(self) -> str:
        return self._virtual_information.virtual_id_hash

    def _validate_edge_descriptor(self, edge_descriptor: EdgeDescriptor):
        if not edge_descriptor.get_virtual_sensors():
            log.error(f"{self.__class__.__name__} did not receive virtual "
                      f"sensors information in EdgeDecriptor")
            raise EdgeParameterNotFoundError(f"{self.__class__.__name__} did not receive virtual "
                                             f"sensors information in EdgeDecriptor")

        if not edge_descriptor.get_virtual_edge_information():
            log.error(f"f{self.__class__.__name__} did not received virtual edge information"
                      f"in Edge Descriptor parameters")
            raise EdgeParameterNotFoundError(f"{self.__class__.__name__} did not receive virtual "
                                             f"sensors information in EdgeDecriptor")

    @staticmethod
    def _validate_position_and_virtual_id(virtual_devices: EdgeDescriptor) -> bool:
        computed_virtual_id = EdgeDescriptor.get_hashed_virtual_id(
            virtual_devices.get_virtual_edge_information().position
        )
        are_equals = computed_virtual_id == virtual_devices.get_virtual_edge_information().virtual_id_hash
        if not are_equals:
            log.error(f"Computed virtual ID does not equals received virtual ID for "
                      f"positions: {virtual_devices.get_virtual_edge_information().position}")
        return are_equals

    def _validate_cameras(self, camera_sensors: List[VirtualSensorObject]) -> bool:
        valid = True
        for camera in camera_sensors:
            if not isinstance(camera.camera_type, CameraType):
                log.error(f"{self.__class__.__name__} received unknown camera type: {camera.camera_type}")
                valid = False

            # TODO: Here we should check if the camera is valid. Handler should offer method.

        return valid

    def connect_device(self):
        log.info("conecting driver {}".format(self.logical_id))
        if self._robotic_arm_controller is not None:
            if not self._robotic_arm_controller.is_arm_fully_connected():
                self.on_driver_state_changed(
                    self.logical_id, DriverState.DISCONNECTED
                )
            else:
                self.on_driver_state_changed(
                    self.logical_id, DriverState.CONNECTED
                )
        else:
            log.info("not valid instanse of controller driver {}".format(
                self.logical_id
            ))


    def disconnect_device(self):
        self.on_driver_state_changed(
            self.logical_id, DriverState.DISCONNECTED
        )

    @classmethod
    def device_name(cls) -> str:
        return "ArmRobot"

    @classmethod
    def is_virtual(cls) -> bool:
        return True

    def _start_sampling_collect(
            self
    ) -> List["Signal"]:
        executed = False
        signals = []
        while not executed:
            if self._stop_current_pulse_signal.is_set():
                break

            if not executed:
                position = self._virtual_information.position

                signals = self._robotic_arm_controller.execute_arm_action(position)

                if signals == ArmControllerError.POSITION_NOT_REACHED:
                    log.info(f"Adding position not reached context in Driver {self.logical_id}")
                    self._add_position_not_reached_context()
                    signals = []
                    executed = True

                elif signals == ArmControllerError.IMAGE_NOT_TAKEN:
                    log.info(f"Image not captured context in Driver {self.logical_id}")
                    self._add_images_no_taken_context()
                    signals = []
                    executed = True

                elif signals:
                    self._add_images_taken_context()

        log.info("{} finished sampling with the amr".format(self.logical_id))
        return signals

    def _stop_sampling_collect(self):
        log.info("Virtual driver {} is stopping sampling and collect".format(self.logical_id))
