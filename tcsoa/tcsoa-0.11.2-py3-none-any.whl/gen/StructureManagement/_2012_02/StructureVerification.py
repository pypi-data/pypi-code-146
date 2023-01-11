from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ReportDefinition
from tcsoa.gen.StructureManagement._2010_09.StructureVerification import ReportCriteria, EndItemDetail
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetAssignmentComparisonDetailsResponse(TcBaseObj):
    """
    response of method getAssignmentComparisonDetails - a vector of AssignmentTypeDetail element and serviceData
    
    :var details: a list of AssignmentType detail elements - for all the input equivalent sets.
    :var serviceData: serviceData element to capture any partial errors.
    """
    details: List[AssignmentTypeDetail] = ()
    serviceData: ServiceData = None


@dataclass
class GetDescendentComparisonDetailsResponse(TcBaseObj):
    """
    structure to capture the response of getDescendentComparisonDetails method. Has the list of details for each input
    set and serviceData to capture partial errors.
    
    :var details: detail list.
    :var serviceData: serviceData member to capture any partial errors.
    """
    details: List[DescendentDetail] = ()
    serviceData: ServiceData = None


@dataclass
class GetPartitionComparisonDetailsResponse(TcBaseObj):
    """
    structure to capture the vector of PartitionDetail elements and serviceData for partial errors.
    
    :var details: vector of partitionDetail elements.
    :var serviceData: serviceData member to capture partial errors.
    """
    details: List[PartitionDetail] = ()
    serviceData: ServiceData = None


@dataclass
class GetPredecessorComparisonDetailsResponse(TcBaseObj):
    """
    return the list of predecessor detail elements and service data for partial errors.
    
    :var details: details about the predecessor detail for each element.
    :var serviceData: serviceData to capture any partial errors.
    """
    details: List[PredecessorDetail] = ()
    serviceData: ServiceData = None


@dataclass
class GetPropertyComparisonDetailsResponse(TcBaseObj):
    """
    response of getPropertyComparisonDetails method.
    
    :var details: the list of elements that have the details for each property in the input.
    :var serviceData: serviceData element to capture any partial errors.
    """
    details: List[PropertyDetail] = ()
    serviceData: ServiceData = None


@dataclass
class AssignmentDetail(TcBaseObj):
    """
    For each line in input equivalent set  holds the tag of the current assigned objects for that line.
    
    :var assignments: size is same as the size of the input equivalent line. It is the list of assignments (one per
    line) - across the row.
    :var matchType: flag to indicate match of the current assignment.
    """
    assignments: List[BusinessObject] = ()
    matchType: int = 0


@dataclass
class AssignmentTypeDetail(TcBaseObj):
    """
    a structure to pair the AssignmentTypeDetail Element with an index into the input vector of equivalent sets of
    objects.
    
    :var index: index into the input vector.
    :var details: the size of the vector is same as maximum number of  assignmentTypes among the set equivalent lines.
    eg: if src1, target1 are equivalent and src1 has 3 manual assignments and target1 has 2 - this vector will have 3
    elements. The first AssignmentTypeDetailElement will have src1_assign1, target1_assign1; the second
    AssignmentTypeDetailElement will have src1_assign2,target1_assign2; the third AssignmentTypeDetailElement will have
    src1_assign3, NULL
    :var equivalentLines: the set of all equivalent lines in input (all equivalent srcs in sequence and then all
    targets in sequence).
    """
    index: int = 0
    details: List[AssignmentTypeDetailElement] = ()
    equivalentLines: List[BusinessObject] = ()


@dataclass
class AssignmentTypeDetailElement(TcBaseObj):
    """
    a structure to capture the details for assignment comparison.
    
    :var assignmentType: a string to indicate the type of assignment (MEConsumed, MEResource etc.)
    :var manualAssignments: length of the vector will be the maximum number of assignments among all the equivalent
    lines for the given type. If there are 3 assigments for src1 and 1 for target1 - the size of this vector will be 3,
    with the first AssignmentDetails element having {src1assign1,target1assign1}, the second AssignmentDetail element
    having {src1assign2,NULLTAG}, the third {src1assign3,NULLTAG}.
    :var logicalAssignments: length of the vector will be the maximum number of logical assignments among all the
    equivalent lines for the given type.
    """
    assignmentType: str = ''
    manualAssignments: List[AssignmentDetail] = ()
    logicalAssignments: List[LogicalAssignmentDetail] = ()


@dataclass
class AsyncACInput(TcBaseObj):
    """
    provides a set of input values for the accountabilityCheckAsync operation.
    
    :var sourceObjects: persistent objects that can be converted to bomlines. Currently, the only supported object is
    VisStructureContext object, with the array length being 1.
    :var targetObjects: persistent objects (target) that can be converted to bomlines. Currently, the only supported
    object is VisStructureContext object, with the array length being 1.
    :var resultName: Name of occurrenceGroup to be created - when report is generated.
    :var resultDesc: optional description of the OccurrenceGroup to be created.
    :var reportCriteria: criteria for printable report.
    :var reportMode: Indicates which mode the accountability check report has to be generated.10 - batch report, 16 -
    batch propagate.
    :var partialMatchCriteria: the set of options to be used for comparison on equivalent lines. It is a map - with the
    key being the name of plugin or string to be used as a discriminator between various components.
    :var includeScopeLines: Flag to indicate whether  to include scope lines as part of result set.
    :var options: mask of integer values representing different UI options.
    :var sourceContextLine: Optional source context line. Currently unused.
    :var targetContextLine: optional target context line. Currently, not used.
    :var matchType: Represents user choice of color display.
    :var sourceFilteringRule: The source filtering rule.
    :var targetFilteringRule: The target filtering rule.
    :var sourceDepth: the depth of source structure. -1 represents all depths.
    :var targetDepth: The depth of target structure from each target root. -1 to set it to any depth.
    """
    sourceObjects: List[BusinessObject] = ()
    targetObjects: List[BusinessObject] = ()
    resultName: str = ''
    resultDesc: str = ''
    reportCriteria: AsyncReportCriteria = None
    reportMode: int = 0
    partialMatchCriteria: AsyncStringToPartialMatchCriteriaMap = None
    includeScopeLines: bool = False
    options: int = 0
    sourceContextLine: BusinessObject = None
    targetContextLine: BusinessObject = None
    matchType: int = 0
    sourceFilteringRule: str = ''
    targetFilteringRule: str = ''
    sourceDepth: int = 0
    targetDepth: int = 0


@dataclass
class AsyncDetails(TcBaseObj):
    """
    details that are to be specified if an operation is to be performed asynchronously. This is same as the BatchUtils
    parameters that is (optionally) passed to accountabilityCheck. Duplicated as structures are not to be shared in soa
    framework.
    
    :var identifier: any user defined string for recognizing the request
    :var mode: processing mode on server. Possible values are "BackGround", "Blocking" and "InProcess" (case
    sensitive). Currently, the only supported value is BackGround. In this mode the Dispatcher services must be
    installed, or the server will default to InProcess (meaning same tcserver as the one the client connects to will be
    used for accountability).
    :var site: processing site. 0 - local. This information is used in the blocking mode to get the http url.
    :var priority: possible values - 0-3, 0 being the lowest.
    :var startTime: start date/time of scheduled dispatcher request
    :var endTime: end date/time of scheduled dispatcher request
    :var daysOfWeek: on which day of the week translator (async process) has to be run. Should have 7 entries and a
    true indicates should be run on that day. Starting on Sunday (1st entry).
    :var endAfterOccurrences: number of times the async process has to run.
    :var primaryObjects: objects used directly or indirectly for the asynchronous processing.
    :var secondaryObjects: any auxiliary objects to be used as additional info during processing of asynchronous
    request. Example - a folder to add some datasets to.
    """
    identifier: str = ''
    mode: str = ''
    site: int = 0
    priority: int = 0
    startTime: datetime = None
    endTime: datetime = None
    daysOfWeek: List[bool] = ()
    endAfterOccurrences: int = 0
    primaryObjects: List[BusinessObject] = ()
    secondaryObjects: List[BusinessObject] = ()


@dataclass
class AsyncPartialMatchCriteria(TcBaseObj):
    """
    a structure to capture generic Partial Match criteria
    
    :var intMap: map of string to vector or integers.
    :var dblMap: map of string to vector of doubles.
    :var strMap: map of string to vector of strings.
    :var objMap: map of string to vector of objects.
    """
    intMap: StringToIntVectorMap = None
    dblMap: StringToDblVectorMap = None
    strMap: StringToStrVectorMap = None
    objMap: StringToObjVectorMap = None


@dataclass
class AsyncReportCriteria(TcBaseObj):
    """
    criteria for generating print report
    
    :var rdTag: report definition Tag (required)
    :var reportName: name of the report.
    :var datasetType: Dataset type to be used.
    :var reportOptionsNames: StructElement name="reportOptionsNames" description="a vector of strings containing the
    Names in a series of Name/Value pairs used to specify additional criteria (optional)
    :var reportOptionsValues: a vector of strings containing the Values in a series of Name/Value pairs used to specify
    additional criteria (optional)
    :var contextObjects: a vector of Tags representing context object(s) (required for item reports)
    :var contextObjectUIDs: a vector of uids representing context objects
    :var stylesheetTag: stylesheet Tag (optional)
    :var stylesheetName: Name of the stylesheet.
    :var datasetName: name of containing DataSet (optional)
    :var criteriaName: a vector of strings containing the Names in a series of Name/Value pairs used to specify
    additional criteria (optional)
    :var criteriaValues: a vector of strings containing the Values in a series of Name/Value pairs used to specify
    additional criteria (optional)
    :var datasetCtxUID: The uid for the context dataset
    :var datasetCtxObj: Dataset context tag
    :var relationName: relation name to be used.
    """
    rdTag: ReportDefinition = None
    reportName: str = ''
    datasetType: str = ''
    reportOptionsNames: List[str] = ()
    reportOptionsValues: List[str] = ()
    contextObjects: List[BusinessObject] = ()
    contextObjectUIDs: List[str] = ()
    stylesheetTag: BusinessObject = None
    stylesheetName: str = ''
    datasetName: str = ''
    criteriaName: List[str] = ()
    criteriaValues: List[str] = ()
    datasetCtxUID: str = ''
    datasetCtxObj: BusinessObject = None
    relationName: str = ''


@dataclass
class LogicalAssignmentDetail(TcBaseObj):
    """
    For each line in input equivalent set  holds the tag of the current assigned objects for that line.
    
    :var criteria: for each line in input equivalent set holds the criteria of the current line's LA - across the row.
    :var resolvedAssignments: length of the vector will be the maximum number of resolved assignments among all the
    equivalent lines for the given type.
    :var matchType: flag to indicate match of the current assignment.
    :var logicalAssignments: For each line in input equivalent set holds the logical assignment or tool requirement
    object.
    """
    criteria: List[str] = ()
    resolvedAssignments: List[AssignmentDetail] = ()
    matchType: int = 0
    logicalAssignments: List[BusinessObject] = ()


@dataclass
class PartialMatchCriteria(TcBaseObj):
    """
    a structure to capture generic Partial Match criteria
    
    :var intMap: map of string to vector or integers.
    :var dblMap: map of string to vector of doubles.
    :var strMap: map of string to vector of strings.
    :var objMap: map of string to vector of objects.
    :var dateMap: map of string to vector of dates
    """
    intMap: StringToIntVectorMap = None
    dblMap: StringToDblVectorMap = None
    strMap: StringToStrVectorMap = None
    objMap: StringToObjVectorMap = None
    dateMap: StringToDateVectorMap = None


@dataclass
class PartitionDetail(TcBaseObj):
    """
    structure to capture the position(index) in the input equivalence set and the partition elements vector.
    
    :var index: position in the input vector.
    :var partitions: The size of the vector matches the equivalent lines. This list the partition per input equivalent
    line as a row.
    :var isDifferent: flag to indicate whether any of the partitions in a single row is different.
    :var equivalentLines: the set of all equivalent lines in input (all equivalent srcs in sequence and then all
    targets in sequence).
    """
    index: int = 0
    partitions: List[BusinessObject] = ()
    isDifferent: bool = False
    equivalentLines: List[BusinessObject] = ()


@dataclass
class PredecessorDetail(TcBaseObj):
    """
    the list of PredecessorDetailElements for each set of input equivalent objects.
    
    :var index: position in the input vector.
    :var details: The size of the vector matches the maximum number of predecessors for each line in input equivalent
    set at index above (given now by equivalentLines - src lines being followed by targetlines). The
    PredecessorDetailElement will be the size of the input lines. Eg: equivalentset(src1,target1) - src1 has 3
    predecessors, target1 has 1 predecessor. details element vector size will be 3. The first PredecessorDetailElement
    will contain 2 predecessors: SrcPred1,targetPred1. The second PredecessorDetailElement will have SrcPred2,NULLTAG,
    and 3rd PredecessorDetailElement will have SrcPred3,NULLTAG.
    :var equivalentLines: the set of all equivalent lines in input (all equivalent srcs in sequence and then all
    targets in sequence).
    """
    index: int = 0
    details: List[PredecessorDetailElement] = ()
    equivalentLines: List[BusinessObject] = ()


@dataclass
class PredecessorDetailElement(TcBaseObj):
    """
    the list of PredecessorDetailElements for each set of input equivalent objects.
    
    :var predecessors: The size of the vector will match the size of the equivalent lines at input index i. This array
    represents one predecessor per input line (row in a table, and not a column). . Eg: SrcPred1, NULLTAG, TargetPred1,
    NULLTAG (assuming 4 eqv. lines)
    :var matchType: 0 means fullmatch, 1 means match, 2 means multiple match
    """
    predecessors: List[BusinessObject] = ()
    matchType: int = 0


@dataclass
class PropagationInput(TcBaseObj):
    """
    the input structure for propagateProperties.
    
    :var target: the target object to which the changes will be propagated.
    :var sources: the source object(s) from which the changes will be propagated to target.
    :var criteria: the partialMatchCriteria structure to be used for change propagation. This is a map of a string (a
    client id) to that client's properties/criteria.
    """
    target: BusinessObject = None
    sources: List[BusinessObject] = ()
    criteria: StringToPartialMatchCriteriaMap = None


@dataclass
class PropagationResponse(TcBaseObj):
    """
    The response of Propagation Service.
    
    :var results: a vector of propagationResults.
    :var logFileTicket: a fms ticket for the transient file that captures the log of propagation service.
    :var serviceData: Service Data object
    """
    results: List[PropagationResult] = ()
    logFileTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class PropagationResult(TcBaseObj):
    """
    a structure to capture a single result for an object that is being propagated from one context to another.
    
    :var index: a integer representing the position in input vector.
    :var propagationResults: a map of string to vector of propagationResultElements. The key of the map would indicate
    the client id corresponding to what is passed in PropagationInput.
    """
    index: int = 0
    propagationResults: PropagationResultMap = None


@dataclass
class PropagationResultElement(TcBaseObj):
    """
    a structure to capture a single result for an object that is being propagated from one context to another.
    
    :var object: an object which is participating in the propagation.
    :var propagatedProperties: successfully propagatedProperties.
    :var logFileTicket: an optional log file ticket. If the extension/server generates a specific logfile - this will
    be the fms ticket for that file (transient).
    """
    object: BusinessObject = None
    propagatedProperties: List[str] = ()
    logFileTicket: str = ''


@dataclass
class PropertyDetail(TcBaseObj):
    """
    the  propertyDetailElement for each of the properties per input vector element.
    
    :var index: index of the input vector of equivalent set of obejcts.
    :var details: the list of PropertyDetailsElement
    """
    index: int = 0
    details: List[PropertyDetailsElement] = ()


@dataclass
class PropertyDetailsElement(TcBaseObj):
    """
    a element to capture the details of a property for an object(s).
    
    :var propertyName: the name of the property.
    :var isDifferent: flag to indicate if any of the objects have a value(s) that is different.
    """
    propertyName: str = ''
    isDifferent: bool = False


@dataclass
class BOMLineNetEffectivityDetail(TcBaseObj):
    """
    structure to encapsulate a BOMLine and the associated endItem effectivity details.
    
    :var line: The bomline for which the effectivity details will added.
    :var effDetails: The array of effectivity details for the bomline
    """
    line: BusinessObject = None
    effDetails: List[EndItemDetail] = ()


@dataclass
class BatchDetails(TcBaseObj):
    """
    details that are to be specified if an operation is to be performed asynchronously.
    
    :var identifier: any user defined string for recognizing the request
    :var mode: processing mode on server. Possible values are "BackGround", "Blocking" and "InProcess" (case
    sensitive). Currently, the only supported value is BackGround. In this mode the Dispatcher services must be
    installed, or the server will default to InProcess (meaning same tcserver as the one the client connects to will be
    used for accountability).
    :var site: processing site. 0 - local. This information is used in the blocking mode to get the http url.
    :var priority: possible values - 0-3, 0 being the lowest.
    :var startTime: start date/time of scheduled dispatcher request
    :var endTime: end date/time of scheduled dispatcher request
    :var daysOfWeek: on which day of the week translator (async process) has to be run. Should have 7 entries and a
    true indicates should be run on that day. Starting on Sunday (1st entry).
    :var endAfterOccurrences: number of times the async process has to run.
    :var primaryObjects: objects used directly or indirectly for the asynchronous processing.
    :var secondaryObjects: any auxiliary objects to be used as additional info during processing of asynchronous
    request. Example - a folder to add some datasets to.
    """
    identifier: str = ''
    mode: str = ''
    site: int = 0
    priority: int = 0
    startTime: datetime = None
    endTime: datetime = None
    daysOfWeek: List[bool] = ()
    endAfterOccurrences: int = 0
    primaryObjects: List[BusinessObject] = ()
    secondaryObjects: List[BusinessObject] = ()


@dataclass
class UnitAndLineDetails(TcBaseObj):
    """
    Structure to capture the Equivalent BomLines (potentially from 2 windows - a source and target window) along with
    their matched units or dates.
    
    :var units: all or a subset of Unit numbers/dates associated with the source and targetlines. The units are in
    pairs - meaning - if you have unit effectivtiy like:1-7,10 - this array will be 1,7,10,10.
    :var dates: If date effectivity is  used - this will have the date ranges for the equivalent lines. Current
    implementation does not support thi
    :var srcLines: list of of srclines that satisfy the units/dates in this structure.
    :var targetLines: list of of target lines ( lines from another window  that are equivalent in some way to the src
    lines - eg: ID in context) that satisfy the units/dates in this structure.
    """
    units: List[int] = ()
    dates: List[datetime] = ()
    srcLines: List[BusinessObject] = ()
    targetLines: List[BusinessObject] = ()


@dataclass
class ACInput(TcBaseObj):
    """
    provides a set of input values for the accountabilityCheck operation.
    
    :var sourceObjects: The source bom lines.
    :var targetObjects: The target bom lines.
    :var resultName: Name of occurrenceGroup to be created - when report is generated.
    :var resultDesc: optional description of the OccurrenceGroup to be created.
    :var reportCriteria: criteria for printable report.
    :var reportMode: Indicates which mode the accountability check report has to be generated. Occurrence group mode of
    excel report mode or coloring mode or a combination of those or batch report or batch propagate. This is a bit
    masked flag. 1 - coloring mode, 2 - generate report, 3 - color and generate report, 4 - occurrence group report, 8
    - batch report, 16 - batch propagate.
    :var partialMatchCriteria: the set of options to be used for comparison on equivalent lines. It is a map - with the
    key being the name of plugin or string to be used as a discriminator between various components.
    :var includeScopeLines: Flag to indicate whether  to include scope lines as part of result set.
    :var options: mask of integer values representing different UI options.
    :var sourceContextLine: Optional source context line.
    :var targetContextLine: optional target context line.
    :var matchType: Represents user choice of color display.
    :var sourceFilteringRule: The source filtering rule.
    :var targetFilteringRule: The target filtering rule.
    :var sourceDepth: the depth of source structure. -1 represents all depths.
    :var targetDepth: The depth of target structure from each target root. -1 to set it to any depth.
    """
    sourceObjects: List[BusinessObject] = ()
    targetObjects: List[BusinessObject] = ()
    resultName: str = ''
    resultDesc: str = ''
    reportCriteria: ReportCriteria = None
    reportMode: int = 0
    partialMatchCriteria: StringToPartialMatchCriteriaMap = None
    includeScopeLines: bool = False
    options: int = 0
    sourceContextLine: BusinessObject = None
    targetContextLine: BusinessObject = None
    matchType: int = 0
    sourceFilteringRule: str = ''
    targetFilteringRule: str = ''
    sourceDepth: int = 0
    targetDepth: int = 0


@dataclass
class CompareNetEffectivityGroup(TcBaseObj):
    """
    structure to capture the response of CompareNetEffectivity method.
    
    :var srcLineEffectivities: effectivities of the source lines.
    :var targetLineEffectivities: effectivities of targetLines.
    :var missingSrcDetails: details of missing src by effectivity comparison.
    :var missingTargetDetails: Details of missing target effectivities
    :var overlappingEffectivities: Details of overlapping effectivities. Source lines that have overlapping units or
    target lines that have overlapping units will be listed.
    :var matchingEffectivities: Details of matching source and target effectivities
    :var isMisMatch: flag that is set to true if there is a mismatch.
    """
    srcLineEffectivities: List[BOMLineNetEffectivityDetail] = ()
    targetLineEffectivities: List[BOMLineNetEffectivityDetail] = ()
    missingSrcDetails: List[EndItemAndUnitDetails] = ()
    missingTargetDetails: List[EndItemAndUnitDetails] = ()
    overlappingEffectivities: List[EndItemAndUnitDetails] = ()
    matchingEffectivities: List[EndItemAndUnitDetails] = ()
    isMisMatch: bool = False


@dataclass
class CompareNetEffectivityResponse(TcBaseObj):
    """
    structure to capture the response of compareNetEffectivityGroup method.  Vector of CompareNetEffectivityGroup
    structures one per input set based equivalent lines and a serviceData member to report partial errors.
    
    :var compareGroups: vector of the compare results for each corresponding set of input vector of equivalent lines
    :var serviceData: serviceData to return any partial errors
    """
    compareGroups: List[CompareNetEffectivityGroup] = ()
    serviceData: ServiceData = None


@dataclass
class DescendentDetail(TcBaseObj):
    """
    the list of DescendentDetailElements for each set of input equivalent objects.
    
    :var index: position in the input vector.
    :var details: The size of the vector matches the maximum number of descendents for each line in input equivalent
    set at index above (given now by equivalentLines - src lines being followed by targetlines). Eg:
    equivalentset(src1,target1) - src1 has 3 children, target1 has 1 child. details element vector size will be 3. The
    first DescendentDetailElement will contain 2 children: SrcChild1,targetChild1. The second DescendentDetailElement
    will have SrcChild2,NULLTAG, and 3rd DescendentDetailElement will have SrcChild3,NULLTAG.
    :var equivalentLines: the set of all equivalent lines in input (all equivalent srcs in sequence and then all
    targets in sequence).
    """
    index: int = 0
    details: List[DescendentDetailElement] = ()
    equivalentLines: List[BusinessObject] = ()


@dataclass
class DescendentDetailElement(TcBaseObj):
    """
    the list of DescendentDetailElements for each set of input equivalent objects.
    
    :var children: The size of the vector will match the size of the equivalent lines at input index i. This array
    represents one predecessor per input line (row in a table, and not a column). . Eg: SrcChild1, NULLTAG,
    TargetChild1, NULLTAG (assuming 4 eqv. lines)
    :var matchType: 0 means fullmatch, 1 means match, 2 means multiple match
    """
    children: List[BusinessObject] = ()
    matchType: int = 0


@dataclass
class EndItemAndUnitDetails(TcBaseObj):
    """
    endItem (item used to specify the unit effectivity) tag and the associated UnitAndLineDetails structure.
    
    :var endItem: Teamcenter::BusinessObject
    The endItem object to be associated with the Unit details
    :var details: structure capturing the details of line(s) and effectivities.
    """
    endItem: BusinessObject = None
    details: List[UnitAndLineDetails] = ()


@dataclass
class EquivalentLines(TcBaseObj):
    """
    Lines from a Source Window and a Target Window that are equivalent. For example - having the same ID in Context or
    other criteria.
    
    :var eqvSrcLines: set of source BOMLine objects that are equivalent based on some criteria like ID in context.
    :var eqvTargetLines: set of target BOMLine objects (not the same window as source lines) that are equivalent in a
    manner consistent with the source lines.
    """
    eqvSrcLines: List[BusinessObject] = ()
    eqvTargetLines: List[BusinessObject] = ()


@dataclass
class EquivalentSetElement(TcBaseObj):
    """
    a structure to capture the equivalent src and target lines along with the partial match criteria.
    
    :var eqvSrcLines: the src lines which are equivalent (currently only id in context)
    :var eqvTargetLines: equivalent target lines - based on In context id (absoccid) or apn or ebop criteria (origin
    link, logical designator, uid )
    :var criteria: input map for specifying criteria, the key being server extension id.
    """
    eqvSrcLines: List[BusinessObject] = ()
    eqvTargetLines: List[BusinessObject] = ()
    criteria: StringToPartialMatchCriteriaMap = None


"""
a map of string to AsyncPartialMatchCriteriaMap
"""
AsyncStringToPartialMatchCriteriaMap = Dict[str, AsyncPartialMatchCriteria]


"""
a map of string (an id) and the vector of PropagationResult objects.
"""
PropagationResultMap = Dict[str, List[PropagationResultElement]]


"""
a map of string to vector of dates
"""
StringToDateVectorMap = Dict[str, List[datetime]]


"""
String to vector of doubles map.
"""
StringToDblVectorMap = Dict[str, List[float]]


"""
map of string to vector of integers.
"""
StringToIntVectorMap = Dict[str, List[int]]


"""
a map of string to vector of objects.
"""
StringToObjVectorMap = Dict[str, List[BusinessObject]]


"""
a map of string to PartialMatchCriteriaMap
"""
StringToPartialMatchCriteriaMap = Dict[str, PartialMatchCriteria]


"""
a map of String to vector of strings.
"""
StringToStrVectorMap = Dict[str, List[str]]
