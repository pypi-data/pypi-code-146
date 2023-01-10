from __future__ import annotations

from enum import Enum
from typing import Dict, List
from tcsoa.gen.BusinessObjects import ListOfValues
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


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
class SecCreateDesc(TcBaseObj):
    """
    Secondary Create Descriptor definition. This is the secondary create descriptor data type for secondary objects
    that get created during object creation. For example, ItemRevision and Item Master are the secondary objects that
    get created during creation of Item. Note that this is a recursive data structure which can itself point to other
    Secondary Create Descriptors (ItemRevision pointing to ItemRevision Master)
    
    :var businessObjectTypeName: Business Object Type Name of the secondary object
    :var isRequired: Boolean field indicating if creation of secondary object is required (non optional) or not
    :var isArray: true indicates the secondary descriptor is part of an array of secondary descriptors (The relation or
    reference property on the primary create descriptor could potentially point to several secondary descriptors i.e
    Create several secondary objects for the same reference or relation property. This is the usecase for which the
    field will be true for each Secondary Descriptor in the array)
    :var compoundingCtxt: enum indicating if the secondary object is a relation (in which case value is
    'CompoundRelation') or a regular business object (in which case value is 'CompoundObject')
    :var propDescs: List of Property Descriptors for the Secondary Object
    :var secondaryCreateDescs: Map '(string, Teamcenter::Soa::Core::_2008_06::PropDescriptor::SecCreateDesc') of the
    secondary descriptor objects. For example, an ItemRevision is the Secondary CreateDescriptor for Item. The
    ItemRevision Secondary Create Descriptor itself will contain SecCreateDesc objects for ItemRevision Master which is
    also created when the ItemRevision is created. The map contains the reference property or relation property name on
    the Parent Secondary Business Object as the key and the 'SecCreateDesc' as the value. If there are no secondary
    objects to be created, the map will be empty (For example, the secondary create descriptor for Item Master  which
    is created when Item is created has an empty map)
    """
    businessObjectTypeName: str = ''
    isRequired: bool = False
    isArray: bool = False
    compoundingCtxt: CompoundingContext = None
    propDescs: List[PropDesc] = ()
    secondaryCreateDescs: SecCreateDescMap = None


@dataclass
class CreateDesc(TcBaseObj):
    """
    Create Descriptor definition
    
    :var businessObjectTypeName: Business Object Type Name
    :var propDescs: Vector of Property Descriptors
    :var secondaryCreateDescs: Map of property name to secondary object's create descriptors
    """
    businessObjectTypeName: str = ''
    propDescs: List[PropDesc] = ()
    secondaryCreateDescs: SecCreateDescMap = None


@dataclass
class CreateDescResponse(TcBaseObj):
    """
    Structure containing Create Descriptor information representing the metadata about the properties relevant to a
    Create Operation
    
    :var createDescs: List of 'Teamcenter::Soa::Core::_2008_06::PropDescriptor::CreateDesc'  objects. Each element in
    the list is a Create Descriptor for a business object which contains metadata information about the properties
    necessary to create the business object i.e, property is mandatory, property is visible, etc. It is a recursive
    data structure which may point to secondary 'CreateDesc' objects e.g Item 'CreateDesc' contains references to
    ItemRevision and Item Master 'CreateDesc' objects
    :var srvData: Service data containing partial errors. If there is any error in retrieving the Create Descriptor for
    any Business Object in the input vector, it is returned as part of the error stack. The service data also contains
    LOV objects for the properties in the plain objects vector in the service data
    """
    createDescs: List[CreateDesc] = ()
    srvData: ServiceData = None


class CompoundingContext(Enum):
    """
    Enum for compounding context. Used to indicate if secondary (compounded) object is a compound object (value will be
    'CompoundObject') or compound relation (value will be 'CompoundRelation'). When the context is 'CompoundRelation',
    it is usually for the roperties on Relation use case when the Relation creation descriptor itself may have
    properties configured for creation 
    NOTE: 'CompoundRelation' case is not supported at this time
    """
    CompoundObject = 'CompoundObject'
    CompoundRelation = 'CompoundRelation'


"""
SecCreateDescMap
"""
SecCreateDescMap = Dict[str, List[SecCreateDesc]]
