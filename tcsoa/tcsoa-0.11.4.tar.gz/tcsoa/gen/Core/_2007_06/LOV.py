from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.BusinessObjects import ListOfValues
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AttachedLOVsResponse(TcBaseObj):
    """
    AttachedLOVsResponse
    
    :var inputTypeNameToLOVOutput: Map of input type name to LOVOutput
    :var serviceData: ServiceData which has output tags as plain objects and errors in partialError
    """
    inputTypeNameToLOVOutput: InputTypeNameToLOVOutputMap = None
    serviceData: ServiceData = None


@dataclass
class LOVInfo(TcBaseObj):
    """
    LOVInfo
    
    :var typeName: The name of the Teamcenter Engineering type to which property belongs
    :var propNames: List of Property names to which the LOV is attached
    """
    typeName: str = ''
    propNames: List[str] = ()


@dataclass
class LOVOutput(TcBaseObj):
    """
    LOVOutput
    
    :var propName: Input Property name to which the LOV is attached
    :var lov: The attached LOV tag found for the input type and property name
    """
    propName: str = ''
    lov: ListOfValues = None


"""
InputTypeNameToLOVOutputMap
"""
InputTypeNameToLOVOutputMap = Dict[str, List[LOVOutput]]
