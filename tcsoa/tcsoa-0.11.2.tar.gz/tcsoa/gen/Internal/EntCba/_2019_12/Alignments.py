from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0Element
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PartDesOccAlignmentData(TcBaseObj):
    """
    The input parameter for performing Alignment or Unalignments
    
    :var partOccurrence: Awb0Element object representing the Part Occurrence
    :var designOccurrence: Awb0Element object representing the Design Occurrence
    :var partContext: Awb0Element object representing the Part context. The value can be NULL.
    :var designContext: Awb0Element object representing the Design context. The value can be NULL.
    """
    partOccurrence: Awb0Element = None
    designOccurrence: Awb0Element = None
    partContext: Awb0Element = None
    designContext: Awb0Element = None
