from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0Element, Awb0ProductContextInfo
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OccurrenceSelection(TcBaseObj):
    """
    This operation is used to save all the occurrences selected by the user in the Active Content Experience
    application of the Active Workspace Client. The selection data is stored in the Awb0SubsetData object related to
    the Awb0BookmarkData object.
    
    :var contextProduct: The Awb0ProductContextInfo object in the context of which the selections were made in the
    Active Workspace.
    :var listOfSelectedOccurrences: List of the Awb0Element objects that were selected in the Active Workspace Client.
    """
    contextProduct: Awb0ProductContextInfo = None
    listOfSelectedOccurrences: List[Awb0Element] = ()
