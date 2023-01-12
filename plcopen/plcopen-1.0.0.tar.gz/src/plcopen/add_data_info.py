from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from plcopen.formatted_text import FormattedText

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class AddDataInfo:
    """
    List of additional data elements used in the document with description.
    """
    class Meta:
        name = "addDataInfo"

    info: List["AddDataInfo.Info"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )

    @dataclass
    class Info:
        """
        :ivar description:
        :ivar name: Unique name of the additional data element.
        :ivar version: Version of additional data, eg. schema version.
        :ivar vendor: Vendor responsible for the definition of the
            additional data element.
        """
        description: Optional[FormattedText] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        version: Optional[Decimal] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        vendor: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
