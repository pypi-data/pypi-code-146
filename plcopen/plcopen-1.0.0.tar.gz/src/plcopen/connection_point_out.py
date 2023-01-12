from dataclasses import dataclass, field
from typing import Optional
from plcopen.add_data import AddData
from plcopen.position import Position

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class ConnectionPointOut:
    """
    Defines a connection point on the producer side.

    :ivar rel_position: Relative position of the connection pin. Origin
        is the anchor position of the block.
    :ivar expression: The operand is a valid iec variable e.g. avar[0].
    :ivar add_data:
    :ivar global_id:
    """
    class Meta:
        name = "connectionPointOut"

    rel_position: Optional[Position] = field(
        default=None,
        metadata={
            "name": "relPosition",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    global_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "globalId",
            "type": "Attribute",
        }
    )
