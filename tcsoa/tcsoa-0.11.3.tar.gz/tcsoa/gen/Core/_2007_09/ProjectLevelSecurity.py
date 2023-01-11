from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TC_Project
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AssignedOrRemovedObjects(TcBaseObj):
    """
    This structure holds the projects and workspace objects.
    
    :var projects: A list of TC_Project objects  to which the the given set of workspace objects need to be assigned or
    from which the objects need to be removed.
    :var objectToAssign: A list of objects that needs to be assigned ( added ) to the given projects.
    :var objectToRemove: A list of objects that needs to be removed  from the given projects.
    """
    projects: List[TC_Project] = ()
    objectToAssign: List[BusinessObject] = ()
    objectToRemove: List[BusinessObject] = ()
