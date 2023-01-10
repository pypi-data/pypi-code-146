from umachine import Pin, ADC
from utime import sleep

_VOLTAGE_REF: float = 3.3
_SAMPLES: int = 65535

class RotaryEncoder:
    """
        :dt_pin int
        :clk_pin int
        :sw: int
        :max_step int
        :wrapper bool
        
        encoder = RotaryEncoder(2, 3, 4, max_step=100)

        while True:
            encoder.read()
            sleep(0.009)
            print(encoder.value)
            print(encoder.is_pressed)
    """
    def __init__(
        self,
        dt_pin: int,
        clk_pin: int,
        sw: int,
        max_step: int=10,
        wrapper: bool=True
    ) -> None:
        self._value: int = 0
        self._is_pressed: bool = False
        self._DT_Pin = Pin(dt_pin, Pin.IN, Pin.PULL_UP)
        self._CLK_Pin = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self._SW = Pin(sw, Pin.IN, Pin.PULL_UP)
        self._wrapper: bool = wrapper
        self._previousValue: int = 1
        self._max_step:int = max_step
    
    @property
    def value(self):
        return self._value
    
    @property
    def is_pressed(self):
        return self._is_pressed
    
    def _read_rotatory_state(self) -> None:
        if self._previousValue != self._CLK_Pin.value():
            if not self._CLK_Pin.value():
                if not self._DT_Pin.value():
                    self._value = (self._value - 1)%self._max_step
                else:
                    self._value = (self._value + 1)%self._max_step
            self._previousValue = self._CLK_Pin.value()
        
    def _read_button_state(self) -> None:
        if self._SW.value() == 0:
            if self._wrapper:
                self._is_pressed = not(self._is_pressed)
            else:
                #TODO Change this for Event()
                self._is_pressed = True
    
    def read(self) -> None:
        self._read_button_state()
        self._read_rotatory_state()
        

class AnalogicInputs:
    """
        valid pins: int [26, 27, 28]
    """
    def __init__(
        self,
        adc_pin: int,
        voltage_ref: float = _VOLTAGE_REF
    ) -> None:
        if adc_pin not in list(range(26,29)):
            raise ValueError('adc_pin defined isn´t analogic pin')
        self._input = ADC(adc_pin)
        self._conversion_factor = voltage_ref / _SAMPLES

    def read_voltage(self) -> float:
        return self._input.read_u16() * self._conversion_factor
    
    def read_adc(self) -> int:
        return self._input.read_u16()

class Potentiometer(AnalogicInputs):
    """
        adc_input = Potentiometer(28)
        while True:
            print(adc_input.read_adc())
            sleep(0.1)
        
        :adc_pin
        :voltage_ref
    """
    def __init__(
        self,
        adc_pin: int,
        voltage_ref: float = _VOLTAGE_REF
    ) -> None:
        super().__init__(adc_pin, voltage_ref)

class Joystick(AnalogicInputs):
    """
        :adc_pin_rx
        :adc_pin_ry
        :button_pin
        :function_after_press -> pure function
        :voltage_ref
        :core_range
        
        joystick = Joystick(26, 27, 22)
        # With event after press button
        # joystick = Joystick(26, 27, 22, function_after_press=test)
        while True:
            direction = joystick.get_direction()
            print(direction)
            sleep(0.1)
    """
    def __init__(
        self,
        adc_pin_rx: int,
        adc_pin_ry: int,
        button_pin:int,
        function_after_press = None,
        voltage_ref: float = _VOLTAGE_REF,
        core_range = (40000, 30000)
    ) -> None:
        super().__init__(adc_pin_rx, voltage_ref)
        self._input_x = self._input
        self._input_y = ADC(adc_pin_ry)
        self._button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        self._function_after_press = function_after_press
        self._rx_value: int
        self._ry_value: int
        self._core_range = core_range

    def _run_event(self):
        if not self._button.value() and self._function_after_press:
            self._function_after_press()
    
    def get_direction(self):
        self._rx_value = self._input_x.read_u16()
        self._ry_value = self._input_y.read_u16()
        self._run_event()
        if self._rx_value > self._core_range[0]:
            return 'Up'
        if self._rx_value < self._core_range[1]:
            return 'Down'
        if self._ry_value > self._core_range[0]:
            return 'Right'
        if self._ry_value < self._core_range[1]:
            return 'Left'
        else: return None

class LM35(AnalogicInputs):
    pass

