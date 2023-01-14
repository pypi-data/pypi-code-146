import serial
import time

class pyAR488:
    """Class to represent AR488 USB-GPIB adapter.
    The AR488 is an Arduino-based USB-GPIB adapter.
    For details see: https://github.com/Twilight-Logic/AR488
    -> implemented by Minu
    """

    def __init__(self, port="COM0", baud=115200, timeout=1):
        try:
            self.ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
            time.sleep(2)  # await for serial interface open
        except Exception as e:
            raise Exception("error opening serial port {}".format(e))

    def __del__(self):
        self.ser.close()

    def close(self):
        self.__del__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.ser.close()

    # bus commands
    def write(self, message):
        """write a message on bus"""
        self.ser.write("{}\n\r".format(message).encode("ASCII"))

    def read(self, decode=True):
        """Read from GPIB bus, decode if specified"""
        val = self.ser.readline()
        if decode:
            val = val.decode('UTF-8')
        return val

    def raw_read(self):
        """read bytes until CR"""
        return self.ser.read_until('\n')

    def query(self, message, response_payload=False, decode=True):
        """Write message to GPIB bus and read results, if a payload is expected send '++read' too,
        decode by default un 'UTF-8'"""
        self.write(message)
        if response_payload:
            self.cmd_read()
        return self.read(decode=decode)

    # Prologix commands
    def cmd_set_address(self, address):
        """set interface address"""
        if 0 <= address <= 29:
            self.write("++addr {}".format(address))
        else:
            raise Exception('invalid GPIB address "{}"'.format(address))

    def cmd_get_address(self):
        """get interface address"""
        return self.query("++addr")

    def cmd_read(self):
        """read device reading"""
        return self.query('++read')

    def cmd_reset(self):
        """reset interface"""
        self.write('++rst')

    def cmd_ver(self):
        """get interface version"""
        self.write('++ver')

# notes:
# '\r', '\n', and '+' are control characters that must be escaped in binary data
#
# Prologix commands:
# ++addr [1-29]
# ++auto [0 | 1 | 2 | 3]
# ++clr
# ++eoi [0 | 1]
# ++eos [0 | 2 | 3 | 4]
# ++eot_enable [0 | 1]
# ++eot_char [<char>]
# ++help (unsupported)
# ++ifc
# ++llo [all]
# ++loc [all]
# ++lon (unsupported)
# ++mode [0 | 1]
# ++read [eoi | <char>]
# ++read_tmo_ms <time>
# ++rst
# ++savecfg
# ++spoll [<PAD> | all | <PAD1> <PAD2> <PAD3> ...]
# ++srq
# ++status [<byte>]
# ++trg [PAD1 ... PAD15]
# ++ver [real]
#
# Custom AR488 commands:
# ++allspoll
# ++dl
# ++default
# ++macro [1-9]
# ++ppoll
# ++setvstr [string]
# ++srqauto [0 | 1]
# ++repeat count delay cmdstring
# ++tmbus [value]
# ++verbose
