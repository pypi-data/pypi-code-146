from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Item, ItemRevision
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class IdInfo2(TcBaseObj):
    """
    A Teamcenter object structure that contains the related information that need to be visualized in Teamcenter
    Visualization.
    
    :var object: The business object to be laucnhed. Launched object could be Item, ItemRevision, Dataset,
    BOMView_Revision, BOMView. The business object will be resolved by the server in some cases (e.g. Item or
    ItemRevision launch) to a directly launchable visualization object (such as a DirectModel Dataset or
    BOMViewRevision).
    :var item: The parent or containing Item of the launched object (object).  If this is not known, the server will
    attempt to identify the parent if it can.  If the parent information cannot be identified, this will not result in
    an error condition, it simply will not pass the information to the visualization client which for some cases may
    affect what features are available in the client.
    :var itemRev: The parent or containg ItemRevision of the launched object (id). If this is not known, the server
    will attempt to identify the parent if it can.
    :var operation: The type of launch action the viewer is instructed to perform (e.g. open, insert, merge, etc).  If
    left empty, it will default to open. This controls the action the viewer will perform when it opens the object. The
    following actions are supported: 
    1. open - Open the object in a new window. 
    2. Insert - Insert the object into the current window that has focus.
    3. merge - Attempt to merge a pruned product structure with one that is already open (and has focus) if it can.
    4. Interop -Present a dialog that lets the user select the launch action.
    :var idAdditionalInfo: This is a generic mechanism for putting additional key value pairs into the VVI file that
    control viewer launch behavior.
    :var structureMode: This specifies the structure launch mode to open the structure object in Teamcenter
    Visualization. The different structure launch modes that are supported are:
    1. Dynamic - When this mode is used, it launches the dynamic structure in Teamcenter Visualization.
    2. Static - When this mode is used, it launches the static structure in Teamcenter Visualization.
    3. Preference - This specifies that Teamcenter Visualization preference is used to launch the structure.
    4. Ask - This mode of launch asks user to specify the launch mode.
    :var clientId: This is the UID of the launched object against which the VVI string buffer will be stored.
    """
    object: BusinessObject = None
    item: Item = None
    itemRev: ItemRevision = None
    operation: str = ''
    idAdditionalInfo: KeyValueMap2 = None
    structureMode: str = ''
    clientId: str = ''


@dataclass
class LaunchInfoResponse(TcBaseObj):
    """
    A response structure for the createLaunchInfo () operation.
    
    :var ticket: The VVI file ticket to the transient volume.
    This member is valid only if  hasTransientVolume flag is set to true in SessionInfo2.
    
    :var vviStrBuffersOutputMap: The map of clientId to the VVI string buffer(stirng/string). This member is valid only
    if hasTransientVolume flag is set to false in SessionInfo2.
    :var serviceData: The object containing error information. In cases where objects can't be launched, error message,
    codes will be mapped to respective object id in the list of partial errors.
    """
    ticket: str = ''
    vviStrBuffersOutputMap: VVIStringBufferOutputMap = None
    serviceData: ServiceData = None


@dataclass
class SessionInfo2(TcBaseObj):
    """
    Object containing session information for the viewer to connect to the session.  Includes the session discriminator
    and any other additional session relevant key value pair.
    
    :var sessionDescriminator: Client-Server session discriminator to connect to an existing tcserver session.  This
    allows the viewer to share an existing tcserver.exe session with the launching client. This should be the same as
    the SessionDescriminator argument of the SessionService.login operaiton.  If this empty string, the viewer will
    present a login prompt if it does not already have a session established.
    :var sessionAdditionalInfo: The additional information related to session to put in the VVI file/buffer in the form
    of key value pair (key (string) = value(/stirng)).(Refer to Teamcenter Visualization VVI documentation on
    acceptable additional information).
    :var hasTransientVolume: If true the VVI information is returned as a file ticket to the transient volume,
    otherwise it is returned directly as a string.
    """
    sessionDescriminator: str = ''
    sessionAdditionalInfo: KeyValueMap2 = None
    hasTransientVolume: bool = False


"""
Map of key-value name pair.
"""
KeyValueMap2 = Dict[str, str]


"""
A map containing client ids or additional Teamcenter object UID  and vviStringBuffer as key/value pairs.
"""
VVIStringBufferOutputMap = Dict[str, str]
