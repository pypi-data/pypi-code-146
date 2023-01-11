from __future__ import annotations

from tcsoa.gen.Ai._2006_03.Ai import ApplicationRef
from enum import Enum
from typing import List
from tcsoa.gen.Ai._2008_06.Ai import ObjectsWithConfig
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetPropertyValuesData(TcBaseObj):
    """
    Used to input the list of objects with related configuration (used to setup bomwindows if needed on server), and
    the properties.
    
    :var objs: list of objects along with configuration.
    :var properties: list of  properties to be queried for on the object.
    """
    objs: List[ObjectsWithConfig] = ()
    properties: List[str] = ()


@dataclass
class GetPropertyValuesResponse(TcBaseObj):
    """
    capture the property values for the specified object and specified properties and any failures.
    
    :var objProps: the properties of the object
    :var failedSetIndices: array of failed indices. The index is the position in the input array. And the indices
    member is the list of failed objects (invalid tags) at each such index.
    """
    objProps: List[ObjPropDetail] = ()
    failedSetIndices: List[ErrorMap] = ()


@dataclass
class ObjPropDetail(TcBaseObj):
    """
    capture the object ApplicationRef and it's property details.
    
    :var obj: the ApplicationReference of the obj (uid/appname/version)
    :var properties: array or property details per
    :var failedPropIndices: index of the failed property for the object - the index maps to the input property array.
    :var failedPropMessages: the error string corresponding to the error id in failedPropIndices.
    """
    obj: ApplicationRef = None
    properties: List[PropertyDetails] = ()
    failedPropIndices: List[int] = ()
    failedPropMessages: List[str] = ()


@dataclass
class PropertyDetails(TcBaseObj):
    """
    details of a property
    
    :var name: display name of the property
    :var values: values in string form. Array - if the property has multiple values. These values can be decoded/parsed
    using the Property SOA client class if needed.
    :var maxStrLen: in case the property value is  a string - the maximum possible length.
    :var type: the type of the property as a string.
    integer = "int", short="short", float="float", double="double", char="char", logical="logical",note="note",
    string="string", date="date", any reference="reference"
    :var access: will be set to 0 if write access is allowed, 1 - for read.
    :var usage: if lov - the usage type of that lov.
    :var lovValues: the lovValues as strings.
    :var nullElement: for each value in an array - is the value Null.
    :var emptyElement: Used to indicate if each element in an array(each value) is empty.
    """
    name: str = ''
    values: List[str] = ()
    maxStrLen: int = 0
    type: str = ''
    access: int = 0
    usage: LOVUSAGE = None
    lovValues: List[str] = ()
    nullElement: List[int] = ()
    emptyElement: List[int] = ()


@dataclass
class ErrorMap(TcBaseObj):
    """
    capture the index of the input array, and the indices for the objects within that array.
    
    :var index: index of the input array with the list of objects and configurations.
    :var indices: Within the index specified by "index" the location of failed indices.
    """
    index: int = 0
    indices: List[int] = ()


class LOVUSAGE(Enum):
    """
    The different kinds of lov usage
    """
    AI_LV_Unknown = 'AI_LV_Unknown'
    AI_LV_Exhaustive_list = 'AI_LV_Exhaustive_list'
    AI_LV_Suggestions = 'AI_LV_Suggestions'
    AI_LV_Ranges = 'AI_LV_Ranges'
    AI_LV_Upper_bound = 'AI_LV_Upper_bound'
