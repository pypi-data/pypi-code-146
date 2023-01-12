from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class RangeSigned:
    """
    Defines a range with signed bounds.
    """
    class Meta:
        name = "rangeSigned"

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
