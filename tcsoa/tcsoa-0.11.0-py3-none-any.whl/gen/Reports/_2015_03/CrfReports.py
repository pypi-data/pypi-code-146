from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ReportDefinition
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.Reports._2008_12.CrfReports import TransientFileTicketInfo
from dataclasses import dataclass


@dataclass
class GeneratePrintReportsOutput(TcBaseObj):
    """
    A structure that contains information about the generated print reports.
    
    :var clientID: The unmodified client id from the input PrintReportsCriteria structure to be used to identify the
    source input data.
    :var transientFileReadTickets: The transient file tickets. This is for future use.
    :var transientFileTicketInfos: The list of 'TransientFileTicketInfo' objects for retrieving generated report file.
    A 'TransientFileTicketInfo' object contains the file name, and the transient ticket information for the generated
    report file.
    """
    clientID: str = ''
    transientFileReadTickets: List[str] = ()
    transientFileTicketInfos: List[TransientFileTicketInfo] = ()


@dataclass
class GeneratePrintReportsResponse(TcBaseObj):
    """
    A structure that contains list of print report outputs, and error information, if any.
    
    :var outputs: The list of output structure elements.
    :var serviceData: Service data including partial errors that are mapped to the client id from the input.
    :var executedAsynchronously: True value indicates that the operation was executed asynchronously.
    """
    outputs: List[GeneratePrintReportsOutput] = ()
    serviceData: ServiceData = None
    executedAsynchronously: bool = False


@dataclass
class GenerateReportsCriteria2Async(TcBaseObj):
    """
    Data needed to generate a report.
    
    :var clientId: The client identifier for routing purposes.
    :var reportDefinition: The ReportDefinition object.
    :var datasetCtxObj: The context Dataset where generated report Dataset will be attached to.
    :var relationName: The relation name to be used to attach generated report Dataset to context Dataset.
    :var datasetType: The Dataset type to be used to store the report.
    :var reportOptionsNames: A list of option names in a series of Name/Value pairs used to specify additional criteria
    (optional).
    :var reportOptionsValues: A list of option values in a series of Name/Value pairs used to specify additional
    criteria (optional).
    :var reportName: The name of the report if reportDefinition is null.
    :var stylesheet: The report style sheet. The stylesheet is selectable from a list of already defined stylesheets on
    the ReportDefinition object. It is typically an XSL (saved in the DB as a Dataset )(optional).
    :var stylesheetName: The name of the report style if stylesheet is not supplied. If neither stylesheet nor
    stylesheetName is specified, a raw xml file is generated as report.
    :var contextObjects: A list of context object(s) (required for item reports).
    :var datasetName: The name of containing DataSet (optional).If supplied, the generated report will be saved as
    Dataset in Teamcenter,otherwise no dataset created for the report.
    :var criteriaNames: A list of strings containing the Names in a series of Name/Value pairs used to specify criteria
    for saved queries(optional).
    :var criteriaValues: A list of strings containing the Values in a series of Name/Value pairs used to specify
    criteria for saved queries(optional).
    :var datasetCtxUID: The uid for the context Dataset if datasetCtxObj is not supplied.
    """
    clientId: str = ''
    reportDefinition: ReportDefinition = None
    datasetCtxObj: BusinessObject = None
    relationName: str = ''
    datasetType: str = ''
    reportOptionsNames: List[str] = ()
    reportOptionsValues: List[str] = ()
    reportName: str = ''
    stylesheet: BusinessObject = None
    stylesheetName: str = ''
    contextObjects: List[BusinessObject] = ()
    datasetName: str = ''
    criteriaNames: List[str] = ()
    criteriaValues: List[str] = ()
    datasetCtxUID: str = ''


@dataclass
class GenerateReportsResponse2(TcBaseObj):
    """
    Contains file ticket of generated report and synchronize flag as well as service data.
    
    :var transientFileReadTickets: File ticket returned to client to download and the file stored in FMS via this file
    read ticket
    
    :var transientFileTicketInfos: A list of TransientFileTicketInfo object(s) for retrieving generated report file.
    The TransientFileTicketInfo object includes the file name, ticket information.
    :var serviceData: The service data.
    :var asyncFlagInfo: Asynchronous flag,if true  pop up notification on client will be displayed.
    """
    transientFileReadTickets: List[str] = ()
    transientFileTicketInfos: List[TransientFileTicketInfo] = ()
    serviceData: ServiceData = None
    asyncFlagInfo: bool = False


@dataclass
class PrintReportsCriteria(TcBaseObj):
    """
    This structure contains the input details for the generation of the print report.
    
    :var clientID: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var inputObject: The input object for which the print report is to be generated.
    :var isBatchPrint: True value indicates to also send the report to physical printer for printing.
    :var printInfos: The list of structures containing print configuration info. This info will be used only when the
    'isBatchPrint' is set to true.
    """
    clientID: str = ''
    inputObject: BusinessObject = None
    isBatchPrint: bool = False
    printInfos: List[PrintSubmitRequestInfo] = ()


@dataclass
class PrintReportsCriteriaAsync(TcBaseObj):
    """
    This structure contains the input details for the generation of the print report.
    
    :var clientID: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var inputObject: The input object for which the print report is to be generated.
    :var isBatchPrint: True value indicates to also send the generated report to physical printer for printing.
    :var printInfos: The list of structures containing print configuration info. This info will be used only when the
    'isBatchPrint' is set to true.
    """
    clientID: str = ''
    inputObject: BusinessObject = None
    isBatchPrint: bool = False
    printInfos: List[PrintSubmitRequestInfo] = ()


@dataclass
class PrintSubmitRequestInfo(TcBaseObj):
    """
    The structure containing the info needed to submit the print request.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var printObjs: A list of Teamcenter business objects (ItemRevision, Item, Dataset) that will be printed.
    :var collate: When two or more copies are printed, this specifies whether the printed pages are collated.
    :var printToScale: The scaling factor. Specifies the scaling factor from 0.000001 to 100.0, applied to an image
    when its printed.
    :var orientation: The paper orientation of "best fit", "portrait" or "landscape".
    :var bannerPage: Specifies whether to print a page including the defined stamps and listing additional data as
    specified by the VVCP setup(i.e. the Lifecycle Visualization print configuration) The following values can be
    specified: "Off", "Single", or "All Files".
    :var extraInfo: The placeholder for extra name value pair (string, string) information.
    :var printerConfigurationName: The PrintConfiguration object name.
    :var printerName: The printer name.
    :var colorMode: The print color mode. The possible values are "Color" or "Monochrome".
    :var userStamp: Text for a user stamp to be applied in addition to any existing system stamp configuration.
    :var paperSize: The print paper size. The sample values are "Legal", "Letter", "11x17" etc.
    :var printStamp: Where the print stamp is applied: "first page", "the banner page", or "all pages".
    :var pageRange: The range of pages to print. Empty value indicates to print all pages.
    :var numberCopies: The number of copies.
    """
    clientID: str = ''
    printObjs: List[BusinessObject] = ()
    collate: bool = False
    printToScale: str = ''
    orientation: str = ''
    bannerPage: str = ''
    extraInfo: AttributeMap = None
    printerConfigurationName: str = ''
    printerName: str = ''
    colorMode: str = ''
    userStamp: str = ''
    paperSize: str = ''
    printStamp: str = ''
    pageRange: str = ''
    numberCopies: str = ''


"""
A map of attribute name to value pairs.
"""
AttributeMap = Dict[str, str]
