from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class MfgImportFromBriefcaseResponse(TcBaseObj):
    """
    MfgImportFromBriefcaseResponse structure defines the response from importFromBriefcase operation. It contains FMS
    ticket of the log file, error file, and partial errors and objects that are imported.
    
    :var logFileFMSTicket: FMS ticket of the import log file, which can be used to download the import log file from
    server to client.
    :var errorFileFMSTicket: FMS ticket of the import error file, which can be used to download the import error file
    from server to client.
    :var serviceData: Service data containing the list of created or modified objects and also the partial errors in
    case of failure conditions.
    """
    logFileFMSTicket: str = ''
    errorFileFMSTicket: str = ''
    serviceData: ServiceData = None


"""
Map (string, string) containing names and values.
"""
NamesAndValues = Dict[str, str]
