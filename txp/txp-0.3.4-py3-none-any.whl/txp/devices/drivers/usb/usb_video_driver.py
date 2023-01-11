"""
This module implements a generic USB video driver based on OpenCV library.
"""
# ============================ imports =========================================

import threading
import cv2
from typing import List
from txp.devices.drivers.driver import DriverState, StateReport
from txp.devices.drivers.usb.usb_base_driver import UsbDriver
from txp.common.edge import EdgeDescriptor

from txp.devices.package_queue import PackageQueueProxy
from txp.common.edge.perception_dimensions import ImageSignal
from txp.common.config import settings
import queue
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# USB Camera Driver Implementation.
# ==============================================================================


class UsbVideoDriver(UsbDriver):
    """Implementation of the USB video camera driver.
    """

    def __init__(
            self,
            edge_descriptor: EdgeDescriptor,
            gateway_packages_queue: PackageQueueProxy,
            on_driver_state_changed: callable,
            host_clock_notification_queue: queue.Queue
    ):
        """
        Note: This Driver receives a USB port address, which is added and passed down by the Gateway operative
        configuration. The USB port address is discovered during the production stage.

        Args
            edge_descriptor: The Edge Descriptor for this Driver.
            gateway_packages_queue: The Gateway Package Queue to put produced packages.
            on_driver_state_changed: Function used to notify driver state changes.
        """
        UsbDriver.__init__(self, edge_descriptor, gateway_packages_queue,
                           on_driver_state_changed, host_clock_notification_queue)
        self.camera_handler = None

    def is_virtual(cls) -> bool:
        return False

    def observation_pulse(self) -> int:
        return 5

    def connect_device(self):
        """Connects to the USB camera with the corresponding physical id.
        """
        log.info(f"Connecting USB camera {self.logical_id}")
        if not self.camera_handler:
            self.camera_handler = cv2.VideoCapture(self._physical_id)

        if not self.camera_handler.isOpened():
            log.error(f"Error connecting to the USB physical_id: {self._physical_id}:")
        else:
            self.on_driver_state_changed(
                self.logical_id, DriverState.CONNECTED
            )

    def disconnect_device(self):
        """Disconnects the USB camera and release the handler.
        """
        if self.camera_handler:
            self.camera_handler.release()
            log.info(f"USB camera {self.logical_id} was disconnected")
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
            A list of ImageSignal collected by the USB camera.
        """
        signals = []

        image = self.get_image()

        signal = ImageSignal.build_signal_from_lists(
            [image],
            (1, len(image)),
            0,
            0
        )
        signals.append(signal)

        return signals

    def _stop_sampling_collect(self):
        """This method will stop the sampling collection in the driver implementation.
        """
        pass

    def get_image(self):
        ret, image = self.camera_handler.read()
        log.info(f"Image taken from {self.logical_id}")
        if not ret:
            log.error("Error reading image")

        ret, image_jpeg = cv2.imencode('.jpeg', image)
        if not ret:
            log.error("Error encoding JPEG image")

        return list(image_jpeg)

    def get_video(self):
        # TODO: Not Supported yet
        pass
