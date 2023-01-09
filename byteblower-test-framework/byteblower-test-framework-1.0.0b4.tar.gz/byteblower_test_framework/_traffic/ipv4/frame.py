"""IPv4 Frame interface module."""
import logging
from typing import Optional, Union  # for type hinting

# XXX - Causes circular import with scapy 2.4.5 on macOS Monterey:
# Similar to https://github.com/secdev/scapy/issues/3246
# from scapy.layers.inet import IP, UDP
# from scapy.layers.l2 import Ether
from scapy.all import IP, UDP, Ether
from scapy.packet import Raw

from ..._endpoint.ipv4.nat import NattedPort  # for type hinting
from ..._endpoint.ipv4.port import IPv4Port  # for type hinting
from ..frame import (
    DEFAULT_FRAME_LENGTH,
    ETHERNET_HEADER_LENGTH,
    UDP_DYNAMIC_PORT_START,
    UDP_HEADER_LENGTH,
    Frame,
)

IPV4_HEADER_LENGTH: int = 20

IPV4_FULL_HEADER_LENGTH: int = (
    ETHERNET_HEADER_LENGTH +  # noqa: W504
    IPV4_HEADER_LENGTH + UDP_HEADER_LENGTH)
assert IPV4_FULL_HEADER_LENGTH == 42, 'Incorrect IPv4 full header length'

DEFAULT_IPV4_TOS: int = 0x00


class IPv4Frame(Frame):
    """Frame interface for IPv4."""

    __slots__ = ('_ip_tos', )

    def __init__(self,
                 length: int = DEFAULT_FRAME_LENGTH,
                 udp_src: int = UDP_DYNAMIC_PORT_START,
                 udp_dest: int = UDP_DYNAMIC_PORT_START,
                 ip_tos: Optional[int] = DEFAULT_IPV4_TOS,
                 latency_tag: bool = False) -> None:
        super().__init__(length, udp_src, udp_dest, latency_tag)
        if ip_tos is None:
            self._ip_tos = DEFAULT_IPV4_TOS
        else:
            self._ip_tos = ip_tos

        # Sanity checks
        if self._length < IPV4_FULL_HEADER_LENGTH:
            raise ValueError(
                'IPv4 frame length too small.'
                ' Must be at least {}B.'.format(IPV4_FULL_HEADER_LENGTH))

    def _build_frame_content(
            self, source_port: Union[IPv4Port, NattedPort],
            destination_port: Union[IPv4Port, NattedPort]) -> Ether:
        udp_dest = self._udp_dest
        udp_src = self._udp_src
        ip_dest = destination_port.layer3.IpGet()
        ip_src = source_port.layer3.IpGet()
        ip_tos = self._ip_tos

        if destination_port.is_natted:
            nat_info = destination_port.nat_discover(
                source_port,
                public_udp_port=self._udp_src,
                nat_udp_port=self._udp_dest)
            logging.debug('NAT translation: %r', nat_info)
            ip_dest, udp_dest = nat_info

        mac_src = source_port.mac
        mac_dst = source_port.layer3.Resolve(ip_dest)

        scapy_layer2_5_headers = self._build_layer2_5_headers(source_port)

        payload = self._build_payload(IPV4_FULL_HEADER_LENGTH)

        scapy_udp_payload = Raw(payload.encode('ascii', 'strict'))
        scapy_udp_header = UDP(dport=udp_dest, sport=udp_src)
        scapy_ip_header = IP(src=ip_src, dst=ip_dest, tos=ip_tos)
        scapy_ethernet_header = Ether(src=mac_src, dst=mac_dst)
        for scapy_layer2_5_header in scapy_layer2_5_headers:
            scapy_ethernet_header /= scapy_layer2_5_header
        scapy_frame = (scapy_ethernet_header / scapy_ip_header /
                       scapy_udp_header / scapy_udp_payload)

        return scapy_frame
