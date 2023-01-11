from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AssignChildLineOccTypes(TcBaseObj):
    """
    This structure defines child lines to be assigned with its occurrence type and client id.
    
    :var lineToAssign: lineToAssign
    :var occType: occurrence type for new assigned line. it can be empty.
    """
    lineToAssign: BOMLine = None
    occType: str = ''


@dataclass
class AssignChildLinesOutput(TcBaseObj):
    """
    Holds the response from assignChildLines
    
    :var newLines: new BOMLines created as a result of assign operation under newParentLine
    :var linesWithoutPreds: a subset new bomlines that do have incoming flows.
    """
    newLines: List[BOMLine] = ()
    linesWithoutPreds: List[BOMLine] = ()


@dataclass
class AssignChildLinesParameter(TcBaseObj):
    """
    This structure provides a set of input values for assignLines operation.
    
    :var newParentLine: new parent line under which the bomlines need to be assigned
    :var linesToAssign: Array of AssignChildLineOccType
    :var copyPreds: should predecessor relationship be copied over from old parent?
    :var copyOccTypeFromSource: occurrence type to be used for newly assigned lines.
    """
    newParentLine: BOMLine = None
    linesToAssign: List[AssignChildLineOccTypes] = ()
    copyPreds: bool = False
    copyOccTypeFromSource: bool = False


@dataclass
class AssignChildLinesResponse(TcBaseObj):
    """
    Holds the response from assignChildLines
    
    :var assignOutput: array of AssignChildLinesOutput
    :var serviceData: Exceptions from internal processing returned as PartialErrors
    """
    assignOutput: List[AssignChildLinesOutput] = ()
    serviceData: ServiceData = None
