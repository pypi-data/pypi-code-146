from umachine import Pin, PWM
from utime import sleep
from gpiopico.utils import AnalogicMap

_SAMPLES: int = 65534


class DigitalSimpleControl:
    """
        :pin(int)
        :inverted_logic(bool)
        
        led = DigitalSimpleControl(2, inverted_logic=True)
        print('ON')
        led.change_state(True)
        sleep(2)
        print('OFF')
        led.change_state(False)
        sleep(2)

    """
    def __init__(self, pin: int, inverted_logic:bool = False):
        self._inverted_logic = inverted_logic
        self._state = True if inverted_logic else False
        self._pin = Pin(pin, Pin.OUT)

    @property
    def state(self):
        return self._state

    def change_state(self, state:bool):
        self._state = (
            state if self._inverted_logic else not(state)
        )
        self._pin.value(self._state)
    
    def on(self):
        self._pin.value(
           0 if self._inverted_logic else 1
        )
    
    def off(self):
        self._pin.value(
           1 if self._inverted_logic else 0
        )

class DigitalFullControl:
    """
        :pin(int)
        :inverted_logic(bool)
        :use_mapping(bool)
        
        led = DigitalFullControl(2, inverted_logic=True)
        led = Led(2, True)
        led.on()
        sleep(2)
        led.off()
        sleep(2)
        led.pwm_value(125)
        sleep(2)
    """
    def __init__(
        self,
        pin: int,
        inverted_logic: bool = False,
        use_mapping: bool=True
    ) -> None:
        self._inverted_logic = inverted_logic
        self._pin = PWM(Pin(pin))
        self._pwm_value = 0
        self._use_mapping = use_mapping
        self._mapping = AnalogicMap()
        self._range_map = (_SAMPLES, 0) if inverted_logic else (0, _SAMPLES)
        self._limit_range = 255

    @property
    def pwm_value(self):
        return self._pwm_value

    def pwm_value(self, pwm_value: int, limit_range=None) -> None:
        if self._use_mapping:
            _pwm_value = (
                self._mapping.create_map(
                    pwm_value,
                    0,
                    limit_range if limit_range else self._limit_range,
                    self._range_map[0],
                    self._range_map[1]
                )
            )
            print(_pwm_value)
            _pwm_value = (
                _pwm_value if self._inverted_logic else _pwm_value
            )
            self._pwm_value = _pwm_value
            self._pin.duty_u16(_pwm_value)
        else:
            self._pwm_value = pwm_value
            self._pin.duty_u16(pwm_value)
    
    def on(self):
        self._pin.duty_u16(
           0 if self._inverted_logic else _SAMPLES
        )
    
    def off(self):
        self._pin.duty_u16(
           _SAMPLES if self._inverted_logic else 0
        )
            

class Relay(DigitalSimpleControl):
    def __init__(self, pin: int, inverted_logic: bool = False):
        super().__init__(pin, inverted_logic)

class Led(DigitalFullControl):
    def __init__(self, pin: int, inverted_logic: bool = False):
        super().__init__(pin, inverted_logic)

class SolidStateRelay(DigitalFullControl):
    def __init__(self, pin: int, inverted_logic: bool = False) -> None:
        super().__init__(pin, inverted_logic)

class Motor:
    """
        :pin_forward(int)
        :pin_backward(int)
        
        from gpiopico import Motor
        motor_a = Motor(0,1)
        motor_a.forward()
        sleep(2)
        motor_a.backward()
        sleep(2)
        motor_a.stop()
    """
    def __init__(self, pin_forward: int, pin_backward: int) -> None:
        self._pin_forward = DigitalFullControl(pin_forward)
        self._pin_backward = DigitalFullControl(pin_backward)
        self._limit_range = 100
        self.stop()
        
    def forward(self, velocity=None) -> None:
        """
            :velocity(int) 0% - 100%
        """
        if velocity:
            self._pin_forward.pwm_value(
                velocity if velocity <= 100 else 100,
                self._limit_range
            )
        self._pin_forward.on()
        self._pin_backward.off()
    
    def backward(self, velocity=None) -> None:
        """
            :velocity(int) 0% - 100%
        """
        if velocity:
            self._pin_backward.pwm_value(
                velocity if velocity <= 100 else 100,
                self._limit_range
            )
        self._pin_backward.on()
        self._pin_forward.off()
    
    def stop(self) -> None:
        self._pin_forward.off()
        self._pin_backward.off()
        sleep(0.5)

