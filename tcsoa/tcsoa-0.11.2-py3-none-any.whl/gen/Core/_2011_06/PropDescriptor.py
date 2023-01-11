from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.BusinessObjects import ListOfValues
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AttachedPropDescsResponse(TcBaseObj):
    """
    AttachedPropDescsResponse  structure contains a map of PropDescOutput2 lists mapped to the input type name  and the
    serviceData with possible errors.
    
    :var inputTypeNameToPropDescOutput: A map of property descriptor lists and the associated input type name.
    :var serviceData: The Service Data.
    """
    inputTypeNameToPropDescOutput: InputTypeNameToPropDescOutputMap2 = None
    serviceData: ServiceData = None


@dataclass
class PropDesc(TcBaseObj):
    """
    The PropDesc struct describes information about the Teamcenter property
    
    :var propName: Name of the property
    :var displayName: Display name of the property
    :var isEnabled: Specifies whether the property is enabled
    :var isModifiable: Specifies whether the property is modifiable
    :var attachedSpecifier: attachedSpecifier
    :var maxLength: maxLength
    :var lovAttachmentsCategory: LOV attachments Category
    :var interdependentProps: interdependentProps
    :var defaultValue: Default value for the property
    :var propValueType: Value type for the property, PROP_untyped (0) No Value type PROP_char (1) Value is a single
    character PROP_date (2) Value is a date PROP_double (3) Value is a double PROP_float (4) Value is a float PROP_int
    (5) Value is an integer PROP_logical (6) Value is a logical PROP_short (7) Value is a short PROP_string (8) Value
    is a character string PROP_typed_reference (9) Value is a typed reference PROP_untyped_reference (10) Value is an
    untyped reference PROP_external_reference (11) Value is an external reference PROP_note (12) Value is a note
    PROP_typed_relation (13) Value is a typed relation PROP_untyped_relation (14) Value is an untyped relation
    :var propType: Type for the property PROP_unknown (0) Property type is Unknown PROP_attribute (1)  Based on a POM
    Attribute (int, string, ...) PROP_reference (2)  Based on a POM Reference PROP_relation (3) Based on an
    ImanRelation PROP_compound (4) Based on a property from another Type PROP_runtime (5) Based on a computed value
    :var isDisplayable: isDisplayable
    :var isArray: Specifies whether the property is an array or single value
    :var maxNumElems: Specifies the max number of elements
    :var lov: ListOfValues object attached to the property (if any)
    :var isRequired: Specifies whether the property is required
    """
    propName: str = ''
    displayName: str = ''
    isEnabled: bool = False
    isModifiable: bool = False
    attachedSpecifier: int = 0
    maxLength: int = 0
    lovAttachmentsCategory: int = 0
    interdependentProps: List[str] = ()
    defaultValue: str = ''
    propValueType: int = 0
    propType: int = 0
    isDisplayable: bool = False
    isArray: bool = False
    maxNumElems: int = 0
    lov: ListOfValues = None
    isRequired: bool = False


@dataclass
class PropDescOutput2(TcBaseObj):
    """
    Property Description Output
    
    :var propName: Input Property name for which PropDesc needs to be fetched
    :var propertyDesc: The PropDescriptor struct describes information about the Teamcenter property
    """
    propName: str = ''
    propertyDesc: PropDesc = None


"""
InputTypeNameToPropDescOutputMap2
"""
InputTypeNameToPropDescOutputMap2 = Dict[str, List[PropDescOutput2]]
