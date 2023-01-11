from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FetchOdsResponse(TcBaseObj):
    """
    The return structure for the fetchOdsRecords operation.
    
    :var serviceData: The ServiceData. Returns partial failure information.
    :var results: The results structure for the fetchOdsRecords operation.
    """
    serviceData: ServiceData = None
    results: FetchOdsResults = None


@dataclass
class FetchOdsResults(TcBaseObj):
    """
    Stores the returned data from this operation.
    
    :var systemLogFiles: A list of the names of the remote system log files used to assist in troubleshooting.
    :var fmsTickets: A list of FMS read tickets to the TCXML output files.
    :var failedObjects: A list of failed Business Objects UIDs.
    :var odsSessionOutput: Data returned from the current ODS session.
    """
    systemLogFiles: List[str] = ()
    fmsTickets: List[str] = ()
    failedObjects: List[str] = ()
    odsSessionOutput: StringVectorMap = None


"""
Map of string array property names to values (string, vector).
"""
StringVectorMap = Dict[str, List[str]]
