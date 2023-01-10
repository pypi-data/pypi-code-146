from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AlignmentMismatches(TcBaseObj):
    """
    This structure provides information about a pair of mismatched lines.
    
    :var mismatchedAlignment: the pair of mismatched BOM lines
    :var mismatchedproperties: the indices of mismatched properties
    """
    mismatchedAlignment: BOMLinePair = None
    mismatchedproperties: List[int] = ()


@dataclass
class BOMLinePair(TcBaseObj):
    """
    This structure provides a pair of BOM lines.
    
    :var source: the source BOM line
    :var target: the target BOM line
    """
    source: BOMLine = None
    target: BOMLine = None


@dataclass
class AlignmentCheckResponse(TcBaseObj):
    """
    This structure provides response of the call.
    
    :var propertyList: the property list used in this alignment check
    :var results: the mismatched BOM lines
    :var serviceData: Partial errors
    """
    propertyList: List[str] = ()
    results: List[AlignmentCheckResult] = ()
    serviceData: ServiceData = None


@dataclass
class AlignmentCheckResult(TcBaseObj):
    """
    This structure provides information about the alignment check in a given scope.
    
    :var scope: the pair of scope BOM lines
    :var mismatches: the mismatched BOM lines
    """
    scope: BOMLinePair = None
    mismatches: List[AlignmentMismatches] = ()
