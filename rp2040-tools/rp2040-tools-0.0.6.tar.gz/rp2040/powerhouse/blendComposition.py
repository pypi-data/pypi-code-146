from .engine import L298N
from .servo import SimpleServo180


class FourWheelServoL298N:
    def __init__(self, front_left, front_right, back_left, back_right, servo, offset=0):
        """
        :param front_left: 前左轮 (pwm, pin_A, pin_B)
        :param front_right: 前右轮 (pwm, pin_A, pin_B)
        :param back_left: 后左轮 (pwm, pin_A, pin_B)
        :param back_right: 后右轮 (pwm, pin_A, pin_B)
        :param servo: 舵机 (pin)
        """
        self.front_left = L298N(*front_left)
        self.front_right = L298N(*front_right)
        self.back_left = L298N(*back_left)
        self.back_right = L298N(*back_right)
        self.servo = SimpleServo180(servo, offset, (-90, 90))

    def stop(self):
        self.front_left.stop()
        self.front_right.stop()
        self.back_left.stop()
        self.back_right.stop()
        self.servo.stop()

    def forward(self, speed):
        """
        :param speed: 0 ~ 100
        """
        self.front_left.forward(speed)
        self.front_right.forward(speed)
        self.back_left.forward(speed)
        self.back_right.forward(speed)

    def backward(self, speed):
        """
        :param speed: 0 ~ 100
        """
        self.front_left.backward(speed)
        self.front_right.backward(speed)
        self.back_left.backward(speed)
        self.back_right.backward(speed)

    def speed(self, speed):
        """
        :param speed: -100 ~ 100
        """
        if speed == 0:
            self.stop()
        elif speed > 0:
            self.forward(speed)
        else:
            self.backward(-speed)

    def left(self, angle):
        """
        :param angle: 0 ~ 90
        """
        angle = max(angle, 0)
        self.servo.angle(-angle)

    def right(self, angle):
        """
        :param angle: 0 ~ 90
        """
        angle = max(angle, 0)
        self.servo.angle(angle)

    def angle(self, angle):
        """
        :param angle: -90 ~ 90
        """
        self.servo.angle(angle)
