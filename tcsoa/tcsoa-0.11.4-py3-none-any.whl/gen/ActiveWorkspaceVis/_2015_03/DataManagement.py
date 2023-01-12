from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OptionInfo(TcBaseObj):
    """
    This structure contains the value of the for a given launch file option and a flag indicating whether the option
    key name and value should be written to the launch file.
    
    :var optionValue: The value for the given option.
    :var includeInLaunchFile: A flag indicating whether the option key/value pair should also be written into the
    launch file.
    """
    optionValue: str = ''
    includeInLaunchFile: bool = False


@dataclass
class ServerInfo(TcBaseObj):
    """
    This structure holds the basic information for Teamcenter Visualization to connect to the server.
    
    :var protocol: A required parameter referencing the protocol type for connection to the server. Use http for
    standard 4 tier connections, and iiop for 2 tier deployments.
    :var hostpath: A required parameter referencing the URL to connect to the server.
    :var servermode: A required parameter referencing the servermode that controls how the connection to the server is
    made: 2 for two tier. 4 for four tier.
    :var serverAdditionalInfo: An optional parameter referencing the additional information of the server in form of
    key/value pair (if any).
    """
    protocol: str = ''
    hostpath: str = ''
    servermode: int = 0
    serverAdditionalInfo: KeyValueMap = None


@dataclass
class SessionInfo(TcBaseObj):
    """
    This structure holds the information about the session information of the client application from where the launch
    operation was initiated.
    
    :var sessionDescriminator: Client/Server session discriminator to connect to existing specified session.  This
    allows the viewer application to share an existing server process session with the client that initiated the
    launch. If this is not specified, the viewer will present a login prompt.
    :var sessionOptions: Map of option names to OptionInfo structures. These options are used to control the creation
    of the launch information in some way.
    
    Current options include:
    
    "UseTransientVolume" - "True" or "False"
       Determines how the service is to return the launch information. If "True" then the launch information is written
    to a file in the transient volume and a FMS ticket is returned in the ticket field of the LaunchInfoResponce
    structure. If "False" then the launch information is written to a string and that string is placed into the
    vviStrBufferOutputMap field of the LaunchInfoResponce structure. In the later case, the key name to be used is
    found in the "ClientId" option that is now required.
    
    :var sessionAdditionalInfo: An optional parameter referencing the additional information of the session in form of
    key/value pair (if any).
    """
    sessionDescriminator: str = ''
    sessionOptions: OptionsMap = None
    sessionAdditionalInfo: KeyValueMap = None


@dataclass
class UserAgentDataInfo(TcBaseObj):
    """
    This structure holds the information about the client application that initiated the launch.
    
    :var userApplication: An optional parameter referencing the client who initiates the launch.
    :var userAppVersion: An optional parameter referencing the version of the client that initiated launch.
    :var userAdditionalInfo: An optional parameter referencing the additional information of client application in form
    of key/value pair (if any).
    """
    userApplication: str = ''
    userAppVersion: str = ''
    userAdditionalInfo: KeyValueMap = None


@dataclass
class IdInfo(TcBaseObj):
    """
    This structure holds information about the object(s) that will be launched to the viewer. It may contain addtional
    option information that can affect how the VVI is to be generated.
    
    :var launchedObject: The business object to be laucnhed. Launched object could be of type Item, ItemRevision,
    Dataset, BOMView, BOMViewRevision or Awb0ProductContextInfo. The business object will be resolved by the server in
    some cases (e.g. Item or ItemRevision launch) to a directly launchable visualization object (such as a DirectModel
    Dataset or BOMViewRevision).
    :var item: The parent or containing Item of the launched object.  If this is not provided, the server will attempt
    to identify the parent if it can. If the parent information cannot be identified, this will not result in an error
    condition. The parent Item information will simply not be passed to the visualization client, which could affect
    what features are available in the client.
    :var itemRev: The parent or containing ItemRevision of the launched object. If this is not known, the server will
    attempt to identify the parent if it can. If the parent information cannot be identified, this will not result in
    an error condition. The parent ItemRevision information will simply not be passed to the visualization client,
    which could affect what features are available in the client.
    :var occurrencesList: The list of selected occurrences being launched. These occurrences may be of type BOMLine or
    Awb0Element. When this vector is non-empty then the launchedObject field of the IdInfo structure must contain an
    object that defines the configuration state for the occurrences. For example, the configuration object is of type
    Awb0ProductContextInfo when the occurrences are of type Awb0Element. The configuration object is of type BOMWindow
    when the occurrences are of type BOMLine.
    :var createOptions: Map of option names to OptionInfo structures. These options are used to control the creation of
    the launch information in some way.
    
    Current options include:
    
    "CreateVisSC" - "True" or "False"
       Informs the service to create a VisStructureContext object based on the laucnhedObject and occurrenceList field
    of the IdInfo structure.
    
    "OVERRIDE_VisDoc_Type" - some replacement string
       Directs the service to replace the value of the VisDoc_Type key in the launch file with the specified string.
    
    "TransientDoc" - "True" or "False"
       Indicates whether the launched object is to be considered transient by the viewer. Transient objects are
    normally deleted when the viewer is finished with the document used to open the launched object.
    
    "Operation" - "open", "insert", "merge", "interop"
       Informs the viewer on what type of launch operation is being requested.
    
    "OperationStructure" - "Dynamic", "Static", "Preference", "Ask"
       Informs the viewer on what type of structure launch is being requested.
    
    "UseTransientVolume" - "True" or "False"
       Determines how the service is to return the launch information. If "True" then the launch information is written
    to a file in the transient volume and a FMS ticket is returned in the ticket field of the LaunchInfoResponce
    structure. If "False" then the launch information is written to a string and that string is placed into the
    vviStrBufferOutputMap field of the LaunchInfoResponce structure. In the later case, the key name to be used is
    found in the "ClientId" option that is now required.
    
    "ClientId" - a unique string used to identify this call to the service.
       Is a required option when the "TransientVolume" option is "False".
    
    "Client" - string used to identify the client calling this service
        Currently the only value being recognized is "AW", which indicates that ActiveWorkspace is the desired client
    viewer.
    
    
    :var idAdditionalInfo: This is a generic mechanism for putting additional key/value pairs into the output launch
    information. This data is considered opaque to the service and the key/value pairs are simply output into the VVI
    launch information.
    """
    launchedObject: BusinessObject = None
    item: Item = None
    itemRev: ItemRevision = None
    occurrencesList: List[BusinessObject] = ()
    createOptions: OptionsMap = None
    idAdditionalInfo: KeyValueMap = None


@dataclass
class LaunchInfoResponse(TcBaseObj):
    """
    The output response structure for the createLaunchInfo () operation.
    
    :var ticket: Holds a FMS transient file ticket for the launch information written to the VVI file.
    This member is valid only when the "UseTransientVolume" option from the IdInfo input structure was set to "True".
    :var vviStrBuffersOutputMap: The map of clientId string to the VVI launch information string buffer(string/string).
    This member is valid only when the "UseTransientVolume" option from the IdInfo input structure was set to "False".
    Also requires the "ClientId" option from the IdInfo input structure to be present and set to non-zero length
    string. The value of the "ClientId" option is used as the key to this map.
    :var serviceData: SOA Framework object containing error information. In cases where objects cannot be launched,
    error message, codes will be mapped to respective object id in the list of partial errors.
    """
    ticket: str = ''
    vviStrBuffersOutputMap: VVIStringBufferOutputMap = None
    serviceData: ServiceData = None


"""
Map of key-value name pairs, each of type std::string.
"""
KeyValueMap = Dict[str, str]


"""
A map of option key names to OptionInfo structures. These options are used to control the creation of the launch file in some way. 

"""
OptionsMap = Dict[str, OptionInfo]


"""
A map containing client ids or additional Teamcenter object UID  and vviStringBuffer as key/value pairs.
"""
VVIStringBufferOutputMap = Dict[str, str]
