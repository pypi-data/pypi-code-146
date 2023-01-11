from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindAndRepopulateDynamicIPAsResponse(TcBaseObj):
    """
    The response of findAndRepopulateDynamicIPAs operation.
    
    It includes:
    
    1. The response includes data about the dynamic IPAs of all the given bop line objects. For each dynamic IPA, the
    response includes its content (i.e. parts underneath). There can be several dynamic IPAs for every process.
    This data is returned for every given bop line, no matter whether its dynamic IPAs were originally empty or not.
    
    2. The following partial errors are returned as part of the serviceData in case invalid parameters are passed to
    the operation:-
    
        25439 :- The type of the given object is not supported
        25440 :- The given object doesn&apos;t have any dynamic IPA.
    
    :var dynamicIPAsData: A list of DynamicIPAsOfLine. Each element in the list contains data about all the dynamic
    IPAs of a single line.
    :var serviceData: The service data.
    
    The following partial errors are returned in case invalid parameters are passed to the operation:-
    
    25439 :- The type of the given object is not supported.
    
    25440 :- The given object doesn&apos;t have any dynamic IPA.
    """
    dynamicIPAsData: List[DynamicIPAsOfLine] = ()
    serviceData: ServiceData = None


@dataclass
class RepopulateDynamicIPAsData(TcBaseObj):
    """
    Input structure for the input for repopulateDynamicIPAs service.
    
    :var topLine: The top BOPLine of the window.
    :var ids: A list of absolute occurrence IDs of processes (Mfg0BvrProcess) or studies (Mfg0BvrShdStudy) in context
    of topLine.
    """
    topLine: BusinessObject = None
    ids: List[str] = ()


@dataclass
class RepopulateDynamicIPAsResponse(TcBaseObj):
    """
    Response structure for repopulateDynamicIPAs service.
    
    :var dynamicIPAsData: List of data containing information about process lines (Mfg0BvrProcess) and their respective
    Dynamic IPA nodes (Mfg0BvrDynamicIPA).
    :var serviceData: Standard service data.
    """
    dynamicIPAsData: List[DynamicIPAsProcLineInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ConsumedPartsInfo(TcBaseObj):
    """
    Structure containing information related to consumed parts.
    
    :var consumedPart: A BOPLine of type Mfg0BvrPart present in the process structure.
    :var referencedPart: A BOMLine of type Mfg0BvrPart present in the product window related to consumedPart.
    :var occInformation: A map ( string, string ) of property information related to the occurrence of consumedPart.
    """
    consumedPart: BusinessObject = None
    referencedPart: BusinessObject = None
    occInformation: OccInformation = None


@dataclass
class DynamicIPAData(TcBaseObj):
    """
    A structure that contains data about a single dynamic IPA.
    
    :var dynamicIPA: A business object from type Mfg0BvrDynamicIPA.
    :var consumedParts: A list of of BOMLine of type Mfg0BvrPart. The parts are the content (the direct children) of
    the dynamic IPA.
    """
    dynamicIPA: BusinessObject = None
    consumedParts: List[BusinessObject] = ()


@dataclass
class DynamicIPAInfo(TcBaseObj):
    """
    Structure containing information related to dynamic IPA node.
    
    :var dynamicIPA: Dynamic IPA node (Mfg0BvrDynamicIPA).
    :var consumedParts: A list of child parts of dynamic IPA node and its related information.
    :var occInformation: A map ( string, string ) of property information related to the of dynamic IPA node.
    """
    dynamicIPA: BusinessObject = None
    consumedParts: List[ConsumedPartsInfo] = ()
    occInformation: OccInformation = None


@dataclass
class DynamicIPAsOfLine(TcBaseObj):
    """
    This structure contains data about all the dynamic IPAs of a single bop line object.
    
    :var bopLine: A business object from type Mfg0BvrProcess or Mfg0BvrShdStudy.
    :var dynamicIPAsData: A list of DynamicIPAData structures. Each element contains data about a single dynamic IPA.
    """
    bopLine: BusinessObject = None
    dynamicIPAsData: List[DynamicIPAData] = ()


@dataclass
class DynamicIPAsProcLineInfo(TcBaseObj):
    """
    This structure contains data about all the dynamic IPAs of a single bop line object.
    
    :var bopLine: A business object of type Mfg0BvrProcess or Mfg0BvrShdStudy.
    :var dynamicIPAsInfo: A list of Dynamic IPA nodes (Mfg0BvrDynamicIPA) and its related information.
    """
    bopLine: BusinessObject = None
    dynamicIPAsInfo: List[DynamicIPAInfo] = ()


"""
A map ( string ,string ) of property information related to current occurrence.    
"""
OccInformation = Dict[str, str]
