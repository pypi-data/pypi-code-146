from RTAPlusL5.SerialComm import SerialComm
from RTAPlusL5.RTACommands import RtaCmd
from RTAPlusL5.logger import log


class RTAPlusL5:
    """
    RTAPlusL5_ class to interface with RTAPlusL5 motor controller devices
    """
    def __init__(self, device_label, address):
        """
        Constructor will initiate serial port communication in rs485 mode and define address for device
        :param device_label: Device label assigned by the operating system when the device is connected
        :param address: Defined by the address switch mounted in the device from 1 to 16
        """
        self._cmd = RtaCmd()
        self._cmd.set_address(address)
        self._comm = SerialComm(device_label, self._cmd)

    def open_communication(self):
        """
        Opens communication with serial device
        :return: None
        """
        self._comm.open_communication()

    def close_communication(self):
        """
        Closes communication with serial device
        :return: None
        """
        self._comm.close_communication()

    def check_communication(self):
        """
        Checks communication with serial device
        :return: None
        """
        log.info(f"Answer from device: {self._comm.read_data_transaction(self._cmd.absolute_pos_reset_cmd())}")

    def stop_motor(self):
        """
        Stops the motor
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.stop_motor_cmd())

    def emergency_stop(self):
        """
        Stops the motor
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.emergency_stop_cmd())

    def current_on(self):
        """
        Turns on current
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.current_on_cmd())

    def current_off(self):
        """
        Turns off current
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.current_off_cmd())

    def absolute_pos_reset(self):
        """
        Resets absolute position
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.absolute_pos_reset_cmd())

    def absolute_pos_set(self, pos):
        """
        Sets absolute position
        :param pos: Position to set
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.absolute_pos_set_cmd(pos))

    def absolute_pos_get(self):
        """
        Gets absolute position
        :return: Absolute position
        """
        return self._cmd.parse_absolute_pos(self._comm.read_data_transaction(self._cmd.absolute_pos_req_cmd()))

    def set_slow_mode(self):
        """
        Sets slow mode
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.slow_mode_cmd())

    def set_fast_mode(self):
        """
        Sets fast mode
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.fast_mode_cmd())

    def move_up_free_w_ramp(self, rpm):
        """
        Moves motor free with ramp
        :param rpm: Speed in rpm
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.move_w_ramp_free_cmd(rpm, self._cmd.UP))
        self._comm.write_data_transaction(self._cmd.execute_cmd())

    def move_down_free_w_ramp(self, rpm):
        """
        Moves motor free with ramp
        :param rpm: Speed in rpm
        :return: None
        """
        self._comm.write_data_transaction(self._cmd.move_w_ramp_free_cmd(rpm, self._cmd.DOWN))
        self._comm.write_data_transaction(self._cmd.execute_cmd())

    def move_steps_w_ramp(self, steps, rpm):
        """
        Moves motor steps with ramp
        :param steps: Number of steps to move
        :param rpm: Speed in rpm
        :return: None
        """
        # ternary operation to determine direction cmd based on steps
        direction = self._cmd.UP if steps > 0 else self._cmd.DOWN
        self._comm.write_data_transaction(self._cmd.move_w_ramp_steps_cmd(abs(steps), rpm, direction))
        self._comm.write_data_transaction(self._cmd.execute_cmd())

if __name__ == '__main__':
    import logging
    import time
    from device_labels import DEV_TTY

    log.setLevel(logging.DEBUG)

    DRIVER_ADDRESS = 0
    motor_driver = RTAPlusL5(DEV_TTY, DRIVER_ADDRESS)
    motor_driver.open_communication()
    motor_driver.absolute_pos_reset()
    motor_driver.current_on()
    motor_driver.stop_motor()
    motor_driver.move_steps_w_ramp(-40000, 100)
    #time.sleep(5)
    # motor_driver.move_steps_w_ramp(-40000, 100)
    #log.info(f'Absolut position is: {motor_driver.absolute_pos_get()}')
    #motor_driver.stop_motor()
    #motor_driver.current_off()
    motor_driver.close_communication()
