from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class AnalyticsData(TcBaseObj):
    """
    This contains an instance of AnalyticsData required to hold software analytics data for logged in user.
    
    :var isDataCollectionEnabled: This is obtained from the value for preference TC_ProductExcellenceProgram to
    indicate the software analytics should be enabled or not.  If data collection is off then the server will not send
    any other information and an instance of AnalyticsData will be empty, this value is set to false.
    :var useInternalServer: This is used to indicate where the analytice data is logged. If true, send analytics data
    to analytics internal server; otherwise, send analytics data to analytics cloud based server (AWS).
    :var burstTimeInterval: The time interval at which software analytics data will be sent to the SA server. This
    value is a recommendation since all clients cannot implement a burst interval other than zero.
    :var analyticsExtraInfo: Map of key\value pairs ( string\string). These are optional fields sent by the server and
    will be sent to the analytics site as is. The intent is that these fields, if present, will be sent to the Software
    Analytics server retaining their name and value. Callers of this SOA should NOT use or rely on any values in this
    map. If isDataCollectionEnabled, this map will likely be empty. Any values passed in this map must have prior
    approval by Siemens Legal team.
    """
    isDataCollectionEnabled: bool = False
    useInternalServer: bool = False
    burstTimeInterval: int = 0
    analyticsExtraInfo: AnalyticsExtraInfo = None


@dataclass
class TCSessionAndAnalyticsInfo(TcBaseObj):
    """
    Data structure representing the current user's Teamcenter session information and software analytics related data.
    
    :var userSession: The user session object.
    :var extraInfoOut: Map of key/value pairs (string/string). Some/all/none of the following keys and values are
    returned, depending on what was passed in extraInfoIn:
    &bull;    TCServerVersion                  The version of the Teamcenter server.
    &bull;    hasProjects                "true" or "false" depending on whether the user has projects
    &bull;    AWC_StartupPreferences      This contains list of preferences to be retrieved at startup by the Active
    workspace client from the Teamcenter server.
    &bull;    AWC_Startuptypes        List of types to be loaded at start up by the Active workspace client from the
    Teamcenter server.
    &bull;    DefaultDateFormat        The default date format required.
    &bull;    AWServerVersion        The version of the Active workspace
    &bull;    typeCacheLMD        UTC formatted last modified date for Type cache Dataset.
    &bull;    WorkspaceId        Workspace Id for current Active workspace user session.
    &bull;    AWC_PostLoginStages    This preference represents list of post login stages in the sequence to be
    displayed in the Active worksapace after successful authentication.
    :var analyticsData: This contains an instance of AnalyticsData required to hold software analytics data for logged
    in user.
    :var serviceData: The service data.
    """
    userSession: BusinessObject = None
    extraInfoOut: SessionExtraInfo = None
    analyticsData: AnalyticsData = None
    serviceData: ServiceData = None


"""
Map of key/value pairs (string, string). Some, all, or none of the following keys and values are returned, depending on what was passed in extraInfoIn
&bull;    TCServerVersion                  The version of the Teamcenter server.
&bull;    hasProjects                "true" or "false" depending on whether the user has projects
&bull;    DefaultDateFormat        The default date format required.
&bull;    typeCacheLMD        UTC formatted last modified date for Type cache Dataset.
"""
SessionExtraInfo = Dict[str, str]


"""
Map of key\value pairs ( string\string). These are optional fields sent by the server and will be sent to the analytics site as is. The intent is that these fields, if present, will be sent to the Software Analytics server retaining their name and value. Callers of this SOA should NOT use or rely on any values in this map. If isDataCollectionEnabled, this map will likely be empty. Any values passed in this map must have prior approval by Siemens Legal team.
"""
AnalyticsExtraInfo = Dict[str, str]
