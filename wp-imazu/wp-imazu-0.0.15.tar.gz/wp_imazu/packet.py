"""Wall Pad Imazu Packet"""

import copy
import logging
from abc import ABC
from enum import Enum
from typing import Optional

_LOGGER = logging.getLogger(__name__)


class Device(Enum):
    """Imazu device"""
    GUARD = "16"
    THERMOSTAT = "18"
    LIGHT = "19"
    DIMMING = "1a"
    GAS = "1b"
    AC = "1c"
    SWITCH = "1f"
    AWAY_MODE = "2a"
    FAN = "2b"
    EV = "34"
    USAGE = "43"
    WPD_AC = "48"  # 에어컨  711102711218711300 712102712217712300 // On/Off, 현재온도, 설정온도 추정.
    IGNORE = "4b"


class Cmd(Enum):
    """Packet cmd"""
    SCAN = '01'
    CHANGE = '02'
    STATUS = '04'


class ValueType(Enum):
    """Packet value type"""
    BOOL = "40"
    MULTI = "41"
    EV = "41"
    DIM = "42"
    VALVE = "43"
    MODE = "46"
    TEMP = "45"
    SPEED = "44"
    SWITCH = "57"
    ACFAN = "5d"
    ACMODE = "5c"


class ImazuPacket(ABC):
    """Abstract imazu packet
    0: f7
    1: len
    2: 01 or 1a(thermo)
    3: device
    4: cmd
    5: value_type
    6: sub
    7: change_value
    8: state_value
    9 checksum
    10: ee
    """

    def __init__(self, packet: list[str]):
        self.state: dict = {}

        self.packet = packet
        self.len = int(packet[1], 16)
        self.type = packet[2]  # 01 or 1a(thermo)
        self.device = Device(packet[3])
        self.cmd = Cmd(packet[4])
        self.value_type = ValueType(packet[5])
        self.sub = packet[6]

        self.change_value = packet[7]
        self.state_value = packet[8: -2]
        self.checksum = packet[-2:-1]

    @property
    def name(self) -> str:
        """Name"""
        return self.device.name

    @property
    def room_id(self) -> int:
        """RoomId"""
        return int(self.sub[:1], 16)

    @property
    def sub_id(self) -> int:
        """SubId"""
        return int(self.sub[1:2], 16)

    @property
    def device_id(self) -> str:
        """DeviceId"""
        return f'{self.device.value}_{self.room_id}_{self.sub_id}'

    def description(self) -> str:
        """Description"""
        desc = f'{self.cmd.name}: {self.name}({self.device_id})'
        if self.cmd == Cmd.SCAN:
            return desc
        if self.cmd == Cmd.CHANGE:
            return f'{desc}, change: {" ".join(self.change_value)}'
        if self.cmd == Cmd.STATUS:
            return f'{desc}, state: {" ".join(self.state_value)}'
        return desc

    def hex(self) -> str:
        """Create a str of hexadecimal numbers from a ImazuPacket object."""
        return ''.join(self.packet)

    def parse_state_packets(self) -> list:
        """State packet Parse"""
        _LOGGER.warning('%s not implement set status, %s', self.name, ''.join(self.packet))
        return []

    def _copy_state_packets(self, states: list[list[str]], parse_state) -> list:
        """State packet Copy"""
        packets = []
        for idx in list(range(len(states))):
            packet = copy.deepcopy(self)
            packet.sub = f'{self.room_id}{idx + 1}'
            packet.state_value = states[idx]
            packet.state = parse_state(packet.state_value)
            packets.append(packet)
        return packets

    def make_base(self, cmd: Cmd, value_type: ValueType) -> bytearray:
        """Base packet Make"""
        # 01 or 1a, device, cmd, value_type, sub, change_value, state_value
        packet: bytearray = bytearray.fromhex(self.type + str(self.device.value))
        packet.append(int(str(cmd.value), 16))
        packet.append(int(str(value_type.value), 16))
        packet.append(int(self.sub, 16))
        return packet

    def make_scan(self, value_type: ValueType) -> bytearray:
        """Scan packet Make"""
        packet = self.make_base(Cmd.SCAN, value_type)
        packet.append(0)
        packet.append(0)
        return packet


class GuardPacket(ImazuPacket):
    """Imazu guard packet"""


class ThermostatPacket(ImazuPacket):
    """Imazu thermostat packet

    - SCAN
    > f7 0b 01 18 01 46 10 00 00 b2 ee
    > f7 22 01 18 04 46 10 00 041415 041412 04140d 041105 000000 000000 000000 000000 94 ee
    > f7 0b 01 18 01 46 11 00 00 b4 ee
    < f7 0d 01 18 04 46 11 00 041415 b5 ee

    - OFF
    > F7 0B 01 18 02 46 11 04 00 B4 EE

    - ON
    > F7 0B 01 18 02 46 11 01 00 B1 EE

    - TEMP
    > F7 0B 01 18 02 45 11 14 00 A7 EE // 20
    > F7 0B 01 18 02 45 11 15 00 A6 EE // 21
    > F7 0B 01 18 02 45 11 16 00 A5 EE // 22
    """

    class Mode(Enum):
        """Thermostat mode"""
        HEAT = "01"
        OFF = "04"
        AWAY = "07"

    def parse_state_packets(self) -> list:
        """State packet Parse"""
        if self.value_type == ValueType.MODE:
            if len(self.state_value) % 3 == 0:
                # zips 난방분배기 (주)한성시스코, GSTART , 클리오(주)
                def parse_state(state_value: list[str]):
                    return {
                        'mode': ThermostatPacket.Mode(state_value[0]),
                        'temp': int(state_value[1], 16),
                        'target': int(state_value[2], 16)
                    }

                if self.sub_id == 0 and self.change_value == '00':
                    states = [self.state_value[i: i + 3]
                              for i in range(0, len(self.state_value), 3)]
                    states = list(filter(lambda x: x != ['00', '00', '00'], states))
                    return super()._copy_state_packets(states, parse_state)

                self.state = parse_state(self.state_value)
                return [self]

            _LOGGER.warning('%s unknown thermostat, %s', self.name, ''.join(self.packet))
            return []
        _LOGGER.warning('%s unknown state packet, %s, %s',
                        self.name, self.value_type.value, ''.join(self.packet))
        return []

    def make_scan_mode(self) -> bytearray:
        """Scan packet Make"""
        return self.make_scan(ValueType.MODE)

    def make_change_mode(self, mode: Mode) -> bytearray:
        """Mode packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.MODE)
        packet.append(int(str(mode.value), 16))
        packet.append(0)
        return packet

    def make_change_target_temp(self, temp: int) -> bytearray:
        """Target temp packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.TEMP)
        packet.append(temp)
        packet.append(0)
        return packet


class LightPacket(ImazuPacket):
    """Imazu light packet

    - SCAN
    > f7 0b 01 19 01 40 11 00 00 b4 ee
    < f7 0b 01 19 04 40 11 00 02 b3 ee

    - OFF
    > f7 0b 01 19 02 40 11 02 00 b5 ee
    < f7 0b 01 19 04 40 11 02 02 b1 ee

    - ON
    > f7 0b 01 19 02 40 11 01 00 b6 ee
    < f7 0b 01 19 04 40 11 01 01 b1 ee
    """

    class Power(Enum):
        """Light Power"""
        ON = "01"
        OFF = "02"

    def parse_state_packets(self) -> list:
        """State packet Parse"""
        if self.value_type == ValueType.BOOL:

            def parse_state(state_value: list[str]):
                return {'power': LightPacket.Power(state_value[0])}

            if self.sub_id == 0 and self.change_value == '00':
                states = [self.state_value[i: i + 1] for i in range(0, len(self.state_value), 1)]
                return super()._copy_state_packets(states, parse_state)

            self.state = parse_state(self.state_value)
            if len(self.state_value) > 1:
                _LOGGER.warning('%s unknown more status, %s, %s',
                                self.name, ' '.join(self.state_value), ' '.join(self.packet))
            return [self]

        _LOGGER.warning('%s unknown state packet, %s, %s',
                        self.name, self.value_type.value, ''.join(self.packet))
        return []

    def make_scan_bool(self) -> bytearray:
        """Scan packet Make"""
        return self.make_scan(ValueType.BOOL)

    def make_change_power(self, power: Power) -> bytearray:
        """Power packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.BOOL)
        packet.append(int(str(power.value), 16))
        packet.append(0)
        return packet


class DimmingPacket(ImazuPacket):
    """Imazu dimming packet"""


class GasPacket(ImazuPacket):
    """Imazu gas packet

    - SCAN
    > F7 0B 01 1B 01 43 11 00 00 B5 EE  F70B011B0143110000B5EE
    < F7 0D 01 1B 04 43 11 00 040000 B2 EE   << 열림상태
    < F7 0D 01 1B 04 43 11 00 030000 B5 EE   << 닫힘상태

    - CLOSE
    > F7 0B 01 1B 02 43 11 03 00 B5 EE
    < F7 0B 01 1B 04 43 11 03 03 B0 EE
    """

    class Valve(Enum):
        """Gas Valve"""
        CLOSE = "03"
        OPEN = "04"

    def parse_state_packets(self) -> list:
        """State packet Parse"""
        if self.value_type == ValueType.VALVE:
            self.state = {'valve': GasPacket.Valve(self.state_value[0])}
            return [self]

        _LOGGER.warning('%s unknown state packet, %s, %s',
                        self.name, self.value_type.value, ''.join(self.packet))
        return []

    def make_scan_valve(self) -> bytearray:
        """Scan packet Make"""
        return self.make_scan(ValueType.VALVE)

    def make_change_valve_close(self) -> bytearray:
        """Valve close packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.VALVE)
        packet.append(int(GasPacket.Valve.CLOSE.value, 16))
        packet.append(0)
        return packet


class AcPacket(ImazuPacket):
    """Imazu ac packet"""


class SwitchPacket(ImazuPacket):
    """Imazu switch packet

    - SCAN
    > f7 0b 01 1f 01 40 10 00 00 b3 ee
    < f7 0c 01 1f 04 40 10 00 0101 b1 ee
    > f7 0b 01 1f 01 40 11 00 00 b2 ee
    < f7 0b 01 1f 04 40 11 00 01 b6 ee

    - OFF
    > F7 0B 01 1F 02 40 11 02 00 B3 EE
    < F7 0B 01 1F 04 40 11 02 02 B7 EE

    - ON
    > F7 0B 01 1F 02 40 11 01 00 B0 EE
    < F7 0B 01 1F 04 40 11 01 01 B7 EE
    """

    class Power(Enum):
        """Switch Power"""
        ON = "01"
        OFF = "02"

    def parse_state_packets(self) -> list:
        """State packet Parse"""
        if self.value_type == ValueType.BOOL:

            def parse_state(state_value: list[str]):
                return {'power': SwitchPacket.Power(state_value[0])}

            if self.sub_id == 0 and self.change_value == '00':
                states = [self.state_value[i: i + 1] for i in range(0, len(self.state_value), 1)]
                return super()._copy_state_packets(states, parse_state)

            self.state = parse_state(self.state_value)

            if len(self.state_value) > 1:
                _LOGGER.warning('%s unknown more status, %s, %s',
                                self.name, ' '.join(self.state_value), ' '.join(self.packet))
            return [self]

        _LOGGER.warning('%s unknown state value_type: %s, %s',
                        self.name, self.value_type.value, ''.join(self.packet))
        return []

    def make_scan_bool(self) -> bytearray:
        """Scan packet Make"""
        return self.make_scan(ValueType.BOOL)

    def make_change_power(self, power: Power) -> bytearray:
        """Power packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.BOOL)
        packet.append(int(str(power.value), 16))
        packet.append(0)
        return packet


class AwayModePacket(ImazuPacket):
    """Imazu away mode packet
    < f7 0e 01 2a 04 40 10 00 19 02 1b 04 82 ee
    < f7 0e 01 2a cmd:04 type:40 sub:10 send:00 data:19021b04 cs:82 ee
    """

    class Power(Enum):
        """AwayMode Power"""
        ON = "01"
        OFF = "02"

    class Valve(Enum):
        """AwayMode Valve"""
        CLOSE = "03"
        OPEN = "04"

    def parse_state_packets(self) -> list:
        """State packet Parse"""
        if self.value_type == ValueType.BOOL:
            def parse_state(state_value: list[str]):
                device = Device(state_value[0])
                if device == Device.LIGHT:
                    return {'power': AwayModePacket.Power(state_value[1])}
                if device == Device.GAS:
                    return {'valve': AwayModePacket.Valve(state_value[1])}
                _LOGGER.warning('%s unknown state device: %s, %s',
                                self.name, self.device.name, ''.join(self.packet))
                return {}

            states = [self.state_value[i: i + 2] for i in range(0, len(self.state_value), 2)]
            return super()._copy_state_packets(states, parse_state)
        _LOGGER.warning('%s unknown state value_type: %s, %s',
                        self.name, self.value_type.value, ''.join(self.packet))
        return []

    def make_scan_bool(self) -> bytearray:
        """Scan packet Make"""
        return self.make_scan(ValueType.BOOL)

    def make_change_power(self, power: Power) -> bytearray:
        """Power packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.BOOL)
        packet.append(int(str(power.value), 16))
        packet.append(0)
        return packet

    def make_change_valve(self, valve: Valve) -> bytearray:
        """Vavle packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.VALVE)
        packet.append(int(str(valve.value), 16))
        packet.append(0)
        return packet


class FanPacket(ImazuPacket):
    """Imazu fan packet
    - SCAN
    > f7 0b 01 2b 01 40 11 00 00 86 ee
    < f7 0c 01 2b 04 40 11 00 0200 86 ee
    > f7 0b 01 2b 01 41 11 00 00 87 ee
    < f7 0c 01 2b 04 41 11 00 0200 87 ee

    - OFF
    > f7 0b 01 2b 02 40 11 02 00 87 ee
    < f7 0c 01 2b 04 41 2b0440 11 00 0207 81 ee

    - ON / 1
    > f7 0b 01 2b 02 42 11 01 00 86 ee
    < f7 0c 01 2b 04 41 2b0440 11 00 0101 84 ee

    - ON / 2
    > f7 0b 01 2b 02 42 11 03 00 84 ee
    < f7 0c 01 2b 04 41 2b0440 11 00 0103 86 ee

    - ON / 3
    > f7 0b 01 2b 02 42 11 07 00 80 ee
    < f7 0c 01 2b 04 42 11 07 0107 87 ee
    < f7 0c 01 2b 04 41 2b0440 11 00 0107 82 ee
    """

    class Power(Enum):
        """Fan power"""
        ON = "01"
        OFF = "02"

    class Speed(Enum):
        """Fan speed"""
        OFF = "00"
        LOW = "01"
        MEDIUM = "03"
        HIGH = "07"

    def parse_state_packets(self) -> list:
        """State packet Parse"""
        if len(self.state_value) > 2:
            _LOGGER.warning('%s unknown more status, %s, %s',
                            self.name, ' '.join(self.state_value), ' '.join(self.packet))

        def parse_state(state_value: list[str]):
            return {
                'power': FanPacket.Power(state_value[0]),
                'speed': FanPacket.Speed(state_value[1]),
            }

        if self.value_type in [ValueType.BOOL, ValueType.DIM]:
            self.state = parse_state(self.state_value)
            return [self]

        if self.value_type == ValueType.MULTI:
            if self.sub == '2b':
                self.sub = self.packet[9]
                self.change_value = self.packet[10]
                self.state_value = self.packet[11: -2]
                self.checksum = self.packet[-2:-1]

            self.state = parse_state(self.state_value)
            return [self]

        _LOGGER.warning('%s unknown state value_type: %s, %s',
                        self.name, self.value_type.value, ''.join(self.packet))
        return []

    def make_scan_bool(self) -> bytearray:
        """Scan packet Make"""
        return self.make_scan(ValueType.BOOL)

    def make_change_power_off(self) -> bytearray:
        """Power off packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.BOOL)
        packet.append(int(FanPacket.Power.OFF.value, 16))
        packet.append(0)
        return packet

    def make_change_speed(self, speed: Speed) -> bytearray:
        """Speed packet Make"""
        packet = super().make_base(Cmd.CHANGE, ValueType.DIM)
        packet.append(int(str(speed.value), 16))
        packet.append(0)
        return packet


def parse_packet(packet: str) -> list[ImazuPacket]:
    """Packet parse"""
    packets = [packet[i: i + 2] for i in range(0, len(packet), 2)]

    def _parse_imazu_packet() -> Optional[ImazuPacket]:
        """Imazu packet Parse"""
        device = packets[3]
        if device == '16':
            return GuardPacket(packets)
        if device == '18':
            return ThermostatPacket(packets)
        if device == '19':
            return LightPacket(packets)
        if device == '1a':
            return DimmingPacket(packets)
        if device == '1b':
            return GasPacket(packets)
        if device == '1c':
            return AcPacket(packets)
        if device == '1f':
            return SwitchPacket(packets)
        if device == '2a':
            return AwayModePacket(packets)
        if device == '2b':
            return FanPacket(packets)
        _LOGGER.warning('unknown device, %s, %s', device, packets)
        return None

    if (imazu_packet := _parse_imazu_packet()) is None:
        return []

    if imazu_packet.cmd in [Cmd.SCAN, Cmd.CHANGE]:
        return []

    if imazu_packet.cmd != Cmd.STATUS:
        _LOGGER.warning('%s unknown cmd, %s, %s',
                        imazu_packet.device.name, imazu_packet.cmd, ''.join(packets))
        return []

    return imazu_packet.parse_state_packets()
