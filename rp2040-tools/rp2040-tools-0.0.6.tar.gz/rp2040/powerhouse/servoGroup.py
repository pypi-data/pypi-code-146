from .servo import SimpleServo180


class RobotArm:

    def __init__(self, hand, forearm, big_arm, hand_offset=0, forearm_offset=0, big_arm_offset=0):
        """
        :param hand: 手 (pin)
        :param forearm: 前臂 (pin)
        :param big_arm: 大臂 (pin)
        """
        self.hand = SimpleServo180(hand, hand_offset, (-90, 90))
        self.forearm = SimpleServo180(forearm, forearm_offset, (-90, 90))
        self.big_arm = SimpleServo180(big_arm, big_arm_offset, (-90, 90))
        self.move(0, -30, 0)

    def stop(self):
        self.hand.stop()
        self.forearm.angle(-30)
        self.big_arm.stop()

    def move(self, hand, forearm, big_arm):
        self.hand.angle(hand)
        self.forearm.angle(forearm)
        self.big_arm.angle(big_arm)

    def set_offset(self, hand, forearm, big_arm):
        self.hand.offset = hand
        self.forearm.offset = forearm
        self.big_arm.offset = big_arm

    def set_range(self, hand, forearm, big_arm):
        self.hand.range(hand)
        self.forearm.range(forearm)
        self.big_arm.range(big_arm)


