from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AddMultiToolCutterResponse(TcBaseObj):
    """
    Output response object for AddMultiToolCutter action.
    
    :var serviceData: Service data that can contain error descriptions.
    
    :var strNewICOUID: UID of newly created ICO.
    :var strNewCutterID: Cutter ID associated with new ICO.
    """
    serviceData: ServiceData = None
    strNewICOUID: str = ''
    strNewCutterID: str = ''


@dataclass
class DeleteMultiToolCutterResponse(TcBaseObj):
    """
    Output response object for DeleteMultiToolCutter action.
    
    :var serviceData: Service data that can contain error descriptions.
    :var lastICOUID: UID of the last ICO. This will be empty when there are multiple ICOs connected with the
    ItemRevision. It will contain the ICO UID when the ItemRevision is connected with a single ICO and all the other
    ICOs were deleted.
    """
    serviceData: ServiceData = None
    lastICOUID: str = ''
