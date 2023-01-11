from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GenerateAndEvaluateStructureResponse(TcBaseObj):
    """
    Response structure for generateAndEvaluateStructure method.
    
    :var xpathToValuesMap: The map of xpath to the values obtained by evaluating this xpath against the generated
    plmxml.
    :var serviceData: partial failures are returned - along with object ids for each plmxml data could not be generated.
    :var transientFileTicket: If an xml is generated on server - input does not specify an existing plmxml or invalid
    filename - a fileticket is returned for that file.
    """
    xpathToValuesMap: XpathToValuesMap = None
    serviceData: ServiceData = None
    transientFileTicket: str = ''


"""
Map of xpath string to the values obtained by running this against the plmxml file.
"""
XpathToValuesMap = Dict[str, List[str]]
