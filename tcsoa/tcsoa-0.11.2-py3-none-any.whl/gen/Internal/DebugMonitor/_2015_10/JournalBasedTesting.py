from __future__ import annotations

from tcsoa.gen.Internal.DebugMonitor._2014_06.JournalBasedTesting import AuxiliaryInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class TerminateJBTResponse(TcBaseObj):
    """
    Contains the service data and any additional information such as the mark point rollback status.
    
    :var additionalInfo: The additional information about a test run. Currently it returns the mark point rollback
    status in the strToStrVectorMap: key is "rollback" and value is "passed" or "failed".
    :var serviceData: The service data containing partial errors.
    """
    additionalInfo: AuxiliaryInfo = None
    serviceData: ServiceData = None
