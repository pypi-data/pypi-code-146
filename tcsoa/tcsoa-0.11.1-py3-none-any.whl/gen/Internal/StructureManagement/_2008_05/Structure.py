from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class BOMLinePair(TcBaseObj):
    """
    This structure provides a pair of BOM lines.
    
    :var source: the source BOM line
    :var target: the target BOM line
    """
    source: BOMLine = None
    target: BOMLine = None
