from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetBriefcaePreviewDataResponse(TcBaseObj):
    """
    GetBriefcaePreviewDataResponse structure defines the response from GetBriefcaePreviewData operation. It contains
    FMS tickets or preview data of the old briefcase file, the new briefcase file and the delta briefcase file. It
    provides the errors if SOA fails too.
    
    :var oldBriefcasePreviewDataFMSTicket: FMS ticket of the preview data from the briefcase specified in
    oldBriefcaseFMSTicket or oldBriefcaseUID which can be used to download from server to client. The preview data
    include the structure in the briefcase and can be displayed on the client.
    :var newBriefcasePreviewDataFMSTIcket: FMS ticket of the preview data from the briefcase specified in
    newBriefcaseFMSTicket or newBriefcaseUID which can be used to download from server to client. The preview data
    include the structure in the briefcase and can be displayed on the client.
    :var deltaBriefcasePreviewFMSTicket: FMS ticket of the delta briefcase preview data from the two input briefcases
    specified in (oldBriefcaseFMSTicket or oldBriefcaseUID) and (newBriefcaseFMSTicket or newBriefcaseUID)   which can
    be used to download from server to client. The delta preview data include the difference of the structures between
    the two input briefcases and can be displayed on the client.
    :var oldBriefcasePreviewData: The preview data from the briefcase specified in oldBriefcaseFMSTicket or
    oldBriefcaseUID. The preview data include the structure in the briefcase and can be displayed on the client.
    :var newBriefcasePreviewData: The preview data from the briefcase specified in newBriefcaseFMSTicket or
    newBriefcaseUID. The preview data include the structure in the briefcase and can be displayed on the client.
    :var deltaBriefcasePreviewData: The delta preview data from the two input briefcases specified in
    (oldBriefcaseFMSTicket or oldBriefcaseUID) and (newBriefcaseFMSTicket or newBriefcaseUID). The delta preview data
    include the difference of the structures between the two input briefcases and can be displayed on the client.
    :var serviceData: Service data contains the errors if the operation fails.
    """
    oldBriefcasePreviewDataFMSTicket: str = ''
    newBriefcasePreviewDataFMSTIcket: str = ''
    deltaBriefcasePreviewFMSTicket: str = ''
    oldBriefcasePreviewData: List[NamesAndValues] = ()
    newBriefcasePreviewData: List[NamesAndValues] = ()
    deltaBriefcasePreviewData: List[NamesAndValues] = ()
    serviceData: ServiceData = None


@dataclass
class NamesAndValues(TcBaseObj):
    """
    NamesAndValues structure represents a generic name-value pair
    
    :var elementName: The name of the name-value pair
    :var elementValues: The values of the name-values pair.
    """
    elementName: str = ''
    elementValues: List[str] = ()


@dataclass
class CheckBriefcaseLicenseResponse(TcBaseObj):
    """
    Response for Briefcase license check operation. Contains true if multisite_server and tc_briefcase license are
    available.
    
    :var licenseExists: True if both "mulitsite_server" and "tc_briefcase" licenses are available.
    :var serviceData: This contains the status of the operation.
    """
    licenseExists: bool = False
    serviceData: ServiceData = None
