from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class FormattedText:
    """
    Formatted text according to parts of XHTML 1.1.
    """
    class Meta:
        name = "formattedText"

    w3_org_1999_xhtml_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "http://www.w3.org/1999/xhtml",
        }
    )
