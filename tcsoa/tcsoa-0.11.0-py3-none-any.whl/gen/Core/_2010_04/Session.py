from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2008_03.Session import FavoritesList
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetShortcutsResponse(TcBaseObj):
    """
    A structure contains Favorites hierarchy and map of LHNSectionComponent given section names.
    
    :var favorites: A hierarchical Favorites tree structure list that contains all the favorites containers and
    favorites objects for the current session user. The Favorites section can be populated only if FavoritesSection is
    passed as a key in the input map to this API.
    :var shortcuts: A map structure that includes the given section name and corresponding content of the section. The
    key is the name of the section and the value is the LHNSectionComponent structure, which has a Teamcenter object
    and a nonTeamcenter object . The preferred keys allowed in this map are MyFavorites, HistoryList,
    QuickLinksSection,  MyQuicklinkSection etc.
    :var serviceData: ServiceData contains any failures and Teamcenter objects  wrapped in LHNSecitonComponents and
    default properties. The following errors may be encountered:
    1700 (error code):  The preference cannot be found.
    515024 ( error code): The given tag does not exist in the database or is not a persistent object tag.
    """
    favorites: FavoritesList = None
    shortcuts: LHNSectionComponentsMap = None
    serviceData: ServiceData = None


@dataclass
class LHNNonTcObjectSectionComponent(TcBaseObj):
    """
    The sections in the left hand navigation can contain either Teamcenter objects or non-Teamcenter 
    objects.
    Sections which contain Teamcenter objects are 'Open Items', 'History', etc and the sections which 
    contain non-Teamcenter bjects are 'I Want To' section. This structure in turn contains the
    LHNSectionComponentDetails which maintains additional information pertaining to the object.
    
    Example:
    Consider that the 'I Want To' section in the left hand navigation contains the command 'Create an 
    Item'.
    This structure would contain the below details in the LHNSectionComponentDetails.
    Key = ActionName, Value = newItemAction
    Key = DisplayName, Value = Create an Item
    Key = CommandID, Value = com.teamcenter.rac.newItem
    
    Consider that the 'QuickLinkSection' section in the left hand navigation contains the command 'like 
    a 'home folder'  in quick links.
    key = QuickLinkId
    
    
    :var nonTcObjects: Non Tc Objects like Home, folder etc
    """
    nonTcObjects: LHNSectionComponentDetails = None


@dataclass
class LHNSectionComponents(TcBaseObj):
    """
    The purpose of this structure is to give a single name to 'LHNNonTcObjectSectionComponentMap' and 
    'LHNTcObjectSectionComponentMap' which is section component. Each section component is puted into 
     LHNSectionComponentsMap.
    
    LHNNonTcObjectSectionComponentMap: It is a map for nontcobject , whose key is 'int' using for 
    placeHolder and value are NonTcObjectSection.
    
    LHNTcObjectSectionComponentMap key is for placeholder and value as tccomponent object.
    
    :var nonTcObjects: nonTcObjects
    :var tcObjects: tcObjects
    """
    nonTcObjects: LHNNonTcObjectSectionComponentMap = None
    tcObjects: LHNTcObjectSectionComponentMap = None


@dataclass
class LHNTcObjectSectionComponent(TcBaseObj):
    """
    The purpose of this structure is to represents the Teamcenter object details, Which is get use in 
    the Left Hand Navigation pane of the clients. Which is either a tcobject or non tcobject.
    
    Teamcenter::BusinessObject  This is a TcComponent which have all the bussiness property of  
    teamcenter object.
    e.g Items in History section, Items in OpenItemSection etc.
                 
    LHNSectionComponentDetails It must contain the detail information about the nonTcObject at which 
    place we have to insert and what are the action name and display name  associated with it.
    e.g LHNSectionComponentDetails('Action Name',  newItemAction );
        LHNSectionComponentDetails('Display Name',  Create an Item );
    
    
    :var tcObject: Specifies the Teamcenter object
    :var details: Additional details of the section component.
    """
    tcObject: BusinessObject = None
    details: LHNSectionComponentDetails = None


@dataclass
class MultiPreferenceResponse2(TcBaseObj):
    """
    The structure used to get the returned preference
    
    :var data: The successful Object ids, partial errors and failures
    :var preferences: List of ReturnedPreferences2 Object
    """
    data: ServiceData = None
    preferences: List[ReturnedPreferences2] = ()


@dataclass
class ReturnedPreferences2(TcBaseObj):
    """
    This is the structure which is used to define the information for one preference.
    
    :var scope: The scope of the preference, "all", "site", "user", "group", or "role".
    :var category: The variable to hold the category name
    :var description: The variable to hold the description
    :var prefType: Preference Type
    :var isArray: Preference Array
    :var isDisabled: Is the preference disabled
    :var values: The value of the preference
    :var name: The name of the preference
    """
    scope: str = ''
    category: str = ''
    description: str = ''
    prefType: int = 0
    isArray: bool = False
    isDisabled: bool = False
    values: List[str] = ()
    name: str = ''


"""
This map is used to maintain the place holder for nonTcObject.

LHNNonTcObjectSectionComponent is a structure in which there is a map element haveing information 
about the non TcObject. Such as for 'IWanToSection' it is 'Action Name' 'Display Name' and 
commandID.
 
Example:                                  
LHNNonTcObjectSectionComponentMap( 1, 'create an item')
LHNNonTcObjectSectionComponentMap( 2, 'create a Dataset')
"""
LHNNonTcObjectSectionComponentMap = Dict[int, LHNNonTcObjectSectionComponent]


"""
This is a map containing the details of a object in the left hand navigation.
The keys vary based on the type of the section name.
Example
For IWantToSection keys are ActionName, DisplayName,  commandID.

Action Name = newItemAction
Display Name = Create an Item
LHNSectionComponentDetails('Action Name',  newItemAction );
LHNSectionComponentDetails('Display Name',  Create an Item );
LHNSectionComponentDetails('Display Name',  com.teamcenter.rac.newItem )
"""
LHNSectionComponentDetails = Dict[str, str]


"""
In this map key is the SectionName and value is the LHNSectionComponent structure, which have 
TcObject and nonTcObject as it's element.
The prefered Keys allowed in this map are MyFavorites, HistoryList, QuickLinksSection, 
MyQuicklinkSection etc.
  
Example   LHNSectionComponentsMap ('HistorySection' , SectionComponent structure for History 
Section)

"""
LHNSectionComponentsMap = Dict[str, LHNSectionComponents]


"""
This is a input parameter to the getShortcuts operation. This is a map where the key represents the 
section name in the left hand navigation 
and the value represents the preference name that needs to be looked up.
Valid key value pairs are:
Key = QuickLinksSection, Value = MyTeamcenterQuicklinksection
Key = FavoritesSection, value = My Favorites

Valid keys in the map are
QuickLinksSection, HistorySection, FavoritesSection, IWantToSection, OpenItemsSection.
Valid values against these keys in the map are
MyFavorites, HistoryList, QuickLinksSection, MyQuicklinkSection, OpenItemSection etc.

"""
LHNShortcutInputs = Dict[str, str]


"""
This map is used to maintain the place holder for the sectioncomponent.Which is either a tcObject or 
nontcobject.


LHNTcObjectSectionComponent It is simply a collection of TcObject or nonTcObject.
             
Example:
LHNTcObjectSectionComponentMap(0, any tcobject or  nontcobject);
LHNTcObjectSectionComponentMap(1, any tcobject or  nontcobject);
"""
LHNTcObjectSectionComponentMap = Dict[int, LHNTcObjectSectionComponent]
