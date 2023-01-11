from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FileTicket(TcBaseObj):
    """
    Structure containing information related to file ticket.
    
    :var ticket: The FMS file ticket.
    :var fileName: The original file name.
    """
    ticket: str = ''
    fileName: str = ''


@dataclass
class ValidateScopeFlowsConsistencyResponse(TcBaseObj):
    """
    Response structure for validateScopeFlowsConsistency service.
    
    :var data: A list of ConsistencyData. Each element in the list contains indication whether the data is consistent
    and information about the in-cosistencies (cycles), if found.
    :var fileTicket: An FMS file ticket. The file contains report about the cycles found by the algorithm.
    :var serviceData: Service data.
    """
    data: List[ConsistencyData] = ()
    fileTicket: FileTicket = None
    serviceData: ServiceData = None


@dataclass
class ConsistencyData(TcBaseObj):
    """
    Structure containing information related to cycles.
    
    :var isConsistent: If true, no cycles are found under the given scope.
    :var cycles: The list of CycleData. Each element in the list contains data about a single cycle.
    """
    isConsistent: bool = False
    cycles: List[CycleData] = ()


@dataclass
class CycleData(TcBaseObj):
    """
    Structure containing information related to a specefic cycle identified.
    
    :var objects: The list of operations/processes that participate in a cycle that. The list contains business objects
    of type Mfg0BvrOperation and Mfg0BvrProcess.
    :var flows: The list of scope flows which participates in the cycle. These objects are of type Mfg0BvrScopeFlow.
    """
    objects: List[BusinessObject] = ()
    flows: List[BusinessObject] = ()
