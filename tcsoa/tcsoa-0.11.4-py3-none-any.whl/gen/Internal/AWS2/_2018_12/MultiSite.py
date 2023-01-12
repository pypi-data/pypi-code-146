from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FetchODSResponse(TcBaseObj):
    """
    The return structure for the fetchODSRecords operation.
    
    :var odsResults: The results structure for the fetchODSRecords operation.
    :var serviceData: The ServiceData returns partial failure information.
    """
    odsResults: FetchODSResults = None
    serviceData: ServiceData = None


@dataclass
class FetchODSResults(TcBaseObj):
    """
    Stores the returned data from fetchODSRecords operation.
    
    :var fmsTickets: A list of FMS read tickets for the TC XML output files.
    :var systemLogFiles: A list of the names of the remote system log files used to assist in troubleshooting.
    :var failedObjects: A list of failed Business Objects UIDs.
    :var odsSessionOutput: A map (string, list of strings) of data returned from the current ODS session.
    """
    fmsTickets: List[str] = ()
    systemLogFiles: List[str] = ()
    failedObjects: List[str] = ()
    odsSessionOutput: StringVectorMap = None


"""
The string key to a vector of string values map.
"""
StringVectorMap = Dict[str, List[str]]
