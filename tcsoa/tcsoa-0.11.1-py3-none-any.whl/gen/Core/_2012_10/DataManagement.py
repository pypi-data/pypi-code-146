from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, PSBOMView, WorkspaceObject
from tcsoa.gen.Core._2007_06.DataManagement import DatasetTypeInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDatasetTypesWithFileExtensionOutput(TcBaseObj):
    """
    This struct contains pair of file extension and the list of DatasetTypeInfo structures.
    
    :var fileExtension: The fileExtension for each dataset type specified in fileExtensions input
    :var datasetTypesInfo: The matching list of named reference information
    """
    fileExtension: str = ''
    datasetTypesInfo: List[DatasetTypeInfo] = ()


@dataclass
class GetDatasetTypesWithFileExtensionResponse(TcBaseObj):
    """
    This struct contains the list dataset type and reference information and Service Data.
    
    :var output: List of named reference information for each dataset type specified in fileExtensions input
    :var serviceData: The DatasetType objects that corresponds to fileExtensions input
    """
    output: List[GetDatasetTypesWithFileExtensionOutput] = ()
    serviceData: ServiceData = None


@dataclass
class TraceReport1(TcBaseObj):
    """
    This structure holds information about generated trace reports with defining and complying trace trees with
    selected objects, and its persistent objects.
    
    :var defRootNode: Represents the root node of Defining Tree in the Trace Report.
    :var compRootNode: Represents the root node of Complying Tree in the Trace Report.
    :var selectedObject: Represents selected object for which Trace Report generated.
    :var persistentObjects: Represents persistent object for the selected object for which Trace Report generated.
    """
    defRootNode: TraceReportTreeNode = None
    compRootNode: TraceReportTreeNode = None
    selectedObject: BusinessObject = None
    persistentObjects: List[BusinessObject] = ()


@dataclass
class TraceReportTreeNode(TcBaseObj):
    """
    This structure holds information of each trace link report line with information of parent object, and its children
    associated with trace link relation
    
    :var object: This object represents any BusinessObject in Teamcenter on which Trace Link is created.
    :var displayObj: If the Trace Link is created on the occurrence then this variable will represent the object to
    show in the Trace Report.
    :var srcContextName: This parameter will hold the name of context for source object of Trace Link.
    :var tarContextName: This parameter will hold the name of context for target object of Trace Link.
    :var bomView: This field represents the BOMView of context line for the TraceLink.
    :var isDirectLink: This flag tells if current object is direct trace link object or not.
    :var isTraceLinkObj: This flag tells if current object is trace link object or not.
    :var childNodes: This represents child nodes with trace link relation with current object.
    """
    object: BusinessObject = None
    displayObj: WorkspaceObject = None
    srcContextName: str = ''
    tarContextName: str = ''
    bomView: PSBOMView = None
    isDirectLink: bool = False
    isTraceLinkObj: bool = False
    childNodes: List[TraceReportTreeNode] = ()


@dataclass
class TraceabilityFilterInput(TcBaseObj):
    """
    TraceabilityFilterInput structure has parameters for property filtering for trace report building. This includes
    name of property on which filter will get applied, operator type, and the value of comparison.
    
    :var logicalOperatorType: Type of the operator applied to concatenate this property clause with previous property
    clause. Below are valid values
    0 - LOGICAL_AND  
    1 - LOGICAL_OR
    :var propertyName: Name of the property to be filtered.
    :var operatorType: Type of operator to be applied to compare the value of property, below are valid values 
                            0 = OP_EQUALS
                            1 = OP_NOT_EQUALS
                             2 = OP_LESS_THAN
                            3 = OP_LESS_OR_EQUAL
                            4 = OP_GREATER_THAN
                            5 = OP_GREATER_OR_EQUAL
    
    :var propertyValue: Value of property expected.
    """
    logicalOperatorType: int = 0
    propertyName: str = ''
    operatorType: int = 0
    propertyValue: str = ''


@dataclass
class TraceabilityInfoInput1(TcBaseObj):
    """
    Information required to generate a trace report.  Type of trace report, if indirect trace link included, and list
    of FND_TraceLink relation type name and object type names to be included in trace report.  Also, it includes all
    the details of apply property filtering and name of property by which trace report needs to updated. Also it has
    details about whether to export trace report to RAC to show or to export to MSExcel application.
    
    :var selectedObjs: List of objects on which to generate the Trace Report.
    :var reportType: Type of Report that is defining(0), complying(1), or both(2).
    :var exportTo: Format name to export trace report. It will be either "TraceReportRACExport" - for exporting
    Traceability report to RAC, or " TraceReportMSExcelExport" - for exporting Traceability report to MSExcel
    application. 
    
    :var exportTemplate: Name of export template to be used to export the trace report.
    :var exportColumnNames: This is list of real property names to be exported to Excel.
    :var reportDepth: Level to which Trace Report should be generated. Its value should be greater than 0.
    :var isIndirectTraceReportNeeded: If true then only Indirect Trace Report will be included in the final Trace
    Report.
    :var filteredTraceLinkTypes: This is the list of FND_TraceLink type, for which type only the Trace Report needs to
    be constructed excluding other types. 
    :var filteredObjectTypes: The list of object type, for which type only the Trace Report needs to be constructed
    excluding other types.
    :var scopeLines: The list of all the scope BOM lines from BOM Window under which the searched object (which is
    going to be added in trace report ) BOM lines needs to be searched.
    :var propertyFilterInput: The list of property filtering inputs. This property filter needs to be applied of the
    trace report going to send to client and only filter criteria report will be sent to the client.
    :var sortPropName: Name of the property name by which the Trace Report needs to be sorted.
    :var sortDirection: 1 to sort ascending order, 2 to sort descending order. 0 if no sort applied.
    """
    selectedObjs: List[BusinessObject] = ()
    reportType: int = 0
    exportTo: str = ''
    exportTemplate: str = ''
    exportColumnNames: List[str] = ()
    reportDepth: int = 0
    isIndirectTraceReportNeeded: bool = False
    filteredTraceLinkTypes: List[str] = ()
    filteredObjectTypes: List[str] = ()
    scopeLines: List[BusinessObject] = ()
    propertyFilterInput: List[TraceabilityFilterInput] = ()
    sortPropName: str = ''
    sortDirection: int = 0


@dataclass
class TraceabilityReportOutput1(TcBaseObj):
    """
    This structure holds information of either of following, including service data:
    1. Generated trace reports with defining and/or complying trace trees with selected objects, and its persistent
    objects
    2. Information about the file ticket for exported file generated at the server.
    
    :var traceReports: This member holds all the Trace Reports user has asked for. This is vector of TraceReport1 type
    of structures.
    :var transientFileReadTickets: The transient file read tickets for the exported file.
    :var serviceData: Service Data.
    """
    traceReports: List[TraceReport1] = ()
    transientFileReadTickets: List[str] = ()
    serviceData: ServiceData = None
