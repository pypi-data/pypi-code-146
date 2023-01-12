from enum import Enum

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


class PouType(Enum):
    """
    Defines the different types of a POU.
    """
    FUNCTION = "function"
    FUNCTION_BLOCK = "functionBlock"
    PROGRAM = "program"
