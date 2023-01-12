from __future__ import annotations

from tcsoa.gen.BusinessObjects import WorkspaceObject, ADA_License
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ConfigurationContextChoice(TcBaseObj):
    """
    A strucure that contains information related to Ace Context.
    
    :var internalValue: Internal value of business object.
    :var displayValue: Display value of business object.
    :var isDefaultValue: If true, this instance of ConfigurationContextChoice should be set as default choice.
    """
    internalValue: str = ''
    displayValue: str = ''
    isDefaultValue: bool = False


@dataclass
class FilterInfo(TcBaseObj):
    """
    A structure containing license related information to filter licenses.
    
    :var licenseType: The type of ADA licenses to be filtered.
    :var licenseId: The ID of the license to be filtered.
    """
    licenseType: str = ''
    licenseId: str = ''


@dataclass
class LicenseInput(TcBaseObj):
    """
    Structure that holds the information required to get list of licenses.
    
    :var selectedObjects: The list of selected WorkspaceObject objects
    :var selectedLicenses: The list of licenses (ADA_License) which are already selected to attach with objects.
    :var filterInfo: The filter criteria based on license type and license ID.
    :var paginationInfo: The pagination criteria.
    :var isAceContext: If true, the user is in ActiveWorkspace Content context.
    :var isAssigned: If true only already attached licenses to objects will return in response. If false than attached
    and available both licenses will return in response.
    :var licenseParamsIn: A list of parameters for future use.
    """
    selectedObjects: List[WorkspaceObject] = ()
    selectedLicenses: List[ADA_License] = ()
    filterInfo: FilterInfo = None
    paginationInfo: PaginationInfo = None
    isAceContext: bool = False
    isAssigned: bool = False
    licenseParamsIn: List[str] = ()


@dataclass
class LicenseOutput(TcBaseObj):
    """
    Structure that holds the licenses object.
    
    :var commonAssignedLicenseList: A list of ADA_License objects which are assigned to the seletectd InputObect. If
    the InputObject is a single select, ead_paragraph will be include. If the InputObject is a multi-select,
    ead_paragraph will be blank.
    :var availableLicenseList: A list of ADA_License objects which are available to attach to the selected InputObject.
    :var allAssignedLicenseList: List of all licenses already selected for attach to selected objects.
    :var assignedLicenseTypes: A list of types of the assignedLicenseList.
    :var availableLicenseTypes: A list of types of the availableLicenseList.
    """
    commonAssignedLicenseList: List[ADA_License] = ()
    availableLicenseList: List[ADA_License] = ()
    allAssignedLicenseList: List[ADA_License] = ()
    assignedLicenseTypes: List[LicenseType] = ()
    availableLicenseTypes: List[LicenseType] = ()


@dataclass
class LicenseType(TcBaseObj):
    """
     structure that holds internal value and display value of ADA_License.
    
    :var internalValue: Internal value of ADA_License.
    :var displayValue: Display value of ADA_License.
    """
    internalValue: str = ''
    displayValue: str = ''


@dataclass
class LicensesWithTypesResponse(TcBaseObj):
    """
    A strucure that holds all license related and pagination related information.
    
    :var licensesOutput: A list of licenseOutputs objects.
    :var licenseOptions: A map (string, list of ConfigurationContextChoice) of ACE context atrributes with the list of
    ACE context atrtributes and possible values.
    :var totalFound: The total licenses found.
    :var endIndex: The end index of the ADA_LICENSE returned by the operation. This end index will be used by the
    client as start index of next iteration.
    :var totalLoaded: The total number of licenses loaded at a time.
    :var licenseParamsOut: A map (string, list of string) for future use. It will used to return values which passed in
    licenseParamsIn parameter of LicenseInputs structure.
    :var serviceData: The SOA framework object containing objects that were created, deleted or updated by the Service,
    plain objects and error information. For this service, all object are returned to the plain objects group. Error
    information will also be returned.
    """
    licensesOutput: LicenseOutput = None
    licenseOptions: LicenseOptions = None
    totalFound: int = 0
    endIndex: int = 0
    totalLoaded: int = 0
    licenseParamsOut: LicenseParamsOut = None
    serviceData: ServiceData = None


@dataclass
class PaginationInfo(TcBaseObj):
    """
    A structure containing pagination criteria.
    
    :var startIndex: The start index to return the licenses. Must be a non-negative value. Otherwise all data will be
    returned and the data will not  be paginated.
    :var maxToReturn: The maximum number of licenses to return. Must be a value greater than zero. Otherwise, all data
    will be returned and the data will not be paginated.
    """
    startIndex: int = 0
    maxToReturn: int = 0


"""
A map (string, list of ConfigurationContextChoice) of ACE context atrributes with the list of ACE context atrtributes and possible values.
"""
LicenseOptions = Dict[str, List[ConfigurationContextChoice]]


"""
A map (string, list of string) for future use. It will used to return values which passed in licenseParamsIn parameter of LicenseInputs structure.
"""
LicenseParamsOut = Dict[str, List[str]]
