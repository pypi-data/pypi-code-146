from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PerformanceJournalLevelResponse(TcBaseObj):
    """
    Return structure for the current level of performance journaling.
    
    :var level: 0 - off, normal journaling
    1 - version 1 performance journaling
    2 - version 2 performance journaling
    """
    level: int = 0
