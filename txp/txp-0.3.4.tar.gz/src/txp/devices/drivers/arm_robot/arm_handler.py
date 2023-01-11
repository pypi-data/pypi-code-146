"""
This module defines the arm handler to govern this enhancer device
"""
# ============================ imports =========================================
import threading
import time
from dataclasses import dataclass
from enum import Enum

from ArmSDK.Arm_Lib import Arm_Device
from txp import settings
import logging

from txp.common.edge import SingletonMeta

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class Servo(Enum):
    def __new__(cls, *values):
        """This defines the cannonical value (int) for the enum, and allows for other
        values. Useful for human readable strings.

        Reference for this solution:
            https://stackoverflow.com/questions/43202777/get-enum-name-from-multiple-values-python
        """
        obj = object.__new__(cls)
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        # human readable value useful for sending payload information to other systems
        obj.human_readable_value = values[1]
        return obj

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    def __str__(self):
        return self.human_readable_value

    NORMAL = 0, 'Normal', 'normal'
    THERMOGRAPHIC = 1, 'Thermographic', 'thermographic'

@dataclass
class ArmPositionDescriptor:
    servo_1:int=90 #base servo
    servo_2:int=90#firt linear extender servo
    servo_3:int=90 #second linea extender servo
    servo_4:int=90 #third linear extender servo
    servo_5:int=90 #cameras rotating enhancer servo
    servo_6 = 15 #dummy value to use servo position

    def get_positions_tuple(self):
        return (self.servo_1,self.servo_2,self.servo_3,self.servo_4,self.servo_5,self.servo_6)

    def get_positions_array(self):
        return list(self.get_positions_tuple())


class ServoConnectionStatusDescriptor:
    def __init__(self,servo_name,servo_index,status):
        self._servo_name = servo_name
        self._servo_index = servo_index
        self._status = status

    def set_servo_status(self,status):
        self._status = status

    def get_servo_status(self):
        return self._status


@dataclass
class ArmServoConnectionStatus:
    """
    ArmServoConnectionStatus validates the connection status of each servo
    if there is no connection with a specific servo this will set to false the status of the specific servo disconnection
    """
    servo_1_connection_status:ServoConnectionStatusDescriptor=ServoConnectionStatusDescriptor("servo_1",1,True)
    servo_2_connection_status:ServoConnectionStatusDescriptor=ServoConnectionStatusDescriptor("servo_2",2,True)
    servo_3_connection_status:ServoConnectionStatusDescriptor=ServoConnectionStatusDescriptor("servo_3",3,True)
    servo_4_connection_status:ServoConnectionStatusDescriptor=ServoConnectionStatusDescriptor("servo_4",4,True)
    servo_5_connection_status:ServoConnectionStatusDescriptor=ServoConnectionStatusDescriptor("servo_5",5,True)

    def set_servo_status(self,servo,status):
        attr = self.__getattribute__("servo_{}_connection_status".format(servo))
        attr.set_servo_status(status)

    def all_servos_connected(self):
        for index in range(1,6):
            if not self.__getattribute__("servo_{}_connection_status".format(index)).get_servo_status():
                return False
        return True

class ArmHandler(metaclass=SingletonMeta):

    _SERVO_POS_ERROR = 8  # 5 Points of error on the servo position.

    def _get_arm_resource(self):
        log.debug("acquiring arm resource")
        return Arm_Device()

    def disable_torque(self):
        """
        Disable torque of the arm
        """
        arm = self._get_arm_resource()
        try:
            arm.Arm_serial_set_torque(0)
            time.sleep(0.1)
        finally:
            self._release_arm_resource(arm)


    def enable_torque(self):
        """
        Disable torque of the arm q
        """
        arm = self._get_arm_resource()
        try:
            arm.Arm_serial_set_torque(1)
            time.sleep(0.1)
        except Exception as ex:
            print(ex)
        finally:
            self._release_arm_resource(arm)

    def flush(self):
        """
        Flush arm commands
        """
        arm = self._get_arm_resource()
        try:
            arm.Arm_reset()
            time.sleep(0.01)
        finally:
            self._release_arm_resource(arm)

    def _get_servo_position(self,id):
        """
        get servo position by ID
        :param id: it is the number of the servo being queried its position
        :return: interger with angle value 0-180 degrees
        """

        arm = self._get_arm_resource()
        pos = None
        try:
            for retries in range(10):
                pos = arm.Arm_serial_servo_read(id)
                if pos is not None:
                    break
                else:
                    arm.Arm_reset()
                    time.sleep(0.01)
        finally:
            self._release_arm_resource(arm)
            return pos

    def get_positions(self):
        """
        returns the current position of all servos in a position object
        :return: ArmPositionDescriptor with arm position.
        """
        angle = ArmPositionDescriptor()
        angle.servo_1 = self._get_servo_position(1)
        angle.servo_2 = self._get_servo_position(2)
        angle.servo_3 = self._get_servo_position(3)
        angle.servo_4 = self._get_servo_position(4)
        angle.servo_5 = self._get_servo_position(5)
        log.info("position captured {}".format(angle))
        return angle

    def _validate_written_arm_pos(self, arm_resource, s1, s2, s3, s4, s5, s6) -> bool:
        pos_1 = arm_resource.Arm_serial_servo_read(1)
        pos_2 = arm_resource.Arm_serial_servo_read(2)
        pos_3 = arm_resource.Arm_serial_servo_read(3)
        pos_4 = arm_resource.Arm_serial_servo_read(4)
        pos_5 = arm_resource.Arm_serial_servo_read(5)
        pos_6 = arm_resource.Arm_serial_servo_read(6)  # NOTE: For some reason, the servo_6 reads None.

        log.debug(f"Arm resource written angle: {(s1, s2, s3, s4, s5, s6)}")
        log.debug(f"Arm resource read angle: {(pos_1, pos_2, pos_3, pos_4, pos_5, pos_6)}")

        return (
            abs(s1-pos_1) <= self._SERVO_POS_ERROR and
            abs(s2-pos_2) <= self._SERVO_POS_ERROR and
            abs(s3-pos_3) <= self._SERVO_POS_ERROR and
            abs(s4-pos_4) <= self._SERVO_POS_ERROR and
            abs(s5-pos_5) <= self._SERVO_POS_ERROR
        )

    def set_arm_angle_position(self, angle) -> bool:
        """
        Returns:
            True if the ARM reached the position.
        """
        arm = self._get_arm_resource()
        try:
            time_to_move = self._calculate_angle_move_time(arm,angle)
            log.debug("arm moving position")
            log.debug(f"computed arm time to wait: {time_to_move/1000} secs")
            arm.Arm_serial_servo_write6(*angle,time_to_move)
            time.sleep(time_to_move/1000)
            time.sleep(1)  # This second wait is intended to reduce effects of movement shaking of the arm
            if self._validate_written_arm_pos(arm, *angle):
                log.debug("THE ARM IS IN VALID POSITION")
                return True
            else:
                log.error("THE ARM COULD NOT REACH THE ANGLE POSITION")
                return False

        except Exception as ex:
            log.error("error moving angle")
        finally:
            self._release_arm_resource(arm)

    def _release_arm_resource(self, arm):
        log.debug("releasing arm resource")
        del arm

    def arm_connection_status(self):
        """
        This retrieves the status of servos connected.
        :return: ArmServoConnectionStatus with statuses of all servos
        """
        arm = self._get_arm_resource()
        status = True
        try:
            for servo in range(1,6):
                log.debug("ping on servo {} connection".format(servo))
                ping_result = arm.Arm_ping_servo(id)
                if ping_result is None:
                    status = False
                log.debug("ping on servo {} connection result is {}".format(servo,status))
        finally:
            self._release_arm_resource(arm)
            return status

    def is_arm_servos_connected(self):
        return

    def execute_arm_action(self,angle):
        arm = self._get_arm_resource()
        time = self._calculate_angle_move_time(arm,angle)
        arm.Arm_serial_servo_write6(*angle,time)

    def _calculate_angle_move_time(self,arm,angle):
        return 2000