from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetPreferencesAtLocationsResponse(TcBaseObj):
    """
    Structure returned by the 'getPreferencesAtLocation' operation.
    
    :var data: Partial errors. Each partial error will contain the index of the related input data.
    :var responses: The preference description and category for the locations OOTB (out-of-the-box), Overlay or Site.
    In the other cases, those strings will be empty.
    """
    data: ServiceData = None
    responses: List[CompletePreference] = ()


@dataclass
class GetPreferencesResponse(TcBaseObj):
    """
    Contains the preference information (value and description if requested), as well as any potential partial errors.
    
    :var data: Contains the partial errors in the same order as in the input list.
    :var response: A list of complete preference information.
    Each structure holds all the preference definition ('PreferenceDefinition' structure) and its values
    ('PreferenceValue' structure).
    """
    data: ServiceData = None
    response: List[CompletePreference] = ()


@dataclass
class ImportPreferencesAtLocationDryRunIn(TcBaseObj):
    """
    A structure that contains all the parameters for the import dry run operation.
    
    :var location: Location where to simulate the import.
    :var fileTicket: Ticket of the input XML file in the transient volume uploaded by the client
    :var categoryNames: Vector of category names to be considered for import. No value means import all categories
    """
    location: PreferenceLocation = None
    fileTicket: str = ''
    categoryNames: List[str] = ()


@dataclass
class ImportPreferencesAtLocationDryRunResponse(TcBaseObj):
    """
    Response from importPreferencesAtLocationDryRun operation.
    
    :var serviceData: A ServiceData structure.
    The following partial errors will be returned:
     * An error 1759 will be returned if the preference name is empty. 
     * An error 1760 will be returned if the preference name is invalid ("*" for instance). 
     * An error 1700 will be returned if the preference does not exist.
     * An error 1751 will be returned if the specified object information does not correspond to any user, role or
    group.
     * An error 1752 will be returned if both an object and a location are specified for an entry.
     * An error 1753 will be returned if the specified location is invalid.
     * An error 1725 will be returned if the logged-in user does not have the requested permission to carry-out the
    operation.
     * An error 1728 will be returned in case the protection scope of the preference prevents a creation of one
    instance at the specified location.
    :var dbImpactedPreferences: List of preferences in the database that would be impacted by the import.
    :var conflictingPreferencesFromFile: Llist of preferences from the input file, for which conflict will arise. 
    Conflicts are cases in which either the preference already exists in the database and is different, or the
    preference does not exist in the database yet.
    """
    serviceData: ServiceData = None
    dbImpactedPreferences: List[CompletePreference] = ()
    conflictingPreferencesFromFile: List[CompletePreference] = ()


@dataclass
class ImportPreferencesAtLocationsIn(TcBaseObj):
    """
    A structure that contains all the parameters for the import operation.
    
    :var locations: A list of structures defining where the preferences are to be imported.
    :var fileTicket: Ticket of the input XML file in the transient volume uploaded by the client.
    :var categoryNames: List of category names to be considered for import. 
    No value means import all categories.
    :var importAction: Specifies what to do when the preference already exists.
    Valid values are:
    - "SKIP": to skip the import of this preference.
    - "OVERRIDE": to override the preference value at this location with the value specified in the input file.
    - "MERGE": to append the preference value from the input file to the preference value at the location. This is only
    possible if the preference is a multi-valued preference. Otherwise, this will result in the "SKIP" action for this
    preference. 
    
    
    If a wrong value is provided, the operation will revert to using the "SKIP" mode.
    """
    locations: List[PreferenceLocation] = ()
    fileTicket: str = ''
    categoryNames: List[str] = ()
    importAction: str = ''


@dataclass
class PreferenceDefinition(TcBaseObj):
    """
    Contains all the preference definition details.
    
    :var name: The name of the preference.
    :var category: The name of the category where the preference is sorted.
    A category is a logical group of preferences.
    :var description: The description associated with the preference.
    :var type: Type of the preference.
    Values are: 
    - 0 : String preference
    - 1: Logical preference
    - 2: Integer preference
    - 3: Double preference
    - 4: Date preference
    
    
    :var isArray: Determines if the preference is multi-valued.
    :var isDisabled: Determines if the preference is disabled. From Teamcenter 11.6.0, this is not supported. It is set
    to false always.
    :var protectionScope: Determines the protection scope of the preference, which is who is the lowest person (in the
    organization) who is allowed to provide values.
    Valid values are User, Role, Group, Site, System.
    :var isEnvEnabled: Determines if the value can be taken from an environment variable.
    :var isOOTBPreference: Determines if the preference is defined out-of-the-box. From Teamcenter 11.6.0, this is not
    supported since there is no differentiation between OOTB and non OOTB preferences. It is set to false always.
    """
    name: str = ''
    category: str = ''
    description: str = ''
    type: int = 0
    isArray: bool = False
    isDisabled: bool = False
    protectionScope: str = ''
    isEnvEnabled: bool = False
    isOOTBPreference: bool = False


@dataclass
class PreferenceLocation(TcBaseObj):
    """
    Defines where the preference is to be retrieved. 
    This structure is used by different operations with different possible values for the location parameter.
    
    :var object: Object where the preferences will be retrieved. This can be a User, Role or Group.
    This value can only be used if the location string is empty.  
    
    :var location: Name of the location.
    This value can only be specified if the object is not specified.
    """
    object: BusinessObject = None
    location: str = ''


@dataclass
class PreferenceResponseWithFileTicket(TcBaseObj):
    """
    Response that also contains a file ticket, which usage differs upon the operation returning it.
    
    :var serviceData: A ServiceData structure.  
    It will contain errors at indexes where errors have occurred. Error details will vary according to the calling
    operation, and it will be specified in its description.
    :var fileTicket: A ticket of a file in the transient volume uploaded by the client.
    The content of the file will depend on the calling operation, and it will be specified in its description.
    """
    serviceData: ServiceData = None
    fileTicket: str = ''


@dataclass
class PreferenceValue(TcBaseObj):
    """
    Contains the preference value and its location. 
    This structure is used by different operations with different possible values for the location parameter.
    
    :var values: The values associated with this preference.
    :var valueOrigination: Defines where the preference values are coming from.
    Valid values are:
    - "COTS": The value is the one defined by Siemens.
    - "Overlay":  The COTS value has been altered.
    - "Group": The value is defined at the group level.
    - "Role": The value is defined at the role level.
    - "User": The value is defined at the user level.
    - "Env": The value is coming from an environment variable.
    
    """
    values: List[str] = ()
    valueOrigination: str = ''


@dataclass
class PreferencesAtLocationIn(TcBaseObj):
    """
    Defines a list of preferences at a provided location.
    
    :var location: The desired location of the requested preferences.
    :var preferenceNames: A list of desired preference names.
    If the list is empty or its first element is "*", all the preferences for the specified locations (and only for
    preference instances at this location) are returned.
    """
    location: PreferenceLocation = None
    preferenceNames: List[str] = ()


@dataclass
class SetPreferences2In(TcBaseObj):
    """
    Structure of preference name and values.
    
    :var preferenceName: The name of the preference.
    :var values: The list of values.
    
    Even though the value can be of a type different than string, the conversion to string should be made using the
    'Property' class provided by the SOA framework.
    """
    preferenceName: str = ''
    values: List[str] = ()


@dataclass
class SetPreferencesAtLocationsIn(TcBaseObj):
    """
    Contains the preference definition, values and the location where to set the information.
    
    :var location: Structure defining where the preferences are to be set.
    
    The intent is that only the system administrator should create a preference. However, this could be needed from
    non-directly-related user interactions. Therefore, the decision to make a call to this operation is delegated to
    its caller.
    :var preferenceInputs: Structure that contains the preference name, definition and values.
    """
    location: PreferenceLocation = None
    preferenceInputs: SetPreferences2In = None


@dataclass
class SetPreferencesDefinitionIn(TcBaseObj):
    """
    Structure containing a 'PreferenceDefinition' structure and a list of strings representing the preference values at
    the site level.
    
    :var definition: A structure holding the preference definition (possibly simplified).
    :var values: The list of values at the site level.
    Even though the values can be of a type different than string, they should be converted to a string through the use
    of the 'Property' class from the SOA framework. 
    """
    definition: PreferenceDefinition = None
    values: List[str] = ()


@dataclass
class CompletePreference(TcBaseObj):
    """
    Composite structure completely representing a preference: its definition is captured in the PreferenceDefinition
    structure, and its values in the PreferenceValue structure.
    
    :var definition: A structure holding all the preference definition parameters.
    :var values: A structure holding the preference values.
    """
    definition: PreferenceDefinition = None
    values: PreferenceValue = None
