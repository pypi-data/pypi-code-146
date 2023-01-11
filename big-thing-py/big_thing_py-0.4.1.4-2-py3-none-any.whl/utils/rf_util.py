from big_thing_py.utils import *

from enum import Enum


try:
    from RF24 import RF24, RF24_PA_LOW, RF24_PA_MAX
except ImportError:
    pass
    # print('RF24 not found', 'red')


class SoPRFProtocol(Enum):
    REG = 'REG'
    RACK = 'RACK'
    VAL = 'VAL'
    LIVE = 'LIVE'
    EXEC = 'EXEC'
    EACK = 'EACK'


class SoPRFPowerMode(Enum):
    try:
        LOW = RF24_PA_LOW
        HIGH = RF24_PA_MAX
    except Exception:
        pass
        # SOPLOG_DEBUG('RF24_PA_LOW or RF24_PA_MAX not found', 'red')


class SoPRFMessage:
    def __init__(self, protocol_type: SoPRFProtocol, device_id: bytearray, service_name: str, payload: bytearray) -> None:
        self.protocol_type = protocol_type
        self.device_id = device_id
        self.service_name = service_name
        self.payload = payload


def decode_RF_message(raw_msg: bytearray) -> SoPRFMessage:
    try:
        protocol_type = SoPRFProtocol(
            raw_msg[:4].rstrip().rstrip(b'\x00').decode().upper())
        device_id = raw_msg[4:8].decode()
        service_name = raw_msg[8:16].rstrip().rstrip(b'\x00').decode()
        payload = raw_msg[16:32].decode()

        return SoPRFMessage(protocol_type=protocol_type, device_id=device_id, service_name=service_name, payload=payload)
    except Exception as e:
        SOPLOG_DEBUG('[mqtt_util.py|dict_to_json_string]' + str(e), 'red')
        return False


def encode_RF_message(msg: SoPRFMessage) -> bytearray:

    protocol_type = bytearray(msg.protocol_type.value.encode())
    device_id = msg.device_id
    service_name = bytearray(msg.service_name.encode())
    payload = msg.payload

    return protocol_type + device_id + service_name + payload
