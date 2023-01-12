from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SearchOrders(TcBaseObj):
    """
    This is to provide the relation search order and dataset type search order preferences
    
    :var relationSearchOrder: The relation search order to look for to get the thumbnail file.
    :var datasetTypeSearchOrder: The dataset types order to look for to get the thumbnail file in a particular relation.
    """
    relationSearchOrder: List[str] = ()
    datasetTypeSearchOrder: List[str] = ()


@dataclass
class ThumbnailFileTicketsResponse(TcBaseObj):
    """
    Return type consisiting of list of thumbnail file tickets in the order of the input list of business objects.
    
    :var thumbnailFileTickets: List of thumbnail file tickets in the same order as input business objects.
    :var serviceData: This will contain the business objects for which thumbnail file ticket is not generated in the
    form of partial errors.
    """
    thumbnailFileTickets: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class UpdateThumbnailInputs(TcBaseObj):
    """
    This structure stores user inputs for updating thumbnail.
    
    :var isNone: True value is to specify no source for thumbnail. Type icon will be used as thumbnail.
    :var isAutoSelect: True value lets system determine source for thumbnail.
    :var thumbnailSource: User specified source for thumbnail. This object should be of type Dataset.
    """
    isNone: bool = False
    isAutoSelect: bool = False
    thumbnailSource: BusinessObject = None
