from __future__ import annotations

from tcsoa.gen.BusinessObjects import ReleaseStatus, Effectivity
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReleaseStatusEffectivityInput(TcBaseObj):
    """
    This structure contains effectivities to be attached to the  release status.
    
    :var status: The ReleaseStatus for which Effectivity objects are to be added or removed.
    :var effectivities: A list of Effectivity objects which are added or removed  to/from status.
    :var addOrRemove: Indicates whether to add or remove Effectivity(s). 
    When true, Effectivity is added.Otherwise,  Effectivity is removed.
    """
    status: ReleaseStatus = None
    effectivities: List[Effectivity] = ()
    addOrRemove: bool = False
