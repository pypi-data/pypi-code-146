from __future__ import annotations

from tcsoa.gen.StructureManagement._2012_02.StructureVerification import AssignmentTypeDetailElement, PartialMatchCriteria
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExtensionAssignmentTypeDetails(TcBaseObj):
    """
    Structure that keeps assignment types details for each extension name.
    
    :var extensionName: Extension name that was compared.
    :var assignmentTypesDetails: A list of details for each assignment type.
    """
    extensionName: str = ''
    assignmentTypesDetails: List[AssignmentTypeDetailElement] = ()


@dataclass
class ExtensionComparisonSummary(TcBaseObj):
    """
    an element to capture the result of an extension comparison
    
    :var extensionName: Extension name that was compared.
    :var isDifferent: True if there is a difference in comparison of this equivalent set for this extension, false
    otherwise.
    """
    extensionName: str = ''
    isDifferent: bool = False


@dataclass
class GetAssignmentComparisonDetailsResponse(TcBaseObj):
    """
    response of method getAssignmentComparisonDetails - a vector of AssignmentTypeDetail element and serviceData
    
    :var serviceData: Object that captures any partial errors.
    :var details: The list of AssignmentType detail elements - one for each input equivalent set.
    """
    serviceData: ServiceData = None
    details: List[AssignmentTypeDetail] = ()


@dataclass
class GetComparisonSummariesResponse(TcBaseObj):
    """
    response of method getComparisonSummaries - a vector of ComparisonSummaries element and serviceData
    
    :var comparisonSummaries: The list of extension summaries elements - one for each input equivalent set.
    :var serviceData: Object that captures any partial errors.
    """
    comparisonSummaries: List[ComparisonSummaries] = ()
    serviceData: ServiceData = None


@dataclass
class AssignmentTypeDetail(TcBaseObj):
    """
    a structure to pair the AssignmentTypeDetail Element with an index into the input vector of equivalent sets of
    objects.
    
    :var index: Index of equivalent set in the input vector for which these details were calculated.
    :var equivalentLines: The list of all equivalent lines in the input equivalent set (all equivalent sources in
    sequence and then all targets in sequence).
    :var assignmentDetails: Assignment type details of this equivalent set.
    """
    index: int = 0
    equivalentLines: List[BusinessObject] = ()
    assignmentDetails: List[ExtensionAssignmentTypeDetails] = ()


@dataclass
class StringToPartialMatchCriteria(TcBaseObj):
    """
    Holds PartialMatchCriteria object for each extension name.
    
    :var extensionName: Extension name that needs to be compared. 
    An extension name is the ID of a "serverExtension" registered in Accountability Check&rsquo;s plugin.xml. It can be
    located in com.teamcenter.rac.cme.accountabilitycheck.relations package.
    :var extensionCriteria: The comparison criteria of this extension.
    """
    extensionName: str = ''
    extensionCriteria: PartialMatchCriteria = None


@dataclass
class ComparisonSummaries(TcBaseObj):
    """
    the  ExtensionComparisonSummary for each extension per input vector element
    
    :var index: Index of equivalent set in the input vector for which these results were calculated.
    :var summaries: The list of elements that capture the result of an extension comparison.
    """
    index: int = 0
    summaries: List[ExtensionComparisonSummary] = ()
