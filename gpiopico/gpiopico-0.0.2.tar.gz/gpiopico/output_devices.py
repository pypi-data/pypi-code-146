from umachine import Pin, PWM
from utime import sleep

class AnalogicMap:
    """
       create_map = AnalogicMap()
       print(create_map.create_map(x, 0, 64300, 0, 100))
    """
    def __init__(self, return_float=False):
        self._return_float = return_float

    def create_map(
        self,
        x,
        in_min,
        in_max,
        out_min,
        out_max
    ):
        
        _value_map = (
            (x-in_min)*(out_max-out_min)/(in_max - in_min)+out_min
        )
        return _value_map if self._return_float else int(_value_map)

class DigitalSimpleControl:
    """
        led = DigitalSimpleControl(2, inverted_logic=True)
        while True:
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

class DigitalFullControl(DigitalSimpleControl):
    """
        led = DigitalFullControl(2, inverted_logic=True)
        while True:
            print('LOW')
            led.change_pwm(0)
            sleep(2)
            print('MEDIUM')
            led.change_pwm(125)
            sleep(2)
            print('HIGH')
            led.change_pwm(255)
            sleep(2)
            for i in range(0, 255):
                print(i)
                led.change_pwm(i)
                sleep(0.01)
            for i in range(255, 0):
                print(i)
                led.change_pwm(i)
                sleep(0.01)
    """
    def __init__(
        self,
        pin: int,
        use_mapping=True,
        inverted_logic: bool = False
    ) -> None:
        super().__init__(pin, inverted_logic)
        self._pin = PWM(Pin(pin))
        self._pwm_value = 0
        self._use_mapping = use_mapping
        self._mapping = AnalogicMap()
        self._range_map = (0, 65535) if inverted_logic else (65535, 0)

    @property
    def pwm_value(self):
        return self._pwm_value

    def change_pwm(self, pwm_value: int):
        if self._use_mapping:
            _pwm_value = (
                self._mapping.create_map(
                    pwm_value, 0, 255, self._range_map[0], self._range_map[1]
                )
            )
            _pwm_value = (
                _pwm_value if self._inverted_logic else _pwm_value
            )
            self._pwm_value = _pwm_value
            self._pin.duty_u16(_pwm_value)
        else:
            self._pwm_value = pwm_value
            self._pin.duty_u16(pwm_value)
            
            

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
    pass
