from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LaunchInfoInput(TcBaseObj):
    """
    The structure contains the needed information to retrieve the launch URL for a Teamcenter Dataset for access Office
    Online Server.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var obj: The Teamcenter BusinessObject. The BusinessObject need to resolve to an Office dataset type such as
    MSWordX.
    :var action: The WOPI action name. The action name is defined by WOPI protocol.
    :var extraInfo: A map (string, string) for extra name value pair information. This is intended for future use.
    """
    clientId: str = ''
    obj: BusinessObject = None
    action: str = ''
    extraInfo: KeyValueMap = None


@dataclass
class LaunchInfoOutput(TcBaseObj):
    """
    The structure contains the information needed to access the Dataset from the Office Online Server.
    
    :var clientId: The unmodified value from the LaunchInfoInput.clientId. This can be used by the caller to indentify
    this data structure with the source input data.
    :var oosUrlString: The launch URL to access the Dataset from the Office Online Server.
    :var accessToken: Teamcenter access token.
    :var accessTtl: Teamcenter access token time to live.
    """
    clientId: str = ''
    oosUrlString: str = ''
    accessToken: str = ''
    accessTtl: str = ''


@dataclass
class LaunchInfoOutputResponse(TcBaseObj):
    """
    The structure contains a list of LaunchInfoOutput and the Service Data.
    
    :var outputs: A list of LaunchInfoOutput.
    :var serviceData: The Service Data.
    """
    outputs: List[LaunchInfoOutput] = ()
    serviceData: ServiceData = None


"""
String to String Map. It is extra information for the request.
"""
KeyValueMap = Dict[str, str]
