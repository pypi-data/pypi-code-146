from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class Action(TcBaseObj):
    """
    Contains the action to perform when the Awp0Tile is clicked in the Gateway.  If URL is populated then urlParams may
    optionally be populated depending on the Tile configuration.  If commandId is populated, then commandArgs may
    optionally be populated depending on the Awp0Tile configuration.
    
    If the Awp0TileTemplate object&rsquo;s awp0ActionType property is 0, 1 or 2 then the url property is populated.  If
    the Awp0TileTemplate object&rsquo;s awp0ActionType property is 3, then the commandId property is populated.
    
    :var actionType: Identifies the action type.   Possible values are 0 (default), 1 (external reference), 2 (static
    resource), 3 (command).
    :var url: The URL to navigate to in the client if commandId is undefined.
    :var commandId: The command ID to execute if URL is undefined.
    :var actionParams: Optional command parameters.  The names and values for this field come directly from the
    awp0Params property on the Awp0Tile object.  These params are an unconstrained list of name/value pairs.
    
    The syntax for awp0Params on the Awp0Tile object is in the format of
    <name>=<value>;<name2>=<value2>;<name3>=<value3>...  Where name/value pairs are delimited by semicolon.
    
    The awp0Params entry is parsed, and each name/value pair is added to a string map, where key is the parameter name,
    and the value is the parameter value.
    
    For example:  awp0Params may contain an entry such as "refresh=true;filter=POM_application_object.owning_user".  
    
    The resulting map would contain the following parsed pairs:
    
    "refresh":"true",
    "filter":"POM_application_object.owning_user"
    """
    actionType: int = 0
    url: str = ''
    commandId: str = ''
    actionParams: ActionParamMap = None


@dataclass
class GetCurrentUserGateway2Response(TcBaseObj):
    """
    GetCurrentUserGateway2Response viewmodel to be presented by the client.  The response consists of  TileGroup
    objects which contain Tile objects in the order they should be presented in the Gateway.   Each Tile object
    contains a reference to the Awp0GatewayTileRel so the Tile may be operated on.
    
    :var serviceData: Contains partial error information.
    :var tileGroups: List of TileGroup to be presented in the Gateway.
    """
    serviceData: ServiceData = None
    tileGroups: List[TileGroup] = ()


@dataclass
class PinObjectInput(TcBaseObj):
    """
    PinObjectInput contains the UID of the BusinessObject to pin, as well as optional data such as actionParams and
    templateId.   This information is used to create the Awp0Tile object in the server, and relate it to an 
    Awp0TileTemplate.
    
    :var uid: The UID of the object to pin.
    :var actionParams: Optional parameters to set on the Awp0Tile object.
    
     The syntax for actionParams is in the format of <name>=<value>;<name2>=<value2>;<name3>=<value3>...  Where
    name/value pairs are delimited by semicolon.
    :var templateId: Optional templateId to set on the Awp0Tile object. The value shall point to a valid template ID
    which is defined by property, awp0TemplateId  on an Awp0TileTemplate object.   If the template ID isn&rsquo;t
    valid, then no template is set on the Awp0Tile object.  If the value is an empty string, then the
    Awp0PinnedObjectTemplate ID is used by default.
    """
    uid: str = ''
    actionParams: str = ''
    templateId: str = ''


@dataclass
class SaveViewModelEditAndSubmitResponse2(TcBaseObj):
    """
    Structure containing saveViewModelEditAndSubmit2 operation response.
    
    :var workflowProcess: Workflow template object for each input object that will be created after it is submitted to
    workflow successfully.
    :var serviceData: Partial errors are returned in the Service Data.
    :var viewModelObjectsJsonString: viewModelObjectsJsonString A JSON string that contains the ViewModelObject
    structures which provide information about the editable status of the properties passed in the input. This
    information can be used by client to show which properties as editable. The ViewModelObjectJsonString is also used
    in loadViewModelForEditing2 and getDeclarativeStyleSheet2 operation which displays the ViewModelObject.
    """
    workflowProcess: List[BusinessObject] = ()
    serviceData: ServiceData = None
    viewModelObjectsJsonString: List[str] = ()


@dataclass
class Tile(TcBaseObj):
    """
    Contains all the information relevant to presenting and operating on the Tile object in the UI.
    
    :var displayName: The display name of the Tile object.
    :var themeIndex: The integer that indicates the theme for color of the Tile. Valid values are presented via a list.
    0: light, 1 medium, 2: highlight, 3: alternate.
    :var icons: Defines the primary and secondary icons to be presented in the Gateway.
    :var action: The action to execute when the Tile is clicked.
    :var tileSize: Size of the Tile. Valid values are 0, 1, or 2 (small, wide, or large).Null value not allowed.
    :var styleOverride: This property indicates any CCS classes to override the default styling of the Tile.
    :var orderNumber: The order number for which this Tile should be presented in the Gateway.
    :var content: Defines the live content to be displayed on a Tile.  Each entry is a line on the Tile.
    :var isProtected: Indicates whether a Tile may be removed from a TileGroup.
    :var validSizes: Sizes of the Tile that this template supports. Can be used to limit available sizes for a tile
    type - if blank, all sizes are allowed. Valid values are presented via a list. 0: small, 1: wide, 2: large.
    :var relUID: The UID of the Awp0GatewayTileRel object  which describes the Tile/TileGroup information.
    """
    displayName: str = ''
    themeIndex: int = 0
    icons: TileIcons = None
    action: Action = None
    tileSize: int = 0
    styleOverride: str = ''
    orderNumber: int = 0
    content: List[ContentEntry] = ()
    isProtected: bool = False
    validSizes: List[int] = ()
    relUID: str = ''


@dataclass
class TileGroup(TcBaseObj):
    """
    Contains the groupName to be presented in the UI, as well as the vector of Tile objects to be presented in the UI. 
    The Tile objects are ordered based on awp0OrderNo property on the Awp0GatewayTileRel object.
    
    :var groupName: The name of the TileGroup.
    :var tiles: The Tile objects to be presented in the TileGroup.
    """
    groupName: str = ''
    tiles: List[Tile] = ()


@dataclass
class TileIcons(TcBaseObj):
    """
    This class represents the icons to be presented for a Tile object.
    
    :var primaryIcon: The primary icon to display on a Tile. Valid values are a file ticket, a static icon name, or
    "__TYPEICON__".  The value of "__TYPEICON__" indicates that the type hierarchy must be walked into order to
    determine the icon to present in the UI.  The 1st icon that it finds in the type hierarchy is the one to use.
    :var secondaryIcon: The secondary icon to display on a Tile. Valid values are a file ticket, a static icon name, or
    "__TYPEICON__". The value of "__TYPEICON__" indicates that the type hierarchy must be walked into order to
    determine the icon to present in the UI.  The 1st icon that it finds in the type hierarchy is the one to use.
    :var typeHierarchy: The type hierarchy for the Tile, if the Tile represents a pinned object. It is empty otherwise.
    If the value of primaryIcon or secondaryIcon is "__TYPEICON__" then this field is used by the client to determine
    which icon to present on the Tile.
    """
    primaryIcon: str = ''
    secondaryIcon: str = ''
    typeHierarchy: List[str] = ()


@dataclass
class UnpinObjectsResponse(TcBaseObj):
    """
    UnpinObjectsResponse contains the gateway viewmodel to be presented by the client.  The response consists of 
    TileGroup objects which contain Tile objects in the order they should be presented in the Gateway. Each Tile object
    contains a reference to the Awp0GatewayTileRel so the Tile may be operated on.
    
    :var tileGroups: List of TileGroup to be presented in the Gateway.
    :var serviceData: Contains partial error information.
    """
    tileGroups: List[TileGroup] = ()
    serviceData: ServiceData = None


@dataclass
class UpdateTilesResponse(TcBaseObj):
    """
    UpdateTilesResponse contains the gateway viewmodel to be presented by the client. The response consists of
    TileGroup objects which contain Tile objects in the order they should be presented in the Gateway. Each Tile object
    contains a reference to the Awp0GatewayTileRel so the Tile may be operated on.
    
    :var tileGroups: List of TileGroup objects to be presented in the Gateway.
    :var serviceData: Contains partial error information.
    """
    tileGroups: List[TileGroup] = ()
    serviceData: ServiceData = None


@dataclass
class ContentEntry(TcBaseObj):
    """
    Contains live Tile information to be presented on Gateway Tile objects, how many items are in the user&rsquo;s
    inbox, for example.
    
    :var contentName: The name to be presented
    :var contentValue: The value to be presented
    """
    contentName: str = ''
    contentValue: str = ''


"""
Contains optional command information to execute after the url or command ID is executed.
"""
ActionParamMap = Dict[str, str]
