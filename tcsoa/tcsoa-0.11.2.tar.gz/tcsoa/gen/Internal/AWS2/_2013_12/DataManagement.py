from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, UserSession
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetStyleSheetClassificationData(TcBaseObj):
    """
    The associated classification trace and classification object associated with the specified Business Object.
    
    :var classificationObject: The Classification object to which this object has been associated.
    :var classificationTrace: The classification trace for this classification assignment.
    """
    classificationObject: BusinessObject = None
    classificationTrace: List[str] = ()


@dataclass
class GetStyleSheetDatasetInfo(TcBaseObj):
    """
    Contains the style sheet dataset info.
    
    :var datasetLastSaveDate: Contains the last save date(lsd) of the dataset
    :var datasetContent: The content of the dataset.
    """
    datasetLastSaveDate: datetime = None
    datasetContent: str = ''


@dataclass
class GetTCSessionInfoResponse(TcBaseObj):
    """
    Data structure representing the different current user's Teamcenter session information.
    
    :var userSession: The Teamcenter user session information.
    :var serviceData: The service data.
    :var hasProjects: Indicates whether this user has projects.
    """
    userSession: UserSession = None
    serviceData: ServiceData = None
    hasProjects: bool = False


@dataclass
class GetTCSessionInfoResponse3(TcBaseObj):
    """
    Data structure representing the current user's Teamcenter session information.
    
    :var userSession: The Teamcenter user session object
    :var extraInfoOut: Map of key/value pairs (string/string). Some/all/none of the following keys and values are
    returned, depending on what was passed in extraInfoIn: - TCServerVersion : The version of the Teamcenter server. -
    hasProjects : "true" or "false" depending on whether the user has projects
    :var serviceData: The service data
    """
    userSession: UserSession = None
    extraInfoOut: ExtraInfo = None
    serviceData: ServiceData = None


"""
Map of extra information
"""
ExtraInfo = Dict[str, str]
