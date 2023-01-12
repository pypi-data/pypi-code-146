"""Module for simplified Frame creation."""
from typing import Any, Mapping, Optional  # for type hinting

from .._endpoint.ipv4.port import IPv4Port
from .._endpoint.ipv6.port import IPv6Port
from .._endpoint.port import Port  # for type hinting
from .._traffic.frame import (  # for type hinting
    DEFAULT_FRAME_LENGTH,
    UDP_DYNAMIC_PORT_START,
    Frame,
)
from .._traffic.ipv4.frame import IPv4Frame
from .._traffic.ipv6.frame import IPv6Frame

FrameConfig = Mapping[str, Any]


def create_frame(source_port: Port,
                 length: int = DEFAULT_FRAME_LENGTH,
                 udp_src: int = UDP_DYNAMIC_PORT_START,
                 udp_dest: int = UDP_DYNAMIC_PORT_START,
                 ip_tos: Optional[int] = None,
                 latency_tag: bool = False) -> Frame:
    """Create a frame based on the (source) Port type."""
    if isinstance(source_port, IPv4Port):
        return IPv4Frame(length=length,
                         udp_src=udp_src,
                         udp_dest=udp_dest,
                         ip_tos=ip_tos,
                         latency_tag=latency_tag)

    if isinstance(source_port, IPv6Port):
        if ip_tos is not None:
            raise ValueError('IP ToS is not supported for IPv6 frames.')
        return IPv6Frame(length=length,
                         udp_src=udp_src,
                         udp_dest=udp_dest,
                         latency_tag=latency_tag)

    raise ValueError('Unsupported Port type')
