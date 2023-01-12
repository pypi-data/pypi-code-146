from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SelectedStudySourceResponse(TcBaseObj):
    """
    Returns the FMS file ticket to the log and service data with partial errors if any.
    Following partial errors may be returned.
    251087    The selected objects are not supported by "Synchronize" operation.
    251088    The mode "abc" is not a valid synchronization mode.
    
    :var serviceData: The service data containing partial errors if any.
    :var logFileTicket: The FMS ticket to the log file.
    """
    serviceData: ServiceData = None
    logFileTicket: str = ''


@dataclass
class SelectedSyncPublishStudyInput(TcBaseObj):
    """
    A list of selected business objects from Simulation Study. The valid types are Mfg0BvrSimStudy, Mfg0BvrProcessArea,
    Mfg0BvrProcessLine, Mfg0BvrProcessStation Mfg0BvrProcess, and Mfg0BvrOperation.It also contains the study root node
    and the synchronization mode (Time based/ Event based).
    
    :var selectedLines: A list of selected objects in a simulation study.The valid types are: Mfg0BvrSimStudy,
    Mfg0BvrProcessArea, Mfg0BvrProcessLine, Mfg0BvrProcessStation, Mfg0BvrProcess, Mfg0BvrOperation and Mfg0BvrWorkarea.
    :var mode: The  mode to synchronize the study. The valid values are: "TimeBased", which performs a full
    synchronization and "EventBased", which performs a partial synchronization.
    """
    selectedLines: List[BusinessObject] = ()
    mode: str = ''
