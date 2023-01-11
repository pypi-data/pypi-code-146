from __future__ import annotations

from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PrecalRoutineInfo(TcBaseObj):
    """
    The PrecalRoutineInfo structure is used give the results of the service that calculates percentage on target
    
    :var routineDate: Date of execution of the events
    :var percentOnTarget: Percentage of attributes on target for that day
    """
    routineDate: str = ''
    percentOnTarget: float = 0.0


@dataclass
class PrecalRoutineInfoResponse(TcBaseObj):
    """
    The PrecalRoutineInfoResponse structure is used to return the calculated values
    
    :var result: A vector of PrecalRoutineInfo structures. Each structure corresponding to a date in the given date
    time range
    """
    result: List[PrecalRoutineInfo] = ()
