from __future__ import annotations

from tcsoa.gen.BusinessObjects import Dataset
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportObjectsToOfflinePackageResponse(TcBaseObj):
    """
    ExportObjectsToOfflinePackageResponse structure defines the response from ExportObjectsToOfflinePackage operation.
    It contains briefcase file FMS ticket, export log file FMS ticekts, briefcase dataset, and partial errors.
    
    :var briefcaseFileFMSTicket: FMS ticket of the briefcase file, which can be used to download the briefcase file
    from server to client.
    :var exportLogFileFMSTickets: FMS ticket of the briefcase file, which can be used to download the briefcase file
    from server to client.
    :var briefcaseDataSet: A Dataset which includes the out briefcase file in its namedReference.
    After export, a new Dataset will be created. The exported briefcase file will be added to the new Dataset. And a
    new mail which contains the Dataset will be added to mailbox folder of the user.  The mail will also be send to
    mail box of the user if the user has set the Email Address.
    
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors listed
    above in case of failure conditions.
    """
    briefcaseFileFMSTicket: str = ''
    exportLogFileFMSTickets: List[str] = ()
    briefcaseDataSet: Dataset = None
    serviceData: ServiceData = None


@dataclass
class ImportObjectsFromOfflinePackageResponse(TcBaseObj):
    """
    ImportObjectsFromOfflinePackageResponse structure defines the response from ImportObjectsFromOfflinePackageResponse
    operation. It contains FMS ticket of the log file, error file, and partial errors and objects that are imported.
    
    :var logFileFMSTicket: FMS ticket of the import log file, which can be used to download the import log file from
    server to client.
    :var errorFileFMSTicket: FMS ticket of the import error file, which can be used to download the import error file
    from server to client.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors listed
    above in case of failure conditions.
    """
    logFileFMSTicket: str = ''
    errorFileFMSTicket: str = ''
    serviceData: ServiceData = None
