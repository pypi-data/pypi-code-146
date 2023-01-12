from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, ReportDefinition
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BOMLineNetEffectivityDetail(TcBaseObj):
    """
    structure to encapsulate a BOMLine and the associated endItem effectivity details.
    
    :var line: The bomline for which the effectivity details will be added.
    :var effDetails: The array of effectivity details for the bomline.
    """
    line: BOMLine = None
    effDetails: List[EndItemDetail] = ()


@dataclass
class ReportCriteria(TcBaseObj):
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
class ACInput(TcBaseObj):
    """
    Provides a set of input values for the accountabilityCheck operation
    
    :var sourceObjects: The source bom lines
    :var targetObjects: The target bom lines
    :var resultName: Name of the OccurrenceGroup to be created.
    :var resultDesc: optional description of the OccurrenceGroup to be created - if OccurrenceGroup report option is
    chosen.
    :var reportCriteria: the criteria for printable report.
    :var reportMode: Indicates in what mode the accountability check is running. It can be occurrence group mode, excel
    report mode, coloring mode, or a combination of report and coloring. Valid values for        reportMode are: 1 -
    coloring mode, 2 - excel report mode, 3 - coloring and excel report mode, 4 - occurrence group mode
    :var options: Sum of integer values representing different UI options
    :var sourceContextLine: The possible source context line
    :var targetContextLine: The possible target context line
    :var matchType: Represents user choice in color display
    :var sourceFilteringRule: The source filtering rule
    :var targetFilteringRule: The target filtering rule
    :var sourceDepth: The source structure search depth; -1 represents all depths
    :var targetDepth: The target structure search depth; -1 represents all depths
    """
    sourceObjects: List[BusinessObject] = ()
    targetObjects: List[BusinessObject] = ()
    resultName: str = ''
    resultDesc: str = ''
    reportCriteria: ReportCriteria = None
    reportMode: int = 0
    options: int = 0
    sourceContextLine: BusinessObject = None
    targetContextLine: BusinessObject = None
    matchType: int = 0
    sourceFilteringRule: str = ''
    targetFilteringRule: str = ''
    sourceDepth: int = 0
    targetDepth: int = 0


@dataclass
class TransientFileInfo(TcBaseObj):
    """
    info about any transient report files that are generated.
    
    :var fileName: Name of the file generated in transient volume.
    :var isText: Flag to indicate whether the file is a text file or binary file.
    :var ticket: transient file ticket string.
    """
    fileName: str = ''
    isText: bool = False
    ticket: str = ''


@dataclass
class UnitAndLineDetails(TcBaseObj):
    """
    Structure to capture the Equivalent BomLines (potentially from 2 windows - a source and target window) along with
    their matched units or dates.
    
    :var units: all or a subset of Unit numbers/dates associated with the source and targetlines. The units are in
    pairs - meaning - if you have unit effectivtiy like:1-7,10 - this array will be 1,7,10,10.
    :var dates: If date effectivity is  used - this will have the date ranges for the equivalent lines. Current
    implementation does not support this.
    :var srcLines: list of of srclines that satisfy the units/dates in this structure.
    :var targetLines: list of of target lines ( lines from another window  that are equivalent in some way to the src
    lines - eg: ID in context) that satisfy the units/dates in this structure.
    """
    units: List[int] = ()
    dates: List[datetime] = ()
    srcLines: List[BOMLine] = ()
    targetLines: List[BOMLine] = ()


@dataclass
class AccountabilityCheckResponse(TcBaseObj):
    """
    Contains all the results from the accountabilityCheck operation
    
    :var accountabilityCheckResults: A vector of accountability check results
    :var reachableTargets: A vector of reachable target lines
    :var serviceData: The service data
    """
    accountabilityCheckResults: List[AccountabilityCheckResult] = ()
    reachableTargets: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class AccountabilityCheckResult(TcBaseObj):
    """
    Encapsulates one accountability check result
    
    :var sourceLine: The source bom line
    :var equivalentSourceLines: A vector of equivalent source lines
    :var equivalentTargetLines: A vector of equivalent target lines
    :var checkResult: Accountability check result represented by a color value
    :var resultViewTag: If OccurrenceGroup report option is chosen, this will be the created OccurrenceGroup.
    :var reportFileInfo: details of report files generated in the transient volume.
    """
    sourceLine: BusinessObject = None
    equivalentSourceLines: List[BusinessObject] = ()
    equivalentTargetLines: List[BusinessObject] = ()
    checkResult: int = 0
    resultViewTag: BusinessObject = None
    reportFileInfo: List[TransientFileInfo] = ()


@dataclass
class CompareNetEffectivityGroup(TcBaseObj):
    """
    structure to capture the response of CompareNetEffectivity method.
    
    :var srcLineEffectivities: effectivities of the source lines.
    :var targetLineEffectivities: effectivities of targetLines.
    :var missingSrcDetails: details of missing src by effectivity comparison.
    :var missingTargetDetails: Details of missing target effectivities.
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
    
    :var compareGroups: vector of the compare results for each corresponding set of input vector of equivalent lines.
    :var serviceData: serviceData to return any partial errors.
    """
    compareGroups: List[CompareNetEffectivityGroup] = ()
    serviceData: ServiceData = None


@dataclass
class EndItemAndUnitDetails(TcBaseObj):
    """
    endItem (item used to specify the unit effectivity) tag and the associated UnitAndLineDetails structure.
    
    :var endItem: The endItem object to be associated with the Unit details.
    :var details: structure capturing the details of line(s) and effectivities.
    """
    endItem: BusinessObject = None
    details: List[UnitAndLineDetails] = ()


@dataclass
class EndItemDetail(TcBaseObj):
    """
    structure to capture the details of enditem - the identifier, effectivity units associated with that enditem and
    dates (future).
    
    :var endItem: the endItem to be associated with the units.
    :var units: unit ranges for the endItem. The units are in pairs - meaning - if you have unit effectivtiy
    like:1-7,10 - this array will be 1,7,10,10.
    :var dates: date ranges. Currently not supported. Meaning - will be empty.
    """
    endItem: BusinessObject = None
    units: List[int] = ()
    dates: List[datetime] = ()


@dataclass
class EquivalentLines(TcBaseObj):
    """
    Lines from a Source Window and a Target Window that are equivalent. For example - having the same ID in Context or
    other criteria.
    
    :var eqvSrcLines: set of source bomlines that are equivalent based on some criteria like ID in context.
    :var eqvTargetLines: set of target bomlines (not the same window as source lines) that are equivalent in a manner
    consistent with the source lines.
    """
    eqvSrcLines: List[BOMLine] = ()
    eqvTargetLines: List[BOMLine] = ()
