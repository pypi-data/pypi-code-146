import utime
from machine import Pin


class HCSR04:

    def __init__(self, trig_pin, echo_pin):
        self.Trig = Pin(trig_pin, Pin.OUT)
        self.Echo = Pin(echo_pin, Pin.IN)
        self.Trig.value(0)

    def distance(self):
        self.Trig.value(1)
        utime.sleep_us(10)
        self.Trig.value(0)
        while self.Echo.value() == 0:
            pass
        t1 = utime.ticks_us()
        while self.Echo.value() == 1:
            pass
        t2 = utime.ticks_us()
        return (t2 - t1) * 0.017
