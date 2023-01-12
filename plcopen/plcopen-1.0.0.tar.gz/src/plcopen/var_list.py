from dataclasses import dataclass, field
from typing import Optional
from plcopen.var_list_plain import VarListPlain

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class VarList(VarListPlain):
    """
    List of variable declarations that share the same memory attributes
    (CONSTANT, RETAIN, NON_RETAIN, PERSISTENT)
    """
    class Meta:
        name = "varList"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    constant: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )
    retain: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )
    nonretain: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )
    persistent: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )
    nonpersistent: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )
