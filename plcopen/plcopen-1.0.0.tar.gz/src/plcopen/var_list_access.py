from dataclasses import dataclass, field
from typing import List, Optional
from plcopen.access_type import AccessType
from plcopen.add_data import AddData
from plcopen.formatted_text import FormattedText
from plcopen.var_list_plain import DataType

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class VarListAccess:
    """
    List of access variable declarations.
    """
    class Meta:
        name = "varListAccess"

    access_variable: List["VarListAccess.AccessVariable"] = field(
        default_factory=list,
        metadata={
            "name": "accessVariable",
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
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )

    @dataclass
    class AccessVariable:
        """
        Declaration of an access variable.

        :ivar type:
        :ivar add_data:
        :ivar documentation:
        :ivar alias: Name that is visible to the communication partner
        :ivar instance_path_and_name: Variable name including instance
            path inside the configuration
        :ivar direction:
        """
        type: Optional[DataType] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
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
        documentation: Optional[FormattedText] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        alias: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        instance_path_and_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "instancePathAndName",
                "type": "Attribute",
                "required": True,
            }
        )
        direction: Optional[AccessType] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
