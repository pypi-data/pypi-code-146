"""Module for voice traffic generation."""
from datetime import timedelta  # for type hinting
from typing import Optional, Union  # for type hinting

from .._endpoint.ipv4.port import IPv4Port  # for type hinting
from .._endpoint.ipv6.port import IPv6Port  # for type hinting
from .._endpoint.port import Port  # for type hinting
from .._factory.frame import create_frame
from .frame import ETHERNET_HEADER_LENGTH, UDP_DYNAMIC_PORT_START
from .frameblastingflow import DEFAULT_NUMBER_OF_FRAMES, FrameBlastingFlow
from .ipv4.frame import IPV4_HEADER_LENGTH
from .ipv6.frame import IPV6_HEADER_LENGTH

DEFAULT_PACKETIZATION: int = 20  # ms


class VoiceFlow(FrameBlastingFlow):
    """Flow for simulating voice traffic.

    The implementation simulates G.711 RTP traffic.
    """

    def __init__(
            self,
            source: Port,
            destination: Port,
            name: Optional[str] = None,
            packetization: Optional[int] = DEFAULT_PACKETIZATION,
            number_of_frames: Optional[int] = DEFAULT_NUMBER_OF_FRAMES,
            duration: Optional[Union[timedelta, float,
                                     int]] = None,  # [seconds]
            initial_time_to_wait: Optional[Union[timedelta, float,
                                                 int]] = None,  # [seconds]
            udp_src: int = UDP_DYNAMIC_PORT_START,
            udp_dest: int = UDP_DYNAMIC_PORT_START,
            ip_tos: Optional[int] = None,
            enable_latency: Optional[bool] = False,
            **kwargs) -> None:
        """Create a G.711 voice flow with the given packetization.

        Typical packetization times are:

        * 20ms packetization
           - Packet rate = 50 pps
           - RTP packet size = 160 Bytes
        * 10ms packetization
           - Packet rate = 100 pps
           - RTP packet size = 80 Bytes

        :param source: Sending port of the voice stream
        :type source: Port
        :param destination: Receiving port of the voice stream
        :type destination: Port
        :param name: Name of this Flow, defaults to auto-generated name
           when set to ``None``.
        :type name: Optional[str], optional
        :param packetization: Packetization time of the RTP packets in
           milliseconds, defaults to DEFAULT_PACKETIZATION.
        :type packetization: Optional[int], optional
        :param number_of_frames: Number of frames to transmit,
           defaults to DEFAULT_NUMBER_OF_FRAMES
        :type number_of_frames: Optional[int], optional
        :param duration: Duration of the flow in seconds,
           defaults to None (use number_of_frames instead)
        :type duration: Optional[Union[timedelta, float, int]], optional
        :param initial_time_to_wait: Initial time to wait to start the flow.
           In seconds, defaults to None (start immediately)
        :type initial_time_to_wait: Optional[Union[timedelta, float, int]],
           optional
        :param udp_src: UDP src port, defaults to UDP_DYNAMIC_PORT_START
        :type udp_src: int, optional
        :param udp_dest: UDP dest port, defaults to UDP_DYNAMIC_PORT_START
        :type udp_dest: int, optional
        :param ip_tos: IP(v4) ToS bits, defaults to 0x00
        :type ip_tos: int, optional
        :param enable_latency: Enable latency tag in the packets
           (required for latency measurements at the destination port),
           defaults to False
        :type enable_latency: Optional[bool], optional
        :raises ValueError:
           When the type of the given source port is not supported.
        """
        frame_rate: float = 1000 / packetization  # pps
        udp_length: int = int(8000 / 1000 * packetization)  # Bytes
        header_length = ETHERNET_HEADER_LENGTH
        if isinstance(source, IPv4Port):
            header_length += IPV4_HEADER_LENGTH
        elif isinstance(source, IPv6Port):
            header_length += IPV6_HEADER_LENGTH
        else:
            raise ValueError(
                f'Unsupported Port type: {type(source).__name__!r}')
        frame_length = header_length + udp_length
        frame = create_frame(source,
                             length=frame_length,
                             udp_src=udp_src,
                             udp_dest=udp_dest,
                             ip_tos=ip_tos,
                             latency_tag=enable_latency)
        super().__init__(source,
                         destination,
                         name=name,
                         frame_rate=frame_rate,
                         number_of_frames=number_of_frames,
                         duration=duration,
                         initial_time_to_wait=initial_time_to_wait,
                         frame_list=[frame],
                         **kwargs)
