from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from plcopen.action_qualifier import ActionQualifier
from plcopen.add_data import AddData
from plcopen.connection_point_in import ConnectionPointIn
from plcopen.connection_point_out import ConnectionPointOut
from plcopen.edge_modifier_type import EdgeModifierType
from plcopen.formatted_text import FormattedText
from plcopen.position import Position
from plcopen.storage_modifier_type import StorageModifierType

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class Body:
    """
    Implementation part of a POU, action or transistion.

    :ivar il:
    :ivar st:
    :ivar fbd:
    :ivar ld:
    :ivar sfc:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    :ivar worksheet_name:
    :ivar global_id:
    """
    class Meta:
        name = "body"

    il: Optional[FormattedText] = field(
        default=None,
        metadata={
            "name": "IL",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    st: Optional[FormattedText] = field(
        default=None,
        metadata={
            "name": "ST",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    fbd: Optional["Body.Fbd"] = field(
        default=None,
        metadata={
            "name": "FBD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    ld: Optional["Body.Ld"] = field(
        default=None,
        metadata={
            "name": "LD",
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )
    sfc: Optional["Body.Sfc"] = field(
        default=None,
        metadata={
            "name": "SFC",
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
    worksheet_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "WorksheetName",
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
    class Fbd:
        """
        :ivar comment:
        :ivar error:
        :ivar connector:
        :ivar continuation: Counterpart of the connector element
        :ivar action_block:
        :ivar vendor_element:
        :ivar block:
        :ivar in_variable: Expression used as producer
        :ivar out_variable: Expression used as consumer
        :ivar in_out_variable: Expression used as producer and consumer
        :ivar label:
        :ivar jump:
        :ivar return_value:
        """
        comment: List["Body.Fbd.Comment"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        error: List["Body.Fbd.Error"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        connector: List["Body.Fbd.Connector"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        continuation: List["Body.Fbd.Continuation"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        action_block: List["Body.Fbd.ActionBlock"] = field(
            default_factory=list,
            metadata={
                "name": "actionBlock",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        vendor_element: List["Body.Fbd.VendorElement"] = field(
            default_factory=list,
            metadata={
                "name": "vendorElement",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        block: List["Body.Fbd.Block"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        in_variable: List["Body.Fbd.InVariable"] = field(
            default_factory=list,
            metadata={
                "name": "inVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        out_variable: List["Body.Fbd.OutVariable"] = field(
            default_factory=list,
            metadata={
                "name": "outVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        in_out_variable: List["Body.Fbd.InOutVariable"] = field(
            default_factory=list,
            metadata={
                "name": "inOutVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        label: List["Body.Fbd.Label"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        jump: List["Body.Fbd.Jump"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        return_value: List["Body.Fbd.Return"] = field(
            default_factory=list,
            metadata={
                "name": "return",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )

        @dataclass
        class Comment:
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            content: Optional[FormattedText] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
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

        @dataclass
        class Error:
            """Describes a graphical object representing a conversion error.

            Used to keep information which can not be interpreted by the
            importing system
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            content: Optional[FormattedText] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
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

        @dataclass
        class Connector:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_in:
            :ivar add_data:
            :ivar documentation:
            :ivar name: The operand is a valid iec variable e.g. avar[0]
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
        class Continuation:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_out:
            :ivar add_data:
            :ivar documentation:
            :ivar name: The operand is a valid iec variable e.g. avar[0]
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
        class ActionBlock:
            """
            :ivar position:
            :ivar connection_point_in:
            :ivar action:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar negated:
            :ivar width:
            :ivar height:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            action: List["Body.Fbd.ActionBlock.Action"] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class Action:
                """
                Association of an action with qualifier.

                :ivar rel_position: Relative position of the action.
                    Origin is the anchor position of the action block.
                :ivar reference: Name of an action or boolean variable.
                :ivar inline: Inline implementation of an action body.
                :ivar connection_point_out:
                :ivar add_data:
                :ivar documentation:
                :ivar local_id:
                :ivar qualifier:
                :ivar width:
                :ivar height:
                :ivar duration:
                :ivar indicator:
                :ivar execution_order_id: Used to identify the order of
                    execution. Also used to identify one special block
                    if there are several blocks with the same name.
                :ivar global_id:
                """
                rel_position: Optional[Position] = field(
                    default=None,
                    metadata={
                        "name": "relPosition",
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        "required": True,
                    }
                )
                reference: Optional["Body.Fbd.ActionBlock.Action.Reference"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                inline: Optional["Body"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                connection_point_out: Optional[ConnectionPointOut] = field(
                    default=None,
                    metadata={
                        "name": "connectionPointOut",
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
                local_id: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "localId",
                        "type": "Attribute",
                        "required": True,
                    }
                )
                qualifier: ActionQualifier = field(
                    default=ActionQualifier.N,
                    metadata={
                        "type": "Attribute",
                    }
                )
                width: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                height: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                duration: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                indicator: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                execution_order_id: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "executionOrderId",
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
                class Reference:
                    name: Optional[str] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )

        @dataclass
        class VendorElement:
            """
            Describes a graphical object representing a call statement.

            :ivar position: Anchor position of the box. Top left corner
                excluding the instance name.
            :ivar alternative_text: An alternative text to be displayed
                in generic representation of unknown elements.
            :ivar input_variables: The list of used input variables
                (consumers)
            :ivar in_out_variables: The list of used inOut variables
            :ivar output_variables: The list of used output variables
                (producers)
            :ivar add_data: Additional, vendor specific data for the
                element. Also defines the vendor specific meaning of the
                element.
            :ivar local_id:
            :ivar width:
            :ivar height:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            alternative_text: Optional[FormattedText] = field(
                default=None,
                metadata={
                    "name": "alternativeText",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            input_variables: Optional["Body.Fbd.VendorElement.InputVariables"] = field(
                default=None,
                metadata={
                    "name": "inputVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            in_out_variables: Optional["Body.Fbd.VendorElement.InOutVariables"] = field(
                default=None,
                metadata={
                    "name": "inOutVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            output_variables: Optional["Body.Fbd.VendorElement.OutputVariables"] = field(
                default=None,
                metadata={
                    "name": "outputVariables",
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
                    "required": True,
                }
            )
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class InputVariables:
                variable: List["Body.Fbd.VendorElement.InputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes an inputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                            "required": True,
                        }
                    )
                    documentation: Optional[FormattedText] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class InOutVariables:
                variable: List["Body.Fbd.VendorElement.InOutVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a inOutVariable of a Function or a FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class OutputVariables:
                variable: List["Body.Fbd.VendorElement.OutputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a outputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

        @dataclass
        class Block:
            """
            Describes a graphical object representing a call statement.

            :ivar position: Anchor position of the box. Top left corner
                excluding the instance name.
            :ivar input_variables: The list of used input variables
                (consumers)
            :ivar in_out_variables: The list of used inOut variables
            :ivar output_variables: The list of used output variables
                (producers)
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar width:
            :ivar height:
            :ivar type_name:
            :ivar instance_name:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            input_variables: Optional["Body.Fbd.Block.InputVariables"] = field(
                default=None,
                metadata={
                    "name": "inputVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            in_out_variables: Optional["Body.Fbd.Block.InOutVariables"] = field(
                default=None,
                metadata={
                    "name": "inOutVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            output_variables: Optional["Body.Fbd.Block.OutputVariables"] = field(
                default=None,
                metadata={
                    "name": "outputVariables",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
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
            instance_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "instanceName",
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class InputVariables:
                variable: List["Body.Fbd.Block.InputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes an inputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                            "required": True,
                        }
                    )
                    documentation: Optional[FormattedText] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class InOutVariables:
                variable: List["Body.Fbd.Block.InOutVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a inOutVariable of a Function or a FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class OutputVariables:
                variable: List["Body.Fbd.Block.OutputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a outputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

        @dataclass
        class InVariable:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_out:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class OutVariable:
            """
            Describes a graphical object representing a variable or expression
            used as l-value.

            :ivar position:
            :ivar connection_point_in:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class InOutVariable:
            """
            Describes a graphical object representing a variable which can be
            used as l-value and r-value at the same time.

            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated_in:
            :ivar edge_in:
            :ivar storage_in:
            :ivar negated_out:
            :ivar edge_out:
            :ivar storage_out:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated_in: bool = field(
                default=False,
                metadata={
                    "name": "negatedIn",
                    "type": "Attribute",
                }
            )
            edge_in: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "name": "edgeIn",
                    "type": "Attribute",
                }
            )
            storage_in: StorageModifierType = field(
                default=StorageModifierType.NONE,
                metadata={
                    "name": "storageIn",
                    "type": "Attribute",
                }
            )
            negated_out: bool = field(
                default=False,
                metadata={
                    "name": "negatedOut",
                    "type": "Attribute",
                }
            )
            edge_out: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "name": "edgeOut",
                    "type": "Attribute",
                }
            )
            storage_out: StorageModifierType = field(
                default=StorageModifierType.NONE,
                metadata={
                    "name": "storageOut",
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
        class Label:
            """
            Describes a graphical object representing a jump label.
            """
            position: Optional[Position] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            label: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Jump:
            """
            Describes a graphical object representing a jump statement.
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            label: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Return:
            """
            Describes a graphical object representing areturn statement.
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
    class Ld:
        """
        :ivar comment:
        :ivar error:
        :ivar connector:
        :ivar continuation: Counterpart of the connector element
        :ivar action_block:
        :ivar vendor_element:
        :ivar block:
        :ivar in_variable: Expression used as producer
        :ivar out_variable: Expression used as consumer
        :ivar in_out_variable: Expression used as producer and consumer
        :ivar label:
        :ivar jump:
        :ivar return_value:
        :ivar left_power_rail:
        :ivar right_power_rail:
        :ivar coil:
        :ivar contact:
        """
        comment: List["Body.Ld.Comment"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        error: List["Body.Ld.Error"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        connector: List["Body.Ld.Connector"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        continuation: List["Body.Ld.Continuation"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        action_block: List["Body.Ld.ActionBlock"] = field(
            default_factory=list,
            metadata={
                "name": "actionBlock",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        vendor_element: List["Body.Ld.VendorElement"] = field(
            default_factory=list,
            metadata={
                "name": "vendorElement",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        block: List["Body.Ld.Block"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        in_variable: List["Body.Ld.InVariable"] = field(
            default_factory=list,
            metadata={
                "name": "inVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        out_variable: List["Body.Ld.OutVariable"] = field(
            default_factory=list,
            metadata={
                "name": "outVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        in_out_variable: List["Body.Ld.InOutVariable"] = field(
            default_factory=list,
            metadata={
                "name": "inOutVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        label: List["Body.Ld.Label"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        jump: List["Body.Ld.Jump"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        return_value: List["Body.Ld.Return"] = field(
            default_factory=list,
            metadata={
                "name": "return",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        left_power_rail: List["Body.Ld.LeftPowerRail"] = field(
            default_factory=list,
            metadata={
                "name": "leftPowerRail",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        right_power_rail: List["Body.Ld.RightPowerRail"] = field(
            default_factory=list,
            metadata={
                "name": "rightPowerRail",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        coil: List["Body.Ld.Coil"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        contact: List["Body.Ld.Contact"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )

        @dataclass
        class Comment:
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            content: Optional[FormattedText] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
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

        @dataclass
        class Error:
            """Describes a graphical object representing a conversion error.

            Used to keep information which can not be interpreted by the
            importing system
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            content: Optional[FormattedText] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
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

        @dataclass
        class Connector:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_in:
            :ivar add_data:
            :ivar documentation:
            :ivar name: The operand is a valid iec variable e.g. avar[0]
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
        class Continuation:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_out:
            :ivar add_data:
            :ivar documentation:
            :ivar name: The operand is a valid iec variable e.g. avar[0]
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
        class ActionBlock:
            """
            :ivar position:
            :ivar connection_point_in:
            :ivar action:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar negated:
            :ivar width:
            :ivar height:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            action: List["Body.Ld.ActionBlock.Action"] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class Action:
                """
                Association of an action with qualifier.

                :ivar rel_position: Relative position of the action.
                    Origin is the anchor position of the action block.
                :ivar reference: Name of an action or boolean variable.
                :ivar inline: Inline implementation of an action body.
                :ivar connection_point_out:
                :ivar add_data:
                :ivar documentation:
                :ivar local_id:
                :ivar qualifier:
                :ivar width:
                :ivar height:
                :ivar duration:
                :ivar indicator:
                :ivar execution_order_id: Used to identify the order of
                    execution. Also used to identify one special block
                    if there are several blocks with the same name.
                :ivar global_id:
                """
                rel_position: Optional[Position] = field(
                    default=None,
                    metadata={
                        "name": "relPosition",
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        "required": True,
                    }
                )
                reference: Optional["Body.Ld.ActionBlock.Action.Reference"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                inline: Optional["Body"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                connection_point_out: Optional[ConnectionPointOut] = field(
                    default=None,
                    metadata={
                        "name": "connectionPointOut",
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
                local_id: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "localId",
                        "type": "Attribute",
                        "required": True,
                    }
                )
                qualifier: ActionQualifier = field(
                    default=ActionQualifier.N,
                    metadata={
                        "type": "Attribute",
                    }
                )
                width: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                height: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                duration: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                indicator: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                execution_order_id: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "executionOrderId",
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
                class Reference:
                    name: Optional[str] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )

        @dataclass
        class VendorElement:
            """
            Describes a graphical object representing a call statement.

            :ivar position: Anchor position of the box. Top left corner
                excluding the instance name.
            :ivar alternative_text: An alternative text to be displayed
                in generic representation of unknown elements.
            :ivar input_variables: The list of used input variables
                (consumers)
            :ivar in_out_variables: The list of used inOut variables
            :ivar output_variables: The list of used output variables
                (producers)
            :ivar add_data: Additional, vendor specific data for the
                element. Also defines the vendor specific meaning of the
                element.
            :ivar local_id:
            :ivar width:
            :ivar height:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            alternative_text: Optional[FormattedText] = field(
                default=None,
                metadata={
                    "name": "alternativeText",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            input_variables: Optional["Body.Ld.VendorElement.InputVariables"] = field(
                default=None,
                metadata={
                    "name": "inputVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            in_out_variables: Optional["Body.Ld.VendorElement.InOutVariables"] = field(
                default=None,
                metadata={
                    "name": "inOutVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            output_variables: Optional["Body.Ld.VendorElement.OutputVariables"] = field(
                default=None,
                metadata={
                    "name": "outputVariables",
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
                    "required": True,
                }
            )
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class InputVariables:
                variable: List["Body.Ld.VendorElement.InputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes an inputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                            "required": True,
                        }
                    )
                    documentation: Optional[FormattedText] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class InOutVariables:
                variable: List["Body.Ld.VendorElement.InOutVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a inOutVariable of a Function or a FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class OutputVariables:
                variable: List["Body.Ld.VendorElement.OutputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a outputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

        @dataclass
        class Block:
            """
            Describes a graphical object representing a call statement.

            :ivar position: Anchor position of the box. Top left corner
                excluding the instance name.
            :ivar input_variables: The list of used input variables
                (consumers)
            :ivar in_out_variables: The list of used inOut variables
            :ivar output_variables: The list of used output variables
                (producers)
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar width:
            :ivar height:
            :ivar type_name:
            :ivar instance_name:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            input_variables: Optional["Body.Ld.Block.InputVariables"] = field(
                default=None,
                metadata={
                    "name": "inputVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            in_out_variables: Optional["Body.Ld.Block.InOutVariables"] = field(
                default=None,
                metadata={
                    "name": "inOutVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            output_variables: Optional["Body.Ld.Block.OutputVariables"] = field(
                default=None,
                metadata={
                    "name": "outputVariables",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
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
            instance_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "instanceName",
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class InputVariables:
                variable: List["Body.Ld.Block.InputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes an inputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                            "required": True,
                        }
                    )
                    documentation: Optional[FormattedText] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class InOutVariables:
                variable: List["Body.Ld.Block.InOutVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a inOutVariable of a Function or a FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class OutputVariables:
                variable: List["Body.Ld.Block.OutputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a outputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

        @dataclass
        class InVariable:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_out:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class OutVariable:
            """
            Describes a graphical object representing a variable or expression
            used as l-value.

            :ivar position:
            :ivar connection_point_in:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class InOutVariable:
            """
            Describes a graphical object representing a variable which can be
            used as l-value and r-value at the same time.

            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated_in:
            :ivar edge_in:
            :ivar storage_in:
            :ivar negated_out:
            :ivar edge_out:
            :ivar storage_out:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated_in: bool = field(
                default=False,
                metadata={
                    "name": "negatedIn",
                    "type": "Attribute",
                }
            )
            edge_in: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "name": "edgeIn",
                    "type": "Attribute",
                }
            )
            storage_in: StorageModifierType = field(
                default=StorageModifierType.NONE,
                metadata={
                    "name": "storageIn",
                    "type": "Attribute",
                }
            )
            negated_out: bool = field(
                default=False,
                metadata={
                    "name": "negatedOut",
                    "type": "Attribute",
                }
            )
            edge_out: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "name": "edgeOut",
                    "type": "Attribute",
                }
            )
            storage_out: StorageModifierType = field(
                default=StorageModifierType.NONE,
                metadata={
                    "name": "storageOut",
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
        class Label:
            """
            Describes a graphical object representing a jump label.
            """
            position: Optional[Position] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            label: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Jump:
            """
            Describes a graphical object representing a jump statement.
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            label: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Return:
            """
            Describes a graphical object representing areturn statement.
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class LeftPowerRail:
            """
            Describes a graphical object representing a left powerrail.

            :ivar position:
            :ivar connection_point_out:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_out: List["Body.Ld.LeftPowerRail.ConnectionPointOut"] = field(
                default_factory=list,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class ConnectionPointOut(ConnectionPointOut):
                formal_parameter: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "formalParameter",
                        "type": "Attribute",
                        "required": True,
                    }
                )

        @dataclass
        class RightPowerRail:
            """
            Describes a graphical object representing a right powerrail.

            :ivar position:
            :ivar connection_point_in:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: List[ConnectionPointIn] = field(
                default_factory=list,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Coil:
            """
            Describes a graphical object representing a boolean variable which
            can be used as l-value and r-value at the same time.

            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar variable: The operand is a valid boolean  iec variable
                e.g. avar[0]
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            variable: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class Contact:
            """
            Describes a graphical object representing a variable which can be
            used as l-value and r-value at the same time.

            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar variable: The operand is a valid boolean iec variable
                e.g. avar[0]
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            variable: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
    class Sfc:
        """
        :ivar comment:
        :ivar error:
        :ivar connector:
        :ivar continuation: Counterpart of the connector element
        :ivar action_block:
        :ivar vendor_element:
        :ivar block:
        :ivar in_variable: Expression used as producer
        :ivar out_variable: Expression used as consumer
        :ivar in_out_variable: Expression used as producer and consumer
        :ivar label:
        :ivar jump:
        :ivar return_value:
        :ivar left_power_rail:
        :ivar right_power_rail:
        :ivar coil:
        :ivar contact:
        :ivar step: A single step in a SFC Sequence. Actions are
            associated with a step by using an actionBlock element with
            a connection to the step element
        :ivar macro_step:
        :ivar jump_step: Jump to a step, macro step or simultaneous
            divergence. Acts like a step. Predecessor should be a
            transition.
        :ivar transition:
        :ivar selection_divergence:
        :ivar selection_convergence:
        :ivar simultaneous_divergence:
        :ivar simultaneous_convergence:
        """
        comment: List["Body.Sfc.Comment"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        error: List["Body.Sfc.Error"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        connector: List["Body.Sfc.Connector"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        continuation: List["Body.Sfc.Continuation"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        action_block: List["Body.Sfc.ActionBlock"] = field(
            default_factory=list,
            metadata={
                "name": "actionBlock",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        vendor_element: List["Body.Sfc.VendorElement"] = field(
            default_factory=list,
            metadata={
                "name": "vendorElement",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        block: List["Body.Sfc.Block"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        in_variable: List["Body.Sfc.InVariable"] = field(
            default_factory=list,
            metadata={
                "name": "inVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        out_variable: List["Body.Sfc.OutVariable"] = field(
            default_factory=list,
            metadata={
                "name": "outVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        in_out_variable: List["Body.Sfc.InOutVariable"] = field(
            default_factory=list,
            metadata={
                "name": "inOutVariable",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        label: List["Body.Sfc.Label"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        jump: List["Body.Sfc.Jump"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        return_value: List["Body.Sfc.Return"] = field(
            default_factory=list,
            metadata={
                "name": "return",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        left_power_rail: List["Body.Sfc.LeftPowerRail"] = field(
            default_factory=list,
            metadata={
                "name": "leftPowerRail",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        right_power_rail: List["Body.Sfc.RightPowerRail"] = field(
            default_factory=list,
            metadata={
                "name": "rightPowerRail",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        coil: List["Body.Sfc.Coil"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        contact: List["Body.Sfc.Contact"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        step: List["Body.Sfc.Step"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        macro_step: List["Body.Sfc.MacroStep"] = field(
            default_factory=list,
            metadata={
                "name": "macroStep",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        jump_step: List["Body.Sfc.JumpStep"] = field(
            default_factory=list,
            metadata={
                "name": "jumpStep",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        transition: List["Body.Sfc.Transition"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        selection_divergence: List["Body.Sfc.SelectionDivergence"] = field(
            default_factory=list,
            metadata={
                "name": "selectionDivergence",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        selection_convergence: List["Body.Sfc.SelectionConvergence"] = field(
            default_factory=list,
            metadata={
                "name": "selectionConvergence",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        simultaneous_divergence: List["Body.Sfc.SimultaneousDivergence"] = field(
            default_factory=list,
            metadata={
                "name": "simultaneousDivergence",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        simultaneous_convergence: List["Body.Sfc.SimultaneousConvergence"] = field(
            default_factory=list,
            metadata={
                "name": "simultaneousConvergence",
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )

        @dataclass
        class Comment:
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            content: Optional[FormattedText] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
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

        @dataclass
        class Error:
            """Describes a graphical object representing a conversion error.

            Used to keep information which can not be interpreted by the
            importing system
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            content: Optional[FormattedText] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
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

        @dataclass
        class Connector:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_in:
            :ivar add_data:
            :ivar documentation:
            :ivar name: The operand is a valid iec variable e.g. avar[0]
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
        class Continuation:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_out:
            :ivar add_data:
            :ivar documentation:
            :ivar name: The operand is a valid iec variable e.g. avar[0]
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
        class ActionBlock:
            """
            :ivar position:
            :ivar connection_point_in:
            :ivar action:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar negated:
            :ivar width:
            :ivar height:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            action: List["Body.Sfc.ActionBlock.Action"] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class Action:
                """
                Association of an action with qualifier.

                :ivar rel_position: Relative position of the action.
                    Origin is the anchor position of the action block.
                :ivar reference: Name of an action or boolean variable.
                :ivar inline: Inline implementation of an action body.
                :ivar connection_point_out:
                :ivar add_data:
                :ivar documentation:
                :ivar local_id:
                :ivar qualifier:
                :ivar width:
                :ivar height:
                :ivar duration:
                :ivar indicator:
                :ivar execution_order_id: Used to identify the order of
                    execution. Also used to identify one special block
                    if there are several blocks with the same name.
                :ivar global_id:
                """
                rel_position: Optional[Position] = field(
                    default=None,
                    metadata={
                        "name": "relPosition",
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        "required": True,
                    }
                )
                reference: Optional["Body.Sfc.ActionBlock.Action.Reference"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                inline: Optional["Body"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                connection_point_out: Optional[ConnectionPointOut] = field(
                    default=None,
                    metadata={
                        "name": "connectionPointOut",
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
                local_id: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "localId",
                        "type": "Attribute",
                        "required": True,
                    }
                )
                qualifier: ActionQualifier = field(
                    default=ActionQualifier.N,
                    metadata={
                        "type": "Attribute",
                    }
                )
                width: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                height: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                duration: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                indicator: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    }
                )
                execution_order_id: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "executionOrderId",
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
                class Reference:
                    name: Optional[str] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )

        @dataclass
        class VendorElement:
            """
            Describes a graphical object representing a call statement.

            :ivar position: Anchor position of the box. Top left corner
                excluding the instance name.
            :ivar alternative_text: An alternative text to be displayed
                in generic representation of unknown elements.
            :ivar input_variables: The list of used input variables
                (consumers)
            :ivar in_out_variables: The list of used inOut variables
            :ivar output_variables: The list of used output variables
                (producers)
            :ivar add_data: Additional, vendor specific data for the
                element. Also defines the vendor specific meaning of the
                element.
            :ivar local_id:
            :ivar width:
            :ivar height:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            alternative_text: Optional[FormattedText] = field(
                default=None,
                metadata={
                    "name": "alternativeText",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            input_variables: Optional["Body.Sfc.VendorElement.InputVariables"] = field(
                default=None,
                metadata={
                    "name": "inputVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            in_out_variables: Optional["Body.Sfc.VendorElement.InOutVariables"] = field(
                default=None,
                metadata={
                    "name": "inOutVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            output_variables: Optional["Body.Sfc.VendorElement.OutputVariables"] = field(
                default=None,
                metadata={
                    "name": "outputVariables",
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
                    "required": True,
                }
            )
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class InputVariables:
                variable: List["Body.Sfc.VendorElement.InputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes an inputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                            "required": True,
                        }
                    )
                    documentation: Optional[FormattedText] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class InOutVariables:
                variable: List["Body.Sfc.VendorElement.InOutVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a inOutVariable of a Function or a FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class OutputVariables:
                variable: List["Body.Sfc.VendorElement.OutputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a outputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

        @dataclass
        class Block:
            """
            Describes a graphical object representing a call statement.

            :ivar position: Anchor position of the box. Top left corner
                excluding the instance name.
            :ivar input_variables: The list of used input variables
                (consumers)
            :ivar in_out_variables: The list of used inOut variables
            :ivar output_variables: The list of used output variables
                (producers)
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar width:
            :ivar height:
            :ivar type_name:
            :ivar instance_name:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            input_variables: Optional["Body.Sfc.Block.InputVariables"] = field(
                default=None,
                metadata={
                    "name": "inputVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            in_out_variables: Optional["Body.Sfc.Block.InOutVariables"] = field(
                default=None,
                metadata={
                    "name": "inOutVariables",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            output_variables: Optional["Body.Sfc.Block.OutputVariables"] = field(
                default=None,
                metadata={
                    "name": "outputVariables",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
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
            instance_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "instanceName",
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class InputVariables:
                variable: List["Body.Sfc.Block.InputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes an inputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                            "required": True,
                        }
                    )
                    documentation: Optional[FormattedText] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class InOutVariables:
                variable: List["Body.Sfc.Block.InOutVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a inOutVariable of a Function or a FunctionBlock.
                    """
                    connection_point_in: Optional[ConnectionPointIn] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointIn",
                            "type": "Element",
                            "namespace": "http://www.plcopen.org/xml/tc6_0201",
                        }
                    )
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

            @dataclass
            class OutputVariables:
                variable: List["Body.Sfc.Block.OutputVariables.Variable"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )

                @dataclass
                class Variable:
                    """
                    Describes a outputVariable of a Function or a
                    FunctionBlock.
                    """
                    connection_point_out: Optional[ConnectionPointOut] = field(
                        default=None,
                        metadata={
                            "name": "connectionPointOut",
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
                    formal_parameter: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "formalParameter",
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    negated: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    edge: EdgeModifierType = field(
                        default=EdgeModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    storage: StorageModifierType = field(
                        default=StorageModifierType.NONE,
                        metadata={
                            "type": "Attribute",
                        }
                    )
                    hidden: bool = field(
                        default=False,
                        metadata={
                            "type": "Attribute",
                        }
                    )

        @dataclass
        class InVariable:
            """
            Describes a graphical object representing a variable, literal or
            expression used as r-value.

            :ivar position:
            :ivar connection_point_out:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class OutVariable:
            """
            Describes a graphical object representing a variable or expression
            used as l-value.

            :ivar position:
            :ivar connection_point_in:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class InOutVariable:
            """
            Describes a graphical object representing a variable which can be
            used as l-value and r-value at the same time.

            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar expression: The operand is a valid iec variable e.g.
                avar[0].
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated_in:
            :ivar edge_in:
            :ivar storage_in:
            :ivar negated_out:
            :ivar edge_out:
            :ivar storage_out:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            expression: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated_in: bool = field(
                default=False,
                metadata={
                    "name": "negatedIn",
                    "type": "Attribute",
                }
            )
            edge_in: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "name": "edgeIn",
                    "type": "Attribute",
                }
            )
            storage_in: StorageModifierType = field(
                default=StorageModifierType.NONE,
                metadata={
                    "name": "storageIn",
                    "type": "Attribute",
                }
            )
            negated_out: bool = field(
                default=False,
                metadata={
                    "name": "negatedOut",
                    "type": "Attribute",
                }
            )
            edge_out: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "name": "edgeOut",
                    "type": "Attribute",
                }
            )
            storage_out: StorageModifierType = field(
                default=StorageModifierType.NONE,
                metadata={
                    "name": "storageOut",
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
        class Label:
            """
            Describes a graphical object representing a jump label.
            """
            position: Optional[Position] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            label: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Jump:
            """
            Describes a graphical object representing a jump statement.
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            label: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Return:
            """
            Describes a graphical object representing areturn statement.
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class LeftPowerRail:
            """
            Describes a graphical object representing a left powerrail.

            :ivar position:
            :ivar connection_point_out:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_out: List["Body.Sfc.LeftPowerRail.ConnectionPointOut"] = field(
                default_factory=list,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class ConnectionPointOut(ConnectionPointOut):
                formal_parameter: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "formalParameter",
                        "type": "Attribute",
                        "required": True,
                    }
                )

        @dataclass
        class RightPowerRail:
            """
            Describes a graphical object representing a right powerrail.

            :ivar position:
            :ivar connection_point_in:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: List[ConnectionPointIn] = field(
                default_factory=list,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Coil:
            """
            Describes a graphical object representing a boolean variable which
            can be used as l-value and r-value at the same time.

            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar variable: The operand is a valid boolean  iec variable
                e.g. avar[0]
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            variable: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class Contact:
            """
            Describes a graphical object representing a variable which can be
            used as l-value and r-value at the same time.

            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar variable: The operand is a valid boolean iec variable
                e.g. avar[0]
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar execution_order_id:
            :ivar negated:
            :ivar edge:
            :ivar storage:
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            variable: Optional[str] = field(
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            edge: EdgeModifierType = field(
                default=EdgeModifierType.NONE,
                metadata={
                    "type": "Attribute",
                }
            )
            storage: StorageModifierType = field(
                default=StorageModifierType.NONE,
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
        class Step:
            """
            Contains actions.

            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar connection_point_out_action:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar name:
            :ivar initial_step:
            :ivar negated:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional["Body.Sfc.Step.ConnectionPointOut"] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out_action: Optional["Body.Sfc.Step.ConnectionPointOutAction"] = field(
                default=None,
                metadata={
                    "name": "connectionPointOutAction",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            initial_step: bool = field(
                default=False,
                metadata={
                    "name": "initialStep",
                    "type": "Attribute",
                }
            )
            negated: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class ConnectionPointOut(ConnectionPointOut):
                formal_parameter: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "formalParameter",
                        "type": "Attribute",
                        "required": True,
                    }
                )

            @dataclass
            class ConnectionPointOutAction(ConnectionPointOut):
                formal_parameter: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "formalParameter",
                        "type": "Attribute",
                        "required": True,
                    }
                )

        @dataclass
        class MacroStep:
            """
            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar body:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar name:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            body: Optional["Body"] = field(
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
            documentation: Optional[FormattedText] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class JumpStep:
            """
            :ivar position:
            :ivar connection_point_in:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar target_name:
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            target_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "targetName",
                    "type": "Attribute",
                    "required": True,
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
        class Transition:
            """
            :ivar position:
            :ivar connection_point_in:
            :ivar connection_point_out:
            :ivar condition:
            :ivar add_data:
            :ivar documentation:
            :ivar local_id:
            :ivar height:
            :ivar width:
            :ivar priority: The priority of a transition is evaluated,
                if the transition is connected to a selectionDivergence
                element.
            :ivar execution_order_id: Used to identify the order of
                execution. Also used to identify one special block if
                there are several blocks with the same name.
            :ivar global_id:
            """
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            condition: Optional["Body.Sfc.Transition.Condition"] = field(
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
            documentation: Optional[FormattedText] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            priority: Optional[int] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            execution_order_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "executionOrderId",
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
            class Condition:
                reference: Optional["Body.Sfc.Transition.Condition.Reference"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                connection_point_in: Optional[ConnectionPointIn] = field(
                    default=None,
                    metadata={
                        "name": "connectionPointIn",
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                inline: Optional["Inline"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    }
                )
                negated: bool = field(
                    default=False,
                    metadata={
                        "type": "Attribute",
                    }
                )

                @dataclass
                class Reference:
                    name: Optional[str] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )

        @dataclass
        class SelectionDivergence:
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: List["Body.Sfc.SelectionDivergence.ConnectionPointOut"] = field(
                default_factory=list,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
            class ConnectionPointOut(ConnectionPointOut):
                formal_parameter: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "formalParameter",
                        "type": "Attribute",
                        "required": True,
                    }
                )

        @dataclass
        class SelectionConvergence:
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: List[ConnectionPointIn] = field(
                default_factory=list,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
        class SimultaneousDivergence:
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: Optional[ConnectionPointIn] = field(
                default=None,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: List["Body.Sfc.SimultaneousDivergence.ConnectionPointOut"] = field(
                default_factory=list,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            name: Optional[str] = field(
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
            class ConnectionPointOut(ConnectionPointOut):
                formal_parameter: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "formalParameter",
                        "type": "Attribute",
                        "required": True,
                    }
                )

        @dataclass
        class SimultaneousConvergence:
            position: Optional[Position] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                    "required": True,
                }
            )
            connection_point_in: List[ConnectionPointIn] = field(
                default_factory=list,
                metadata={
                    "name": "connectionPointIn",
                    "type": "Element",
                    "namespace": "http://www.plcopen.org/xml/tc6_0201",
                }
            )
            connection_point_out: Optional[ConnectionPointOut] = field(
                default=None,
                metadata={
                    "name": "connectionPointOut",
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
            local_id: Optional[int] = field(
                default=None,
                metadata={
                    "name": "localId",
                    "type": "Attribute",
                    "required": True,
                }
            )
            height: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                }
            )
            width: Optional[Decimal] = field(
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
class Inline(Body):
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
