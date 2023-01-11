from __future__ import annotations

from tcsoa.gen.BusinessObjects import ListOfValues, CadAttrMappingDefinition
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAllAttrMappingsResponse(TcBaseObj):
    """
    The response from the 'getAllAttrMappings2' operation.
    
    :var attrMappingInfos: A list of attribute mapping information.
    :var serviceData: The 'ServiceData'.  This operation will populate the 'ServiceData' plain objects with
    'CadAttrMappingDefinition' objects and property descriptor LOV objects.
    """
    attrMappingInfos: List[AttrMappingInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AttrMappingInfo(TcBaseObj):
    """
    Attribute mapping information.
    
    :var cadAttrMappingDefinition: The CadAttrMappingDefinition object reference representing the mapping definition.
    :var propDesc: The property descriptor structure containing property information for the mapping definition
    property.
    """
    cadAttrMappingDefinition: CadAttrMappingDefinition = None
    propDesc: PropDescriptor = None


@dataclass
class PropDescriptor(TcBaseObj):
    """
    The 'PropDescriptor' struct describes information about the Teamcenter property
    
    :var propName: Name of the property
    :var displayName: Display name of the property. This is the localized name for the property.
    :var isModifiable: Specifies whether the property is modifiable
    :var attachedSpecifier: Attached specifier holds the following information: 
    - Is it a hierarchical LOV attachment? If it is hierarchical LOV attachment, the specifier value is 0;  This value
    can be 0 in following cases:
    -     Standard LOV attachment (Combobox, Range etc)
    -     Value Ddescription attachment only ( specifier value is 0 for the value attachment )
    -     To check whether it is hierarchical or not, one needs to verify the children LOVs (value filters from LOV).
    If there are children LOVs then it could be a hierarchical LOV.
    -  Is it attached with interdependent?
    - bool isInterdependent = ( specifier & (1 << 1) ) != 0;
    -  Is it attached with description attachment?
    - bool  isDescriptionAttach = ( specifier & (1 << 1) )!= 0;
    
    
    If attached with interdependent or description attachment what is the order of the attachment?
    int order = specifier >> 8;
    :var maxLength: Maximum length for a string property.
    :var lovAttachmentsCategory: Defines categories of LOVs attached to the property.
        0:  No attachments
        1:  Only isTrue condition is attached
        2:  Only session based conditions are attached
        3:  One or more object based conditions are attached
    
    :var interdependentProps: Interdependent properties for interdependent LOVs.
    :var defaultValue: Default value for the property. This is also sometimes known as the initial value of the property
    :var propValueType: Value type for the property in integer form: 
    PROP_untyped (0) No value
    PROP_char (1) Value is a single character
    PROP_date (2) Value is a date
    PROP_double (3) Value is a double
    PROP_float (4) Value is a float
    PROP_int (5) Value is an integer
    PROP_logical (6) Value is a logical
    PROP_short (7) Value is a short
    PROP_string (8) Value is a character string
    PROP_typed_reference (9) Value is a typed reference
    PROP_untyped_reference (10) Value is an untyped reference
    PROP_external_reference (11) Value is an external reference
    PROP_note (12) Value is a note
    PROP_typed_relation (13) Value is a typed relation
    PROP_untyped_relation (14) Value is an untyped relation
    :var propType: Type for the property in integer form: 
    PROP_unknown (0) Property type is unknown
    PROP_attribute (1)  Based on a POM attribute (int, string, ...)
    PROP_reference (2)  Based on a POM reference
    PROP_relation (3) Based on an ImanRelation
    PROP_compound (4) Based on a property from another type
    PROP_runtime (5) Based on a computed value
    :var isDisplayable: Boolean property indicating if the property should be displayed (true) or not (false).
    :var isArray: Specifies whether the property is an array or single value
    :var lov: ListOfValues object attached to the property (if any)
    :var isRequired: Specifies whether the property is required
    :var isEnabled: Specifies whether the property is enabled
    """
    propName: str = ''
    displayName: str = ''
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
    lov: ListOfValues = None
    isRequired: bool = False
    isEnabled: bool = False
