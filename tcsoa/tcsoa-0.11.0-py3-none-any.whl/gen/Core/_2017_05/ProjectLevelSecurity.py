from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, PSBOMView, AssemblyArrangement, VariantRule, ItemRevision, RevisionRule, Folder, User, CFMOverrideEntry, TC_Project, Item, ConfigurationContext
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.Core._2012_09.ProjectLevelSecurity import TeamMemberInfo
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ModifyProjectsInfo2(TcBaseObj):
    """
    This structure holds the TC_Project object and the information required to modify the project.
    
    :var sourceProject: The TC_Project object to be modified.
    :var projectInfo: The information required to create the destination project.
    :var clientId: Unique identifier used by the client to track any errors.
    """
    sourceProject: TC_Project = None
    projectInfo: ProjectInformation2 = None
    clientId: str = ''


@dataclass
class OverrideInfo(TcBaseObj):
    """
    This contains information about the override RevisionRule entry
    
    :var ruleEntry: Refers to the CFMOverrideEntry of a RevisionRule object.
    :var folder: Refers to the Folder of override rule entry of RevisionRule object .
    """
    ruleEntry: CFMOverrideEntry = None
    folder: Folder = None


@dataclass
class PaginationInfo(TcBaseObj):
    """
    A Structure containing pagination criteria.
    
    :var startIndexForAvailableProjects: The start index to return the  available projects.
    :var maxToReturnForAvailableProjects: The maximum number of available available projects to return.
    """
    startIndexForAvailableProjects: int = 0
    maxToReturnForAvailableProjects: int = 0


@dataclass
class ProjectAssignOrRemoveInput(TcBaseObj):
    """
    
    Contains data used for assigning given set of objects to a list project objects for a given set of  configuration
    context.
    
    :var projectsToAssign: A list of TC_Project objects to for assignment.
    :var objectsForAssignment: A list of BusinessObject that needs to be assigned (added) to the given projects
    provided by projectsToAssing input parameter.
    :var projectsForRemoval: The TC_Project objects which needs to be removed from the given set of objects.
    :var objectsToRemoveFromProjects: A list of BusinessObject that needs to be removed from the given set of projects
    provided in projectsForRemoval parameter.
    :var contextInfo: A PropagationConfigurationContext structure.
    :var processAsynchronously: Flag indicating if this operation needs to be processed in asynchronously. A value True
    means to process it asynchronously. If the value is not set or is set to False then processing happens
    synchronously in the same request.
    """
    projectsToAssign: List[TC_Project] = ()
    objectsForAssignment: List[BusinessObject] = ()
    projectsForRemoval: List[TC_Project] = ()
    objectsToRemoveFromProjects: List[BusinessObject] = ()
    contextInfo: PropagationConfigurationContext = None
    processAsynchronously: bool = False


@dataclass
class ProjectInformation2(TcBaseObj):
    """
    Structure that holds the information required to create the destination project.
    
    :var projectId: The project ID of the project to be created.
    :var projectName: The name of the project to be created.
    :var projectDescription: The description of the project to be created.
    :var useProgramContext: The value of useProgramContext property in TC_Project.
    If value is true TC_Project is treated as program and if false it is project.
    :var active: The value of property  in TC_Project.
    If value is true than project is active so user can add/remove objects into this project. If value is false than
    project is no longer active. It will only available for viewing purpose. No further modification can be done on
    project.
    :var visible: The value of visible property in TC_Project.
    If value is true than this project will be visible to user in teamcenter otherwise project will be invisible.
    :var teamMembers: A list of TeamMemberInfo structures.
    :var clientId: Unique identifier used by the client to track any errors.
    :var propertyMap: A map of property names and desired values (string/string). This is map with property name and
    list of values in string format. The calling client is responsible for converting the different property types
    (int, float, date .etc) to a string using the appropriate functions in the SOA client framework's Property class.
    """
    projectId: str = ''
    projectName: str = ''
    projectDescription: str = ''
    useProgramContext: bool = False
    active: bool = False
    visible: bool = False
    teamMembers: List[TeamMemberInfo] = ()
    clientId: str = ''
    propertyMap: ProjectPropertiesMap = None


@dataclass
class ProjectOrLicenseDataInput(TcBaseObj):
    """
    Structure containing data for changing license and project data on WorkspaceObject.
    
    :var selectedObjects: A list of WorkspaceObject objects to be either attached or detached from selected list of
    Licenses or assigned or removed from selected list of projects
    :var selectedProjectsOrLicenses: A list of license IDs of ADA_License or Project IDs for TC_Project. These are
    strings of each with a maximum of 128 bytes size.
    :var eadParagraph: A list of authorizing paragraphs for the licenses being attached to WorkspaceObject objects.
    These are strings with a maximum of 80 bytes size. The size of eadParagraph vector should match the size of the
    selectedLicenses (each entry in eadParagraph maps to corresponding entry in selectedLicenses). If a paragraph entry
    is not applicable for a specific license (paragraph entries are applicable only for licenses of ITAR type), then
    that entry can be left blank. System will ignore any paragraph entry if it is not applicable for a license to be
    attached. This is an optional parameter. The eadParagraph is used for setting the ead_Paragraph attribute on
    WorkspaceObject.
    :var propertyName: The name of the property associated with the data it is either project_list or license_list.
    """
    selectedObjects: List[BusinessObject] = ()
    selectedProjectsOrLicenses: List[str] = ()
    eadParagraph: List[str] = ()
    propertyName: str = ''


@dataclass
class ProjectsInput(TcBaseObj):
    """
    A structure contain logged in user info, selected input objects list, configuration context info and pagination
    info.
    
    :var user: A user object, which is used to retrieve available projects to assign.
    :var selectedObjects: A list of Selected Input Objects.
    :var assignedObjects: A list of assigned objects from UI but not yet committed.
    :var paginationInfo: The pagination criteria.
    :var filterText: The filterText which should be applied for available projects to be returned.
    :var isAceContext: If true, the user is in ActiveWorkspace Content context; otherwise, false.
    """
    user: User = None
    selectedObjects: List[BusinessObject] = ()
    assignedObjects: List[TC_Project] = ()
    paginationInfo: PaginationInfo = None
    filterText: str = ''
    isAceContext: bool = False


@dataclass
class ProjectsOutput(TcBaseObj):
    """
    A list of projectsOutput objects.
    
    :var assignedProjectsList: A list of TC_Project objects which are assigned to the selected InputObject.
    :var selectedObjects: A list of selected input objects.
    """
    assignedProjectsList: List[TC_Project] = ()
    selectedObjects: List[BusinessObject] = ()


@dataclass
class ProjectsOutputResponse(TcBaseObj):
    """
    This structure holds the information for all assigned projects to the input objects and all the available projects.
    
    :var projectOutput: A list of projectsOutput objects.
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information. For this service, all objects are returned to the plain objects
    group. Error information will also be returned.
    :var availableProjectList: A list of available TC_Project objects sorted in  alphabetical order.
    :var projectOptions: A map(string, list of ConfigurationContextChoice) of ActiveWorkspace Content context
    attributes with the list of ActiveWorkspace Content context attributes possible values.
    :var totalFound: The total number of projects found.
    :var totalLoaded: The total number of projects loaded.
    :var endIndex: The end index to return the projects.
    """
    projectOutput: ProjectsOutput = None
    serviceData: ServiceData = None
    availableProjectList: List[TC_Project] = ()
    projectOptions: ProjectOptions = None
    totalFound: int = 0
    totalLoaded: int = 0
    endIndex: int = 0


@dataclass
class PropagationConfigurationContext(TcBaseObj):
    """
    PropagationConfigurationContext contains data which can be applied to assign to projects and remove from projects
    operation.
    
    :var selectedTopLevelObject: Selected top level object in context of ACE ( Active Content Expericence ), if this
    object is passed we will fetch variant rule and revision rule.
    :var variantRule: 
    The VariantRule in context of the assign to project  or attach to license operation.
    :var revisionRule: The RevisionRule associated with the assign to project or attach to license operation.
    :var typeOption: An integer indicating the type of Item or Item Revision, valid values are 0 for Item and 1 for
    Item Revision.
    :var depth: A number indicating how deep the traversal needs to be performed for a given structure, applicable only
    for structures.
    """
    selectedTopLevelObject: BusinessObject = None
    variantRule: VariantRule = None
    revisionRule: RevisionRule = None
    typeOption: int = 0
    depth: int = 0


@dataclass
class PropagationDataInput(TcBaseObj):
    """
    Structure selected objects, configuration information which will be used for propagation and a structure of
    ReconstructBOMWindowInfo.
    
    :var assignOrAttachData: A list of projects to be assigned to a given set of objects or list of licenses that needs
    to be attached to a given set of objects.
    :var removeOrDetachData: A list containing license to be detached from a given set of objects or projects to be
    removed from a given set of objects.
    :var propertyDataToSetAndPropagate: A list of selected business object with property value to be removed or added.
    :var configInfo: The configuration information for propagation.
    :var reconstructConfigurationInfo: Information that will be used to reconstruct the given BOMWindow if the
    operation needs to be performed in a different process.
    """
    assignOrAttachData: List[ProjectOrLicenseDataInput] = ()
    removeOrDetachData: List[ProjectOrLicenseDataInput] = ()
    propertyDataToSetAndPropagate: List[PropertyChangeData] = ()
    configInfo: PropagationConfigurationContext = None
    reconstructConfigurationInfo: ReconstructBOMWindowsInfo = None


@dataclass
class PropertyChangeData(TcBaseObj):
    """
    A Structure containing the name of property which needs to be modified, the new intended value after modification
    and set of selected objects.
    
    :var selectedObjects: A list of selected objects for which the property needs to be changed.
    :var propertyName: The name of propagation enabled property for modification.
    :var newPropertyValues: A list of values that are need to be set for the given property. This is the intended
    property values after the change.
    """
    selectedObjects: List[BusinessObject] = ()
    propertyName: str = ''
    newPropertyValues: List[str] = ()


@dataclass
class ReconstructBOMWindowsInfo(TcBaseObj):
    """
    This contains the list of BOMWindow objects and the corresponding RevisionRule and VariantRule objects or
    StoredOptionSet object information.
    
    :var item: Item object reference.
    :var itemRev: ItemRevision object reference.
    :var bomView: PSBOMView object reference.
    :var objectsForConfigure: List of variant rules or single stored option set object to set on this window.
    :var revRuleConfigInfo: Refers to a RevisionRuleConfigInfo struct object.
    :var activeAssemblyArrangement: Active assembly arrangement of this BOMWindow.
    :var configContext: ConfigurationContext object reference.
    :var bomWinPropFlagMap: Mapping for window property and respective value that needs to be set on window. User need
    to populate this map with following property string values as key and true or false as value, which will be set or
    unset on the window. Valid property values are
    """
    item: Item = None
    itemRev: ItemRevision = None
    bomView: PSBOMView = None
    objectsForConfigure: List[BusinessObject] = ()
    revRuleConfigInfo: RevisionRuleConfigInfo = None
    activeAssemblyArrangement: AssemblyArrangement = None
    configContext: ConfigurationContext = None
    bomWinPropFlagMap: StringMap = None


@dataclass
class RevisionRuleConfigInfo(TcBaseObj):
    """
    This contains the RevisionRule object and a RevisionRuleEntryProps  structure.
    
    :var revRule: The RevisionRule object used for configuration of this BOMWindow object.
    :var props: Refers to RevisionRuleEntryProps struct object.
    """
    revRule: RevisionRule = None
    props: RevisionRuleEntryProps = None


@dataclass
class RevisionRuleEntryProps(TcBaseObj):
    """
    This contains information about the RevisionRule entry properties.
    
    :var unitNo: The unit number of RevisionRule object.
    :var date: The date of RevisionRule object.
    :var today:  Refers to a flag to indicate that the date is today on RevisionRule object.
    :var endItem: The  Item that indicates end item for RevisionRule object.
    :var endItemRevision: The ItemRevision that indicates end item revision for RevisionRule object.
    :var overrideFolders: A list of OverrideInfo struct.
    """
    unitNo: int = 0
    date: datetime = None
    today: bool = False
    endItem: Item = None
    endItemRevision: ItemRevision = None
    overrideFolders: List[OverrideInfo] = ()


@dataclass
class ConfigurationContextChoice(TcBaseObj):
    """
    This structure contains context related info.
    
    :var internalValue: Internal value of business object.
    :var displayValue: Display value of business object.
    :var isDefaultValue: If true, this choice is set to default; otherwise, false.
    """
    internalValue: str = ''
    displayValue: str = ''
    isDefaultValue: bool = False


@dataclass
class CopyProjectsInfo2(TcBaseObj):
    """
    Structure that holds project information required to create a new TC_Project object using this operation.
    
    :var sourceProject: The TC_Project object needs to be copied.
    :var projectInfo: The information required to copy the project.
    :var clientId: Unique identifier used by the client to track any errors.
    """
    sourceProject: TC_Project = None
    projectInfo: ProjectInformation2 = None
    clientId: str = ''


"""
A map(string/list of ConfigurationContextChoice) of ActiveWorkspace Content context attributes with the list of ActiveWorkspace Content context attributes possible values.
"""
ProjectOptions = Dict[str, List[ConfigurationContextChoice]]


"""
A map (string, string) of property names and desired values. The calling client is responsible for converting the different property types (int, float, date .etc) to a string using the appropriate functions in the SOA client framework's Property class.
"""
ProjectPropertiesMap = Dict[str, List[str]]


"""
 A StringMap which holds string as key and value as string.
"""
StringMap = Dict[str, str]
