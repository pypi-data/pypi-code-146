from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LicAdminInput(TcBaseObj):
    """
    Key pair used to perform a licensing action.
    
    :var featureKey: The product as listed in the license file (e.g. teamcenter_author).
    :var licensingAction: The desired action. Valid values are:
    
    "init"                    Connect to the license server.
    "release"                Checks in the feature key back to the license server.
    "check"                Checks if the feature key exists in the license file.
    "exit"                    Checks in all open feature keys and disconnects from the license server.
    "get"                    Checks if the feature key exists in the license file  and then checks out the feature key.
    "init_get"            Connects to the license server (if not already connected, checks if the feature key exists in
    the license file  and then checks out the feature key.
    "release_exit"        Checks the feature key back to the license server and disconnects from the license server.
    """
    featureKey: str = ''
    licensingAction: str = ''
