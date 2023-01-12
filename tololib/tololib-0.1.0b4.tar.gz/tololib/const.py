from enum import IntEnum

DEFAULT_PORT = 51500

DEFAULT_RETRY_COUNT = 3
DEFAULT_RETRY_TIMEOUT = 1

MESSAGE_PREFIX = b"\xAA\xAA"
MESSAGE_SUFFIX = b"\x55\x55"


class AromaTherapy(IntEnum):
    A = 0
    B = 1


class Calefaction(IntEnum):
    HEAT = 0
    INACTIVE = 1
    UNCLEAR = 2  # TODO find correct meaning
    KEEP = 3


class LampMode(IntEnum):
    MANUAL = 0
    AUTOMATIC = 1


class Model(IntEnum):
    DOMESTIC = 0
    COMMERCIAL = 1


class SettingsMessageLength(IntEnum):
    REQUEST = 0
    RESPONSE = 8


class StatusMessageLength(IntEnum):
    REQUEST = 0
    RESPONSE = 17
