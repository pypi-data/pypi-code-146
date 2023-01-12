"""Module providing general options used in reporting."""
from enum import Enum


# Cfr. GUI: Window > Preferences > Project > Bitrate
class Layer2Speed(Enum):
    """What will be included in the Layer 2 speed calculation."""

    frame = 'frame'
    """Frame without FCS.

    * Frame (as build and send by ByteBlower)

    This way, each Frame gets 0 Bytes extra.
    """

    frame_with_fcs = 'frame_with_fcs'
    """Frame with FCS.

    * Frame (as build and send by ByteBlower)
    * FCS (CRC Frame Checksum, 4 Bytes)

    This way, each Frame gets 4 Bytes extra.
    """

    # TODO: Future use case
    # physical = 'physical'
    # """Frame with FCS and physical overhead.

    # * Frame (as build and send by ByteBlower)
    # * FCS (CRC Frame Checksum, 4 Bytes)
    # * Preamble (7 Bytes)
    # * SFD (Start Frame Delimiter, 1 Byte)
    # * Pause (12 Bytes)

    # This way, each Frame gets 24 Bytes extra.
    # """


def layer2_speed_info(layer2_speed: Layer2Speed) -> str:
    """Provide textual information about the Layer 2 speed configuration."""
    if layer2_speed == Layer2Speed.frame:
        return _INFO_PREFIX + """Frame without FCS.

    * Frame (as build and send by ByteBlower)

This way, each Frame gets 0 Bytes extra.
"""

    if layer2_speed == Layer2Speed.frame_with_fcs:
        return _INFO_PREFIX + """Frame with FCS.

    * Frame (as build and send by ByteBlower)
    * FCS (CRC Frame Checksum, 4 Bytes)

This way, each Frame gets 4 Bytes extra.
"""

    # TODO: Future use case
#     if layer2_speed == Layer2Speed.physical:
#         return _INFO_PREFIX + """Frame with FCS and physical overhead.

#     * Frame (as build and send by ByteBlower)
#     * FCS (CRC Frame Checksum, 4 Bytes)
#     * Preamble (7 Bytes)
#     * SFD (Start Frame Delimiter, 1 Byte)
#     * Pause (12 Bytes)

# This way, each Frame gets 24 Bytes extra.
# """

    raise ValueError('Invalid Layer 2 speed option')


_INFO_PREFIX = """The Layer 2 frame size and speed is calculated using the following fields:

"""  # noqa: E501
