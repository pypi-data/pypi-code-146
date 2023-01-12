from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TraceLink
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ManagedRelationResponse(TcBaseObj):
    """
    Managed Relation Response
    
    :var managedRelationObjects: List of Managed Relation Objects
    :var serviceData: The successful Object ids, partial errors and failures
    """
    managedRelationObjects: List[TraceLink] = ()
    serviceData: ServiceData = None


@dataclass
class ModifyManagedRelationInput(TcBaseObj):
    """
    Modify Managed Relation Input
    
    :var relationTag: Tag of the Relation
    :var setSourcesInput: Modify Sources Input
    :var setTargetsInput: Modify Targets Input
    """
    relationTag: BusinessObject = None
    setSourcesInput: ModifySources = None
    setTargetsInput: ModifyTargets = None


@dataclass
class ModifySources(TcBaseObj):
    """
    Modify Sources
    
    :var addSources: List of Sources to Add
    :var removeSources: List of Sources to Remove
    """
    addSources: List[BusinessObject] = ()
    removeSources: List[BusinessObject] = ()


@dataclass
class ModifyTargets(TcBaseObj):
    """
    Modify Targets
    
    :var addTargets: List of Targets to Add
    :var removeTargets: List of Targets to Remove
    """
    addTargets: List[BusinessObject] = ()
    removeTargets: List[BusinessObject] = ()


@dataclass
class TraceabilityInfoInput(TcBaseObj):
    """
    Traceability Information Input
    
    :var inputTag: Tag of the input
    :var reportType: Report Type
    :var reportDepth: Report Depth
    """
    inputTag: BusinessObject = None
    reportType: str = ''
    reportDepth: int = 0


@dataclass
class TraceabilityReportOutput(TcBaseObj):
    """
    Traceability Report Output
    
    :var definingTree: List of Defining Reports
    :var indirectDefiningTree: List of Defining Reports (Indirect)
    :var complyingTree: List of Complying Reports
    :var indirectComplyingTree: List of Complying Reports (Indirect)
    :var serviceData: The successful Object ids, partial errors and failures
    """
    definingTree: List[DefiningReport] = ()
    indirectDefiningTree: List[DefiningReport] = ()
    complyingTree: List[ComplyingReport] = ()
    indirectComplyingTree: List[ComplyingReport] = ()
    serviceData: ServiceData = None


@dataclass
class ComplyingReport(TcBaseObj):
    """
    Complying Report
    
    :var parent: Tag of the Parent
    :var children: List of Children
    """
    parent: BusinessObject = None
    children: List[BusinessObject] = ()


@dataclass
class CreateManagedRelationInput(TcBaseObj):
    """
    This structure has all the information needed to create TraceLink managed relation.
    
    :var name: name
    :var type: Type will decide what relation to be created
    :var primaryTagList: primaryTagList
    :var secondaryTagList: secondaryTagList
    """
    name: str = ''
    type: str = ''
    primaryTagList: List[BusinessObject] = ()
    secondaryTagList: List[BusinessObject] = ()


@dataclass
class DefiningReport(TcBaseObj):
    """
    Defining Report
    
    :var parent: Tag of the Parent
    :var children: List of Children
    """
    parent: BusinessObject = None
    children: List[BusinessObject] = ()
