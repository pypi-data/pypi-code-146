from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, Item, ReleaseStatus, ItemRevision
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReleaseStatusEffectivityInput(TcBaseObj):
    """
    The information required to create effectivity on a release status
    
    :var releaseStatus: The release status for which to set effectivity
    :var effectivityInfoInput: A structure to hold effectivity input info
    """
    releaseStatus: ReleaseStatus = None
    effectivityInfoInput: EffectivityInfoInput = None


@dataclass
class CreateOccEffectivityInput(TcBaseObj):
    """
    The information required to create occurrence effectivity for a list of BOMLine 
    
    :var bomLines: The BOMLine objects for which to add effectivity
    :var effectivityInfoInput: A structure to hold effectivity info
    :var isShared: True to share effectivity among BOMLine objects
    False to not share effectivity among BOMLine objects
    """
    bomLines: List[BOMLine] = ()
    effectivityInfoInput: EffectivityInfoInput = None
    isShared: bool = False


@dataclass
class EffectivityInfoInput(TcBaseObj):
    """
    A structure to hold effectivity info
    
    :var effectivityId: Effectivity ID
    :var endItem: Effectivity end Item
    :var endItemRev: Effectivity end ItemRevision
    :var unitRangeText: Effectivity unit range, a valid range of unit numbers. Always specified in the context of the
    end Item to which the units apply. It can be a discrete,noncontinuous range.
    :var dateRange: The array of effectivity date range,a valid range of dates. 
    -    Open range,for example,from 05 January onward.
    -    Closed range,for example,from 01 January to 30 April.
    
    :var openEndedStatus: Effectivity open ended status, 0 for EFFECTIVITY_closed, 1 for EFFECTIVITY_open_ended, 2 for
    FFECTIVITY_stock_out
    :var isProtected: True to add new range to any existing ranges
    False to overwrite existing ranges
    """
    effectivityId: str = ''
    endItem: Item = None
    endItemRev: ItemRevision = None
    unitRangeText: str = ''
    dateRange: List[datetime] = ()
    openEndedStatus: int = 0
    isProtected: bool = False
