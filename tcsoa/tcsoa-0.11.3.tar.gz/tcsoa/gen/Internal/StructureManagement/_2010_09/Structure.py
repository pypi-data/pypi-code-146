from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReSequenceParameter(TcBaseObj):
    """
    This strucure provides a set of input values for the re-sequence action
    
    :var bomLines: the selected BOM lines to re-sequence find numbers of their  children
    :var startNumber: the start number of the new Find Number
    :var increNumber: the incremental between find numbers
    :var recursive: recursively re-sequence the lines and their children
    :var ignoreFlows: re-sequence the structure ignoring the Pert flows
    """
    bomLines: List[BOMLine] = ()
    startNumber: int = 0
    increNumber: int = 0
    recursive: bool = False
    ignoreFlows: bool = False
