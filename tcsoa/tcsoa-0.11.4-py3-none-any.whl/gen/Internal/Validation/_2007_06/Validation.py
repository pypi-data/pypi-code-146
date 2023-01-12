from __future__ import annotations

from tcsoa.gen.BusinessObjects import ClosureRule, WorkspaceObject, Dataset, User, ValidationData, ValidationResult, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExternalRuleInfo(TcBaseObj):
    """
    The ExternalRuleInfo struct represents the information for external rule dataset for validation data.
    
    :var useExistingObject: A bool value that indicates if an existing closure rule object will be used.
    :var extenralRuleObject: Pointer to an existing closure rule object to be used.
    :var ruleDatasetInfo: The structure contains necessary data for creating a rule dataset.
    """
    useExistingObject: bool = False
    extenralRuleObject: Dataset = None
    ruleDatasetInfo: DatasetInfo = None


@dataclass
class GetValResultsInput(TcBaseObj):
    """
    The GetValResultsInput struct  holds the input data for getValidationResult .  There is no one to one mapping
    between these two input lists. When both lists are NULL, all validation results in the database will be returned.
    
    :var targetObjects: A list of  target objects. It can be NULL, when it is NULL, it means validation result with any
    target object is ok.
    :var validationDatas: A list of  ValidationData objects. It can be NULL, when it is NULL; it means validation
    result with any validation data is ok.
    """
    targetObjects: List[WorkspaceObject] = ()
    validationDatas: List[ValidationData] = ()


@dataclass
class GetValidationResultResponse(TcBaseObj):
    """
    Holds the response for getValidationResult.
    
    :var results: A vector of ValidationResult objects.
    :var serviceData: Teamcenter::Soa::Server::ServiceData is the Framework class that holds model objects and partial
    errors.
    """
    results: List[ValidationResult] = ()
    serviceData: ServiceData = None


@dataclass
class AttributeInfo(TcBaseObj):
    """
    The AttributeInfo struct represents the parameter <name, value, operation> tuple for both ValidationData and
    ValidationResult.
    
    :var name: A parameter name string.
    :var value: A parameter value string.
    :var operation: A string indicating the comparison method, valid values are = or empty string.
    """
    name: str = ''
    value: str = ''
    operation: str = ''


@dataclass
class ReportFileInfo(TcBaseObj):
    """
    The structure contains the information for new report datasets that are associated with ValidationResult objects.
    
    :var useExistingObject: A bool value that indicates if an existing dataset will be updated.
    :var reportFileObject: Pointer to a valid ImanFile object for the dataset.
    :var reportDatasetInfo: The name reference data needed for updating the given file object.
    """
    useExistingObject: bool = False
    reportFileObject: Dataset = None
    reportDatasetInfo: DatasetInfo = None


@dataclass
class ValidationAgentInfo(TcBaseObj):
    """
    The ValidationAgentInfo structure is the main input to the createValidationData and updateValidationData service.
    This struct refers to the ValidationData, closure rule, external rule and requirement Used to create or update
    those objects.
    
    :var existingValidationAgent: The object to be updated. When it is NULL, a new ValidationAgent object will be
    created.
    :var clientId: Client supplied identifier string that helps the client map from the input for the object(s)
    created. It should be unique in the client session.
    :var name: The name for a validation agent.
    :var description: The description for a validation agent.
    :var utilityCommand: The validation utility command.
    :var utilityArgs: The arguments for the validation utility command.
    :var closureRule: Struct ClosureRuleInfo describing the closure rule.
    :var checkUserPriviledge: When it is set to true, only system administrators or validation administrators can
    create or modify a ValidationAgent When it is set to false, it will bypass the privilege checking.
    """
    existingValidationAgent: ValidationData = None
    clientId: str = ''
    name: str = ''
    description: str = ''
    utilityCommand: str = ''
    utilityArgs: str = ''
    closureRule: ClosureRuleInfo = None
    checkUserPriviledge: bool = False


@dataclass
class ValidationAgentOutput(TcBaseObj):
    """
    The ValidationAgentOutput struct holds the information for created or updated validation agent and it child
    validation data.
    
    :var clientId: Unique client identifier string.
    :var validationAgent: Pointer to a validation agent.
    :var childValidationData: The associated validation checker objects for the validation agent.
    """
    clientId: str = ''
    validationAgent: ValidationData = None
    childValidationData: List[ValidationData] = ()


@dataclass
class ValidationDataInfo(TcBaseObj):
    """
    The ValidationDataInfo struct is the main input to the createOrUpdateValidationData service. This struct refers to
    the ValidationData, closure rule, external rule and requirement used to create or update those objects.
    
    :var existingValidationData: The object to be updated. When it is NULL or points to a NULL TAG, a new
    ValidationResult will be created
    :var clientId: Client supplied identifier string that helps the client map from the input for the create to the
    object(s) created. This client ID should be unique in the client session. It is the clients way of identifying the
    ValidationData (not necessarily an attribute persisted in Teamcenter).
    :var checkUserPriviledge: When it is set to true, only SA or GA can create or modify a ValidationData object. When
    it is set to false, it will bypass the privilege checking.
    :var name: The name for validation data.
    :var description: The description for validation data.
    :var agentName: The name of the validation agent that this checker belongs to.
    :var category: The name for the category.
    :var closureRule: Struct ClosureRuleInfo describing the closure rule.
    :var attrList: A map of parameter names and parameter values, both name and value is string type.
    :var externalRule: Struct externalRuleInfo describing the external rule.
    :var requirementObject: The object as the requirement for validation.
    """
    existingValidationData: ValidationData = None
    clientId: str = ''
    checkUserPriviledge: bool = False
    name: str = ''
    description: str = ''
    agentName: str = ''
    category: str = ''
    closureRule: ClosureRuleInfo = None
    attrList: List[AttributeInfo] = ()
    externalRule: ExternalRuleInfo = None
    requirementObject: WorkspaceObject = None


@dataclass
class ValidationDataResponse(TcBaseObj):
    """
    The ValidationDataResponse struct holds the response for createOrUpdateValidationData.
    
    :var output: A vector of :ValidationDatasOutput structures.
    :var serviceData: Teamcenter::Soa::Server::ServiceData is the SOA Framework class that holds model objects and
    partial errors. Any created objects and the updated container object will be sent back in the standard ServiceData
    lists of created and updated object respectively. Any failure will be returned with the client ID mapped to the
    error message in the list of partial errors. Following are some possible errors returned:
    - 206001  Insufficient system administration privileges.
    - 206002  Validation data object failed to initialize.
    - 206003  Failed to create validation data objects.
    - 206004  Cannot create duplicate validation data objects.
    - 206005  Failed to get validation data objects from database.
    
    """
    output: List[ValidationDatasOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ValidationDatasOutput(TcBaseObj):
    """
    The ValidationDatasOutput struct contains the output information from createOrUpdateValidationData for result
    validation data and its closure rule and external rule..
    
    :var clientId: Unique client identifier string.
    :var validationDataObject: Pointer to a ValidationData object.
    :var closureRule: Pointer to a ClosureRule object that will be used to collect validation targets from a given
    Business Object.
    :var externalRuleDataset: Pointer to an external rule dataset object that will be used by the ValidationData object.
    :var datasetOutput: A structure that contains the created or updated Dataset and its file ticket information for
    the named references.
    """
    clientId: str = ''
    validationDataObject: ValidationData = None
    closureRule: ClosureRule = None
    externalRuleDataset: Dataset = None
    datasetOutput: DatasetOutput = None


@dataclass
class ValidationResultInfo(TcBaseObj):
    """
    The ValidationResultInfo struct is the main input to the createOrUpdateValidationResults This struct refers to the
    existing ValidationResult, attribute list, report files, and one or more Dataset structs used to create those
    report datasets.
    
    :var existingValidationResult: A valid object pointer to an existing validation result object for update.
    The value will be NULL when a new validation result is to be created.
    :var clientId: Client supplied Identifier string that helps the client map from the input for the object(s) created
    or updated. It should be unique in the client session.
    :var user: The user who performed the validation check and created the validation result.
    :var isAdhoc: A logical flag indicating whether the validation result needs human to decide whether the validation
    result is Passed or Failed.
    :var attrList: A map of parameter name string and parameter value string pairs used for the validation check.
    :var reports: Information to create new validation report datasets that will be attached to the validation result
    object.
    :var replaceExistingReport: This flag specifies whether the new report datasets will replace the existing report
    datasets or will be appended to the existing report datasets array.
    :var targetItemRev: The target ItemRevision of the validation result.
    :var targetObject: The validation target datatset for this validation result.
    :var validationDataObject: The referenced validation data object that was used to create this validation result
    object.
    :var resultId: The value corresponding to the attribute ValidationResult.result_id in the validation result object.
    :var result: This flag indicates whether this validation result is Passed or Failed. When the value is TRUE, the
    result is Passed. When the value is FALSE, the result is Failed.
    :var status: An integer that indicates the validation result status as defined by the validation agent.
    :var comment: The comments for this validation result.
    :var date: The date and time when the validation was last performed.
    """
    existingValidationResult: ValidationResult = None
    clientId: str = ''
    user: User = None
    isAdhoc: bool = False
    attrList: List[AttributeInfo] = ()
    reports: List[ReportFileInfo] = ()
    replaceExistingReport: bool = False
    targetItemRev: ItemRevision = None
    targetObject: Dataset = None
    validationDataObject: ValidationData = None
    resultId: str = ''
    result: bool = False
    status: int = 0
    comment: str = ''
    date: datetime = None


@dataclass
class ValidationResultsOutput(TcBaseObj):
    """
    The structure contains the information for created or updated ValidationResult object and the associated report
    datasets.
    
    :var clientId: Unique client identifier string.
    :var resultObject: Pointer to a ValdiationResult object.
    :var datasetOutputs: A vector of structures that contains the created datasets and the associated file ticket
    information for the named references.
    :var reportDatasets: A vector of updated report datasets associated with the ValidationResult object.
    """
    clientId: str = ''
    resultObject: ValidationResult = None
    datasetOutputs: List[DatasetOutput] = ()
    reportDatasets: List[Dataset] = ()


@dataclass
class ValidationResultsResponse(TcBaseObj):
    """
    Holds the response for createOrUpdateValidationResults.
    
    :var output: A vector of ValidationResultsOutpu structures.
    :var serviceData: Holds model objects and partial errors. Any created objects and the updated container object will
    be sent back in the standard ServiceData lists of created and updated object respectively. Any failure will be
    returned with client id mapped to error message in the ServiceData list of partial errors. Following are some
    possible errors returned in ServiceData:
    - 206002  Validation data object failed to initialize.
    - 206007  Query falied to find the required objects.
    - 206010  Failed to create ValidationResult object.
    
    """
    output: List[ValidationResultsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ClosureRuleInfo(TcBaseObj):
    """
    The ClosureRuleInfo struct represents the information for a new closure rule or an existing one.
    
    :var useExistingObject: The flag indicates whether to use existing closure rule.
    :var closureRuleObject: Pointer to an existing ClousreRule object when 'useExistingObject' is TRUE.
    :var closureRuleName: The name for a ClosureRule object. If 'useExistingObject' is TRUE and 'closureRuleObject' is
    NULL, a ClosureRule with this name will be used.
    :var type: A vector of DatasetType names. These inputs are only used when 'useExistingObject' is false. They are
    mainly for NX application. When closure rule with the same name does not exist, dataset types will be used to
    create a new closure rule. Otherwise, dataset types will be used to append to current closure rule.
    """
    useExistingObject: bool = False
    closureRuleObject: ClosureRule = None
    closureRuleName: str = ''
    type: List[str] = ()


@dataclass
class CreateOrUpdateValidationAgentsResponse(TcBaseObj):
    """
    The CreateOrUpdateValidationAgentsResponse struct holds the response for createOrUpdateValidationAgents.
    
    :var output: A vector of ValidationAgentOutput structures.
    :var serviceData: Teamcenter::Soa::Server::ServiceData is the  Teamcenter Services framework class that holds model
    objects and partial errors. Any created objects and the updated container object will be sent back in the standard
    ServiceData lists of created and updated object respectively. Any failure will be returned with the client id ID
    mapped to the error message in the ServiceData list of partial errors. Following are some possible errors returned
    in SserviceData:
    - 206001  In sufficient system administration privileges.
    - 206002  Validation data object failed to initialize.
    - 206003  Failed to create validation data objects.
    - 206004  Cannot create duplicate validation data objects.
    - 206005  Failed to get validation data objects from database.
    
    """
    output: List[ValidationAgentOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DatasetFileInfoCAD(TcBaseObj):
    """
    The DatasetFileInfoCAD struct represents all of the data necessary to construct the named references in the dataset
    referenced by validation data and validation result.
    
    :var clientId: Unique client identifier string.
    :var fileName: File name including the path. It cannot be NULL.
    :var namedReferencedName: Name for the named reference. If it is NULL, the reference name in preference
    TC_VALIDATION_FILE_TYPES based on first file extension in the fileinfos will be used.
    :var textFlag: Flag to indicate whether it is binary file or an ASCII text file. Valid values are 0, 1, and 2. 
    0 means it will be decided by system based on reference name, 1 means text file, while 2 means binary file.
    """
    clientId: str = ''
    fileName: str = ''
    namedReferencedName: str = ''
    textFlag: int = 0


@dataclass
class DatasetFileTicketInfoCAD(TcBaseObj):
    """
    The DatasetFileTicketInfoCAD struct contains the information for dataset and its file ticket.
    
    :var datasetFileInfo: The structure contains name reference data, associated file name, file type of a dataset.
    :var ticket: The FMS ticket string of a file for the dataset.
    """
    datasetFileInfo: DatasetFileInfoCAD = None
    ticket: str = ''


@dataclass
class DatasetInfo(TcBaseObj):
    """
    The DatasetInfo struct represents all of the data necessary to construct the dataset object.
    
    :var clientId: Unique client identifier string.
    :var name: The name for a dataset. If NULL, a name will be automatically generated for the new dataset.
    :var type: A dataset type name string. If it is NULL, the type in preference TC_VALIDATION_FILE_TYPES based on the
    first file extension in the fileinfos input parameter will be used.
    :var fileInfos: Information about files attached to the dataset.
    """
    clientId: str = ''
    name: str = ''
    type: str = ''
    fileInfos: List[DatasetFileInfoCAD] = ()


@dataclass
class DatasetOutput(TcBaseObj):
    """
    The DatasetOutput struct contains the created or updated dataset and its file ticket information for the named
    reference.
    
    :var clientId: Unique client identifier string.
    :var dataset: Pointer to a dataset object.
    :var datasetFileTicketInfos: The FMS file ticket info for the dataset.
    """
    clientId: str = ''
    dataset: Dataset = None
    datasetFileTicketInfos: List[DatasetFileTicketInfoCAD] = ()
