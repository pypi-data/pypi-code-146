"""pysentio - constants"""

NAME = 'pysentio'
VERSION = '0.0.52'

SERIAL_READ_TIMEOUT = 2

DEFAULT_BAUD = 57600
DEFAULT_SERIALPORT = '/dev/ttyUSB1'

CONFIG = 'config'
FAN = 'fan'
FAN_VAL = 'fan val'
GET = 'get'
HEATTIMER = 'heattimer'
HEATTIMER_VAL = 'heattimer val'
HUMIDITY_VAL = 'humidity val'
INFO = 'info'
LIGHT = 'light'
LIGHT_VAL = 'light val'
SET = 'set'
SAUNA = 'sauna'
SAUNA_VAL = 'sauna val'
STATUS = 'status'
TEMP_BENCH_VAL = 'temp-bench'
TEMP_HEATER_VAL = 'temp-heater val'
TIMER = 'timer'
TIMER_VAL = 'timer val'
USER_PROG = 'user-prog'
USER_PROG_VAL = 'user-prog val'

SAUNA_RESPONSE = {
    CONFIG: 'CONFIG',
    FAN: 'FAN',
    FAN_VAL: 'FAN',
    HEATTIMER: 'HEATTIMER',
    HEATTIMER_VAL: 'HEATTIMER',
    INFO: 'INFO',
    LIGHT: 'LIGHT',
    SAUNA: 'SAUNA',
    STATUS: 'STATUS',
    TEMP_BENCH_VAL: 'TEMP-BENCH',
    TEMP_HEATER_VAL: 'TEMP-HEATER',
    USER_PROG: 'USER-PROG',
    USER_PROG_VAL: 'USER-PROG',
}