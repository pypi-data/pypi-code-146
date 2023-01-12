"""Module for gaming flow related definitions."""
from typing import Optional  # for type hinting

from numpy.random import normal

from .._endpoint.ipv4.port import IPv4Port  # for type hinting
from .._endpoint.ipv6.port import IPv6Port  # for type hinting
from .._endpoint.port import Port  # for type hinting
from .frame import ETHERNET_HEADER_LENGTH
from .frameblastingflow import FrameBlastingFlow
from .imix import Imix, ImixFrameConfig
from .ipv4.frame import IPV4_HEADER_LENGTH
from .ipv6.frame import IPV6_HEADER_LENGTH

# Explicitly define __all__ to avoid export of 'normal' function (variable)
# => Shouldn't be exported nor documented
#    (causes issues with documentation generation)
__all__ = ('GamingFlow', )


class GamingFlow(FrameBlastingFlow):
    """Simulate traditional gaming network traffic.

    .. note::
       This does not simulate *cloud gaming*.
    """

    # TODO - Cleanup code and define slots
    # __slots__ = (
    # )

    _CONFIG_ELEMENTS = FrameBlastingFlow._CONFIG_ELEMENTS + (
        "frame_length",
        "frame_length_deviation",
        "frame_length_max",
        "frame_length_min",
        "max_threshold_latency",
    )

    def __init__(
            self,
            source: Port,
            destination: Port,
            name: Optional[str] = None,
            packet_length: int = 110,
            packet_length_deviation: float = 20,
            packet_length_min: int = 22,
            packet_length_max: int = 1480,
            frame_rate: float = 30,
            imix_number_of_frames: int = 20,
            ip_tos: Optional[int] = None,
            # TODO - Analyser-specific config
            #      * (but useful for report output)
            max_threshold_latency: float = 1.0,
            **kwargs) -> None:
        """Instanciate a new Gaming Flow.

        :param source:
           Source port for this flow
        :type source: Port
        :param destination:
           Destination Port for this flow
        :type destination: Port
        :param name:
           Name for this Flow, defaults to None
        :type name: str, optional
        :param packet_length:
           Mean UDP length of the frames we are going to send, defaults to 110
        :type packet_length: int, optional
        :param packet_length_deviation:
           Deviation of the frame length, defaults to 20
        :type packet_length_deviation: float, optional
        :param packet_length_min:
           Minimum UDP packet length, defaults to 22
        :type packet_length_min: int, optional
        :param packet_length_max:
           Maxmimum UDP packet length, defaults to 1480
        :type packet_length_max: int, optional
        :param frame_rate:
           Packet rate at which we will send these frames, defaults to 30
        :type frame_rate: float, optional
        :param imix_number_of_frames:
           Add ``<x>`` frames with a length which is normaly distributed,
           defaults to 20
        :type imix_number_of_frames: int, optional
        :param max_threshold_latency:
           Threshold in ms. Is percentile 99 of the this flow is below this
           threshold, the flow will pass for this test, defaults to 1.0
        :type max_threshold_latency: float, optional
        :raises ValueError:
           When an unsupported source Port type is given.
        """
        header_length = ETHERNET_HEADER_LENGTH
        if isinstance(source, IPv4Port):
            header_length += IPV4_HEADER_LENGTH
        elif isinstance(source, IPv6Port):
            header_length += IPV6_HEADER_LENGTH
        else:
            raise ValueError(
                f'Unsupported Port type: {type(source).__name__!r}')
        self.frame_length = header_length + packet_length
        self.frame_length_deviation = packet_length_deviation
        self.frame_length_max = header_length + packet_length_max
        self.frame_length_min = header_length + packet_length_min
        # self._imix_number_of_frames = imix_number_of_frames

        # Objects we need
        # Add <x> frames with a length which is normaly distributed
        lengths = normal(self.frame_length, self.frame_length_deviation,
                         imix_number_of_frames)

        def limit_range(length: int) -> int:
            if length < self.frame_length_min:
                return self.frame_length_min
            elif length > self.frame_length_max:
                return self.frame_length_max
            return length

        imix_frame_config = [
            ImixFrameConfig(length=limit_range(int(length)), weight=1)
            for length in lengths
        ]
        imix = Imix(frame_config=imix_frame_config,
                    ip_tos=ip_tos,
                    latency_tag=True)

        super().__init__(source,
                         destination,
                         name=name,
                         frame_rate=frame_rate,
                         imix=imix,
                         **kwargs)

        # Analyser parameters (used for reporting only)
        # * Required Analysers are to be added via test script
        self.max_threshold_latency = max_threshold_latency

    def analyse(self) -> None:
        """Pass or fail for this test."""
        self.updatestats()

        return super().analyse()
