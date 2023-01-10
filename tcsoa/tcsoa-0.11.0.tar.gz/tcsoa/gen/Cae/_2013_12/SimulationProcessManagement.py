from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ConfigurationContext
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InputObjectData(TcBaseObj):
    """
    Structure containing the input object on which tool needs to be launched and the configuration information which
    needs to be applied in case the input object is of type ItemRevision.
    
    :var object: The business object on which configured tool needs to be launched.
    :var configCntx: Object holding the configuration information that needs to be applied on the input object if it is
    of type ItemRevision.
    """
    object: BusinessObject = None
    configCntx: ConfigurationContext = None


@dataclass
class InputObjectsStructure2(TcBaseObj):
    """
    Structure containing selected input object data on which pre-configured simulation tool needs to be launched.
    
    :var inputObjectDataVec: Array of InputObjectData on which pre-configured simulation tool needs to be launched.
    """
    inputObjectDataVec: List[InputObjectData] = ()
