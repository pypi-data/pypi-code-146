import binascii
import re
import serial
from serial.serialutil import (SerialException, SerialTimeoutException)
from .exceptions import SmartmeterException, SmartmeterSerialException, SmartmeterTimeoutException
from .supplier import SUPPLIERS
from .decrypt import Decrypt
from .obisdata import ObisData


class Smartmeter():
    def __init__(self,
                 supplier_name: str,
                 port: str,
                 key_hex_string : str,
                 interval : int = 1,
                 baudrate : int = 2400,
                 parity: str = serial.PARITY_NONE,
                 stopbits: str = serial.STOPBITS_ONE,
                 bytesize: str = serial.EIGHTBITS) -> None:
        self._supplier_name = supplier_name
        self._port: str = port
        self._key_hex_string = key_hex_string
        self._baudrate : int = baudrate
        self._parity: str = parity
        self._stopbits: str = stopbits
        self._bytesize: str = bytesize
        self._interval: int = interval

        self._mySerial : serial = None
        self._serial_read_chunk_size : int = 100
        self._obisData : ObisData = None

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, is_running):
        self._is_running = is_running

    @property
    def obisData(self) -> ObisData:
        return self._obisData

    @obisData.setter
    def obisData(self, obisData):
        self._obisData = obisData

    def close(self) -> None:
        self.is_running = False

    # read method was mainly taken from https://github.com/tirolerstefan/kaifa
    def read(self) -> None:
        self.__open_serial()

        supplier = SUPPLIERS.get(self._supplier_name)
        self._is_running = self._mySerial.isOpen()

        stream = b''      # filled by serial device
        frame1 = b''      # parsed telegram1
        frame2 = b''      # parsed telegram2

        frame1_start_pos = -1          # pos of start bytes of telegram 1 (in stream)
        frame2_start_pos = -1          # pos of start bytes of telegram 2 (in stream)

        timeout_counter = 0
        
        # "telegram fetching loop" (as long as we have found two full telegrams)
        # frame1 = first telegram (68fafa68), frame2 = second telegram (68727268)
        while self._is_running:
            # Read in chunks. Each chunk will wait as long as specified by
            # serial timeout. As the meters we tested send data every 5s the
            # timeout must be <5. Lower timeouts make us fail quicker.
            byte_chunk = self._mySerial.read(size=self._serial_read_chunk_size)
            stream += byte_chunk
            frame1_start_pos = stream.find(supplier.frame1_start_bytes)
            frame2_start_pos = stream.find(supplier.frame2_start_bytes)

            # fail as early as possible if we find the segment is not complete yet.
            if((stream.find(supplier.frame1_start_bytes) < 0)
                    or (stream.find(supplier.frame2_start_bytes) <= 0)
                    or (stream[-1:] != supplier.frame2_end_bytes)
                    or (len(byte_chunk) == self._serial_read_chunk_size)):
                if (timeout_counter < 15):
                    timeout_counter+=1              
                    continue
                else:
                    raise SmartmeterTimeoutException()
            
            timeout_counter = 0
            if (frame2_start_pos != -1):
                # frame2_start_pos could be smaller than frame1_start_pos
                if frame2_start_pos < frame1_start_pos:
                    # start over with the stream from frame1 pos
                    stream = stream[frame1_start_pos:len(stream)]
                    continue

                # we have found at least two complete telegrams
                regex = binascii.unhexlify('28' + supplier.frame1_start_bytes_hex + '7c' + supplier.frame2_start_bytes_hex + '29')  # re = '(..|..)'
                my_list = re.split(regex, stream)
                my_list = list(filter(None, my_list))  # remove empty elements
                # l after split (here in following example in hex)
                # l = ['68fafa68', '53ff00...faecc16', '68727268', '53ff...3d16', '68fafa68', '53ff...d916', '68727268', '53ff.....']

                # take the first two matching telegrams
                for i, el in enumerate(my_list):
                    if el == supplier.frame1_start_bytes:
                        frame1 = my_list[i] + my_list[i + 1]
                        frame2 = my_list[i + 2] + my_list[i + 3]
                        break

                # check for weird result -> exit
                if (len(frame1) == 0) or (len(frame2) == 0):
                    self.is_running = False

                break

        dec = Decrypt(supplier, frame1, frame2, self._key_hex_string)
        dec.parse_all()

        self.obisData = ObisData(dec, supplier.supplied_values)

        self.__close_serial()

    def __open_serial(self):
        try:
            self._mySerial = serial.Serial(
                port=self._port,
                baudrate=self._baudrate,
                parity=self._parity,
                stopbits=self._stopbits,
                bytesize=self._bytesize,
                timeout=self._interval)
        except SerialTimeoutException as ex:
            raise SmartmeterTimeoutException(f"'{self._port}' has a timeout.") from ex
        except SerialException as ex:
            raise SmartmeterSerialException(f"'{self._port}' cannot be opened.") from ex
        except Exception as ex:
            raise SmartmeterException(f"Connection to '{self._port}' failed.") from ex

    def __close_serial(self):
        try:
            self._mySerial.close()
        except Exception as ex:
            raise SmartmeterException(f"Closing port '{self._port}' failed.") from ex
