from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Item, ItemRevision
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class IdInfo(TcBaseObj):
    """
    This structure holds the information about the objects that will be launched to the viewer.
    
    :var id: A required parameter that references the object to be launched. If needed, launched object will be
    resolved by the server to a launch able object.
    :var item: An optional object reference of the Item containing launch able object. If this is not known, the server
    will attempt to identify the parent if it can.
    :var itemRev: An optional object reference of the ItemRevision containing launchable object. If this is not known,
    the server will attempt to identify if it can.
    :var operation: An optional parameter references the type of launch action. This controls the action the viewer
    will perform when it opens the object. The actions supported are one of following: 'Open', 'Insert', 'Merge' or
    'Interop'.  'Open' will open the object in a new window.  'Insert' will insert the object into the current window
    that has focus.  'Merge' will attempt to merge a pruned product structure with one that is already open if it can. 
    'Interop' will present a dialog that lets the user select the launch action.
    :var idAdditionalInfo: An optional parameter referencing the additional information of launched objects in form of
    key/value pair (if any).
    """
    id: BusinessObject = None
    item: Item = None
    itemRev: ItemRevision = None
    operation: str = ''
    idAdditionalInfo: KeyValueMap = None


@dataclass
class ServerInfo(TcBaseObj):
    """
    This structure holds the basic information for Teamcenter Visualization to connect to the server.
    
    :var protocol: A required parameter referencing the protocol type for connection to the server. Use http for
    standard 4 tier connections, and iiop for 2 tier deployments.
    :var hostpath: A required parameter referencing the URL to connect to the server.
    :var servermode: A required parameter referencing the servermode that controls how the connection to the server is
    made: 2 for two tier. 4 for four tier.
    :var serverAdditionalInfo: An optional parameter referencing the additional  information of the server in form of
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
    :var sessionAdditionalInfo: An optional parameter referencing the additional information of the session in form of
    key/value pair (if any).
    """
    sessionDescriminator: str = ''
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
class VVITicketsResponse(TcBaseObj):
    """
    Used to return information from the 'createLaunchFile' operation. The structure holds the 'serviceData' object and
    a FMS transient read ticket corresponding to the launch file (VVI or VFZ).
    
    :var ticket: The FMS transient read ticket of the launch file (VVI or VFZ) generated for the objects that can be
    launched. The file will be placed in the transient file volume and the caller will need to download it from there
    with the ticket sent by the service.
    :var serviceData: SOA Framework object containing error information. In cases where objects cannot be launched,
    error message, codes will be mapped to respective object id in the list of partial errors.
    """
    ticket: str = ''
    serviceData: ServiceData = None


"""
Map of key-value name pair.
"""
KeyValueMap = Dict[str, str]
