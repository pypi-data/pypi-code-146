from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class RangeUnsigned:
    """
    Defines a range with unsigned bounds.
    """
    class Meta:
        name = "rangeUnsigned"

    lower: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    upper: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
