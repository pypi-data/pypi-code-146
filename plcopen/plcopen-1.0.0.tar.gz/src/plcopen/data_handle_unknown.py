from enum import Enum

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


class DataHandleUnknown(Enum):
    PRESERVE = "preserve"
    DISCARD = "discard"
    IMPLEMENTATION = "implementation"
