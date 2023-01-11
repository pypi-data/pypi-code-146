"""
This module defines a common Camara driver this class is designed to wrap up
the camera functionalities to be used as a resource in a txp driver class.
this class does not innherits from driver.py which is driver txp class.
"""
# ============================ imports =========================================
import logging
from enum import Enum
from typing import Optional
try:
    import pyudev
except ModuleNotFoundError:
    pass
import cv2
from txp import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class CameraType(Enum):
    """CameraType.
    All possible camera types will be listed here.
    NORMAL: regular camera
    THERMOGRAPHIC: thermal camera
    TODO: this intends to  have in the enumerated type the enum including the model

    """
    def __new__(cls, *values):
        """This defines the cannonical value (int) for the enum, and allows for other
        values. Useful for human readable strings.

        Reference for this solution:
            https://stackoverflow.com/questions/43202777/get-enum-name-from-multiple-values-python
        """
        obj = object.__new__(cls)
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        # human readable value useful for sending payload information to other systems
        obj.human_readable_value = values[1]
        return obj

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    def __str__(self):
        return self.human_readable_value

    NORMAL = 0, 'Normal', 'normal'
    THERMOGRAPHIC = 1, 'Thermographic', 'thermographic'
    THERMOCOUPLE = 2, 'Thermocouple', 'thermocouple'


class CameraHandlerBase:

    def __init__(self, camera_type: str, camera_id: str):
        if not CameraType.has_value(camera_type):
            log.error(f"Camera Handler does not recognize unknown camera type: {camera_type}")
            raise ValueError(f"Unknown CameraType: {camera_type}")

        self._camera_handler = None
        self._camera_id = camera_id
        self._camera_type = CameraType(camera_type)

    @classmethod
    def detect_usb_camera(cls) -> Optional[str]:
        """Detects the connection of a USB Camera connected to some of the USB ports.

        Returns:
            The camera_id detected. None if nothing was detected.
        """
        result = list()
        context = pyudev.Context()
        for device in context.list_devices(
            subsystem="video4linux", ID_V4L_CAPABILITIES=":capture:"
        ):
            links = device.get("DEVLINKS").split()
            physical_link = list(filter(lambda link : "/by-id/" in link,links))
            link_name = physical_link.pop()
            result.append(link_name)
            #result.append(device.get("DEVLINKS"))
            log.info(
                f"CameraHandler: USB Camera {device.get('ID_VENDOR_ID', None)}:{device.get('ID_MODEL_ID', None)} "
                f"found from {device.get('ID_VENDOR', None)}"
                f"Device name {link_name}"
            )


        return result[-1] #last item mounted

    def connect(self):
        """Connects to the USB camera with the corresponding physical id.

        Returns:
            True if camara was correctly detected and connected
        """
        log.debug(f"Connecting USB camera")
        if not self._camera_handler:
            self._camera_handler = cv2.VideoCapture(self._camera_id)

        if not self._camera_handler.isOpened():
            log.error(f"Error connecting to the USB physical_id: {self._camera_id}:")
            return False

        return True

    def disconnect(self):
        """
            Disconnects the USB camera and release the handler.
        """
        if self._camera_handler:
            self._camera_handler.release()
            log.info(f"USB camera {self._camera_id} was disconnected")

    def get_camera_id(self):
        """
        :return: returns the camera camera_id
        """
        return self._camera_id

    def get_camera_type(self):
        """

        :return: camera type
        """
        return self._camera_type

    def is_connected(self):
        """

        :return: True if resource is connected
        """
        if self._camera_handler is not None:
            camera_status = self._camera_handler.isOpened()
            log.debug("camera status {}".format(camera_status))
            return camera_status
        return False

    def get_image(self):
        for i in range(1,20):
            ret, image = self._camera_handler.read()
        log.info(f"Image taken from {self._camera_id}")
        if not ret:
            log.error("Error reading image")
            return []  # Calling cv2.imencode with empty image will crash. Return here.

        ret, image_jpeg = cv2.imencode('.jpeg', image)
        if not ret:
            log.error("Error encoding JPEG image")

        log.info("returning JPEG")
        return list(image_jpeg)

