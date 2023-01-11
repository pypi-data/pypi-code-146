from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class FailedObjInfo(TcBaseObj):
    """
    The failed client object property name and failed error list.
    
    :var failedForeignObjectName: the name of the failed client object property.
    :var errorStack: the list of failure errors.
    """
    failedForeignObjectName: str = ''
    errorStack: List[str] = ()


@dataclass
class AttrExchangeMapping(TcBaseObj):
    """
    The metadata exchange mapping information and the client object property name.
    
    :var foreignObjectPropertyName: the property name of the client object which the Teamcenter property would be
    exchanged with.
    :var mapping: the top level MappingObject.
    """
    foreignObjectPropertyName: str = ''
    mapping: MappingObject = None


@dataclass
class AttrExchangeMappingSetValue(TcBaseObj):
    """
    The metadata exchange mapping information and the value to be set on the Teamcenter property.
    
    :var attrExchange: the attribute exchange mapping information.
    :var tcPropertyValue: the property value to be on the Teamcenter object attribute.
    """
    attrExchange: AttrExchangeMapping = None
    tcPropertyValue: str = ''


@dataclass
class MappingObject(TcBaseObj):
    """
    This is the key structure holding the metadata exchange mapping information.  Only one of the three values can be
    set: nextLevelMappedObject, relationObject, or attributeName.  
    - If the next level mapping is linked by referenced Teamcenter object, then the nextLevelMappedObject is set.  
    - If the next level mapping is linked by Teamcenter relation, then the relationObject is set.  
    - If the current Teamcenter object is where the property is from, then the attributeName is set.
    
    
    
    :var objectType: the Teamcenter object type name.
    :var referencedName: the Teamcenter property on the upper level Teamcenter object by which the current Teamcenter
    object is being referenced (For example, an Item Revision relates to a Dataset with the References relation, the
    upper level object is the Item Revision, and the current object is the Dataset).  This value is set when Teamcenter
    property type is any other Teamcenter type.
    :var path: the indicator of how to find the next level.  If ReferencedObject is the value then use referencedObject
    from the MappingObject.  If Realtion is the value, then use relationObject, or if Leaf is the value then use
    attributeName.
    :var attributeName: the name of the Teamcenter property on the last level object for the exchange.
    :var nextLevelMappedObject: the MappingObject collection which contains mapping information for the next level. 
    This will be a vector of single object.  Using a collection since circular references are not supported.
    :var relationObject: the relationship information between the current Teamcenter object and the next level object.
    """
    objectType: str = ''
    referencedName: str = ''
    path: str = ''
    attributeName: str = ''
    nextLevelMappedObject: List[MappingObject] = ()
    relationObject: List[Relation] = ()


@dataclass
class Relation(TcBaseObj):
    """
    The information about relationship between two Teamcenter objects.
    
    :var relationName: the relationship name that exists between two Teamcenter objects.
    :var mappedObject: a next level object which contains mapping information.  This collection will only contain one
    object, using a collection since circular references are not supported.
    :var relationType: the information about what the relation is between two Teamcenter objects.  The values could be
    Primary or Secondary. If it is primary, the containing object is the primary object in the relation.  If it is
    secondary, the containing object is the secondary object in the relation.
    """
    relationName: str = ''
    mappedObject: List[MappingObject] = ()
    relationType: str = ''


@dataclass
class ResolveAndGetData(TcBaseObj):
    """
    The Teamcenter object property values based on the given metadata exchange mapping information.
    
    :var foreignObjectPropertyName: the property name of the client object which the Teamcenter object property would
    be exchanged with.
    :var tcAttrVal: the Teamcenter property value to be set on the client object property.
    :var isFailed: this value is true if the mapping resolve for this input object failed.
    :var errorStack: these are the errors return from the server for the particular mapping resolve or getting
    properties.
    """
    foreignObjectPropertyName: str = ''
    tcAttrVal: TcAttributeValue = None
    isFailed: bool = False
    errorStack: List[str] = ()


@dataclass
class ResolveAndGetResult(TcBaseObj):
    """
    The WorkspaceObject (the current implementation in the Microsoft Office client, this is the Dataset) object and its
    corresponding resolved attribute mapping outputs.
    
    :var dataset: the WorkspaceObject (the current implementation in the Microsoft Office client, this is the Dataset)
    object from which the resolving of the mapping begins.
    :var resolveAndGetDataList: the list of resolved attribute structures whether it succeeded or failed.
    """
    dataset: WorkspaceObject = None
    resolveAndGetDataList: List[ResolveAndGetData] = ()


@dataclass
class ResolveAndSetResult(TcBaseObj):
    """
    The Teamcenter object and the corresponding failed mapping information about which Teamcenter object property
    setting has failed.
    
    :var dataset: the WorkspaceObject (the current implementation in the Microsoft Office client, this is the Dataset) 
    object where the attribute mapping start from.
    :var failedObjInfos: the list of the failed mappping information.
    """
    dataset: WorkspaceObject = None
    failedObjInfos: List[FailedObjInfo] = ()


@dataclass
class ResolveAttrMappingsAndGetPropertiesInfo(TcBaseObj):
    """
    The input structure for ResolveAttrMappingsAndGetProperties service method.
    
    :var locale: the locale information for the dataset content.
    :var datsetObject: the WorkspaceObject (the current implementation in the Microsoft Office client, this is the
    Dataset) object from which the metadata exchange is initiated.
    :var attrExchange: the list of structures with the metadata exchange mapping information.
    """
    locale: str = ''
    datsetObject: WorkspaceObject = None
    attrExchange: List[AttrExchangeMapping] = ()


@dataclass
class ResolveAttrMappingsAndGetPropertiesResponse(TcBaseObj):
    """
    The return structure for resolving metadata exchange mappings and the Teamcenter object property values.
    
    :var resolveAndGetResults: the list of structures that have the Teamcenter object property values.
    :var serviceData: the list of errors.  The error would be associated with the property names of the client object
    property for the which the metadata exchange failed.
    """
    resolveAndGetResults: List[ResolveAndGetResult] = ()
    serviceData: ServiceData = None


@dataclass
class ResolveAttrMappingsAndSetPropertiesInfo(TcBaseObj):
    """
    The input structure for resolving metadata exchange mappings and to set the Teamcenter object property.
    
    :var locale: the locale information for the dataset content.
    :var datasetObject: the WorkspaceObject (normally is Dataset) object from which the metadata exchange is initiated.
    :var attrExchange: the list of structures with the metadata exchange mapping information.
    """
    locale: str = ''
    datasetObject: WorkspaceObject = None
    attrExchange: List[AttrExchangeMappingSetValue] = ()


@dataclass
class ResolveAttrMappingsAndSetPropertiesResponse(TcBaseObj):
    """
    The return structure for resolving metadata exchange mappings, and the Teamcenter object property values.
    
    :var serviceData: the list of partial errors returned for failed metadata exchange object.
    :var resolvedAndSetResults: the list of structures that have the client object property name that fails to set and
    the corresponding list of errors.
    """
    serviceData: ServiceData = None
    resolvedAndSetResults: List[ResolveAndSetResult] = ()


@dataclass
class TcAttributeValue(TcBaseObj):
    """
    The resolved attribute information.
    
    :var tcVal: the Teamcenter property value.  The actual value is converted to string before sending to the client.
    :var typeOfVal: the Teamcenter property type.  The type of the value can be of char, double, float, int, logical,
    short or string.  The client and the server will need to do the conversion based on these types.
    """
    tcVal: str = ''
    typeOfVal: str = ''
