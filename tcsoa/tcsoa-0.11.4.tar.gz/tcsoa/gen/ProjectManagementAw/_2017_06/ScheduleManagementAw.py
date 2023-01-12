from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import Schedule
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MasterScheduleCreateInput(TcBaseObj):
    """
    Input structure containing information to create the master Schedule.
    
    :var name: Name of the Master Schedule.
    :var description: Descrption of the master Schedule.
    :var schedulesToInsert: A list of Schedule to be inserted into the master Schedule.
    :var timeZone: Specifies Time Zone for the master Schedule.
    """
    name: str = ''
    description: str = ''
    schedulesToInsert: List[Schedule] = ()
    timeZone: str = ''
