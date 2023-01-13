from machine import ADC, Pin
from rp2040.base import SimpleOut


class BoardLed(SimpleOut):
    """
    板载LED(绿色)
    """

    def __init__(self):
        super().__init__(25, 0)


class Vsys:
    """
    电池电压
    """

    def __init__(self, pin=29):
        self.pin = ADC(pin)
        self.voltage = 0

    def read(self):
        self.voltage = self.pin.read_u16() / 65535 * 9.9
        return self.voltage


class Vbus:
    """
    USB电源检测
    """

    def __init__(self, pin=24):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)

    def read(self):
        return self.pin.value()
