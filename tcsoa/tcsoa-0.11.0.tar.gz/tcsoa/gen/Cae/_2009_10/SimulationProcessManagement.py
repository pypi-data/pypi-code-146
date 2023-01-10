from __future__ import annotations

from tcsoa.gen.BusinessObjects import ItemRevision
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InputObjectsStructure(TcBaseObj):
    """
    Structure containing selected input ItemRevision objects on which pre-configured simulation tool needs to be
    launched.
    
    :var inputItemRevisions: Array of selected ItemRevision objects on which pre-configured simulation tool needs to be
    launched.
    """
    inputItemRevisions: List[ItemRevision] = ()
