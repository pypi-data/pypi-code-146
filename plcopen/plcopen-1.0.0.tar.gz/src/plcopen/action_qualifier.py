from enum import Enum

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


class ActionQualifier(Enum):
    P1 = "P1"
    N = "N"
    P0 = "P0"
    R = "R"
    S = "S"
    L = "L"
    D = "D"
    P = "P"
    DS = "DS"
    DL = "DL"
    SD = "SD"
    SL = "SL"
