from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.BusinessObjects import TC_Project
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LoadProjectDataForUserResponse(TcBaseObj):
    """
    Object that holds applicable projects.
    
    :var applicableProjects: List of TC_project objects found.
    :var serviceData: A  standard  ServicData.
    """
    applicableProjects: List[TC_Project] = ()
    serviceData: ServiceData = None
