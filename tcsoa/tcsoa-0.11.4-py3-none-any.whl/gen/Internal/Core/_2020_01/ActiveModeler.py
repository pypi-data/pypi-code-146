from __future__ import annotations

from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PropertyDefinition(TcBaseObj):
    """
    Structure which has all the information needed for a property.
    
    :var name: Name of the Property.
    :var displayName: Display name of the property.
    :var description: Description about the property.
    :var propertyStorageType: Storage type of property. Supported types are
    - Boolean
    - Character
    - Double
    - Integer
    - Date
    - String
    - LongString
    
    
    :var propertyOptions: A map (string, list of strings) which has a list of string options. Key is property option's
    name and value is option values as a list of strings. Supported Options are
    - initialValue - value to populate the attribute. 
    - lowerBound - lower numerical limit for a numerical or alphanumerical attribute. 
    - upperBound - upper numerical limit for a numerical or alphanumerical attribute.
    - maxStringLength - Maximum String length. 0 for non-string datatypes.
    - isArray - Specifies that the attribute is an array of the data of the data type (for example, string). Takes
    boolean value as a string (true/false). Default is false. 
    - unlimited - Indicates that there is no limit on the number of array elements used for the attribute. Default is
    false.
    - maxLength - Specifies the maximum number of array elements allowed for the attribute.
    - isTransient - Does not persist the attribute in the database. Takes boolean value as a string (true/false).
    Default is false.
    - nullsAllowed - Allows an empty value for the attribute. Takes boolean value as a string (true/false). Default is
    true.
    - isUnique - Specifies that the attribute value cannot be duplicated. Takes boolean value as a string (true/false).
    Default is false.
    - followOnExport - For typed and untyped references, exports the referenced object when the attribute is exported.
    Takes boolean value as a string (true/false). Default is false
    - isPublicRead - Grants everyone read access to the attribute. Takes boolean value as a string (true/false).
    Default is false
    - isPublicWrite - Grants everyone write privileges on the attribute. Takes boolean value as a string (true/false).
    Default is false
    - isCandidateKey - Specifies that when exporting an object, send this attribute and rely on the receiving site to
    look up this string in the local database. This is typically used for system administration defined classes such as
    unit of measure where a local administrator may want to control what units exist on his site. Takes boolean value
    as a string (true/false). Default is false
    - exportAsString - Specifies that when exporting an object, export this attribute as a string. Takes boolean value
    as a string (true/false). Default is false
    - noBackpointer - Does not record the attribute in the POM backpointer table. Each time a forward pointer is
    created for an attribute, an inverse record is stored in the POM backpointer table. Therefore, the backpointer
    table keeps a record of where-referenced attributes and is used for where-referenced calls and for a check that
    things are not referenced when an item is deleted. To help system optimization, you may want to use the No
    Backpointer key for those attributes that are unlikely ever to be deleted (such as owning-user, owning-group, or
    dataset-type). Selecting the No Backpointer key saves the POM system from having to check every reference column in
    the table whenever a where-referenced or delete action is called. Takes boolean value as a string (true/false).
    Default is false.
    - isRequired - The Required property allows you to specify whether a value must be entered for a specific object
    property. Takes boolean value as a string (true/false). Default is false.
    
    
    :var propertyType: Specifies type of property. Valid values are:
    - Attribute
    - Runtime
    - Relation
    - Compound
    - Table
    - Name-value
    
    """
    name: str = ''
    displayName: str = ''
    description: str = ''
    propertyStorageType: str = ''
    propertyOptions: StringVectorMap = None
    propertyType: str = ''


@dataclass
class TypeDefinition(TcBaseObj):
    """
    Business object type definition structure used to create the DataModel update Input.
    
    :var name: Name of business object type.
    :var displayName: Display name of business object type.
    :var parentTypeName: Parent type name of the business object type.
    :var typeClassName: Class type name of the business object type.
    :var description: Description of business object type.
    :var createPrimaryBusinessObject: Creates a new class that stores the data for the new business object type.
    :var isAbstract: Disallows the creation of the business object instances in user interfaces.
    :var typeOptions: Map (string, list of strings) containing additional options. Key is BO option's name and value is
    option values as a vector of strings.
    Options supported:
    - component - Component name of this business object type.
    - storeAsLightWeightObject - Store as light weight business object (true/false). Default is false.
    - allowCreateInstanceOfSecBO - Allow instance creation of Secondary Business Object (true/false). Default is true.
    - isExportable - (true/false). Default is false.
    - isUninstantiable - (true/false). Default is false.
    - isUninheritable - (true/false). Default is false.
    
    """
    name: str = ''
    displayName: str = ''
    parentTypeName: str = ''
    typeClassName: str = ''
    description: str = ''
    createPrimaryBusinessObject: bool = False
    isAbstract: bool = False
    typeOptions: StringVectorMap = None


@dataclass
class TypeInput(TcBaseObj):
    """
    Structure which contains all the information to create a new business object type.
    
    :var typeDefinition: Structure which represents the business object type definitions.
    :var typeInputsMap: Map (string, TypeInput) containing all the dependent business object types. Key is business
    object type name and the value is a TypeInput.
    :var dataModelOptions: Map (string, vector<strings>) containing data model options with key as a string and value
    is a vector of strings
    """
    typeDefinition: TypeDefinition = None
    typeInputsMap: TypeInputMap = None
    dataModelOptions: StringVectorMap = None


@dataclass
class AddPropsOnTypeInput(TcBaseObj):
    """
    Input structure to add properties on a business object type.
    
    :var type: Type name on which new properties are being added.
    :var propDefinitions: A list of Property definitions to add properties on a business object type.
    """
    type: str = ''
    propDefinitions: List[PropertyDefinition] = ()


"""
Map with key as a string and value as vector of strings (string, vector<string>).
"""
StringVectorMap = Dict[str, List[str]]


"""
Map which contains TypeInputs. Key is business object type name and value is TypeInput.
"""
TypeInputMap = Dict[str, TypeInput]
