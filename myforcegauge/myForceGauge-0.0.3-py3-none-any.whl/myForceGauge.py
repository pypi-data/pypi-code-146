# 0.0.3

import serial
import time

class ForceGauge_communication:
    def __init__(self):
        self._ser: serial.serialwin32.Serial = None
        self._alldata = ''
        self._time = time.perf_counter()

    def __del__(self):
        self.exit()

    def init(self, COM):
        try:
            self._ser = serial.Serial(COM, baudrate=460800, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE, timeout=0.0001)
            time.sleep(0.001)
            self._ser.write(b'XAG\r')
            time.sleep(0.001)
            return 1
        except serial.serialutil.SerialException:
            return -1

    def read(self):
        self._alldata = self._alldata + self._ser.read_all().decode()
        values = self._alldata.split('\r')
        for i in range(1, len(values)):
            now_value = values[-i]
            if len(now_value)==20:
                break
        now_value = float(now_value[1:7])
        return now_value

    def reset_zero(self):
        self._ser.write(b'Z\r')
        time.sleep(0.0001)
        _ = self._ser.read_all()

    def exit(self):
        try:
            self._ser.write(b'XAS\r')
            time.sleep(0.0001)
            self._ser.close()
            print('Port is closed')
        except serial.serialutil.PortNotOpenError:
            pass


