from __future__ import annotations

from tcsoa.gen.BusinessObjects import Discipline
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDisciplineResponse(TcBaseObj):
    """
    This structure is the object returned by this operation. It holds the Discipline object found and ServiceData
    object.
    
    :var discipline: The discipline object found with the given name.
    :var serviceData: The object which holds the possible error in the search of the discipline.
    """
    discipline: Discipline = None
    serviceData: ServiceData = None
