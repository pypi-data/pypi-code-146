from dataclasses import dataclass, field
from typing import List, Optional
from plcopen.add_data import AddData
from plcopen.formatted_text import FormattedText
from plcopen.range_signed import RangeSigned
from plcopen.range_unsigned import RangeUnsigned
from plcopen.value import Value

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class VarListPlain:
    """
    List of variable declarations without attributes.
    """
    class Meta:
        name = "varListPlain"

    variable: List["VarListPlain.Variable"] = field(
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
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )

    @dataclass
    class Variable:
        """
        Declaration of a variable.
        """
        type: Optional["DataType"] = field(
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
        name: Optional[str] = field(
            default=None,
            metadata={
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
        global_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "globalId",
                "type": "Attribute",
            }
        )


@dataclass
class DataType:
    """
    A generic data type.

    :ivar bool_value:
    :ivar byte:
    :ivar word:
    :ivar dword:
    :ivar lword:
    :ivar sint:
    :ivar int_value:
    :ivar dint:
    :ivar lint:
    :ivar usint:
    :ivar uint:
    :ivar udint:
    :ivar ulint:
    :ivar real:
    :ivar lreal:
    :ivar time:
    :ivar date:
    :ivar dt:
    :ivar tod:
    :ivar string:
    :ivar wstring:
    :ivar any:
    :ivar any_derived:
    :ivar any_elementary:
    :ivar any_magnitude:
    :ivar any_num:
    :ivar any_real:
    :ivar any_int:
    :ivar any_bit:
    :ivar any_string:
    :ivar any_date:
    :ivar array:
    :ivar derived: Reference to a user defined datatype or POU. Variable
        declarations use this type to declare e.g. function block
        instances.
    :ivar enum:
    :ivar struct:
    :ivar subrange_signed:
    :ivar subrange_unsigned:
    :ivar pointer:
    """
    class Meta:
        name = "dataType"

    bool_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "BOOL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    byte: Optional[object] = field(
        default=None,
        metadata={
            "name": "BYTE",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    word: Optional[object] = field(
        default=None,
        metadata={
            "name": "WORD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    dword: Optional[object] = field(
        default=None,
        metadata={
            "name": "DWORD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    lword: Optional[object] = field(
        default=None,
        metadata={
            "name": "LWORD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    sint: Optional[object] = field(
        default=None,
        metadata={
            "name": "SINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    int_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "INT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    dint: Optional[object] = field(
        default=None,
        metadata={
            "name": "DINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    lint: Optional[object] = field(
        default=None,
        metadata={
            "name": "LINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    usint: Optional[object] = field(
        default=None,
        metadata={
            "name": "USINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    uint: Optional[object] = field(
        default=None,
        metadata={
            "name": "UINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    udint: Optional[object] = field(
        default=None,
        metadata={
            "name": "UDINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    ulint: Optional[object] = field(
        default=None,
        metadata={
            "name": "ULINT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    real: Optional[object] = field(
        default=None,
        metadata={
            "name": "REAL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    lreal: Optional[object] = field(
        default=None,
        metadata={
            "name": "LREAL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    time: Optional[object] = field(
        default=None,
        metadata={
            "name": "TIME",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    date: Optional[object] = field(
        default=None,
        metadata={
            "name": "DATE",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    dt: Optional[object] = field(
        default=None,
        metadata={
            "name": "DT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    tod: Optional[object] = field(
        default=None,
        metadata={
            "name": "TOD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    string: Optional["DataType.String"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    wstring: Optional["DataType.Wstring"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_derived: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_DERIVED",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_elementary: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_ELEMENTARY",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_magnitude: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_MAGNITUDE",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_num: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_NUM",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_real: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_REAL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_int: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_INT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_bit: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_BIT",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_string: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_STRING",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    any_date: Optional[object] = field(
        default=None,
        metadata={
            "name": "ANY_DATE",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    array: Optional["DataType.Array"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    derived: Optional["DataType.Derived"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    enum: Optional["DataType.EnumType"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    struct: Optional[VarListPlain] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    subrange_signed: Optional["DataType.SubrangeSigned"] = field(
        default=None,
        metadata={
            "name": "subrangeSigned",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    subrange_unsigned: Optional["DataType.SubrangeUnsigned"] = field(
        default=None,
        metadata={
            "name": "subrangeUnsigned",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    pointer: Optional["DataType.Pointer"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )

    @dataclass
    class String:
        """
        The single byte character string type.
        """
        length: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass
    class Wstring:
        """
        The wide character (WORD) string type.
        """
        length: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass
    class Array:
        dimension: List[RangeSigned] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "min_occurs": 1,
            }
        )
        base_type: Optional["DataType"] = field(
            default=None,
            metadata={
                "name": "baseType",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
            }
        )

    @dataclass
    class Derived:
        """
        The user defined alias type.
        """
        add_data: Optional[AddData] = field(
            default=None,
            metadata={
                "name": "addData",
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

    @dataclass
    class EnumType:
        values: Optional["DataType.EnumType.Values"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
            }
        )
        base_type: Optional["DataType"] = field(
            default=None,
            metadata={
                "name": "baseType",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )

        @dataclass
        class Values:
            value: List["DataType.EnumType.Values.Value"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "min_occurs": 1,
                }
            )

            @dataclass
            class Value:
                """
                An enumeration value used to build up enumeration types.
                """
                name: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )
                value: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )

    @dataclass
    class SubrangeSigned:
        range: Optional[RangeSigned] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
            }
        )
        base_type: Optional["DataType"] = field(
            default=None,
            metadata={
                "name": "baseType",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
            }
        )

    @dataclass
    class SubrangeUnsigned:
        range: Optional[RangeUnsigned] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
            }
        )
        base_type: Optional["DataType"] = field(
            default=None,
            metadata={
                "name": "baseType",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
            }
        )

    @dataclass
    class Pointer:
        base_type: Optional["DataType"] = field(
            default=None,
            metadata={
                "name": "baseType",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
                "required": True,
            }
        )
