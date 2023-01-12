"""IPv6 Frame interface module."""
from scapy.layers.inet6 import UDP, Ether, IPv6
from scapy.packet import Raw

from ..._endpoint.ipv6.port import IPv6Port  # for type hinting
from ..frame import (
    DEFAULT_FRAME_LENGTH,
    ETHERNET_HEADER_LENGTH,
    UDP_DYNAMIC_PORT_START,
    UDP_HEADER_LENGTH,
    Frame,
)

IPV6_HEADER_LENGTH: int = 40

IPV6_FULL_HEADER_LENGTH = (
    ETHERNET_HEADER_LENGTH +  # noqa: W504
    IPV6_HEADER_LENGTH + UDP_HEADER_LENGTH)
assert IPV6_FULL_HEADER_LENGTH == 62, 'Incorrect IPv6 full header length'


class IPv6Frame(Frame):
    """Frame interface for IPv6."""

    __slots__ = ()

    def __init__(self,
                 length: int = DEFAULT_FRAME_LENGTH,
                 udp_src: int = UDP_DYNAMIC_PORT_START,
                 udp_dest: int = UDP_DYNAMIC_PORT_START,
                 latency_tag: bool = False) -> None:
        super().__init__(length, udp_src, udp_dest, latency_tag)

        # Sanity checks
        if self._length < IPV6_FULL_HEADER_LENGTH:
            raise ValueError(
                'IPv6 frame length too small.'
                ' Must be at least {}B.'.format(IPV6_FULL_HEADER_LENGTH))

    def _build_frame_content(self, source_port: IPv6Port,
                             destination_port: IPv6Port) -> Ether:
        udp_dest = self._udp_dest
        udp_src = self._udp_src
        # ip_dest = destination_port.layer3.IpDhcpGet()
        # ip_src = source_port.layer3.IpDhcpGet()
        ip_dest = str(destination_port.ip)
        ip_src = str(source_port.ip)
        mac_src = source_port.mac
        mac_dst = source_port.layer3.Resolve(ip_dest)

        scapy_layer2_5_headers = self._build_layer2_5_headers(source_port)

        payload = self._build_payload(IPV6_FULL_HEADER_LENGTH)

        scapy_udp_payload = Raw(payload.encode('ascii', 'strict'))
        scapy_udp_header = UDP(dport=udp_dest, sport=udp_src)
        scapy_ip_header = IPv6(src=ip_src, dst=ip_dest)
        scapy_ethernet_header = Ether(src=mac_src, dst=mac_dst)
        for scapy_layer2_5_header in scapy_layer2_5_headers:
            scapy_ethernet_header /= scapy_layer2_5_header
        scapy_frame = (scapy_ethernet_header / scapy_ip_header /
                       scapy_udp_header / scapy_udp_payload)

        return scapy_frame
