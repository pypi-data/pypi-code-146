from dataclasses import dataclass, field
from typing import List, Optional
from plcopen.add_data import AddData
from plcopen.connection import Connection
from plcopen.position import Position

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class ConnectionPointIn:
    """
    Defines a connection point on the consumer side.

    :ivar rel_position: Relative position of the connection pin. Origin
        is the anchor position of the block.
    :ivar connection:
    :ivar expression: The operand is a valid iec variable e.g. avar[0]
        or an iec expression or multiple token text e.g. a + b (*sum*).
        An iec 61131-3 parser has to be used to extract variable
        information.
    :ivar add_data:
    :ivar global_id:
    """
    class Meta:
        name = "connectionPointIn"

    rel_position: Optional[Position] = field(
        default=None,
        metadata={
            "name": "relPosition",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    connection: List[Connection] = field(
        default_factory=list,
        metadata={
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
