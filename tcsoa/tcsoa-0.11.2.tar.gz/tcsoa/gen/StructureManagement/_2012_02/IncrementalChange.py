from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class BomLineInfo(TcBaseObj):
    """
    This structure holds the source and the target BOMLine objects.
    
    :var sourceLine: The source BOMLine.
    :var targetLine: The target BOMLine.
    """
    sourceLine: BOMLine = None
    targetLine: BOMLine = None
