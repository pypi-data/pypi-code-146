from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDynamicIPALinesResponse(TcBaseObj):
    """
    This structure is returned as response for getDynamicIPALines operation -
    It returns - 
    1. Map of input bop lines and their corresponding DIPA nodes.
    2. Partial errors as part of the serviceData. These errors will be those encountered during various aspects of
    traversal of process structure. 
    
    :var bopLineToIPALines: A map (BOMLine, list of BOMLline) where the key represents BOMLine of type Mfg0BvrProcess
    and value is list of BOMLine of type Mfg0BvrDynamicIPA. What constitutes a dynamic IPA node is defined by the
    preference 'MEDynamicIPAOccurrenceTypes', or lines below consumed lines as traversed by the closure rule specified
    by the preference 'MEDynamicIPALinesTraversalRule'.
    :var serviceData: The ServiceData.
    """
    bopLineToIPALines: BopLineToIPALinesMap = None
    serviceData: ServiceData = None


@dataclass
class CleanDynamicIPALinesInfo(TcBaseObj):
    """
    Structure containing information for cleaning the dynamic IPA lines.
    
    :var inputBOPLines: List of business objects representing BOP lines
    :var cleanSubHierarchy: Flag indicating whether to consider processes in sub-hierachy to clean the dynamic IPA
    liines
    """
    inputBOPLines: List[BusinessObject] = ()
    cleanSubHierarchy: bool = False


"""
A map (BOMLine, list of BOMLline) where the key represents BOMLine of type Mfg0BvrProcess and value is list of BOMLine of type Mfg0BvrDynamicIPA. What constitutes a dynamic IPA node is defined by the preference 'MEDynamicIPAOccurrenceTypes', or lines below consumed lines as traversed by the closure rule specified by the preference 'MEDynamicIPALinesTraversalRule'.
"""
BopLineToIPALinesMap = Dict[BusinessObject, List[BusinessObject]]
