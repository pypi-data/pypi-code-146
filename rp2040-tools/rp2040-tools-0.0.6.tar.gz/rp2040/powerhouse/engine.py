from machine import Pin, PWM


class Engine:

    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(1000)
        self.pwm.duty_u16(0)

    def speed(self, speed):
        """
        speed: 0 ~ 100
        :param speed: int
        """
        self.pwm.duty_u16(speed * 65535 // 100)

    def stop(self):
        self.pwm.duty_u16(0)


class L298N:

    def __init__(self, pwm, pin_A, pin_B, reverse=False):
        self.pwm = PWM(Pin(pwm))
        self.pwm.freq(1000)
        self.pin_A = Pin(pin_A, Pin.OUT)
        self.pin_B = Pin(pin_B, Pin.OUT)
        self.reverse = reverse
        self.stop()

    def stop(self):
        self.pwm.duty_u16(0)
        self.pin_A.off()
        self.pin_B.off()

    def forward(self, speed):
        """
        speed: 0 ~ 100
        :param speed: int
        """
        if self.reverse:
            self.pin_A.off()
            self.pin_B.on()
        else:
            self.pin_A.on()
            self.pin_B.off()
        self.pwm.duty_u16(speed * 65535 // 100)

    def backward(self, speed):
        """
        speed: 0 ~ 100
        :param speed: int
        """
        if self.reverse:
            self.pin_A.on()
            self.pin_B.off()
        else:
            self.pin_A.off()
            self.pin_B.on()
        self.pwm.duty_u16(speed * 65535 // 100)

    def run(self, speed):
        """
        speed: -100 ~ 100
        :param speed: int
        """
        if speed == 0:
            self.stop()
        elif speed > 0:
            self.forward(speed)
        else:
            self.backward(-speed)

