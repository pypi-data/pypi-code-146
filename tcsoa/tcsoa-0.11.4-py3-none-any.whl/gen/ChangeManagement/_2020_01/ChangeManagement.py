from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DeepCopyData(TcBaseObj):
    """
    DeepCopyData stores the deep copy information that will be copied via derive operation. It also stores the nested
    deep copy data at the next level.
    
    :var attachedObject: The related object to be deep copied.
    :var deepCopyProperties: deepCopyProperties.
    :var operationInputType: Object type name of the operation being perfomed.
    :var childDeepCopyData: A list of DeepCopyData for the objects of the relation or reference property objects of the
    attached object.
    :var inputProperties:  Map to provide input property names and values of attached object. These property values
    will be applied on propagated objects. Map of property name(key) and property values(values) (string, list of
    strings) in string format of attached object, to be set on copied object of attached object. The calling client is
    responsible for converting the different property types (int, float, date .etc) to a string using the appropriate
    toXXXString functions in the SOA client framework Property class.
    """
    attachedObject: BusinessObject = None
    deepCopyProperties: PropertyValueMap = None
    operationInputType: str = ''
    childDeepCopyData: List[DeepCopyData] = ()
    inputProperties: PropertyValueMap = None


@dataclass
class DeriveInput(TcBaseObj):
    """
    Structure that contains multiple Change Items object to be derived, a structure containing property name and values
    to be propagated,  Deep Copy Data, a flag to automatically submit to workflow or not, a workflow template name and
    a flag to propagate relations or not.
    
    :var selectedObjects: A list of Problem Report or Change Request objects to be derived.
    :var derivePropertyData: A map of property name (as key) and property values (as value) in string format. Each
    value is a list of strings to support both single valued and multi valued properties of types. The calling client
    is responsible for converting the different property types (like integer, double, date, etc) to a string using the
    appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class.
    :var deepCopyDatas: A list of DeepCopyData to be propagated to the derived Change Item objects.
    :var submitToWorkflow: This is used to indicate whether the derived Change Item object will be automatically
    submitted to Workflow. If true will submit the derived object to designated workflow template, otherwise the
    derived object will not be submitted to workflow.
    :var workflowTemplateName: The workflow template name to be executed, if not informed, the default workflow
    template will be used.
    :var propagateRelation: If TRUE will propagate the relation defined in Deep Copy Rule, if FALSE will not propagate
    the relations.
    """
    selectedObjects: List[BusinessObject] = ()
    derivePropertyData: DerivePropertyValueInput = None
    deepCopyDatas: List[DeepCopyData] = ()
    submitToWorkflow: bool = False
    workflowTemplateName: str = ''
    propagateRelation: bool = False


@dataclass
class DerivePropertyValueInput(TcBaseObj):
    """
    This map is of property name (as key) and a vector of property values input, business object in string format,
    property name values map and compund derive input. The business object is a simple string. The property name values
    is a list of strings to support both single valued and multi valued properties of types. The calling client is
    responsible for converting the different property types (like integer, double, date, etc) to a string using the
    appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class.
    The compound derive input is another type of def of property value input data structure.
    
    :var boName: The buisness object name to which the properties belong.
    :var propertyNameValues: Map of property name values.
    :var compoundDeriveInput: Vector of derive property value input.
    """
    boName: str = ''
    propertyNameValues: PropertyValueMap = None
    compoundDeriveInput: DerivePropertyValueInputMap = None


"""
This map is of derive property value input with a string (as key) and a vector of derive property values input consisting of a business object in string format, a property name values map and compund input of derive property values.
"""
DerivePropertyValueInputMap = Dict[str, List[DerivePropertyValueInput]]


"""
This map is of property name (as key) and property values (as value) in string format. Each value is a list of strings to support both single valued and multi valued properties of types. The calling client is responsible for converting the different property types (like integer, double, date, etc) to a string using the appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class
"""
PropertyValueMap = Dict[str, List[str]]
