from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FullTextResponse(TcBaseObj):
    """
    Represents the output data after retrieving the FullText dataset versions.
    
    :var revToFullText: A map( BusinessObject, list of BusinessObject) of Requirement Revision and its FullText dataset.
    :var objectPropValues: A map(BusinessObject, PropertyValues) of property name and values to be displayed.
    :var serviceData: The Service Data
    """
    revToFullText: RevisionToFullTextObjects = None
    objectPropValues: ObjectPropertyValues = None
    serviceData: ServiceData = None


@dataclass
class PropertyValues2(TcBaseObj):
    """
    A map of property name (key) and property values (values) in string format.
    
    :var propName: The property name.
    :var propValues: list of property values.
    """
    propName: str = ''
    propValues: List[str] = ()


@dataclass
class RequirementInput(TcBaseObj):
    """
    Represents the input data containing a list of input objects of type Requirement Revision or Arm0RequirementElement
    required to get the FullText dataset versions.
    
    :var operationType: The type of operation to perform. 
    If the value is 'DERIVED' then the properties of the FullText dataset for the derived Requirement specification
    will be retrieved. If no value is provided then all the properties of the FullText dataset for the Requirement
    specification along with body_text property will be retrieved.
    :var baseURL: This is address of the FMS servers that client machine uses.
    :var selectedObjects: The list of input objects of type Requirement Revision or Arm0RequirementElement to query its
    FullText dataset versions and its contents.
    """
    operationType: str = ''
    baseURL: str = ''
    selectedObjects: List[BusinessObject] = ()


"""
A list of property name and values to be displayed on the FullText dataset.
"""
ObjectPropertyValues = Dict[BusinessObject, List[PropertyValues2]]


"""
A map of Requirement Revision and its FullText dataset.
"""
RevisionToFullTextObjects = Dict[BusinessObject, List[BusinessObject]]
