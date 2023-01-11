"""Wall Pad Imazu Socket Client"""
import logging
from typing import Optional

from wp_socket.client import WpSocketClient

from wp_imazu.packet import parse_packet

_LOGGER = logging.getLogger(__name__)

PACKET_HEADER = b'\xf7'
PACKET_TAIL = b'\xee'


def checksum(packet: bytes) -> bool:
    """Imazu packet checksum"""
    if len(packet) == 0 or len(packet) != packet[1]:
        return False
    p_sum = 0
    for i in range(0, len(packet) - 2):
        p_sum ^= packet[i]
    return packet[len(packet) - 2] == p_sum


def makesum(packet: bytes) -> Optional[int]:
    """Imazu packet make checksum"""
    if len(packet) < packet[1] - 2:
        return None
    p_sum = 0
    for i in range(0, len(packet) - 2):
        p_sum ^= packet[i]
    return p_sum


class ImazuClient(WpSocketClient):
    """Wall Pad Imazu Socket Client"""

    def __init__(self, host: str, port: int, async_packet_handler):
        super().__init__(host, port, self._async_packets_handler)
        self.async_packet_handler = async_packet_handler
        self.prev_packets = None

    async def async_on_connected(self):
        """Socket connected notifications"""
        _LOGGER.debug('connected')

    async def async_send(self, packet: bytes):
        """Socket write imazu packet"""
        data = bytearray(PACKET_HEADER)
        data.append(0)  # len
        data.extend(packet)  # 01 or 1a, device, cmd, value_type, sub, change_value, state_value
        data.append(0)  # checksum
        data.extend(PACKET_TAIL)
        data[1] = len(data)  # len

        # checksum
        if (_makesum := makesum(data)) is None:
            _LOGGER.warning('send invalid makesum: %s', data.hex())
            return
        data[-2] = _makesum

        if not checksum(data):
            _LOGGER.warning('send invalid packet: %s', data.hex())
            return

        await super().async_send_packet(data)

    async def _async_packets_handler(self, packets):
        """Queue imazu packet handler"""
        packet_list = self._parse_packets(packets)
        for packet in packet_list:
            try:
                if not checksum(packet):
                    _LOGGER.warning('receive invalid packet: %s', packet.hex())
                    continue
                imazu_packets = parse_packet(packet.hex())
                for imazu_packet in imazu_packets:
                    _LOGGER.debug(imazu_packet.description())
                    await self.async_packet_handler(imazu_packet)

            except Exception as ex:
                _LOGGER.error('packets handler error, %s, %s', ex, packet.hex())

    def _parse_packets(self, packets):
        """Queue imazu packet parse"""
        packet_list = []
        if self.prev_packets:
            packets = self.prev_packets + packets
            self.prev_packets = None

        while packets:
            if (start_idx := packets.find(PACKET_HEADER)) == -1:
                _LOGGER.warning('unknown packets %s', packets.hex())
                break
            if start_idx != 0:
                _LOGGER.warning('unknown start packets %s', packets.hex())

            if (end_idx := packets.find(PACKET_TAIL, start_idx + 8)) == -1:
                self.prev_packets = packets
                break
            packet_list.append(packets[start_idx: end_idx + 1])
            packets = packets[end_idx + 1:]
        return packet_list
