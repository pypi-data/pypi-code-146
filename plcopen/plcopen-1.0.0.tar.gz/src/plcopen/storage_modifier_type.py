from enum import Enum

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


class StorageModifierType(Enum):
    """
    Defines the storage mode (S/R) behaviour of a variable.
    """
    NONE = "none"
    SET = "set"
    RESET = "reset"
