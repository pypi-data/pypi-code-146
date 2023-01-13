import utime
import uasyncio
from machine import Pin, PWM, ADC


class SimpleOut:

    def __init__(self, pin, default=0):
        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(default)

    def read(self):
        return self.pin.value()

    def write(self, value):
        return self.pin.value(value)

    def switch(self):
        value = 1 - self.pin.value()
        self.pin.value(value)

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)


class SimpleIn:

    def __init__(self, pin, default=Pin.PULL_UP):
        self.pin = Pin(pin, Pin.IN, default)

    def read(self):
        return self.pin.value()

    def write(self, value):
        return self.pin.value(value)


class Button(SimpleIn):

    def __init__(self, pin, default=Pin.PULL_UP):
        """
        A button is a simple input that can be pressed.
        :param pin: pin
        :param default: default value Pin.PULL_UP or Pin.PULL_DOWN
        """
        super().__init__(pin, default)
        if default == Pin.PULL_UP:
            self.default = 1
        elif default == Pin.PULL_DOWN:
            self.default = 0
        else:
            raise ValueError("default must be Pin.PULL_UP or Pin.PULL_DOWN")

    def is_pressed(self, wait=True):
        """
        Returns True if the button is pressed.
        """
        if not wait:
            return self.pin.value() != self.default
        if self.pin.value() != self.default:
            utime.sleep_ms(15)
            if self.pin.value() != self.default:
                return True
        return False

    async def async_is_pressed(self, wait=True):
        """
        Returns True if the button is pressed.
        """
        if not wait:
            return self.pin.value() != self.default
        if self.pin.value() != self.default:
            await uasyncio.sleep_ms(15)
            if self.pin.value() != self.default:
                return True
        return False

    def is_released(self, wait=True):
        """
        Returns True if the button is released.
        """
        if not wait:
            return self.pin.value() == self.default
        if self.pin.value() == self.default:
            utime.sleep_ms(15)
            if self.pin.value() == self.default:
                return True
        return False

    async def async_is_released(self, wait=True):
        """
        Returns True if the button is released.
        """
        if not wait:
            return self.pin.value() == self.default
        if self.pin.value() == self.default:
            await uasyncio.sleep_ms(15)
            if self.pin.value() == self.default:
                return True
        return False

    def pressed(self, callback=None, hard=False):
        """
        设置按键按下回调
        """
        if callback is None:
            return
        self.pin.irq(trigger=Pin.IRQ_FALLING if self.default else Pin.IRQ_RISING, handler=callback, hard=hard)

    def released(self, callback=None, hard=False):
        """
        设置按键释放回调
        """
        if callback is None:
            return
        self.pin.irq(trigger=Pin.IRQ_RISING if self.default else Pin.IRQ_FALLING, handler=callback, hard=hard)

    def pressed_or_released(self, callback=None, hard=False):
        """
        设置按键按下或释放回调
        """
        if callback is None:
            return
        self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback, hard=hard)


class Led:

    def __init__(self, pin, status=False, grade=0xFFFF):
        """
        :param pin: pin
        :param grade: 0-65535
        """
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(1000)
        self.grade = grade
        self.pwm.duty_u16(grade if status else 0)

    def switch(self, grade=None):
        """
        Switches the LED on or off.
        :param grade: 0-65535
        """
        if grade:
            self.grade = grade
            self.pwm.duty_u16(self.grade)
        elif self.pwm.duty_u16() == 0:
            self.pwm.duty_u16(self.grade)
        else:
            self.pwm.duty_u16(0)

    def on(self):
        self.pwm.duty_u16(self.grade)

    def off(self):
        self.pwm.duty_u16(0)

    def read(self):
        return self.pwm.duty_u16()

    def write(self, value):
        self.pwm.duty_u16(value)
