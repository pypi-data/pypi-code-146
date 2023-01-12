from enum import Enum

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


class EdgeModifierType(Enum):
    """
    Defines the edge detection behaviour of a variable.
    """
    NONE = "none"
    FALLING = "falling"
    RISING = "rising"
