from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ObjectInfoLegacy(TcBaseObj):
    """
    This structure holds object information of source or target object of trace link in Report structure.
    
    :var contextName: This parameter will hold the name of context for source or target object of
     trace link.
    :var displayObj: If the trace link is created on the occurrence then this variable will represent the object to
    show in the trace report.
    
    
    :var object: This object represent any Business Object in Teamcenter on which Trace Link is 
    created.
    
    :var bomView: This field represents the PSBOMView of context line for the trace link.
    :var contextLineObj: This field represents the context line for the trace link, this will be PSBOMViewRevision
    object.
    """
    contextName: str = ''
    displayObj: WorkspaceObject = None
    object: BusinessObject = None
    bomView: BusinessObject = None
    contextLineObj: BusinessObject = None


@dataclass
class ReportLegacy(TcBaseObj):
    """
    This structure holds information about each trace link report with information of parent object, and its children
    associated with trace link relation.
    
    :var parent: Parent object of trace link.
    :var children: List of all child objects for the parent with trace link relation.
    """
    parent: ObjectInfoLegacy = None
    children: List[ObjectInfoLegacy] = ()


@dataclass
class TraceReport2(TcBaseObj):
    """
    This structure holds information about generated trace reports with defining and complying trace trees with
    selected objects, and its persistent objects.
    
    :var defRootNode: The root node of defining tree in the trace report.
    :var compRootNode: The root node of complying tree in the trace report.
    :var selectedObject: The selected object for which trace report generated.
    :var persistentObjects: Persistent objects for the selected object for which Trace Report generated.
    """
    defRootNode: TraceReportTreeNode2 = None
    compRootNode: TraceReportTreeNode2 = None
    selectedObject: BusinessObject = None
    persistentObjects: List[BusinessObject] = ()


@dataclass
class TraceReportLegacy(TcBaseObj):
    """
    This structure holds information about generated trace reports with defining and complying trace trees with
    selected objects, and its persistent objects.
    
    :var definingTree: List of objects in the Defining Tree in the Trace Report giving all defining trace link details.
    
    :var indirectDefiningTree: List of objects in Indirect Defining Tree in the Trace  Report.
    :var complyingTree: List of objects in the Complying Tree in the Trace Report giving all complying trace link
    details.
    
    :var indirectComplyingTree: List of objects in Indirect Complying Tree in the Trace  Report.
    :var selectedObject: This structure member represents the object on which Trace Report is generated.
    :var persistentObjects: List of persistent object for the selected object.
    """
    definingTree: List[ReportLegacy] = ()
    indirectDefiningTree: List[ReportLegacy] = ()
    complyingTree: List[ReportLegacy] = ()
    indirectComplyingTree: List[ReportLegacy] = ()
    selectedObject: BusinessObject = None
    persistentObjects: List[BusinessObject] = ()


@dataclass
class TraceReportTreeNode2(TcBaseObj):
    """
    This structure holds information of each trace link report line with information of parent object, and its children
    associated with trace link relation.
    
    :var object: BusinessObject instance in Teamcenter on which Trace Link is created.
    :var displayObj: If the trace link is created on the occurrence then this variable will represent   the object to
    show in the trace report.
    :var srcContextName: Context name for source object of trace link.
    :var tarContextName: Context name for target object of trace link.
    :var bomView: The PSBOMView of context line for the Trace Link.
    :var contextLineObj: The context line (PSBOMViewRevision) for the Trace Link
    :var isDirectLink: If true, the object is a direct trace line object.
    :var isTraceLinkObj: If true, the current object  is a trace  link.
    :var childNodes: Child nodes with trace link relation with current object.
    """
    object: BusinessObject = None
    displayObj: WorkspaceObject = None
    srcContextName: str = ''
    tarContextName: str = ''
    bomView: BusinessObject = None
    contextLineObj: BusinessObject = None
    isDirectLink: bool = False
    isTraceLinkObj: bool = False
    childNodes: List[TraceReportTreeNode2] = ()


@dataclass
class TraceabilityReportOutput2(TcBaseObj):
    """
    TraceabilityReportOutput2 structure holds information of either of following including service data:
    1.    Generated trace reports with defining and/or complying trace trees with selected objects, and its persistent
    objects
    2.    Information about the file ticket for exported file generated at the server.
    
    The following partial error may be returned:
    1.     223201: MS Excel's outlining feature is limited to 8 levels, and the selected structure exceeds that level.
    Therefore it will be exported as a flat list with the "Level" column added.
    2.    223209: The Trace View template <template_name> is invalid. Please select an appropriate template as per the
    report type of trace view.
    3.    223036: Some of the objects were skipped during the export operation as no matching rule was found in the
    <sheet_name> sheet of the Excel template <template_name>.
    4.    214411: No input objects found. Please select the object to get traceability report.
    
    
    
    :var traceReports: All of the requested Trace Reports.
    :var transientFileReadTickets: The transient file read tickets for the exported file, this is specific to Export to
    Excel.
    :var serviceData: Service Data.
    """
    traceReports: List[TraceReport2] = ()
    transientFileReadTickets: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class TraceabilityReportOutputLegacy(TcBaseObj):
    """
    TraceabilityReportOutputLegacy structure holds information about generated trace reports with defining and
    complying trace trees with selected objects and its persistent objects, including service data.
    
    The following partial errors may be returned:
    214311: No input objects found. Please select the object to get traceability report. 
    214312: The provided report type value is not correct; allowed values are 1,2 and 3.
    214313: The provided report depth value is not correct; please provide any value greater than zero.
    
    
    :var traceReports: This member holds all the Trace Reports user has asked for. This is list of 
    TraceReport type of structures.
    :var serviceData: Service Data.
    """
    traceReports: List[TraceReportLegacy] = ()
    serviceData: ServiceData = None
