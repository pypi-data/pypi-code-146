from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import PartialErrors
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class Feature(TcBaseObj):
    """
    Information for a single client cache feature.
    
    :var name: Name of the feature,  ClientMetaModel or TextData.
    :var cacheTickets: A map of Dataset names and FMS tickets (string/string) for each Dataset that makes up the client
    cache feature.
    """
    name: str = ''
    cacheTickets: CacheTickets = None


@dataclass
class LoginResponse(TcBaseObj):
    """
    Basic information about the server and  partial errors are returned when the authentication is successful but
    requested 'role' or 'locale' is not supported.
    
    :var serverInfo: Name/Value pairs (string/string) of data related to the server. The following keys are valid:
    - Version         The version of the Teamcenter server.
    - HostName     The name of the Teamcenter server's host machine.
    - LogFile         The full path of the Teamcenter server's log file.
    - Locale          The locale of this session.
    - TcServerID    The unique ID of this instance of the Teamcenter server.
    
    
    :var partialErrors: Partial errors or warnings resulting from the login attempt.
    """
    serverInfo: ServerInfo = None
    partialErrors: PartialErrors = None


@dataclass
class ClientCacheInfo(TcBaseObj):
    """
    Data for the requested cached features.
    
    :var features: The list of  features.
    :var partialErrors: Errors are return for features that do not exist or if there are other errors in getting data
    for a given service. The client ID in the partial error will be that of the feature name.
    """
    features: List[Feature] = ()
    partialErrors: PartialErrors = None


@dataclass
class Credentials(TcBaseObj):
    """
    The credentials needed to authenticate a user.
    
    :var user: The user's Teamcenter user name.
    :var password: The user's Teamcenter password or SSO token.
    :var group: The group ID for this session. If blank (""), the user's default group is assumed.
    :var role: The role the user is performing in the group. If blank (""), the user's default role in the group is
    assumed.
    :var locale: The locale to be used by the Teamcenter server process for this session. If blank (""), the server's
    default locale will be used.
    :var descrimator: Client defined identifier for this session. This argument is ignored when the client application
    is deployed in a 2Tier environment (IIOP communication).
    """
    user: str = ''
    password: str = ''
    group: str = ''
    role: str = ''
    locale: str = ''
    descrimator: str = ''


"""
Name/Value pairs of data related to the server. The following keys are valid:  Version, HostName, LogFile, Locale, TcServerID.
"""
ServerInfo = Dict[str, str]


"""
A map of FMS file tickes, the key is the name of the file, and the value is the FMS ticket.
"""
CacheTickets = Dict[str, str]
