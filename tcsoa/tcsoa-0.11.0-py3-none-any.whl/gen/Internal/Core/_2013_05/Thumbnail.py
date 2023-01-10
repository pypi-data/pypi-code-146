from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List


@dataclass
class ThumbnailFileTicketsResponse2(TcBaseObj):
    """
    Return type consisiting of list of thumbnail file tickets of the input list of business objects.
    
    :var thumbnailFileTicketsMap: A map of business object and thumbnail FMS tickets (business object/vector(string)).A
    business object may have multiple thumbnails.
    :var serviceData: The list of partial errors.
    """
    thumbnailFileTicketsMap: ThumbnailFileTicketsMap = None
    serviceData: ServiceData = None


"""
A map of  the business object and the thumbnail file tickets.
"""
ThumbnailFileTicketsMap = Dict[BusinessObject, List[str]]
