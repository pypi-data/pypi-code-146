from __future__ import annotations

from tcsoa.gen.BusinessObjects import Item, WorkspaceObject, ItemRevision
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class LDSelectedInputInfo(TcBaseObj):
    """
    Launch definition selected input information.
    
    :var id: The id can be an Item, an ItemRevision business object, a Dataset business object or a markup control
    object.  It is required.  If empty, invalid object error is returned
    :var item: Related item to input id.
    :var itemRev: Related ItemRevision to the input id.
    :var controlObj: Related markup control object (related to the markup through MarkupContextRelation). The control
    object is determined based on the business object constant Fnd0MarkupControlObject set to true.
    :var requestMode: There are 3 possible values for this element. MARKUP, VIEW, EDIT.  Example, MARKUP is for
    View/Markup action.  VIEW and EDIT is for View/Open action on an office dataset business object.
    :var additionalInfo: This is the map of additional information in the form of key value pair strings.  This can be
    empty.
    """
    id: WorkspaceObject = None
    item: Item = None
    itemRev: ItemRevision = None
    controlObj: WorkspaceObject = None
    requestMode: str = ''
    additionalInfo: KeyValueMap = None


@dataclass
class LaunchDefinitionResponse(TcBaseObj):
    """
    Return data for the laucnh definition.
    
    :var xmlLaunchDef: For the ViewMarkup and OfficeOpen operations, the launch definition xml string.
    For the AWOfficeOpen operation, the launch definition file ticket string.
    :var svcData: The Service Data. Partial errors and failures are updated and returned through this object
    """
    xmlLaunchDef: str = ''
    svcData: ServiceData = None


@dataclass
class ServerInfo(TcBaseObj):
    """
    Server Information.
    
    :var protocol: http or iiop (Protocol type for connection to the server). http is for four tier and iiop is for two
    tier deployment
    :var hostPath: The host path
    :var serverMode: Single character. 2 for two tier. 4 for four tier.  This is to support the VIS legacy ITK
    :var useTccs: If client uses Single Sign On(SSO) to connect to server, then this should be set to true. Otherwise,
    false
    :var useSso: If client uses SSO to connect to server, then this should be set to true. Otherwise, false
    :var tccsEnvironment: Teamcenter client communication system (TCCS) environment name
    :var ssoInfo: SSO information
    :var additionalInfo: This is the map of additional information in the form of key value pair strings
    """
    protocol: str = ''
    hostPath: str = ''
    serverMode: str = ''
    useTccs: bool = False
    useSso: bool = False
    tccsEnvironment: str = ''
    ssoInfo: SsoInfo = None
    additionalInfo: KeyValueMap = None


@dataclass
class SessionInfo(TcBaseObj):
    """
    Session information.
    
    :var descriminator: Client Server session discriminator to connect existing specified session.
    :var additionalInfo: This is the map of additional information in the form of key value pair strings.
    """
    descriminator: str = ''
    additionalInfo: KeyValueMap = None


@dataclass
class SsoInfo(TcBaseObj):
    """
    The information for SSO.
    
    :var loginServiceUrl: The login service Uniform resource locator (Url).
    :var appId: The application Id of the Teamcenter server in this Single Sign On(SSO) environment.
    """
    loginServiceUrl: str = ''
    appId: str = ''


@dataclass
class UserAgentDataInfo(TcBaseObj):
    """
    User application information.
    
    :var userApplication: Client who initiates the VVI launch. The VVI file contains the information necessary for the
    stand alone viewer to open the file.
    :var userAppVersion: Version of the client.
    :var additionalInfo: This is the map of additional information in the form of key value pair strings.
    """
    userApplication: str = ''
    userAppVersion: str = ''
    additionalInfo: KeyValueMap = None


"""
Key value map.
"""
KeyValueMap = Dict[str, str]
