from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2013_05.IPAManagement import FileTicketDetails
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SaveDynamicIPALinesResponse(TcBaseObj):
    """
    FMS file ticket of the log file for input dynamicIPA lines. The following partial errors may be returned:
    - 253126 : The target object cannot be modified, because the user does not have write access.
    
    
    
    :var serviceData: Partial errors as part of the serviceData. These errors will be those encountered during various
    aspects of traversal of process structure.
    :var logFile: The details of the log file ticket.
    """
    serviceData: ServiceData = None
    logFile: FileTicketDetails = None


@dataclass
class CleanDynamicIPALinesResponse(TcBaseObj):
    """
    A FMS file ticket for the log file for the process and the following partial errors may be returned:
    
    253130 : The Clean Dynamic Assembly Tree operation has failed. Please check the Teamcenter server syslog file for
    more information.
    253134 : The Clean Dynamic Assembly Tree operation has failed, because there are no Dynamic Assembly Tree nodes
    related to the current configuring structure.
    253131 : The Create/Update Dynamic Assembly Tree operation has failed. Please check the Teamcenter server syslog
    file for more information.
    200411    - The dynamic In Process Assembly tree cannot be found.
    
    :var serviceData: Partial errors as part of the serviceData.
    :var logFileTicket: The details of the log file ticket.
    """
    serviceData: ServiceData = None
    logFileTicket: FileTicketDetails = None


@dataclass
class DynamicIPAInputInfo(TcBaseObj):
    """
    BOP line along with its recursive flag information.
    
    :var inputLine: Business objects representing BOP line.
    :var isRecursive: Flag to consider processes in sub-hierarchy to clean the dynamic IPA lines.
    
    true - Cleans the dyanmic IPA lines for all the processes in the sub-hierarchy of the input BOPLines.
    false- Cleans the Dynamic IPA lines for the input BOPLines only.
    """
    inputLine: BusinessObject = None
    isRecursive: bool = False


@dataclass
class DynamicIPALinesResponse(TcBaseObj):
    """
    A map of input BOPLines and their corresonding  DIPA(Mfg0BvrDynamicIPA) nodes and a FMS file ticket for the log
    file for the process. The following partial errors may be returned:
    
    253131 : The Create/Update Dynamic Assembly Tree operation has failed. Please check the Teamcenter server syslog
    file for more information.
    253132 : The Create/Update Dynamic Assembly Tree operation has failed, because there are more than one configuring
    structures. Please check the Teamcenter server syslog file for more information.
    253133 : The Create/Update Dynamic Assembly Tree operation has failed, because the selected process(es) do not have
    predecessors.
    
    :var bopLineToIPALinesMap: A map (BOMLine, list of BOMLline) where the key represents BOPLine of type
    Mfg0BvrProcess and value is list of BOPLine of type Mfg0BvrDynamicIPA.
    :var serviceData: Partial errors as part of the serviceData.
    :var logFileTicket: The details of the log file ticket.
    """
    bopLineToIPALinesMap: BopLineToDynamicIPALinesMap = None
    serviceData: ServiceData = None
    logFileTicket: FileTicketDetails = None


"""
A map (BOMLine, list of BOMLline) where the key represents BOPLine of type Mfg0BvrProcess and value is list of BOPLine of type Mfg0BvrDynamicIPA.
"""
BopLineToDynamicIPALinesMap = Dict[BusinessObject, List[BusinessObject]]
