from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CompareResultsCursor(TcBaseObj):
    """
    CompareResultsCursor is a cursor that is returned for use in subsequent calls to get next page of results.
    
    :var startReached: If true, the first page of the results has been reached.
    :var endReached: If true, the last page of the results has been reached.
    :var startIndex: The Cursor start position for the result returned so far.
    :var endIndex: The Cursor end position for the result returned so far.
    :var pageSize: The maximum number of results that can be returned in one service call.
    :var isForward: If true scrolling is done in forward direction.
    """
    startReached: bool = False
    endReached: bool = False
    startIndex: int = 0
    endIndex: int = 0
    pageSize: int = 0
    isForward: bool = False
