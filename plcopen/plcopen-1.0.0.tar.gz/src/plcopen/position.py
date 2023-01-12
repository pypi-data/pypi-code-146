from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class Position:
    """
    Defines a graphical position in X, Y coordinates.
    """
    class Meta:
        name = "position"

    x: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    y: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
