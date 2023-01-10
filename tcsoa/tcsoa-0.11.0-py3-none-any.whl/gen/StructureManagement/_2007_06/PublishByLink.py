from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow, PublishLink, PSBOMView
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindSourceOutput(TcBaseObj):
    """
    Contains source BOMLine and integer based index to point output to corresponding input.
    
    :var inputIndex: Integer pointing to input. Useful to map output with input.
    :var sourceLine: Source BOMLine for input target BOMLine and source BOMWindow. Source BOMLine and Target BOMLine
    are associated via PublishLink.
    """
    inputIndex: int = 0
    sourceLine: BOMLine = None


@dataclass
class FindSourceResponse(TcBaseObj):
    """
    Contains 'FindSourceOutput' containing source BOMLine and index to map to source BOMLine to corresponding input
    target BOMLine.
    
    :var output: 'FindSourceOutput' containing source BOMLine and integer index to map source BOMLine to input target
    BOMLine.
    :var serviceData: 'ServiceData' with plain objects containing source BOMLine and partial errors.
    """
    output: List[FindSourceOutput] = ()
    serviceData: ServiceData = None


@dataclass
class FindTargetsOutput(TcBaseObj):
    """
    Contains target BOMLines and integer based index to point output to corresponding input.
    
    :var inputIndex: Integer pointing to input. Useful to map output with input.
    :var targetLines: Target BOMLine for given source BOMLine and target BOMWindow.Target BOMLine and Source BOMLine
    are associated via PublishLink.
    """
    inputIndex: int = 0
    targetLines: List[BOMLine] = ()


@dataclass
class FindTargetsResponse(TcBaseObj):
    """
    Contains 'FindTargetsOutput' containing target BOMLine objects and index to map to target BOMLine to corresponding
    source.
    
    :var output: 'FindTargetsOutput' containing target BOMLine for input source BOMLine and integer index to map target
    BOMLine to input source BOMLine.
    :var serviceData: 'ServiceData' with plain objects containing target BOMLine objects and partial errors.
    """
    output: List[FindTargetsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetSourceTopLevelOutput(TcBaseObj):
    """
    Contains context PSBOMView of the source of PublishLink for given input target BOMLine. Integer based index points
    PSBOMView to corresponding input.
    
    :var inputIndex: Integer pointing to input. Useful to map output with input.
    :var topLevelBomView: PSBOMView of the source of PublishLink.
    """
    inputIndex: int = 0
    topLevelBomView: PSBOMView = None


@dataclass
class GetSourceTopLevelResponse(TcBaseObj):
    """
    'GetSourceTopLevelResponse' contains vector of 'GetSourceTopLevelOutput' and 'ServiceData'.
    
    :var output: 'GetSourceTopLevelOutput'  containing PSBOMView in which context targets were added and integer index
    to map PSBOMView to input BOMLine.
    :var serviceData: 'ServiceData' containing partial error and PSBOMView in plain objects list.
    """
    output: List[GetSourceTopLevelOutput] = ()
    serviceData: ServiceData = None


@dataclass
class LineAndWindow(TcBaseObj):
    """
    Contains source BOMLine and target BOMWindow in which associated target BOMLine of PublishLink to look for.
    
    :var line: Source BOMLine object.
    :var window: Target BOMWindow object.
    """
    line: BOMLine = None
    window: BOMWindow = None


@dataclass
class LogicallyEquivalentLinesOutput(TcBaseObj):
    """
    Contains logically equivalent BOMLines from input BOMWindow and BOMLine. The integer based index points equivalent
    line to input BOMLine.
    
    :var inputIndex: Integer pointing to input BOMLine. Useful to map output with input.
    :var lines: Logically equivalent BOMLine objects.
    """
    inputIndex: int = 0
    lines: List[BOMLine] = ()


@dataclass
class LogicallyEquivalentLinesResponse(TcBaseObj):
    """
    'LogicallyEquivalentLinesResponse' contains vector of 'LogicallyEquivalentLinesOutput' and 'ServiceData'.
    
    :var output: 'LogicallyEquivalentLinesOutput' with equivalent BOMLine objects  for input BOMLine pointed by integer
    inputIndex.
    :var serviceData: 'ServiceData' with equivalent BOMLines in plain objects and partial errors.
    """
    output: List[LogicallyEquivalentLinesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class PublishDataInfo(TcBaseObj):
    """
    Contains 'PublishLinkInfo' and 'dataFlags'. Each bit of 'dataFlags' denotes what data to be published.
    
    :var linkInfo: 'PublishLinkInfo' containing information to create PublishLink.
    :var dataFlags: 'dataFlags' representing what data to be published.
    """
    linkInfo: PublishLinkInfo = None
    dataFlags: int = 0


@dataclass
class PublishLinkInfo(TcBaseObj):
    """
    Required data to create a PublishLink like name, type, source and target BOMLines.
    
    :var name: object_name to be set on the PublishLink.
    :var type: Valid type to set on the PublishLink's object_type.
    :var source: BOMLine object.
    :var targets: List of BOMLine objects.
    """
    name: str = ''
    type: str = ''
    source: BOMLine = None
    targets: List[BOMLine] = ()


@dataclass
class PublishLinkOutput(TcBaseObj):
    """
    Contains PublishLink created by the operation and integer based index points PublishLink to corresponding input.
    
    :var inputIndex: Integer pointing to input. Useful to map output with input.
    :var publishLink: PublishLink object created during the operation.
    """
    inputIndex: int = 0
    publishLink: PublishLink = None


@dataclass
class PublishLinksResponse(TcBaseObj):
    """
    'PublishLinksResponse' contains list of 'PublishLinkOutput' structures and 'ServiceData'.
    
    :var output: 'PublishLinkOutput' containing PublishLink to which targets were added and integer index to map
    PublishLink to input BOMLine
    :var serviceData: 'ServiceData' with created objects and partial errors.
    """
    output: List[PublishLinkOutput] = ()
    serviceData: ServiceData = None


@dataclass
class SourceAndTargets(TcBaseObj):
    """
    Input structure that contains BOMLine objects representing source and targets of PublishLink
    
    :var source: BOMLine as source for PublishLink object
    :var targets: BOMLine objects as target for PublishLink object
    """
    source: BOMLine = None
    targets: List[BOMLine] = ()


@dataclass
class CompletenessCheckInputData(TcBaseObj):
    """
    Contains string mentioning which action be performed on input BOMLine representing Part.
    
    :var action: string representing action to be performed on BOMLine. Valid values are 'VerifyPartStructInteractive'
    and 'ClearCompletenessCheckResults'. The Completeness check is performed with action string is
    'VerifyPartStructInteractive'. The Completeness check is cleared if string is 'ClearCompletenessCheckResults'.
    :var bomline: BOMLine representing Part structure for which Completeness Check has to be performed.
    """
    action: str = ''
    bomline: BOMLine = None


@dataclass
class CompletenessCheckOutput(TcBaseObj):
    """
    Contains set of Complete, Incomplete and Skipped BOMLines for CompletenessCheck. Integer based index points output
    to corresponding input.
    
    :var inputIndex: Integer pointing to input. Useful to map output with input.
    :var completeLines: BOMLines that satisfy Completeness criteria.
    :var incompleteLines: BOMLines that do not satisfy Completeness criteria.
    :var skippedLines: BOMLines for which Completeness criteria do not apply.
    """
    inputIndex: int = 0
    completeLines: List[BOMLine] = ()
    incompleteLines: List[BOMLine] = ()
    skippedLines: List[BOMLine] = ()


@dataclass
class CompletenessCheckResponse(TcBaseObj):
    """
    'CompletenessCheckResponse' containing list of 'CompletenessCheckOutput' and 'ServiceData'. 
    'CompletenessCheckOutput' contains list of Complete, Incomplete and Skipped BOMLines and integer to map with input
    BOMLine. 'ServiceData' contains any error that might have occurred during operation.
    
    :var output: 'CompletenessCheckOutput' containing Complete, Incomplete and Skipped BOMLine objects. The integer
    inputIndex maps to index of input BOMLine to map output and input.
    :var serviceData: 'ServiceData' contains partial error (if any)
    """
    output: List[CompletenessCheckOutput] = ()
    serviceData: ServiceData = None
