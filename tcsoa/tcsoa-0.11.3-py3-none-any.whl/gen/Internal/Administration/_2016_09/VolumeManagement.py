from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanVolume
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class VolumeInfoResponse(TcBaseObj):
    """
    This operation returns the list of accessible volumes, default volume and  default local volume for the given user
    and group.
    
    :var accessibleVolumes: A list of accessible volumes for the given user and group combination
    :var defaultVolume: Default volume for  the given  user and group combination
    :var defaultLocalVolume: Default local volume for the given user and group combination
    :var serviceData: The Teamcenter Services structure used to return status of the operation
    """
    accessibleVolumes: List[ImanVolume] = ()
    defaultVolume: ImanVolume = None
    defaultLocalVolume: ImanVolume = None
    serviceData: ServiceData = None
