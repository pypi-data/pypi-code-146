from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ReportDefinition
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateReportsCriteria(TcBaseObj):
    """
    Criteria needed to retrieve report definitions
    or generate report definition ids. At least one
    of the optional parameters must be included.
    
    :var clientId: The client identifier for routing purposes.
    :var rdTag: The Report Definition ID.
    :var datasetCtxUID: The uid for the context Dataset UID.
    :var datasetCtxObj: The Dataset context id.
    :var relationName: The relation name to be used.
    :var datasetType: The Dataset type to be used.
    :var reportName: Designates the name of the report given the report definition is not supplied.
    :var stylesheetTag: The report style sheet ID (optional). If no report style is provided, then the report will be
    displayed in xml format to the end user.
    :var stylesheetName: The name of the stylesheet if known
    :var contextObjects: A list of ID's representing context object(s) (required for item reports).
    :var contextObjectUIDs: A list of UIDs representing context objects.
    :var datasetName: The name of containing Dataset (optional). If the dataset name is provided, then it will save the
    generated report as a Dataset in Teamcenter database, otherwise will not.
    :var criteriaNames: The names in a series of Name/Value pairs used to specify additional criteria (optional).
    :var criteriaValues: The values in a series of Name/Value pairs used to specify additional criteria (optional).
    """
    clientId: str = ''
    rdTag: ReportDefinition = None
    datasetCtxUID: str = ''
    datasetCtxObj: BusinessObject = None
    relationName: str = ''
    datasetType: str = ''
    reportName: str = ''
    stylesheetTag: BusinessObject = None
    stylesheetName: str = ''
    contextObjects: List[BusinessObject] = ()
    contextObjectUIDs: List[str] = ()
    datasetName: str = ''
    criteriaNames: List[str] = ()
    criteriaValues: List[str] = ()


@dataclass
class GenerateReportsResponse(TcBaseObj):
    """
    The Response object from generateReports operation.
    
    :var transientFileReadTickets: It is for future use, may be null.
    :var transientFileTicketInfos: A list of TransientFileTicketInfo object(s) for retrieving generated report file.
    The TransientFileTicketInfo object includes the file name, ticket information.
    :var serviceData: The ServiceData which includes the failure information.
    """
    transientFileReadTickets: List[str] = ()
    transientFileTicketInfos: List[TransientFileTicketInfo] = ()
    serviceData: ServiceData = None


@dataclass
class TransientFileInfo(TcBaseObj):
    """
    The information required for file upload.
    
    :var fileName: Absolute file path to transient volume
    :var isText: true if filetype is text
    """
    fileName: str = ''
    isText: bool = False


@dataclass
class TransientFileTicketInfo(TcBaseObj):
    """
    TransientFileInfo with a ticket.
    
    :var transientFileInfo: file information structure
    :var ticket: FMS file ticket
    """
    transientFileInfo: TransientFileInfo = None
    ticket: str = ''
