"""
This module defines the arm controller to admin the arm as a shared physical resource

"""
# ============================ imports =========================================
import threading
import time
from typing import List, Callable, Union

from txp import settings
import logging

from txp.common.edge import ImageSignal, ThermalImageSignal, EdgeDescriptor, Signal
from txp.devices.drivers.arm_robot.arm_handler import ArmHandler
from txp.devices.drivers.usb.camera.camera_handler_base import CameraHandlerBase, CameraType
import enum

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class ArmControllerError(enum.Enum):
    POSITION_NOT_REACHED = 1
    IMAGE_NOT_TAKEN = 2


class ArmController:

    def __init__(self, edge_descriptor:EdgeDescriptor):
        log.info("ArmController is instanciated")
        self.descriptor = edge_descriptor
        self._arm_handler = ArmHandler()
        self._camera_handlers: List[CameraHandlerBase] = []
        self._set_camera_handlers(edge_descriptor)
        self._lock = threading.Lock()
        log.info(f"Setting initial robot position (90,90,90,90,90,90)")
        self._arm_handler.set_arm_angle_position([90, 90, 90, 90, 90, 90])

    def execute_arm_action(self, angle) -> Union[List, ArmControllerError]:
        """
        TODO: thinking on the production to take only the angles of connected servo based on its status...
              then use Arm_serial_servo_write instead of Arm_serial_servo_write6

        :param angle: tuple of 6 angles for the servo.
        :return: Signal images asociated to the arm.one ImageSignal ThermalImageSignal

        """
        acquired = self._lock.acquire(blocking=False)
        if not acquired:
            log.debug(f"Arm resource is locked when tryin to move to {angle}. "
                      f"Return immediately.")
            return []
        else:
            log.info("acquiring arm resource by driver angle {}".format(angle))
            images = []
            position_reached = False
            try:
                servo_status = self._arm_handler.arm_connection_status()
                log.info("servo status is {}".format(servo_status))
                if servo_status:
                    log.info("moving angle {}".format(angle))

                    position_reached = self._arm_handler.set_arm_angle_position(angle)

                    if position_reached:
                        time.sleep(1)
                        images = self._get_signals_image()

            except Exception as ex:
                log.error("Exception in ArmController {}".format(ex))
            finally:
                self._lock.release()
                log.info("images captured resource released")
                if not position_reached:
                    log.info("POSITION NOT REACHED")
                    return ArmControllerError.POSITION_NOT_REACHED
                elif not images:
                    log.info("IMAGES NOT TAKEN")
                    return ArmControllerError.IMAGE_NOT_TAKEN
                else:
                    log.info(f"IMAGES TAKEN")
                    return images

    def disconnect(self):
        self._lock.acquire()
        try:
            for camera in self._camera_handlers:
                camera.disconnect()
            self._camera_handlers = []
            self._arm_handler.flush()
        finally:
            self._lock.release()
            log.info("disconnecting released resource")

    def is_arm_fully_connected(self):
        """
        Validates that all cameras and servos are connected and working.
        :return: True is all resources are connected False if any physical device is in failure
        """
        log.info("validating if it is fully connected")
        connected = True
        try:
            for camera in self._camera_handlers:
                if not bool(camera.is_connected()):
                    connected = False
                log.info("camera {} status is {}".format(camera.get_camera_id(),connected))
            if not self._arm_handler.arm_connection_status():
                connected = False
        except Exception as ex:
            log.error("Arm is not fully connected exception {}".format(ex) )
            connected = False
        return connected

    def _get_signals_image(self):
        """
        Returns signal images
        :return: returns the signals of the images
        """
        log.info("getting camera images")
        image_signals = []
        for camera in self._camera_handlers:
            if camera.is_connected():
                image = camera.get_image()
                camera_type = camera.get_camera_type()
                if len(image) == 0:
                    return []
                elif camera.get_camera_type() == CameraType.NORMAL:
                    image_signals.append(ImageSignal.build_signal_from_lists(
                        [image],
                        (1, len(image)),
                        0,
                        0
                    ))
                else:
                    image_signals.append(ThermalImageSignal.build_signal_from_lists(
                        [image],
                        (1, len(image)),
                        0,
                        0
                    ))
                log.debug("getting image from {}".format(camera_type))
            else:
                log.error("camera {} is not connected for {}".format(camera_type,self.descriptor.logical_id))
                return None
        return image_signals

    def _set_camera_handlers(self, edge_descriptor):

        sensors = edge_descriptor.get_virtual_sensors()

        for sensor  in sensors:
            if sensor.camera_type == CameraType.NORMAL:
                camera_handler_base = CameraHandlerBase(str(CameraType.NORMAL), sensor.physical_id)
                camera_handler_base.connect()
                log.info("Created camera handler {} with physical ID {} and status is {}".format(CameraType.NORMAL,sensor.physical_id,camera_handler_base.is_connected()))
                self._camera_handlers.append(camera_handler_base)
            if sensor.camera_type == CameraType.THERMOGRAPHIC:
                camera_handler_base = CameraHandlerBase(str(CameraType.THERMOGRAPHIC), sensor.physical_id)
                camera_handler_base.connect()
                log.info("Created camera handler {} with physical ID {} and status is {}".format(CameraType.THERMOGRAPHIC,sensor.physical_id,camera_handler_base.is_connected()))
                self._camera_handlers.append(camera_handler_base)



