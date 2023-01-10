from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0LicenseServer
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LicenseServerInput(TcBaseObj):
    """
    The 'LicenseServerInput' structure contains information for properties such as license server name, host, port,
    protocol and failover servers, for a given license server.  A license server location is defined by its host and
    port.
    
    :var licenseServer: The license server object to be updated.
    :var licenseServerName: The input name of the license server.
    :var failoverLicenseServers: The list of license server objects used as failover license servers.
    :var hostName: The host name of the license server
    :var portNumber: The port number of the license server.  This is used in combination with the hostName to connect
    to the license server.
    :var protocol: The protocol used when connecting to the license server.  The protocol can only be "TCP/IP".
    """
    licenseServer: Fnd0LicenseServer = None
    licenseServerName: str = ''
    failoverLicenseServers: List[Fnd0LicenseServer] = ()
    hostName: str = ''
    portNumber: int = 0
    protocol: int = 0
