from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportDataModelResponse(TcBaseObj):
    """
    Holds the response data of the 'exportDataModel' operation.
    
    :var modelXmlFileTicket: The file ticket for the output xml containing the data model extracted.
    :var logFileTicket: The file ticket for the extractor log file.
    :var serviceData: This contains the status of the operation. Possible error codes are , 
    - 216007: Extraction of data model failed
    
    """
    modelXmlFileTicket: str = ''
    logFileTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class ImportDataModelResponse(TcBaseObj):
    """
    The ImportDataModelResponse structure holds the output data from running the deployDataModel operation (which
    replaced the deprecated importDataModel operation).
    
    :var logFileTickets: The file ticket corresponding to output log/logs from the deployDataModel operation.
    :var serviceData: This contains the status of the operation.
    """
    logFileTickets: List[str] = ()
    serviceData: ServiceData = None
