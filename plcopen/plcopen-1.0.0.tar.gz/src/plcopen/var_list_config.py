from dataclasses import dataclass, field
from typing import List, Optional
from plcopen.add_data import AddData
from plcopen.formatted_text import FormattedText
from plcopen.value import Value
from plcopen.var_list_plain import DataType

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class VarListConfig:
    """
    List of VAR_CONFIG variables.
    """
    class Meta:
        name = "varListConfig"

    config_variable: List["VarListConfig.ConfigVariable"] = field(
        default_factory=list,
        metadata={
            "name": "configVariable",
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
    class ConfigVariable:
        """
        Declaration of an access variable.

        :ivar type:
        :ivar initial_value:
        :ivar add_data:
        :ivar documentation:
        :ivar instance_path_and_name: Variable name including instance
            path
        :ivar address:
        """
        type: Optional[DataType] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
            }
        )
        initial_value: Optional[Value] = field(
            default=None,
            metadata={
                "name": "initialValue",
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
        instance_path_and_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "instancePathAndName",
                "type": "Attribute",
                "required": True,
            }
        )
        address: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
