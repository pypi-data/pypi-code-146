"""Interfaces for traffic generation."""
# `Flow` is not really needed, but is useful for type hinting:
from ._traffic.flow import Flow  # noqa: F401
from ._traffic.frame import \
    DEFAULT_FRAME_LENGTH  # noqa: F401; for user convenience
from ._traffic.frame import \
    ETHERNET_FCS_LENGTH  # noqa: F401; for user convenience
from ._traffic.frame import \
    ETHERNET_HEADER_LENGTH  # noqa: F401; for user convenience
from ._traffic.frame import \
    UDP_DYNAMIC_PORT_START  # noqa: F401; for user convenience
from ._traffic.frame import \
    UDP_HEADER_LENGTH  # noqa: F401; for user convenience
from ._traffic.frame import Frame
from ._traffic.frameblastingflow import FrameBlastingFlow
from ._traffic.gamingflow import GamingFlow
from ._traffic.httpflow import HTTPFlow
from ._traffic.imix import \
    DEFAULT_IMIX_FRAME_CONFIG  # noqa: F401; for user convenience
from ._traffic.imix import Imix, ImixFrameConfig
from ._traffic.ipv4.frame import \
    DEFAULT_IPV4_TOS  # noqa: F401; for user convenience
from ._traffic.ipv4.frame import \
    IPV4_FULL_HEADER_LENGTH  # noqa: F401; for user convenience
from ._traffic.ipv4.frame import \
    IPV4_HEADER_LENGTH  # noqa: F401; for user convenience
from ._traffic.ipv4.frame import IPv4Frame
from ._traffic.ipv6.frame import \
    IPV6_FULL_HEADER_LENGTH  # noqa: F401; for user convenience
from ._traffic.ipv6.frame import \
    IPV6_HEADER_LENGTH  # noqa: F401; for user convenience
from ._traffic.ipv6.frame import IPv6Frame
from ._traffic.tcpflow import HttpMethod, TCPCongestionAvoidanceAlgorithm
from ._traffic.videoflow import VideoFlow
from ._traffic.voiceflow import VoiceFlow

# Export the user interfaces.
#
# Outcomes:
# * Limits import on `from byteblower_test_framework.traffic import *`
# * Exposes the interfaces in the (Sphinx) documentation
#
# NOTE
#   Exporting imported variables does not introduce them in the (Sphinx) docs.
#   For example 'DEFAULT_FRAME_LENGTH', 'IPV4_HEADER_LENGTH',
#   'IPV6_HEADER_LENGTH', ...
#   It does introduce their name and value in `help()` of this module though.
#
__all__ = (
    # Constants:
    # OSI Layer 1/2 constants:
    'DEFAULT_FRAME_LENGTH',
    'DEFAULT_IMIX_FRAME_CONFIG',
    'ETHERNET_FCS_LENGTH',
    'ETHERNET_HEADER_LENGTH',
    # OSI Layer 3 constants:
    'IPV4_FULL_HEADER_LENGTH',
    'IPV4_HEADER_LENGTH',
    'DEFAULT_IPV4_TOS',
    'IPV6_FULL_HEADER_LENGTH',
    'IPV6_HEADER_LENGTH',
    # OSI Layer 4 constants:
    'UDP_HEADER_LENGTH',
    'UDP_DYNAMIC_PORT_START',
    # Frames:
    Imix.__name__,
    ImixFrameConfig.__name__,
    Frame.__name__,
    IPv4Frame.__name__,
    IPv6Frame.__name__,
    # Basic/generic flows:
    FrameBlastingFlow.__name__,
    HTTPFlow.__name__,
    HttpMethod.__name__,
    TCPCongestionAvoidanceAlgorithm.__name__,
    # Application simulation:
    VoiceFlow.__name__,
    GamingFlow.__name__,
    VideoFlow.__name__,
)
