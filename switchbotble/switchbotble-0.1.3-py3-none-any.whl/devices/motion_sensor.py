from bleak.backends.scanner import BLEDevice
from .base import SwitchBotDevice

# see: https://github.com/OpenWonderLabs/python-host/wiki/Motion-Sensor-BLE-open-API
# PIR = Passive infrared(IR) sensor, motion sensor

class MotionSensor(SwitchBotDevice):
    def __init__(self, d: BLEDevice, service_data: bytearray, **kwargs):
        self.motion_timeout_limit = 0
        self.motion_timeout = kwargs.get('motion_timeout', 30)
        self.ignore_motion_timeout = False
        super().__init__(d, service_data, **kwargs)

    def clear_current_motion_timeout(self):
        if self.motion:
            self.ignore_motion_timeout = True

    def _update_properties(self, d: BLEDevice, service_data: bytearray):
        # Battery
        self.battery = service_data[2] & 0x7f
        # Light state
        self.light = True if service_data[5] & 0x02 else False
        # PIR state
        self.motion_raw = True if service_data[1] & 0x40 else False
        self.last_motion = service_data[4] + service_data[3]*256 + ((service_data[5] & 0x80) >> 7)*65536
        self.motion = self.motion_raw

    def _check_diff(self):
        self._check_diff_light()
        self._check_diff_motion()

    def _check_diff_light(self):
        # Checking Light state
        if self.prev['light'] != self.light:
            if self.light:
                self.publish("light")
            else:
                self.publish("dark")
            self.log(f"light: {self.prev['light']} -> {self.light}")

    def _check_diff_motion(self):
        # Checking PIR state
        if self.prev['motion_raw'] != self.motion_raw:
            if self.motion_raw:
                self.motion_timeout_limit = 0
            else:
                self.motion_timeout_limit = self.last_motion + (self.motion_timeout - 30 if self.motion_timeout > 30 else 0)
            self.log(f"motion_raw: {self.prev['motion_raw']} -> {self.motion_raw}, last_motion: {self.prev['last_motion']} -> {self.last_motion}")
        if not self.motion_raw and self.last_motion < self.motion_timeout_limit:
            self.motion = True
        if self.prev['motion'] != self.motion:
            if self.motion == True:
                self.publish("motion")
            else:
                if self.ignore_motion_timeout:
                    self.ignore_motion_timeout = False
                else:
                    self.publish("no_motion")
            self.log(f"motion: {self.prev['motion']} -> {self.motion}, last_motion: {self.prev['last_motion']} -> {self.last_motion}")

    def __str__(self):
        return f"{self.__class__.__name__}: battery={self.battery}, light={self.light}, motion_raw={self.motion_raw}, motion={self.motion}, last_motion={self.last_motion}"
