from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ReportDefinition
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AccessorInfo(TcBaseObj):
    """
    This structure is used to pass the accessor information( combination of Group UID, Role UID and User UID ).
    Supported use cases are:
    1. Group UID is passed, Role UID and User UID are empty, which means the Awp0SearchFolder is expected to be shared
    with the particular group.
    2. Role UID and Group UID are passed, User UID is empty, which means the Awp0SearchFolder is expected to be shared
    with the particular role within the particular group.
    3. User UID is passed, Role UID and Group UID are empty, which means the Awp0SearchFolder is expected to be shared
    with the particular user.
    
    :var groupUID: Specifies the UID of the Group with which the input Awp0SearchFolder is expected to be shared with.
    :var roleUID: Specifies the UID of the Role with which the input Awp0SearchFolder is expected to be shared with.
    :var userUID: Specifies the UID of the User with which the input Awp0SearchFolder is expected to be shared with.
    """
    groupUID: str = ''
    roleUID: str = ''
    userUID: str = ''


@dataclass
class GetSearchFolderAccessorsOutput(TcBaseObj):
    """
    Output structure that holds the accessors info for provided Awp0SearchFolder UIDs.
    
    :var searchFolderAndItsAccessors: A map (string, list of business objects) to hold the Awp0SearchFolder and list of
    its associated accessors. Supported types for the business objects are POM_accessor, POM_group and POM_user or
    GroupMember.
    :var serviceData: Service data for holding the partial errors.
    """
    searchFolderAndItsAccessors: SearchFolderAndItsAccessorsMap = None
    serviceData: ServiceData = None


@dataclass
class ImportInput(TcBaseObj):
    """
    Structure defines the mode, the UID of the input Awp0SearchFolder object and the transient file ticket for the
    TCXML file specified in the Active Workspace client for the importSearchFolder service operation.
    The mode parameter has two valid values, preview and import. The preview mode is a way for the user to see what
    structure is going to be imported into the input Awp0SearchFolder object. The import mode is when the user wants to
    do the TCXML import of the Awp0SearchFolder hierarchy along with its ReportDefinition and Awp0SearchFolderShareRule
    which is specified in the TCXML into the input Awp0SearchFolder object.
    The searchFolderUID specifies the UID of the input active folder under which the hierarchy is to be imported.
    If it is passed as empty, then the import will happen into the Awp0MySearchFolder instance of the logged in user.
    
    :var mode: Specifies whether to get the preview of the Awp0SearchFolder with its hierarchy or to import the
    Awp0SearchFolder and its hierarchy. Valid values are: "import" and "preview".
    Import:  Used to import the Awp0SearchFolder object,  its children, and Awp0SearchFolderShareRule and
    ReportDefinition objects attached to it as a child of the searchFolderUID. 
    Preview:  Provides the preview of the root Awp0SearchFolder object specified in the TCXML along with its hierarchy
    (its children) in tree view mode in a JSON string format.
    :var transientFileTicket: The file ticket for the TCXML to be imported into the selected Awp0SearchFolder.
    (required)
    :var searchFolderUID: UID of the input Awp0SearchFolder under which the contents of the TCXML needs to be imported.
    Required for import mode; otherwise, it is empty.
    """
    mode: str = ''
    transientFileTicket: str = ''
    searchFolderUID: str = ''


@dataclass
class ImportSearchFolderResponse(TcBaseObj):
    """
    The response contains the serviceData and the preview string in JSON format. The serviceData contains any partial
    errors returned from the import operation using TIE import and the preview of the hierarchy of the Awp0SearchFolder
    object specified in the input TCXML file. Hierarchy meaning it will mention the name of the root Awp0SearchFolder
    and the names of its children active folders till the leaf Awp0SearchFolder object. The previewStringJSON will be
    only returned if the input mode parameter is passed as preview. Otherwise for the import mode, it will be empty.
    
    Structure of JSON schema:
    
    "dataForTheTree":
    [ 
        { 
              "label": "Active Folder 001", 
              "children": 
               [
                   { 
                        "label": "Active Folder 001-Child", 
                        "children":
                        [
                             {
                                    "label": "Active Folder Sub Child", 
                                 "children":[]
                             }
                        ]
                   }, 
                  {
                         "label": "Active Folder 002-Child"
                   }
                  ] 
        }
    ]
    
    :var serviceData: Service data for holding the partial errors returned for the import of the transient file ticket
    or preview of the TCXML file to be imported.
    :var previewStringJSON: A preview of the hierarchy of the Awp0SearchFolder specified in the TCXML. Output is in
    JSON format which the client will read to show the hierarchy in tree view mode. Only returned when the mode is
    preview. Empty for the import mode.
    """
    serviceData: ServiceData = None
    previewStringJSON: str = ''


@dataclass
class ReportChartObject(TcBaseObj):
    """
    Teamcenter type and property name for which charting information is desired.
    
    :var chartTypeName: Internal name of the Teamcenter type.
    :var chartPropertyName: Internal name of the Teamcenter property.
    :var isPropertyLocalized: If true, indicates that localized value of this property has been indexed in the search
    engine.
    :var chartPropertyType: Teamcenter property type.
    """
    chartTypeName: str = ''
    chartPropertyName: str = ''
    isPropertyLocalized: bool = False
    chartPropertyType: str = ''


@dataclass
class ReportSearchRecipe(TcBaseObj):
    """
    Structure to represent Search recipe for individual Teamcenter ReportDefinition object.
    
    :var reportObject: Teamcenter ReportDefinition object.
    :var translatedBaseCriteria: Translated primary search criteria.
    :var translatedFilterQueries: An list of translated filter criteria.
    :var reportChartObjects: A list of chart objects supported by the ReportDefinition object.
    :var reportSearchRecipeExtraInfo: A map (string, string) of additional search related parameter and value pairs.
    Following parameters are supported: lastTotalFound: Total number of objects returned when this ReportDefinition was
    last executed by the current user.
    lastExecutedTime: Timestamp of when this ReportDefinition object was last executed by the current user.
    """
    reportObject: ReportDefinition = None
    translatedBaseCriteria: str = ''
    translatedFilterQueries: List[str] = ()
    reportChartObjects: List[ReportChartObject] = ()
    reportSearchRecipeExtraInfo: SearchRecipeExtraInfo = None


@dataclass
class ReportSearchRecipeInput(TcBaseObj):
    """
    Input criteria to retrieve ReportDefinition objects. One of reportID or reportUID is mandatory.
    
    :var reportID: The unique ID of the Teamcenter ReportDefinition object to be retrieved (optional if reportUID is
    provided).
    :var reportUID: The UID of the ReportDefinition object (optional if reportID is provided).
    :var reportSource: Data source type for the ReportDefinition object. Example: Active Workspace, Teamcenter
    (optional).
    """
    reportID: str = ''
    reportUID: str = ''
    reportSource: str = ''


@dataclass
class ReportSearchRecipeResponse(TcBaseObj):
    """
    Structure to hold a list of ReportSearchRecipe structures and search filter queries that are common for the entire
    session.
    
    :var reportSearchRecipeObjects: A list of ReportSearchRecipe structures. Each ReportSearchRecipe holds search
    recipe specific to a single ReportDefinition object.
    :var commonSearchParameters: Search filters that are common for the entire session. This includes:
    globalRevisionRule: Search filter query representing the active global revision rule.
    userContextInfo : Search filter query representing the current session context info.
    additionalFilters : Other search filter queries that are common for the entire session.
    :var serviceData: Teamcenter service data containing ReportDefinition objects being returned.
    """
    reportSearchRecipeObjects: List[ReportSearchRecipe] = ()
    commonSearchParameters: SearchRecipeExtraInfo = None
    serviceData: ServiceData = None


@dataclass
class SearchFoldersInput(TcBaseObj):
    """
    Input structure to create or edit the Awp0SearchFolder passed in the searchFolderUID.
    
    :var parentFolderUID: Parent Folder UID for the Awp0SearchFolder being created. Set to empty in edit case.
    :var searchFolderUID: UID of the Awp0SearchFolder which is being edited. Set to empty in creation case.
    :var reportDefinitionUID: UID of the ReportDefinition object that is being edited. Only passed in case of editing
    the search definition. Otherwise empty.
    :var searchCriteria: A list that contains different search criteria and their values.
    
    Example:
    
    If user is doing Active Workspace global search and wants to search for all items in the system that match the
    keyword "hdd" and is owned by user "ed", in this case the searchCriteria list would be as follows: 
    CriteriaAndValue[0] {    criteriaName "searchString"
    criteriaValues ["hdd"] }
    CriteriaAndValue[1]{    criteriaName "owning_user"
    criteriaValues ["ed"] }
    :var searchFolderAttributes: Map (string, list of strings) of Awp0SearchFolder attribute names and their values.
    The following attributes can be set when an Active Folder is created.
        Name,
        Description,
        Shared with User,
        Shared with Role,
        Shared with Group,
        Shared with Project.
                            
    Example:     
    Creation Case:
    When "Active Folder 1" is created and shared with Group1, Group2 and with Project1, entries of this map are going
    to be following: 
    Name    {Specification Search}
    Description                {All active 
                specifications}
    Shared with Group        {Group1UID, Group2UID}
    Shared with Project       {Project1UID}
    
    An Activer Folder with name "Specification Search" and description "All active specifications" is created and
    shared with Group1, Group2 and Project1.
    
    Edit Case:
    If "Specification Search" folder needs to be shared with User1 and User2, now entries of this map are going to be
    following: 
    Shared with User    {User1UID, User2UID}
    
    Now Active Folder is also shared with User1 and User2.
    :var searchFolderAccessors: A list used to pass the accessor information( combination of Group UID, Role UID and
    User UID ).
    Supported use cases are:
    1. Group UID is passed, Role UID and User UID are empty, which means the Awp0SearchFolder is expected to be shared
    with the particular group.
    2. Role UID and Group UID are passed, User UID is empty, which means the Awp0SearchFolder is expected to be shared
    with the particular role within the particular group.
    3. User UID is passed, Role UID and Group UID are empty, which means the Awp0SearchFolder is expected to be shared
    with the particular user.
    """
    parentFolderUID: str = ''
    searchFolderUID: str = ''
    reportDefinitionUID: str = ''
    searchCriteria: List[CriteriaAndValue] = ()
    searchFolderAttributes: SearchFolderAttributes = None
    searchFolderAccessors: List[AccessorInfo] = ()


@dataclass
class CreateOrEditSearchFoldersOutput(TcBaseObj):
    """
    Structure holds the createOrEditSearchFolders operation response.
    
    :var searchFolders: A list of created or edited instances of Awp0SearchFolder along with ReportDefinition objects.
    :var serviceData: Service data for holding the partial errors.
    """
    searchFolders: List[CreatedOrEditedSearchFolder] = ()
    serviceData: ServiceData = None


@dataclass
class CreatedOrEditedSearchFolder(TcBaseObj):
    """
    Structure holds the created or edited Awp0SearchFolder and ReportDefinition objects.
    
    :var searchFolder: Created or edited Awp0SearchFolder business object.
    :var reportDefinition: The created or edited ReportDefinition business object.
    :var searchFolderAttributes: Search Folder attributes map (string, a list strings).
    """
    searchFolder: BusinessObject = None
    reportDefinition: BusinessObject = None
    searchFolderAttributes: SearchFolderAttributes = None


@dataclass
class CriteriaAndValue(TcBaseObj):
    """
    This structure holds the criteria name and its values for representing a search definition.It has 2 special cases,
    for FullTextSearch case searchString will be sent as key search string. And in the case of Advanced Search,
    savedQueryUID will be sent as key to identify associated SavedQuery.
    
    :var criteriaName: Search criteria name. Supported values are: "searchString" in case of FullTextSearch.
    "savedQueryUID" in case of Advanced Search. These are 2 known values for this attribute rest of the values are
    dynamic. For example, for a given search, user can provide any filter to limit the search results. Example of
    filter values can be project list, last modified date or release status.
    :var criteriaValues: A list of the criteria values. Supported values: ImanQuery UID value in case of SavedSearch.
    Keyword search value in case of FullTextSearch. Filter values for any filter criteria. 
    Example: For finding all items matching criteria hdd for owning user ed, CriteriaAndValue is going to be
    CriteriaAndValue[0] {criteriaName searchString, criteriaValues [hdd ]}CriteriaAndValue[1]{criteriaName
    owning_user,criteriaValues [ed] }
    """
    criteriaName: str = ''
    criteriaValues: List[str] = ()


@dataclass
class ExportSearchFoldersResponse(TcBaseObj):
    """
    Structure holds the file tickets of the exported TCXML files.
    
    :var transientFileReadTickets: A list of transient file read tickets for the exported files.
    :var serviceData: Service data for holding the partial errors while generating file tickets.
    """
    transientFileReadTickets: List[str] = ()
    serviceData: ServiceData = None


"""
This map holds search folder and list of the business objects which are its accssors. Key is Awp0SearchFolder UID and the corresponding value is a vector of business objects( supported types are POM_accessor, GroupMember, POM_group and POM_user ) containing the accessors.
"""
SearchFolderAndItsAccessorsMap = Dict[str, List[BusinessObject]]


"""
Map (string, list of strings) of Awp0SearchFolder attribute names and their values.
The following attributes can be set when a Awp0SearchFolder is created or edited.
    Name,
    Description,
    Shared with User,
    Shared with Role,
    Shared with Group,
    Shared with Project.
                        
Example:     
Creation Case:
When "Active Folder1" is created and shared with Group1, Group2 and with Project1, entries of this map are going to be following: 
Name    {Specification Search}
Description                {All active 
            specifications}
Shared with Group        {Group1UID, Group2UID}
Shared with Project       {Project1UID}

An Active Folder with name "Specification Search" and description "All active specifications" is created and shared with Group1, Group2 and Project1.

Edit Case:
If "Specification Search" folder needs to be shared with User1 and User2, now entries of this map are going to be following: 
Shared with User    {User1UID, User2UID}
Now Active Folder is also shared with User1 and User2.
"""
SearchFolderAttributes = Dict[str, List[str]]


"""
A map (string, string) of additional search parameter and value pairs. This includes additional information sent as part of the translated Search recipe response for ReportDefinition objects.
"""
SearchRecipeExtraInfo = Dict[str, str]
