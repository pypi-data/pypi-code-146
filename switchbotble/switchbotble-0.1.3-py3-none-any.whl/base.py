import asyncio
from typing import List
from bleak import BleakScanner
from bleak.backends.scanner import BLEDevice, AdvertisementData
from .devices.base import SwitchBotDevice
from .devices.factory import SwitchBotDeviceFactory as factory
from blinker import signal

found     = signal('found')
motion    = signal('motion')
no_motion = signal('no_motion')
light     = signal('light')
dark      = signal('dark')
opened    = signal('opened')
closed    = signal('closed')
entered   = signal('entered')
exited    = signal('exited')
pushed    = signal('pushed')

class SwitchBotBLE(BleakScanner):
    # via: https://www.bluetooth.com/ja-jp/specifications/assigned-numbers/company-identifiers/
    __company_id = 0x0969 # Woan Technology (Shenzhen) Co., Ltd.

    # via: https://www.bluetooth.com/specifications/assigned-numbers/ "16-bit UUIDs"
    # 0xfd3d : Woan Technology (Shenzhen) Co., Ltd.
    __uuid = "0000fd3d-0000-1000-8000-00805f9b34fb"

    def __init__(self, **kwargs):
        super().__init__()
        self.__switchbot_devices = {}
        self.__kwargs = kwargs
        self.register_detection_callback(self.__detection_callback)

    def __detection_callback(self, d: BLEDevice, ad: AdvertisementData) -> None:
        if ad.service_data and self.__uuid in ad.service_data:
            service_data = ad.service_data[self.__uuid]
            if d.address in self.__switchbot_devices:
                self.__switchbot_devices[d.address].update(d, service_data)
            else:
                self.__switchbot_devices[d.address] = factory.create(d, service_data, **self.__kwargs)
