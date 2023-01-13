from machine import Pin, PWM


class SimpleServo360:

    def __init__(self, pin):
        """
        :param pin: pin
        """
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.stop()

    def stop(self):
        """
        停止
        """
        self.pwm.duty_ns(1_500_000)

    def clockwise(self, speed=1000):
        """
        顺时针旋转
        :param speed: 0-1000
        """
        if speed <= 0:
            self.stop()
        elif speed > 1000:
            speed = 1000
        self.pwm.duty_ns(1_500_000 + speed * 1_000)

    def anticlockwise(self, speed=1000):
        """
        逆时针旋转
        :param speed: 0-1000
        """
        if speed <= 0:
            self.stop()
        elif speed > 1000:
            speed = 1000
        self.pwm.duty_ns(1_500_000 - speed * 1_000)


class SimpleServo180:

    def __init__(self, pin, offset=0, angle_range=None):
        """
        :param pin: pin
        :param offset: 偏移量
        :param angle_range: (-90, 90) 角度范围
        """
        if angle_range is None:
            angle_range = (-180, 180)
        self._angle = 0
        self.__angle = 2_000_000 / 180
        self.offset = offset
        self.offset_range = (-90 - offset, 90 - offset)
        self._range = None
        self.range(angle_range)
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.stop()

    def range(self, angle_range=None):
        """
        设置角度范围
        :param angle_range: (-90, 90)
        """
        if angle_range is None:
            return self._range
        self._range = (
            max(angle_range[0], self.offset_range[0]),
            min(angle_range[1], self.offset_range[1])
        )
        return self._range

    def stop(self):
        """
        停止并居中
        """
        self.angle(0)

    def angle(self, angle=None):
        """
        设置角度
        :param angle: -90~90
        """
        if angle is None:
            return self._angle
        if angle < self._range[0]:
            angle = self._range[0]
        elif angle > self._range[1]:
            angle = self._range[1]
        self.pwm.duty_ns(int(1_500_000 + (angle + self.offset) * self.__angle))


MG995D360 = SimpleServo360
MG995D180 = SimpleServo180
SG90180 = SimpleServo180
