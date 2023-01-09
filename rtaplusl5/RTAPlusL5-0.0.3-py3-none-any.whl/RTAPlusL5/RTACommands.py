from RTAPlusL5.logger import log

class RtaCmd:
    UP = '+'
    DOWN = '-'
    CR = '\r'

    def __init__(self):
        self._steps_per_rev = 0
        self.drive_address = 0
        self.mem_addr = 100
        self.next_inst_addr = 0
        self.multiplier = 1
        self.ramp_code = 42

    def set_address(self, address):
        """
        Set the drive address
        :param address:
        :return:
        """
        self.drive_address = address

    def valid_response_cmd(self):
        """
        Return a valid response command
        :return:
        """
        return f'{self.drive_address:02d}{CmdCode.VALID_RESPONSE}{self.CR}'

    def invalid_response_cmd(self):
        """
        Return an invalid response command
        :return:
        """
        return f'{self.drive_address:02d}{CmdCode.INVALID_RESPONSE}{self.CR}'

    def execute_cmd(self):
        """
        Execute the command
        :return:
        """
        return f'{self.drive_address:02d}{CmdCode.EXECUTE}{self.CR}'

    def stop_motor_cmd(self):
        """
        Stop the motor
        :return:
        """
        return f'{self.drive_address:02d}{CmdCode.STOP_MOTOR}{self.CR}'

    def emergency_stop_cmd(self):
        """
        Emergency stop
        :return:
        """
        return f'{self.drive_address:02d}{CmdCode.EMERGENCY_STOP}{self.CR}'

    def slow_mode_cmd(self):
        """
        Set the drive to slow mode
        :return:
        """
        self._steps_per_rev = 4000
        return f'{self.drive_address:02d}{CmdCode.SLOW_MODE}{self.CR}'

    def fast_mode_cmd(self):
        """
        Set the drive to fast mode
        :return:
        """
        self._steps_per_rev = 400
        return f'{self.drive_address:02d}{CmdCode.FAST_MODE}{self.CR}'

    def absolute_pos_reset_cmd(self):
        """
        Reset the absolute position to zero
        :return:
        """
        return f'{self.drive_address:02d}{CmdCode.ABS_POS_RESET}{self.CR}'

    def absolute_pos_set_cmd(self, pos):
        """
        Set the absolute position
        :param pos:
        :return:
        """
        sign = self.UP if pos >= 0 else self.DOWN
        return f'{self.drive_address:02d}{CmdCode.ABS_POS_SET},{sign}{pos:04d}{self.CR}'

    def absolute_pos_req_cmd(self):
        """
        Request the absolute position
        :return:
        """
        return f'{self.drive_address:02d}{ReqCode.ABS_POS_REQ}{self.CR}'

    def parse_absolute_pos(self, pos_ans):
        """
        Parse the absolute position response
        :param pos_ans:
        :return:
        """
        log.debug(f'pos_ans: {pos_ans}')
        value = None

        if pos_ans is not None and isinstance(pos_ans, str) and \
                pos_ans.startswith(f'{self.drive_address:02d}{ReqCode.ABS_POS_REQ}'):
            try:
                value = int(pos_ans[5:-1])
            except ValueError:
                log.error(f'Invalid absolute position response: {pos_ans}')
                value = None
            return value
        else:
            return value

    def current_on_cmd(self):
        """
        Turn the current on
        :return:
        """
        return f'{self.drive_address:02d}{CmdCode.CURRENT_ON}{self.CR}'

    def current_off_cmd(self):
        """
        Turn the current off
        :return:
        """
        return f'{self.drive_address:02d}{CmdCode.CURRENT_OFF}{self.CR}'

    def do_steps_cmd(self, steps, rpm, direction):
        """
        Do steps
        :param steps:
        :param rpm:
        :param direction:
        :return:
        """
        hz = self.rpm2hz(rpm)
        return f'{self.drive_address:02d}WN,{self.mem_addr:03d},{InstCode.HI_RUN_NO_RAMP},' \
               f'{hz:04d},{direction}{steps},x{self.multiplier},{self.next_inst_addr:03d}{self.CR}'

    def do_slow_mode_cmd(self, rpm, direction):
        """
        Do slow mode
        :param rpm:
        :param direction:
        :return:
        """
        hz = self.rpm2hz(rpm)
        return f'{self.drive_address:02d}WN,{self.mem_addr:03d},{InstCode.HI_FREE_RUN_NO_RAMP},' \
               f'{hz:04d},{direction},x{self.multiplier},{self.next_inst_addr:03d}{self.CR}'

    def do_fast_mode_cmd(self, rpm, direction):
        """
        Do fast mode
        :param rpm:
        :param direction:
        :return:
        """
        hz = self.rpm2hz(rpm)
        return f'{self.drive_address:02d}WN,{self.mem_addr:03d},{InstCode.HI_FREE_RUN_RAMP},' \
               f'{hz:04d},{self.ramp_code} ,{direction},x{self.multiplier},{self.next_inst_addr:03d}{self.CR}'

    def rpm2hz(self, rpm):
        """
        Convert rpm to hz
        :param rpm:
        :return:
        """
        hz_per_rpm = (self._steps_per_rev * 10) / 60.0
        hz = int(hz_per_rpm * rpm)
        return hz

    def move_w_ramp_steps_cmd(self, steps, rpm, direction):
        """
        Move with ramp steps
        :param steps:
        :param rpm:
        :param direction:
        :return:
        """
        hz = self.rpm2hz(rpm)
        return f'{self.drive_address:02d}WN,{self.mem_addr:03d},{InstCode.HI_RUN_RAMP},' \
               f'{91:03d},{self.ramp_code},{direction}{steps},x{self.multiplier},{self.next_inst_addr:03d}{self.CR}' #

    def move_w_ramp_free_cmd(self, rpm, direction):
        """
        Move with ramp free
        :param rpm:
        :param direction:
        :return:
        """
        hz = self.rpm2hz(rpm)
        return f'{self.drive_address:02d}WN,{self.mem_addr:03d},{InstCode.HI_FREE_RUN_RAMP},' \
               f'{rpm},42,{direction},x{self.multiplier},{self.next_inst_addr:03d}{self.CR}' # hz:04d

    def move_no_ramp_steps_cmd(self, steps, rpm, direction):
        """
        Move no ramp steps
        :param steps:
        :param rpm:
        :param direction:
        :return:
        """
        hz = self.rpm2hz(rpm)
        return f'{self.drive_address:02d}WN,{self.mem_addr:03d},{InstCode.HI_RUN_NO_RAMP},' \
               f'{hz:04d},{direction}{steps},x{self.multiplier},{self.next_inst_addr:03d}{self.CR}'

    def move_no_ramp_free_cmd(self, rpm, direction):
        """
        Move no ramp free
        :param rpm:
        :param direction:
        :return:
        """
        hz = self.rpm2hz(rpm)
        return f'{self.drive_address:02d}WN,{self.mem_addr:03d},{InstCode.HI_FREE_RUN_NO_RAMP},' \
               f'{hz:04d},{direction},x{self.multiplier},{self.next_inst_addr:03d}{self.CR}'


class InstCode:
    """
    Instruction codes
    """
    RUN_RAMP = '01'
    HI_RUN_RAMP = '31'
    FREE_RUN_RAMP = '02'
    HI_FREE_RUN_RAMP = '32'
    RUN_NO_RAMP = '11'
    HI_RUN_NO_RAMP = '21'
    FREE_RUN_NO_RAMP = '12'
    HI_FREE_RUN_NO_RAMP = '22'
    ZERO_SEARCH = '03'


class CmdCode:
    """
    Command codes
    """
    STOP_MOTOR = 'ES'
    EMERGENCY_STOP = 'EE'
    EXECUTE = 'PS,100'
    VALID_RESPONSE = 'Y'
    INVALID_RESPONSE = 'N'
    SLOW_MODE = 'WS,RS,D3'
    FAST_MODE = 'WS,RS,BO'
    CURRENT_ON = 'CY'
    CURRENT_OFF = 'CN'
    ABS_POS_RESET = 'RA'
    ABS_POS_SET = 'SA'


class ReqCode:
    """
    Request codes
    """
    ABS_POS_REQ = 'QA'


class SpeedMode:
    """
    Speed modes
    """
    NONE = 0
    FAST = 1
    SLOW = 2
