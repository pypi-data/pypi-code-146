from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime
from plcopen.add_data import AddData
from plcopen.add_data_info import AddDataInfo
from plcopen.body import Body
from plcopen.formatted_text import FormattedText
from plcopen.pou_instance import PouInstance
from plcopen.pou_type import PouType
from plcopen.value import Value
from plcopen.var_list import VarList
from plcopen.var_list_access import VarListAccess
from plcopen.var_list_config import VarListConfig
from plcopen.var_list_plain import DataType

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class Project:
    """
    The complete project.

    :ivar file_header:
    :ivar content_header:
    :ivar types:
    :ivar instances:
    :ivar add_data:
    :ivar documentation: Additional userspecific information to the
        element
    """
    class Meta:
        name = "project"
        namespace = "http://www.plcopen.org/xml/tc6_0201"

    file_header: Optional["Project.FileHeader"] = field(
        default=None,
        metadata={
            "name": "fileHeader",
            "type": "Element",
            "required": True,
        }
    )
    content_header: Optional["Project.ContentHeader"] = field(
        default=None,
        metadata={
            "name": "contentHeader",
            "type": "Element",
            "required": True,
        }
    )
    types: Optional["Project.Types"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    instances: Optional["Project.Instances"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    add_data: Optional[AddData] = field(
        default=None,
        metadata={
            "name": "addData",
            "type": "Element",
        }
    )
    documentation: Optional[FormattedText] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

    @dataclass
    class FileHeader:
        company_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "companyName",
                "type": "Attribute",
                "required": True,
            }
        )
        company_url: Optional[str] = field(
            default=None,
            metadata={
                "name": "companyURL",
                "type": "Attribute",
            }
        )
        product_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "productName",
                "type": "Attribute",
                "required": True,
            }
        )
        product_version: Optional[str] = field(
            default=None,
            metadata={
                "name": "productVersion",
                "type": "Attribute",
                "required": True,
            }
        )
        product_release: Optional[str] = field(
            default=None,
            metadata={
                "name": "productRelease",
                "type": "Attribute",
            }
        )
        creation_date_time: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "creationDateTime",
                "type": "Attribute",
                "required": True,
            }
        )
        content_description: Optional[str] = field(
            default=None,
            metadata={
                "name": "contentDescription",
                "type": "Attribute",
            }
        )

    @dataclass
    class ContentHeader:
        """
        :ivar comment:
        :ivar coordinate_info:
        :ivar add_data_info:
        :ivar add_data:
        :ivar name:
        :ivar version:
        :ivar modification_date_time:
        :ivar organization:
        :ivar author:
        :ivar language: Documentation language of the project e.g. "en-
            US"
        """
        comment: Optional[str] = field(
            default=None,
            metadata={
                "name": "Comment",
                "type": "Element",
            }
        )
        coordinate_info: Optional["Project.ContentHeader.CoordinateInfo"] = field(
            default=None,
            metadata={
                "name": "coordinateInfo",
                "type": "Element",
                "required": True,
            }
        )
        add_data_info: Optional[AddDataInfo] = field(
            default=None,
            metadata={
                "name": "addDataInfo",
                "type": "Element",
            }
        )
        add_data: Optional[AddData] = field(
            default=None,
            metadata={
                "name": "addData",
                "type": "Element",
            }
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        version: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        modification_date_time: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "modificationDateTime",
                "type": "Attribute",
            }
        )
        organization: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        author: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        language: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )

        @dataclass
        class CoordinateInfo:
            page_size: Optional["Project.ContentHeader.CoordinateInfo.PageSize"] = field(
                default=None,
                metadata={
                    "name": "pageSize",
                    "type": "Element",
                }
            )
            fbd: Optional["Project.ContentHeader.CoordinateInfo.Fbd"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            ld: Optional["Project.ContentHeader.CoordinateInfo.Ld"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            sfc: Optional["Project.ContentHeader.CoordinateInfo.Sfc"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )

            @dataclass
            class PageSize:
                x: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )
                y: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )

            @dataclass
            class Fbd:
                scaling: Optional["Project.ContentHeader.CoordinateInfo.Fbd.Scaling"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "required": True,
                    }
                )

                @dataclass
                class Scaling:
                    x: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    y: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )

            @dataclass
            class Ld:
                scaling: Optional["Project.ContentHeader.CoordinateInfo.Ld.Scaling"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "required": True,
                    }
                )

                @dataclass
                class Scaling:
                    x: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    y: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )

            @dataclass
            class Sfc:
                scaling: Optional["Project.ContentHeader.CoordinateInfo.Sfc.Scaling"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "required": True,
                    }
                )

                @dataclass
                class Scaling:
                    x: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )
                    y: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )

    @dataclass
    class Types:
        data_types: Optional["Project.Types.DataTypes"] = field(
            default=None,
            metadata={
                "name": "dataTypes",
                "type": "Element",
                "required": True,
            }
        )
        pous: Optional["Project.Types.Pous"] = field(
            default=None,
            metadata={
                "type": "Element",
                "required": True,
            }
        )

        @dataclass
        class DataTypes:
            data_type: List["Project.Types.DataTypes.DataType"] = field(
                default_factory=list,
                metadata={
                    "name": "dataType",
                    "type": "Element",
                }
            )

            @dataclass
            class DataType:
                """
                :ivar base_type:
                :ivar initial_value:
                :ivar add_data:
                :ivar documentation: Additional userspecific information
                    to the element
                :ivar name:
                """
                base_type: Optional[DataType] = field(
                    default=None,
                    metadata={
                        "name": "baseType",
                        "type": "Element",
                        "required": True,
                    }
                )
                initial_value: Optional[Value] = field(
                    default=None,
                    metadata={
                        "name": "initialValue",
                        "type": "Element",
                    }
                )
                add_data: Optional[AddData] = field(
                    default=None,
                    metadata={
                        "name": "addData",
                        "type": "Element",
                    }
                )
                documentation: Optional[FormattedText] = field(
                    default=None,
                    metadata={
                        "type": "Element",
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
        class Pous:
            pou: List["Project.Types.Pous.Pou"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                }
            )

            @dataclass
            class Pou:
                """
                :ivar interface:
                :ivar actions:
                :ivar transitions:
                :ivar body:
                :ivar add_data:
                :ivar documentation: Additional userspecific information
                    to the element
                :ivar name:
                :ivar pou_type:
                :ivar global_id:
                """
                interface: Optional["Project.Types.Pous.Pou.Interface"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                actions: Optional["Project.Types.Pous.Pou.Actions"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                transitions: Optional["Project.Types.Pous.Pou.Transitions"] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                body: List[Body] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                    }
                )
                add_data: Optional[AddData] = field(
                    default=None,
                    metadata={
                        "name": "addData",
                        "type": "Element",
                    }
                )
                documentation: Optional[FormattedText] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                name: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )
                pou_type: Optional[PouType] = field(
                    default=None,
                    metadata={
                        "name": "pouType",
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
                class Interface:
                    """
                    :ivar return_type:
                    :ivar local_vars:
                    :ivar temp_vars:
                    :ivar input_vars:
                    :ivar output_vars:
                    :ivar in_out_vars:
                    :ivar external_vars:
                    :ivar global_vars:
                    :ivar access_vars:
                    :ivar add_data:
                    :ivar documentation: Additional userspecific
                        information to the element
                    """
                    return_type: Optional[DataType] = field(
                        default=None,
                        metadata={
                            "name": "returnType",
                            "type": "Element",
                        }
                    )
                    local_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "localVars",
                            "type": "Element",
                            "sequential": True,
                        }
                    )
                    temp_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "tempVars",
                            "type": "Element",
                            "sequential": True,
                        }
                    )
                    input_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "inputVars",
                            "type": "Element",
                            "sequential": True,
                        }
                    )
                    output_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "outputVars",
                            "type": "Element",
                            "sequential": True,
                        }
                    )
                    in_out_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "inOutVars",
                            "type": "Element",
                            "sequential": True,
                        }
                    )
                    external_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "externalVars",
                            "type": "Element",
                            "sequential": True,
                        }
                    )
                    global_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "globalVars",
                            "type": "Element",
                            "sequential": True,
                        }
                    )
                    access_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "accessVars",
                            "type": "Element",
                            "sequential": True,
                        }
                    )
                    add_data: Optional[AddData] = field(
                        default=None,
                        metadata={
                            "name": "addData",
                            "type": "Element",
                        }
                    )
                    documentation: Optional[FormattedText] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        }
                    )

                @dataclass
                class Actions:
                    action: List["Project.Types.Pous.Pou.Actions.Action"] = field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                        }
                    )

                    @dataclass
                    class Action:
                        """
                        :ivar body:
                        :ivar add_data:
                        :ivar documentation: Additional userspecific
                            information to the element
                        :ivar name:
                        :ivar global_id:
                        """
                        body: Optional[Body] = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "required": True,
                            }
                        )
                        add_data: Optional[AddData] = field(
                            default=None,
                            metadata={
                                "name": "addData",
                                "type": "Element",
                            }
                        )
                        documentation: Optional[FormattedText] = field(
                            default=None,
                            metadata={
                                "type": "Element",
                            }
                        )
                        name: Optional[str] = field(
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
                class Transitions:
                    transition: List["Project.Types.Pous.Pou.Transitions.Transition"] = field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                        }
                    )

                    @dataclass
                    class Transition:
                        """
                        :ivar body:
                        :ivar add_data:
                        :ivar documentation: Additional userspecific
                            information to the element
                        :ivar name:
                        :ivar global_id:
                        """
                        body: Optional[Body] = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "required": True,
                            }
                        )
                        add_data: Optional[AddData] = field(
                            default=None,
                            metadata={
                                "name": "addData",
                                "type": "Element",
                            }
                        )
                        documentation: Optional[FormattedText] = field(
                            default=None,
                            metadata={
                                "type": "Element",
                            }
                        )
                        name: Optional[str] = field(
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
    class Instances:
        configurations: Optional["Project.Instances.Configurations"] = field(
            default=None,
            metadata={
                "type": "Element",
                "required": True,
            }
        )

        @dataclass
        class Configurations:
            configuration: List["Project.Instances.Configurations.Configuration"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                }
            )

            @dataclass
            class Configuration:
                """
                Represents a group of resources and global variables.

                :ivar resource:
                :ivar global_vars:
                :ivar access_vars:
                :ivar config_vars:
                :ivar add_data:
                :ivar documentation: Additional userspecific information
                    to the element
                :ivar name:
                :ivar global_id:
                """
                resource: List["Project.Instances.Configurations.Configuration.Resource"] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                    }
                )
                global_vars: List[VarList] = field(
                    default_factory=list,
                    metadata={
                        "name": "globalVars",
                        "type": "Element",
                    }
                )
                access_vars: Optional[VarListAccess] = field(
                    default=None,
                    metadata={
                        "name": "accessVars",
                        "type": "Element",
                    }
                )
                config_vars: Optional[VarListConfig] = field(
                    default=None,
                    metadata={
                        "name": "configVars",
                        "type": "Element",
                    }
                )
                add_data: Optional[AddData] = field(
                    default=None,
                    metadata={
                        "name": "addData",
                        "type": "Element",
                    }
                )
                documentation: Optional[FormattedText] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                name: Optional[str] = field(
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
                class Resource:
                    """
                    Represents a group of programs and tasks and global
                    variables.

                    :ivar task:
                    :ivar global_vars:
                    :ivar pou_instance:
                    :ivar add_data:
                    :ivar documentation: Additional userspecific
                        information to the element
                    :ivar name:
                    :ivar global_id:
                    """
                    task: List["Project.Instances.Configurations.Configuration.Resource.Task"] = field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                        }
                    )
                    global_vars: List[VarList] = field(
                        default_factory=list,
                        metadata={
                            "name": "globalVars",
                            "type": "Element",
                        }
                    )
                    pou_instance: List[PouInstance] = field(
                        default_factory=list,
                        metadata={
                            "name": "pouInstance",
                            "type": "Element",
                        }
                    )
                    add_data: Optional[AddData] = field(
                        default=None,
                        metadata={
                            "name": "addData",
                            "type": "Element",
                        }
                    )
                    documentation: Optional[FormattedText] = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        }
                    )
                    name: Optional[str] = field(
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
                    class Task:
                        """
                        Represents a periodic or triggered task.

                        :ivar pou_instance:
                        :ivar add_data:
                        :ivar documentation: Additional userspecific
                            information to the element
                        :ivar name:
                        :ivar single:
                        :ivar interval: Vendor specific: Either a
                            constant duration as defined in the IEC or
                            variable name.
                        :ivar priority:
                        :ivar global_id:
                        """
                        pou_instance: List[PouInstance] = field(
                            default_factory=list,
                            metadata={
                                "name": "pouInstance",
                                "type": "Element",
                            }
                        )
                        add_data: Optional[AddData] = field(
                            default=None,
                            metadata={
                                "name": "addData",
                                "type": "Element",
                            }
                        )
                        documentation: Optional[FormattedText] = field(
                            default=None,
                            metadata={
                                "type": "Element",
                            }
                        )
                        name: Optional[str] = field(
                            default=None,
                            metadata={
                                "type": "Attribute",
                                "required": True,
                            }
                        )
                        single: Optional[str] = field(
                            default=None,
                            metadata={
                                "type": "Attribute",
                            }
                        )
                        interval: Optional[str] = field(
                            default=None,
                            metadata={
                                "type": "Attribute",
                            }
                        )
                        priority: Optional[int] = field(
                            default=None,
                            metadata={
                                "type": "Attribute",
                                "required": True,
                                "min_inclusive": 0,
                                "max_inclusive": 65535,
                            }
                        )
                        global_id: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "globalId",
                                "type": "Attribute",
                            }
                        )
