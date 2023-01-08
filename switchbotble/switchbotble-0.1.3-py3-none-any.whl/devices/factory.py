from abc import ABCMeta, abstractmethod
from bleak.backends.scanner import BLEDevice
from .base import SwitchBotDevice
from .contact_sensor import ContactSensor
from .motion_sensor import MotionSensor

class SwitchBotDeviceFactory(metaclass=ABCMeta):
    @staticmethod
    def create(d: BLEDevice, service_data: bytearray, **kwargs) -> SwitchBotDevice:
        dev_type = service_data[0]
        if dev_type == ord('d') or dev_type == ord('D'):
            return ContactSensor(d, service_data, **kwargs)
        elif dev_type == ord('s') or dev_type == ord('S'):
            return MotionSensor(d, service_data, **kwargs)
