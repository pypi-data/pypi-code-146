from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from datetime import datetime


@dataclass
class GetAITypesResponse(TcBaseObj):
    """
    GetAITypesResponse structure contains an additionalInfo element, and serviceData to return partial errors. The
    AdditionalInfo type member currently supports the following:
    
    AdditionalInfo.strMap:
    Key:AITypeNames
    Value: list of AppInterfaceType object names.
    
    AdditionalInfo.objMap:
    Key:Specific AITypeName from the Value above
    Value:AppInterfaceType object object at index 0, Tool optionally at index 1.
    
    For each name in AdditionalInfo.strMap, there is an entry in the AdditionalInfo.objMap. The value being the
    AppInterfaceType object. In case, there is a tool associated with the specific AppInterfaceType object, it will be
    the second index in the list of values.
    
    :var additionalInfo: A generic structure of keys and vectors of values (integer,double,object,string,date types)
    for passing additional metadata. Currently, the following name/value pairs are supported:
    
    strMap entries:
    Key:AITypeNames
    Value: list of AppInterfaceType object names.
    
    For each name in list above, there is an entry in the objMap. The value being the AppInterfaceType object. In case,
    there is a tool associated with the specific AppInterfaceType object, that will be present as the second element in
    this value.
    :var serviceData: Service data capturing partial errors.
    """
    additionalInfo: AdditionalInfo = None
    serviceData: ServiceData = None


@dataclass
class AdditionalInfo(TcBaseObj):
    """
    a generic structure to capture additional information.
    
    :var intMap: A map (string/list of integers) of generic key to integer values.
    :var dblMap: A map (string/list of doubles) of generic key to double values.
    :var strMap: A map (string/list of strings) of generic key to string values.
    :var objMap: A map (string/list of BusinessObjects) of generic key to  BusinessObject values.
    :var dateMap: A map (string/list of dates) of generic key to date values.
    """
    intMap: StringToIntVectorMap = None
    dblMap: StringToDblVectorMap = None
    strMap: StringToStrVectorMap = None
    objMap: StringToObjVectorMap = None
    dateMap: StringToDateVectorMap = None


"""
a map of string to vector of dates
"""
StringToDateVectorMap = Dict[str, List[datetime]]


"""
String to vector of doubles map.
"""
StringToDblVectorMap = Dict[str, List[float]]


"""
map of string to vector of integers.
"""
StringToIntVectorMap = Dict[str, List[int]]


"""
a map of string to vector of objects.
"""
StringToObjVectorMap = Dict[str, List[BusinessObject]]


"""
A map of string to vector of strings.
"""
StringToStrVectorMap = Dict[str, List[str]]
