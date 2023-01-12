from enum import Enum

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


class AccessType(Enum):
    """
    Defines the different access types to an accessVariable.
    """
    READ_ONLY = "readOnly"
    READ_WRITE = "readWrite"
