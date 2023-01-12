from dataclasses import dataclass, field
from typing import Optional
from plcopen.add_data import AddData
from plcopen.formatted_text import FormattedText

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class PouInstance:
    """
    Represents a program or function block instance either running with or
    without a task.
    """
    class Meta:
        name = "pouInstance"

    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    documentation: Optional[FormattedText] = field(
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
    type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "typeName",
            "type": "Attribute",
            "required": True,
        }
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        }
    )
