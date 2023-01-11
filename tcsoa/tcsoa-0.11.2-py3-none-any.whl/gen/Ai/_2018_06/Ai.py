from __future__ import annotations

from tcsoa.gen.Ai._2006_03.Ai import ApplicationRef
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Ai._2008_06.Ai import Configuration
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetObjectsByApplicationRefsRespElem(TcBaseObj):
    """
    The objects found for the input ApplicationRefs.
    
    :var objects: A list of BusinessObject representing persistent or runtime business objects associated with the
    input ApplicationRef objects.
    :var createdWindows: A list of BOMWindow objects the client should close.
    :var additionalInfo: Reserved for future use.
    """
    objects: List[BusinessObject] = ()
    createdWindows: List[BusinessObject] = ()
    additionalInfo: AdditionalInfo2 = None


@dataclass
class GetObjectsByApplicationRefsResponse(TcBaseObj):
    """
    The objects found for the input ApplicationRefs.
    
    :var responseElements: A list of GetObjectsForApplicationRefsElement objects specifying the business objects
    associated with the input list of ConfigurationInformation objects.
    :var additionalInfo: Reserved for future use.
    :var serviceData: Partial errors
    """
    responseElements: List[GetObjectsByApplicationRefsRespElem] = ()
    additionalInfo: AdditionalInfo2 = None
    serviceData: ServiceData = None


@dataclass
class ConfigurationInfo(TcBaseObj):
    """
    Configuration and Application Ref info used to find associated BOM Lines.
    
    :var configInfo: Configuration information including BOMWindow or configuringObject.
    :var appRefs: List of ApplicationRef objects for which associated business objects are found. Using the PLMXML
    format.
    :var additionalInfo: A generic structure to be used for additional information.
    """
    configInfo: Configuration = None
    appRefs: List[ApplicationRef] = ()
    additionalInfo: AdditionalInfo2 = None


@dataclass
class AdditionalInfo2(TcBaseObj):
    """
    A generic structure to capture additional information.
    
    :var intMap: A map containing a set of (string/vector<int>) elements.
    :var dblMap: A map containing a set of (string/vector<double>) elements.
    :var strMap: A map containing a set of (string/vector<string>) elements.
    :var objMap: A map containing a set of (string/vector<businessObject>) elements.
    :var dateMap: A map containing a set of (string/vector<dateTime>) elements.
    """
    intMap: StringToIntVectorMap2 = None
    dblMap: StringToDblVectorMap2 = None
    strMap: StringToStrVectorMap2 = None
    objMap: StringToObjVectorMap2 = None
    dateMap: StringToDateVectorMap2 = None


"""
A map containing a set of (string/vector<DateTime>) elements.
"""
StringToDateVectorMap2 = Dict[str, List[datetime]]


"""
A map containing a set of (string/vector<double>) elements.
"""
StringToDblVectorMap2 = Dict[str, List[float]]


"""
A map containing a set of (string/vector<int>) elements.
"""
StringToIntVectorMap2 = Dict[str, List[int]]


"""
A map containing a set of (string/vector<BusinessObject>) elements.
"""
StringToObjVectorMap2 = Dict[str, List[BusinessObject]]


"""
A map containing a set of (string/vector<string>) elements.
"""
StringToStrVectorMap2 = Dict[str, List[str]]
