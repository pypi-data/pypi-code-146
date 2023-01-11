from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ListOfValues
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetValidRelationTypesResponse(TcBaseObj):
    """
    Response of the getValidRelationTypes SOA.
    
    :var relationTypesResults: Array of relation types results
    :var serviceData: Exceptions from internal processing returned as PartialErrors
    """
    relationTypesResults: List[RelationTypesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class AttachedPropDescsResponse(TcBaseObj):
    """
    Attached Property Descriptors Response
    
    :var inputTypeNameToPropDescOutput: Map of input type name to PropertyDescriptor
    :var serviceData: ServiceData which has output tags as plain objects and errors in partialError
    """
    inputTypeNameToPropDescOutput: InputTypeNameToPropDescOutputMap = None
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
    :var interdependentProps: interdependentProps
    :var namingPatterns: Naming patterns for property, can be null
    :var defaultValue: Default value for the property
    :var propValueType: Value type for the property,
    PROP_untyped (0) No Value type
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
    :var propType: Type for the property
    PROP_unknown (0) Property type is Unknown
    PROP_attribute (1)  Based on a POM Attribute (int, string, ...)
    PROP_reference (2)  Based on a POM Reference
    PROP_relation (3) Based on an ImanRelation
    PROP_compound (4) Based on a property from another Type
    PROP_runtime (5) Based on a computed value
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
    interdependentProps: List[str] = ()
    namingPatterns: List[str] = ()
    defaultValue: str = ''
    propValueType: int = 0
    propType: int = 0
    isDisplayable: bool = False
    isArray: bool = False
    maxNumElems: int = 0
    lov: ListOfValues = None
    isRequired: bool = False


@dataclass
class PropDescInfo(TcBaseObj):
    """
    Property Description Information
    
    :var typeName: The name of the Teamcenter Engineering type to which property belongs
    :var propNames: List of Property names for which PropDesc needs to be fetched
    """
    typeName: str = ''
    propNames: List[str] = ()


@dataclass
class PropDescOutput(TcBaseObj):
    """
    Property Description Output
    
    :var propName: Input Property name for which PropDesc needs to be fetched
    :var propertyDesc: The PropDescriptor struct describes information about the Teamcenter property
    """
    propName: str = ''
    propertyDesc: PropDesc = None


@dataclass
class RelationTypeInfo(TcBaseObj):
    """
    RelationType information
    
    :var name: Name of the relation type.
    :var displayName: Display name of the relation type (localized).
    """
    name: str = ''
    displayName: str = ''


@dataclass
class RelationTypesInput(TcBaseObj):
    """
    Input structure for the getValidRelationTypes SOA.
    
    :var sourceType: Type of the source for assignment (part, tool, etc.)
    :var targetType: Type of the target for assignment (process, operation, etc.)
    """
    sourceType: BusinessObject = None
    targetType: BusinessObject = None


@dataclass
class RelationTypesOutput(TcBaseObj):
    """
    Output structure for the getValidRelationTypes SOA.
    
    :var sourceType: Type of the source for assignment (part, tool, etc.)
    :var targetType: Type of the target for assignment (process, operation, etc.)
    :var validRelationTypes: Array of PSOccurrenceType names
    """
    sourceType: BusinessObject = None
    targetType: BusinessObject = None
    validRelationTypes: List[RelationTypeInfo] = ()


"""
InputTypeNameToPropDescOutputMap
"""
InputTypeNameToPropDescOutputMap = Dict[str, List[PropDescOutput]]
