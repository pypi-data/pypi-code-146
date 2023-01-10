import serial
import serial.rs485
import threading
from RTAPlusL5.logger import log


class SerialComm:
    """
    RTAPlusL5_ class to interface with RTAPlusL5 motor controller devices
    """
    TRYOUTS_LIMIT = 1
    mutex = threading.Lock()

    def __init__(self, device_label, rta_cmd_ref):
        """
        Constructor will initiate serial port communication in rs485 mode and define address for device
        :param device_label: Device label assigned by the operating system when the device is connected
        """
        self._port = serial.rs485.RS485(device_label,
                                        baudrate=9600,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS,
                                        timeout=0.02
                                        )

        self._port.rs485_mode = serial.rs485.RS485Settings()
        self.mutex = threading.Lock()
        self._cmd = rta_cmd_ref

    def open_communication(self):
        """
        Opens communication with serial device
        :return:
        """
        opening_port_trials = 0
        if self._port.isOpen():
            self._port.flush()
            log.info("Port is Open!")
        elif not self._port.isOpen() and opening_port_trials < 5:
            log.info("Port closed, trying to open...")
            self._port.open()
            opening_port_trials += 1
            self.open_communication()

    def close_communication(self):
        """
        Closes communication with serial device
        :return: None
        """
        self._port.flush()
        self._port.close()
        log.info('Closing communication with device')

    def read_data_transaction(self, message):
        """
        Reads data from device
        :param message:
        :return:
        """
        message = self._instruction_exchange(message)
        return message

    def write_data_transaction(self, message):
        """
        Writes data to device
        :param message:
        :return:
        """
        return self._instruction_exchange(message)

    def _instruction_exchange(self, cmd):
        """
        Sends command to device and receives response
        :param cmd:
        :return:
        """
        fine_transaction = False
        tryouts = 0
        while not fine_transaction and tryouts < self.TRYOUTS_LIMIT:
            self._send_message(cmd)
            message = self._receive_message()
            if message != '':
                if message == self._cmd.valid_response_cmd():
                    log.debug(f"VALID COMMAND: {cmd}")
                    return message
                elif message == self._cmd.invalid_response_cmd():
                    log.debug(f"INVALID COMMAND: {cmd}")
                    return message
                elif len(message) > 1:
                    log.debug(f"VALID RESPONSE: {message}")
                    return message
                else:
                    log.debug(f"NO RESPONSE: {message}")
                    return message
            else:
                log.error("BAD TRANSACTION")
                fine_transaction = False
                self._port.flush()
            tryouts += 1

    def _send_message(self, message):
        """
        Sends message to device
        :param message:
        :return:
        """
        log.debug(f"TXin' this: {message}")
        self.mutex.acquire()
        try:
            self._port.write(message.encode('ascii'))  # self.get_ascii_list(message)
        finally:
            self.mutex.release()
    def _receive_message(self):
        """
        Receives message from device
        :return:
        """
        self.mutex.acquire()
        try:
            message = self._port.readline()
        finally:
            self.mutex.release()
        try:
            message = message.decode('ascii')
        except UnicodeDecodeError:
            log.error("UnicodeDecodeError")
            message = ''
        log.debug(f"RXin' this: {message}")
        return message

    @staticmethod
    def get_ascii_list(string):
        return [ord(c) for c in string]
