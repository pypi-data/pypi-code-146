from dataclasses import dataclass, field
from typing import List, Optional
from plcopen.add_data import AddData
from plcopen.position import Position

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class Connection:
    """Describes a connection between the consumer element (eg.

    input variable of a function block) and the producer element (eg.
    output variable of a function block). It may contain a list of
    positions that describes the path of the connection.

    :ivar position: All positions of the directed connection path. If
        any positions are given, the list has to contain the first
        (input pin of the consumer element) as well as the last (output
        pin of the producer element).
    :ivar add_data:
    :ivar global_id:
    :ivar ref_local_id: Identifies the element the connection starts
        from.
    :ivar formal_parameter: If present: This attribute denotes the name
        of the VAR_OUTPUT / VAR_IN_OUTparameter of the pou block that is
        the start of the connection. If not present: If the refLocalId
        attribute refers to a pou block, the start of the connection is
        the first output of this block, which is not ENO. If the
        refLocalId attribute refers to any other element type, the start
        of the connection is the elements single native output.
    """
    class Meta:
        name = "connection"

    position: List[Position] = field(
        default_factory=list,
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
    ref_local_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "refLocalId",
            "type": "Attribute",
            "required": True,
        }
    )
    formal_parameter: Optional[str] = field(
        default=None,
        metadata={
            "name": "formalParameter",
            "type": "Attribute",
        }
    )
