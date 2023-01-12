from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0LicenseServer
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LicenseServerInput2(TcBaseObj):
    """
    The 'LicenseServerInput2' structure contains information for properties such as license server name, host, port,
    protocol, failover servers and multiple license servers, for a given license server. A license server location is
    defined by its host and port.
    
    :var licenseServerName: The input name of the license server.
    :var hostName: The host name of the license server.
    :var licenseServerType: The type of the license server.  Valid values are: "RLS" (Regular License Server) and "ILS"
    (Integration License Server).
    :var portNumber: The port number of the license server.  This is used in combination with the hostName to connect
    to the license server.
    :var protocol: The protocol used when connecting to the license server.  The protocol can only be "TCP/IP".
    :var licenseServer: The license server object to be updated.
    :var failoverLicenseServers: A list of license server objects used as failover license servers.
    :var multipleLicenseServers: A list of license server objects used as multiple license servers.
    """
    licenseServerName: str = ''
    hostName: str = ''
    licenseServerType: str = ''
    portNumber: int = 0
    protocol: int = 0
    licenseServer: Fnd0LicenseServer = None
    failoverLicenseServers: List[Fnd0LicenseServer] = ()
    multipleLicenseServers: List[Fnd0LicenseServer] = ()
