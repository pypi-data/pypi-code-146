from __future__ import annotations

from tcsoa.gen.BusinessObjects import Group, ImanVolume, POM_imc, TC_WorkContext, User, Role, TC_Project
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetTCSessionInfoResponse(TcBaseObj):
    """
    Data structure representing the different current user's Teamcenter session information.
    
    :var serverVersion: The version of the server.
    :var transientVolRootDir: Path to the root folder of the transient volume.
    :var site: The site object for this session
    :var bypass: True if bypass is enabled.
    :var journaling: True if journaling is enabled.
    :var appJournaling: True if application journaling is enabled.
    :var secJournaling: True if sec journaling is enabled.
    :var admJournaling: True if administration journaling is enabled.
    :var privileged: True if the user is privileged.
    :var isPartBOMUsageEnabled: True if the Part BOM Usage is enabled.
    :var isSubscriptionMgrEnabled: True if the Subscription Manager is enabled.
    :var textInfos: textInfos
    :var isInV7Mode: True if the server is operating in V7 mode.
    :var extraInfo: Map of kev/value pairs (string/string).The following keys are returned:
    - TcServerIDUnique  ID of this Teamcenter server instance.
    - systemTypeType  of server, always 'Teamcenter'.
    - syslogFile  The absolute path of the system log file (.syslog) on the server host.
    - Hostname  The host name of the machine hosting the Teamcenter server process.
    - TCServerLocale The locale of the Teamcenter server.
    - currentOrganization The UID of the user's current Organization. The business object instance is in the
    ServiceData plain list
    - loginGroupOrganization  The UID of the user's login Organization. The business object instance is in the
    ServiceData plain list
    - currentChangeNotice  The UID of the user's current ChangeNotice The business object instance is in the
    ServiceData plain list
    - locationCodePref  The preferred location code.
    - displayCurrentCountryPage  True if the current country selection page is needed.
    
    
    :var serviceData: serviceData
    :var moduleNumber: This element is not to be used anymore and always returns a -1.
    :var user: The User object for this session.
    :var group: The Group object for this session.
    :var role: The Role object for this session.
    :var tcVolume: The ImanVolume object for this session.
    :var project: The Project object for this session.
    :var workContext: The WorkContext object for this session.
    """
    serverVersion: str = ''
    transientVolRootDir: str = ''
    site: POM_imc = None
    bypass: bool = False
    journaling: bool = False
    appJournaling: bool = False
    secJournaling: bool = False
    admJournaling: bool = False
    privileged: bool = False
    isPartBOMUsageEnabled: bool = False
    isSubscriptionMgrEnabled: bool = False
    textInfos: List[TextInfo] = ()
    isInV7Mode: bool = False
    extraInfo: ExtraInfo = None
    serviceData: ServiceData = None
    moduleNumber: int = 0
    user: User = None
    group: Group = None
    role: Role = None
    tcVolume: ImanVolume = None
    project: TC_Project = None
    workContext: TC_WorkContext = None


@dataclass
class MultiPreferencesResponse(TcBaseObj):
    """
    Multiple Preferences Response
    
    :var preferences: List of Returned Preferences
    :var serviceData: The successful Object ids, partial errors and failures
    """
    preferences: List[ReturnedPreferences] = ()
    serviceData: ServiceData = None


@dataclass
class ReturnedPreferences(TcBaseObj):
    """
    Info for one preference
    
    :var name: The preference name.
    :var scope: The scope of the preference, "all", "site", "user", "group", or "role".
    :var values: The values for the perference.
    """
    name: str = ''
    scope: str = ''
    values: List[str] = ()


@dataclass
class ScopedPreferenceNames(TcBaseObj):
    """
    Info for getPreferences
    
    :var scope: The scope of the preference, "all", "site", "user", "group", or "role".
    :var names: The names of the perferences.
    """
    scope: str = ''
    names: List[str] = ()


@dataclass
class TextInfo(TcBaseObj):
    """
    Text Information
    
    :var realName: Real Name
    :var displayName: Display Name
    """
    realName: str = ''
    displayName: str = ''


"""
ExtraInfo
"""
ExtraInfo = Dict[str, str]
