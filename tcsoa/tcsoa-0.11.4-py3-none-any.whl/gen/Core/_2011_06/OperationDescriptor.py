from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Core._2008_06.PropDescriptor import PropDesc
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PropDescSaveAs(TcBaseObj):
    """
    This structure captures a property definition for a 'SaveAs' Descriptor.
    
    :var parent: Core property descriptor structure
    :var copyFromOriginal: Indicating if the property value is to be copied from original object to the object copy - 
    true indicates the property value is to be copied.
    """
    parent: PropDesc = None
    copyFromOriginal: bool = False


@dataclass
class SaveAsDesc(TcBaseObj):
    """
    This structure captures the list of property description data for 'SaveAs' Descriptor. Clients can use this
    information to generically construct 'SaveAs' dialogs for any business object.
    
    :var businessObjectName: Name of business object that owns the descriptor
    :var propDescs: List of property description data
    """
    businessObjectName: str = ''
    propDescs: List[PropDescSaveAs] = ()


@dataclass
class SaveAsDescResponse(TcBaseObj):
    """
    Structure that contains metadata information about the properties relevant to the SaveAs operation i.e, property is
    mandatory, property is visible, if value is to be copied from original object, etc. It also has the 'DeepCopyData'
    embedded within which is a recursive data structure. The 'DeepCopyData' contains information about how the
    secondary objects (related and referenced objects) are to be copied (reference, copy as object, no copy).
    
    :var saveAsDescMap: A map of business object types and SaveAs Descriptors (string/SaveAsDesc).  This is the
    container of metadata for SaveAs that can be used by clients to generically construct SaveAs dialogs for business
    objects.
    :var deepCopyInfoMap: A map of business objects and 'DeepCopyData' (business object/'DeepCopyData'). Each business
    object from the method input will have a 'DeepCopyData' in the map. The 'DeepCopyData' object contains all the
    information about how the attached objects are to be copied (Copy as Object, Copy as Reference, NoCopy, etc.). 
    'DeepCopyData' is a recursive data structure that contains the details for the attached objects at the next level.
    NOTE: Attached objects can be either referenced objects or related objects.
    :var serviceData: Service data containing errors, etc. The plain object list of the Service data is populated with
    the target objects which are to be copied as part of the SaveAs operation. If there is an error retrieving Business
    Object for the business object name corresponding to the target object, it is added to the error stack of the
    'ServiceData' as a partial error
    """
    saveAsDescMap: SaveAsDescMap = None
    deepCopyInfoMap: DeepCopyInfoMap = None
    serviceData: ServiceData = None


@dataclass
class SaveAsInput(TcBaseObj):
    """
    This structure stores all the property input that are to be set to the object copy by the 'SaveAs' operation.
    
    :var boName: Business object name
    :var stringProps: Map (string, string) containing propName, stringValue> pairs for string properties
    :var boolArrayProps: Map (string, vector<bool>) containing <'propName, boolList'> for bool array properties
    :var dateProps: Map (string, DateTime) containing <'propName, dateTimeValue'> for date properties
    :var dateArrayProps: Map (string, vector<DateTime>) containing <'propName, dateTimeList'> for date  array properties
    :var tagProps: Map ('string, BusinessObject') containing <propName, businessObject> for reference properties
    :var tagArrayProps: Map (string, vector<BusinessObject>) containing <'propName, businessObjectList'> for reference
    array properties
    :var stringArrayProps: Map (string, vector<string>) containing <'propName, stringList'> pairs for string array
    properties
    :var doubleProps: Map (string, double) containing <'propName, doubleValue'> pairs for double properties
    :var doubleArrayProps: Map (string, vector<double>) containing <'propName, doubleList'> for double array properties
    :var floatProps: Map (string, float) containing <'propName, floatValue'> for float properties
    :var floatArrayProps: Map (string, vector<float>) containing <'propName, floatList'> for float  array properties
    :var intProps: Map (string, int) containing <'propName, intValue'> for int properties
    :var intArrayProps: Map (string, vector<int>) containing <'propName, intList'> for int array properties
    :var boolProps: Map (string, bool) containing <'propName, boolValue'> for bool properties
    """
    boName: str = ''
    stringProps: StringMap = None
    boolArrayProps: BoolVectorMap = None
    dateProps: DateMap = None
    dateArrayProps: DateVectorMap = None
    tagProps: TagMap = None
    tagArrayProps: TagVectorMap = None
    stringArrayProps: StringVectorMap = None
    doubleProps: DoubleMap = None
    doubleArrayProps: DoubleVectorMap = None
    floatProps: FloatMap = None
    floatArrayProps: FloatVectorMap = None
    intProps: IntMap = None
    intArrayProps: IntVectorMap = None
    boolProps: BoolMap = None


@dataclass
class DeepCopyData(TcBaseObj):
    """
    DeepCopyData stores the deep copy information and 'OperationInput' data of the objects that will be copied via
    'saveAs' or revise operation. It also stores the nested deep copy data at the next level.
    
    :var attachedObject: Other side object
    :var propertyName: Name of relation type or reference property for which 'DeepCopy' rule is configured
    :var propertyType: Enumeration indicating if 'DeepCopyRule' is configured for relation or feference property
    :var copyAction: DeepCopy action [NoCopy, CopyAsReference, CopyAsObject or Select]
    :var isTargetPrimary: Flag indicating if target object is primary or secondary
    :var isRequired: If flag is false, the copy action can be dynamicaly changed by user
    :var copyRelations: Flag indicating whether the properties on the relation object itself need to be copied or not
    :var saveAsInputTypeName: SaveAsInput type name
    :var childDeepCopyData: List of DeepCopy data for the objects on the other side of the relation property or
    reference property
    :var saveAsInput: Store the user inputs on the 'SaveAs' dialog. NOTE: This field is not used in the 'getSaveAsDesc'
    operation. It is used in the 'saveAsObjects' operation
    """
    attachedObject: BusinessObject = None
    propertyName: str = ''
    propertyType: PropertyType = None
    copyAction: str = ''
    isTargetPrimary: bool = False
    isRequired: bool = False
    copyRelations: bool = False
    saveAsInputTypeName: str = ''
    childDeepCopyData: List[DeepCopyData] = ()
    saveAsInput: SaveAsInput = None


class PropertyType(Enum):
    """
    This is an enumeration of the property types for which DeepCopy Rule configuration is enabled.
    """
    Relation = 'Relation'
    Reference = 'Reference'


"""
Map contains a list of <name, value> pairs '(string, DateTime').  Each pair stores information for a date property. In each pair,  name is the property name and value is  a DateTime for the property.
"""
DateMap = Dict[str, datetime]


"""
Map contains a list of <name, valueList> pairs ('string, vector< DateTime>').  Each pair stores information for a Date array property. In each pair, name is the property name and value is a list of DateTime for the property.
"""
DateVectorMap = Dict[str, List[datetime]]


"""
Map contains a list of <name, value> pairs ('BusinessObject, vector<DeepCopyData>').  For each pair, name is the business object and value holds  the deep copy data for the business object.
"""
DeepCopyInfoMap = Dict[BusinessObject, List[DeepCopyData]]


"""
Map contains a list of <name, value> pairs ('string, double').  Each pair stores information for a double property. In each pair, name is the property name and value is a double for the property.
"""
DoubleMap = Dict[str, float]


"""
Map contains a list of <name, valueList> pairs ('string, vector< double>').  Each pair stores information for a double array property. In each pair, name is the property name and value is a list of doubles for the property.
"""
DoubleVectorMap = Dict[str, List[float]]


"""
Map contains a list of <name, value> pairs ('string, float').  Each pair stores information for a float property. In each pair,  name is the property name and value is a float for the property.
"""
FloatMap = Dict[str, float]


"""
Map contains a list of <name, valueList> pairs ('string, vector< float>').  Each pair stores information for a float array property. In each pair, name is the property name and  value is a list of floats for the property.
"""
FloatVectorMap = Dict[str, List[float]]


"""
Map contains a list of <name, value> pairs '(string, vector< int>').  Each pair stores information for an int property. In each pair,  name is the property name and value is an int value for the property.
"""
IntMap = Dict[str, int]


"""
Map contains a list of <name, valueList> pairs ('string, int').  Each pair stores information for an int array property. In each pair, name is the property name and  value is the list of ints for the property.
"""
IntVectorMap = Dict[str, List[int]]


"""
Map contains a list of <name, value> pairs ('string, SaveAsDesc').  For each pair, name is the business object name and value corresponds to 'SaveAs' Descriptor data for the business object.
"""
SaveAsDescMap = Dict[str, SaveAsDesc]


"""
Map contains a list of <name, value> pairs ('string, bool').  Each pair stores information for a bool property. In each pair, name is the property name and  value is a bool for the property.
"""
BoolMap = Dict[str, bool]


"""
Map contains a list of <name, value> pairs ('string, string').  Each pair stores information for a string property. In each pair,  name is the property name and  value is a string for the property.
"""
StringMap = Dict[str, str]


"""
Map contains a list of <name, valueVector> pairs '(string, vector< string>').   Each pair stores information for a string array property. In each pair, name is the property name  and value is a list of strings for the property.
"""
StringVectorMap = Dict[str, List[str]]


"""
Map contains a list of <name, valueVector> pairs.  Each pair stores information for a bool array property. In each pair, name is the property name and value is a list of bool values for the property.
"""
BoolVectorMap = Dict[str, List[bool]]


"""
Map contains a list of <name, value> pairs ('string, BusinessObjec't).  Each pair stores information for a reference property. In each pair, name is the property name and  value is the business object for the property.
"""
TagMap = Dict[str, BusinessObject]


"""
Map contains a list of <name, valueList> pairs ('string, vector<BusinessObject>').  . Each pair stores information for a reference array property. In each pair, name is the property name and value is the list of business objects for the property.
"""
TagVectorMap = Dict[str, List[BusinessObject]]
