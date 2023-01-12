from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class Value:
    """
    A generic value.
    """
    class Meta:
        name = "value"

    simple_value: Optional["SimpleValue"] = field(
        default=None,
        metadata={
            "name": "simpleValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    array_value: Optional["ArrayValue"] = field(
        default=None,
        metadata={
            "name": "arrayValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    struct_value: Optional["StructValue"] = field(
        default=None,
        metadata={
            "name": "structValue",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )

@dataclass
class SimpleValue:
    """
    Value that can be represented as a single token string.
    """
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

@dataclass
class ArrayValue:
    """Array value consisting of a list of occurrances - value pairs"""
    value: List["ArrayValue._Value"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )

    @dataclass
    class _Value(Value):
        repetition_value: str = field(
            default="1",
            metadata={
                "name": "repetitionValue",
                "type": "Attribute",
            }
        )

@dataclass
class StructValue:
    """Struct value consisting of a list of member - value pairs"""
    value: List["StructValue._Value"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )

    @dataclass
    class _Value(Value):
        member: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
