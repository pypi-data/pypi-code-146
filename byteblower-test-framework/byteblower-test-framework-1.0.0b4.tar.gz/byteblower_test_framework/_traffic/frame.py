"""Frame interface module."""
from abc import ABC, abstractmethod
from typing import List, Sequence  # for type hinting

from byteblowerll.byteblower import Frame as TxFrame  # for type hinting
from byteblowerll.byteblower import FrameTagTx  # for type hinting
from byteblowerll.byteblower import Stream as TxStream  # for type hinting
from byteblowerll.byteblower import VLANTag
# XXX - Avoid circular import with scapy 2.4.5 on macOS Monterey:
# Similar to https://github.com/secdev/scapy/issues/3246
# from scapy.layers.inet import Ether  # for type hinting
from scapy.all import Ether  # for type hinting
from scapy.all import Dot1Q

from .._endpoint.port import Port, VlanConfig  # for type hinting

ETHERNET_HEADER_LENGTH: int = 14  # [Bytes]
ETHERNET_FCS_LENGTH: int = 4  # [Bytes]
UDP_HEADER_LENGTH: int = 8  # [Bytes]

DEFAULT_FRAME_LENGTH: int = 1024  # [Bytes]
# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Dynamic,_private_or_ephemeral_ports  # noqa: E501
# The range 49152–65535 (2^15 + 2^14 to 2^16 − 1) contains
# dynamic or private ports that cannot be registered with IANA.
UDP_DYNAMIC_PORT_START: int = 49152


class Frame(ABC):
    """Frame interface."""

    __slots__ = (
        '_length',
        '_udp_src',
        '_udp_dest',
        '_latency_tag',
        '_frame',
    )

    def __init__(self,
                 length: int = DEFAULT_FRAME_LENGTH,
                 udp_src: int = UDP_DYNAMIC_PORT_START,
                 udp_dest: int = UDP_DYNAMIC_PORT_START,
                 latency_tag: bool = False) -> None:
        self._length = length
        self._udp_src = udp_src
        self._udp_dest = udp_dest
        self._latency_tag = latency_tag
        self._frame: TxFrame = None

    def _build_layer2_5_headers(self, source_port: Port) -> Sequence[Dot1Q]:
        vlan_configs: List[VlanConfig] = list()
        layer2_5 = source_port.layer2_5
        for l2_5 in layer2_5:
            if not isinstance(l2_5, VLANTag):
                raise ValueError(
                    f'Unsupported Layer 2.5 configuration: {type(l2_5)!r}')
            vlan_configs.append(
                (l2_5.IDGet(), l2_5.DropEligibleGet(), l2_5.PriorityGet()))

        return [
            # ! FIXME - This currently mismatches the VLAN stack configuration
            #         * of a ByteBlower Port, which does use S-tag + C-tag.
            # TODO - We need to default to VLAN Q-in-Q S-tag and C-tags,
            #        C-tags-only can be provided as *alternative* config.
            Dot1Q(prio=vlan_pcp, id=vlan_dei, vlan=vlan_id)
            for vlan_id, vlan_dei, vlan_pcp in vlan_configs
        ]

    def _build_payload(self, header_length: int) -> str:
        return 'a' * (self._length - header_length)

    @abstractmethod
    def _build_frame_content(self, source_port: Port,
                             destination_port: Port) -> Ether:
        pass

    def _add(self, source_port: Port, destination_port: Port,
             stream: TxStream) -> None:
        scapy_frame = self._build_frame_content(source_port, destination_port)

        # Add this frame to the stream
        frame_content = bytearray(bytes(scapy_frame))

        # The ByteBlower API expects an 'str' as input
        # for the Frame::BytesSet(), we need to convert the bytearray.
        hexbytes = ''.join((format(b, '02x') for b in frame_content))
        self._frame: TxFrame = stream.FrameAdd()
        self._frame.BytesSet(hexbytes)

        if self._latency_tag:
            # Enable latency for this frame.
            # The frame frame contents will be altered
            # so it contains a timestamp.
            frame_tag: FrameTagTx = self._frame.FrameTagTimeGet()
            frame_tag.Enable(True)

        # Enable auto checksum, ....
        self._frame.L3AutoChecksumEnable(True)
        self._frame.L3AutoLengthEnable(True)
        self._frame.L4AutoChecksumEnable(True)
        self._frame.L4AutoLengthEnable(True)

    @property
    def udp_src(self):
        return self._udp_src

    @property
    def udp_dest(self):
        return self._udp_dest
