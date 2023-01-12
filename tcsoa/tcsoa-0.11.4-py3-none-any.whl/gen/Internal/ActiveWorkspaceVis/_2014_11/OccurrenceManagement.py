from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile, Awb0ProductContextInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SaveVisBookmarkInfoResponse(TcBaseObj):
    """
    This structure contains a list of Awb0ProductContextInfo instances,  ImanFile object and the read file ticket to
    the ImanFile object  that contains the visualization bookmark information that was saved.
    
    :var visBookmarkInfos: A list of 'VisBookmarkInfo' structures.
    :var serviceData: The Service Data through which the errors are communicated to the client.
    """
    visBookmarkInfos: List[VisBookmarkInfo] = ()
    serviceData: ServiceData = None


@dataclass
class SaveVisBookmarkInput(TcBaseObj):
    """
    This structure contains  the  Awb0ProductContextInfo, and transient file ticket for the bookmark file that was
    uploaded to the transient volume.
    
    :var productContextInfo: Awb0ProductContextInfo for which the visualization bookmark information is updated.
    :var visBookmarkTransientFileTicket: FMS transient file ticket for a file which was uploaded to the transient
    volume.
    """
    productContextInfo: Awb0ProductContextInfo = None
    visBookmarkTransientFileTicket: str = ''


@dataclass
class VisBookmarkInfo(TcBaseObj):
    """
    This structure contains  the  Awb0ProductContextInfo, and its visualization bookmark information. The visualization
    bookmark information is contained in the file for which the FMS read ticket is being returned.
    
    :var productContextInfo: Awb0ProductContextInfo for which the visualization bookmark information was saved.
    :var visBookmarkFile: ImanFile object containing the visualization bookmark information that was saved.
    :var visBookmarkFileReadTicket: FMS read ticket for the ImanFile object.
    """
    productContextInfo: Awb0ProductContextInfo = None
    visBookmarkFile: ImanFile = None
    visBookmarkFileReadTicket: str = ''


@dataclass
class GetVisBookmarkInfoResponse(TcBaseObj):
    """
    This structure contains a list of Awb0ProductContextInfo instances,  ImanFile object and the read file ticket to
    the ImanFile object  that contains the visualization bookmark information.
    
    :var visBookmarkInfos: A list of 'VisBookmarkInfo' structures.
    :var serviceData: The Service Data through which the errors are communicated to the client.
    """
    visBookmarkInfos: List[VisBookmarkInfo] = ()
    serviceData: ServiceData = None
