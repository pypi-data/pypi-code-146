from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AttributeDetailElement(TcBaseObj):
    """
    Comparison result of an attribute in an Attribute Group.
    
    :var attributeNames: Corresponding attribute names for each member 	of the equivalentObjects vector. The size of
    this vector matches the size of equivalentObjects vector and it has corresponding indices.       
    :var isDifferent: False if the property value is equal in the source and target, otherwise true.
    """
    attributeNames: List[str] = ()
    isDifferent: bool = False


@dataclass
class AttributeGroupAndFormComparisonResponse(TcBaseObj):
    """
    For each supplied attribute group the operation returns the list of its attributes, the attributes' values for each
    supplied source and target, and the result of comparing each attribute on all supplied sources and targets.
    
    :var serviceData: Contains the property values for each property in each attribute group for each supplied
    equivalent set and any partial errors.
    :var attributeGroupAndFormDetails: List of attribute groups information elements - one for each input equivalent
    set.
    """
    serviceData: ServiceData = None
    attributeGroupAndFormDetails: List[AttributeGroupAndFormDetail] = ()


@dataclass
class AttributeGroupAndFormDetail(TcBaseObj):
    """
    Attribute groups details of an equivalent set of objects. 
    
    :var index: Index of equivalent set in the input vector for which these details were calculated.
    :var equivalentObjects: The list of all equivalent business objects in the input equivalent set (all equivalent
    sources in sequence and then all targets in sequence).
    :var attributeGroupDetailElements: Attribute groups details of this equivalent set. Each element in the list
    represents one attribute group.
    """
    index: int = 0
    equivalentObjects: List[BusinessObject] = ()
    attributeGroupDetailElements: List[AttributeGroupsDetailElement] = ()


@dataclass
class AttributeGroupsDetailElement(TcBaseObj):
    """
    Comparison results of an Attribute Group.
    
    :var attributeGroupName: The name of this attribute group.
    :var isDifferent: True if any of the properties in this attribute group are different, otherwise false.
    :var attrGroupsAndForms: Corresponding attribute groups and forms objects for each member of the equivalentObjects
    vector. 		The size of this vector matches the size of equivalentObjects vector and it has corresponding indices.
    :var attributeDetails: The list of details for each mapped property in the attribute group.
    """
    attributeGroupName: str = ''
    isDifferent: bool = False
    attrGroupsAndForms: List[BusinessObject] = ()
    attributeDetails: List[AttributeDetailElement] = ()


@dataclass
class BusinessObjectVec(TcBaseObj):
    """
    Vector of business objects.
    
    :var businessObjects: Vector of business objects.
    """
    businessObjects: List[BusinessObject] = ()


@dataclass
class ConnectedObjectsComparisonResponse(TcBaseObj):
    """
    For each input set of equivalent objects a vector of comparison results of their connected elements (can be full
    match, partial match, or multiple match) and for each object in the set a detailed connected elements breakdown.
    
    :var serviceData: Object that captures any partial errors.
    :var connectedObjectsDetails: List of connected objects information elements - one for each input equivalent set.
    """
    serviceData: ServiceData = None
    connectedObjectsDetails: List[ConnectedObjectsDetail] = ()


@dataclass
class ConnectedObjectsDetail(TcBaseObj):
    """
    Comparison results of connected elements of an equivalent set of objects (can be full match, partial match, or
    multiple match) and for each object in the set a detailed connected elements breakdown. 
    
    :var index: The index of equivalent set in the input list for which these details were calculated.
    :var matchResults: A list of the comparison results (0 means full match, 1 means partial match, 2 means multiple
    match) of all rows of the output table. Each vector element is the result of comparing one equivalent group of
    connected objects (one row in the table).
    :var connectedObjectsDetails: A list of input equivalent object and its detailed set of connected elements. This
    vector contains the whole ouput results table, where each vector element represents a column in the table.
    """
    index: int = 0
    matchResults: List[int] = ()
    connectedObjectsDetails: List[ConnectedObjectsDetailElement] = ()


@dataclass
class ConnectedObjectsDetailElement(TcBaseObj):
    """
    Contains connected objects of the equivalentObject.
    
    :var equivalentObject: The input equivalent object for which these details are defined.
    :var connectedObjects: The set of connected objects for this input object. The outer vector is 	insync with the
    index of the matchResults, each element representing one cell in the output table, and the inner vector will be the
    group of connected elements that are equivalent to each other (if there are no equivalent elements in this group at
    all the inner vector will be empty). Each inner list will have only one element, and all equivalent elements will
    be put in separate inner list.
    """
    equivalentObject: BusinessObject = None
    connectedObjects: List[BusinessObjectVec] = ()
