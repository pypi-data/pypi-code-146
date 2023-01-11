from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ItemRevision, Dataset
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InsertDatasetVersionArgs(TcBaseObj):
    """
    The InsertDatasetVersionArgs struct is used to pass in multiple sets of data
    to be used in a single call.  These structs are passed in the collection of
    input arguments to the function insertDatasetVersion.
    
    :var dataset: The Dataset of you would like insert a version.
    :var versionNumber: The version number you would like to insert.
    """
    dataset: BusinessObject = None
    versionNumber: int = 0


@dataclass
class InsertDatasetVersionResponse(TcBaseObj):
    """
    The InsertDatasetVersionResponse struct is the output values for the call to
    the function insertDatasetVersion.
    
    :var datasetTags: A two(2) element array where the first element represents the Dataset version which was inserted
    and the second element representing the zero Dataset.
    :var svcData: The service data needed to pass the above values back.
    """
    datasetTags: List[BusinessObject] = ()
    svcData: ServiceData = None


@dataclass
class QueryTranslationRequestsArgs(TcBaseObj):
    """
    The QueryTranslationRequestsArgs is the possible data to be used in querying for Translation
    Request objects.  These values can all be set, some of them, etc.
    
    If none of the values are set, then 0 items will be returned and the query
    will be skipped.
    
    :var providers: A list of providers.
    :var services: A list of services (i.e. translators)
    :var states: A list of states (i.e. INITIAL, TERMINAL)
    :var priorities: A list of priorities (i.e. 1,2,3)
    :var modifiedDate: A modified before date.  This is only a single date and
    not a list of them because that would create a range and
    not a before date.
    :var primaryObjects: The primary objects (i.e. Datasets)
    :var taskIDs: taskIDs
    """
    providers: List[str] = ()
    services: List[str] = ()
    states: List[str] = ()
    priorities: List[int] = ()
    modifiedDate: str = ''
    primaryObjects: List[BusinessObject] = ()
    taskIDs: List[str] = ()


@dataclass
class QueryTranslationRequestsOutput(TcBaseObj):
    """
    The QueryTranslationRequestsOutput struct is the output structure containing the requests
    that were returned from the corresponding input arguments to the query.
    
    :var queriedRequests: A list of the ETSTranslationRequests returned from the query within the Teamcenter database.
    """
    queriedRequests: List[BusinessObject] = ()


@dataclass
class QueryTranslationRequestsResponse(TcBaseObj):
    """
    The QueryTranslationRequestsResponse struct is the output values for the call to
    the function queryTranslationRequests.
    
    :var outputObjects: A list of the output data associated with this call.
    :var svcData: he service data needed to pass the above values back.
    """
    outputObjects: List[QueryTranslationRequestsOutput] = ()
    svcData: ServiceData = None


@dataclass
class UpdateTranslationRequestArgs(TcBaseObj):
    """
    The UpdateTranslationRequestArgs is the possible data to be used in updating a
    Translation Request object.
    
    :var requestToUpdate: The Translation Request to update.  This value MUST be
    set and can not be empty.
    :var priority: The priority to assign to the request. (0 LOW to 3 HIGH)
    :var currentState: The current state of the request.  This value is used as a safety check when setting the
    nextState of the request to make sure we have the current up to date request.
    :var nextState: The next state to assign to the request.
    
    Valid states include: COMPLETE, DUPLICATE, DELETE, CANCELLED, SUPERSEDED, NO_TRANS, PREPARING, SCHEDULED,
    SUPERSEDING, TRANSLATING, LOADING
    
    :var taskID: The task ID to assign to the request.
    :var translatorArgs: The translator arguments to assign to the request.  This will override the current translator
    arguments and is not append to the current list.
    """
    requestToUpdate: BusinessObject = None
    priority: int = 0
    currentState: str = ''
    nextState: str = ''
    taskID: str = ''
    translatorArgs: List[str] = ()


@dataclass
class UpdateTranslationRequestOutput(TcBaseObj):
    """
    The UpdateTranslationRequestOutput struct is the output structure containing the request
    that was updated and a boolean value stating if the request was updated.
    
    :var requestUpdated: This is the request that was updated and should be the
    request that the client was previously referencing.
    :var wasRequestUpdated: This is a boolean representing whether or not the request
    was successfully updated.
    """
    requestUpdated: BusinessObject = None
    wasRequestUpdated: bool = False


@dataclass
class UpdateTranslationRequestResponse(TcBaseObj):
    """
    The UpdateTranslationRequestResponse struct is the output values for the call to
    the function updateTranslationRequest.
    
    :var outputObjects: A list of the output data associated with this call.
    :var svcData: The service data needed to pass the above values back.
    """
    outputObjects: List[UpdateTranslationRequestOutput] = ()
    svcData: ServiceData = None


@dataclass
class CreateDatasetOfVersionArgs(TcBaseObj):
    """
    The CreateDatasetOfVersionArgs is used to carry the data needed to create a Dataset of a particular version.  This
    is similar to the core create Dataset method with the exception that this method takes a specific version and
    creates the Dataset at that version even if it is the first instance of that Dataset.
    
    :var itemRevision: After creation, any release status assigned to this ItemRevision will be copied to the Dataset.
    :var datasetName: The name of the Dataset to create.
    :var typeName: The type of the Dataset to create.
    :var tool: The Tool to associate with the new Dataset.
    :var version: The version to assign to the new Dataset.
    """
    itemRevision: ItemRevision = None
    datasetName: str = ''
    typeName: str = ''
    tool: BusinessObject = None
    version: int = 0


@dataclass
class CreateDatasetOfVersionResponse(TcBaseObj):
    """
    The CreateDatasetOfVersionResponse structure is the output values for the call to the function
    createDatasetOfVersion.
    
    :var createdDatasets: A list of the Datasets created corresponding to the list of input data.
    :var svcData: The service data needed to pass the above values back.
    """
    createdDatasets: List[Dataset] = ()
    svcData: ServiceData = None
