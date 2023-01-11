from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile, ItemRevision, Dataset
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InsertDatasetVersionArgs(TcBaseObj):
    """
    The InsertDatasetVersionArgs struct is used to pass multiple sets of data to be used in a single call.  These
    structures are passed in the collection of input arguments to the function insertDatasetVersion.
    
    :var dataset: The Dataset of you would like insert a version.
    :var versionNumber: The version number you would like to insert.
    """
    dataset: BusinessObject = None
    versionNumber: int = 0


@dataclass
class InsertDatasetVersionResponse(TcBaseObj):
    """
    The InsertDatasetVersionResponse struct is the output values for the call to the function insertDatasetVersion.
    
    :var datasetTags: A 2 element array where the first element represents the dataset version tag and the second
    element represents the zero (0) dataset tag.
    :var svcData: The service data needed to pass the above values back.
    """
    datasetTags: List[BusinessObject] = ()
    svcData: ServiceData = None


@dataclass
class InternalDataFiles(TcBaseObj):
    """
    This structure represents the key/file pairs that can be attached to the Dispatcher Request.
    
    :var key: The key of the key/file pair.
    :var file: file
    """
    key: str = ''
    file: ImanFile = None


@dataclass
class InternalKeyValueArguments(TcBaseObj):
    """
    This structure represents the key/value pairs that can be attached to the Dispatcher Request.
    
    :var key: The key of the key/value pair.
    :var value: The value of the key/value pair.
    """
    key: str = ''
    value: str = ''


@dataclass
class QueryDispatcherRequestsArgs(TcBaseObj):
    """
    The QueryDispatcherRequestsArgs is the possible data to be used in querying for DispatcherRequests.  Ant
    combination of the available data can be set.  If none of the values are set though, no items will be returned and
    the query will be skipped.
    
    :var providers: A list of providers.
    :var services: A list of services
    :var states: A list of states (i.e. INITIAL, TERMINAL)
    :var priorities: A list of priorities (i.e. 1,2,3)
    :var modifiedDate: A modified before date.  This is only a single date and not a list of them because that would
    create a range and not a before date.
    :var primaryObjects: The primary objects (i.e. Datasets)
    :var taskID: The task identifier of the request.  This is helpful for loading a specific request.
    :var type: The type of the request.
    :var unLoaded: If the service data should NOT be loaded with returning object.
    """
    providers: List[str] = ()
    services: List[str] = ()
    states: List[str] = ()
    priorities: List[int] = ()
    modifiedDate: str = ''
    primaryObjects: List[BusinessObject] = ()
    taskID: List[str] = ()
    type: List[str] = ()
    unLoaded: bool = False


@dataclass
class QueryDispatcherRequestsOutput(TcBaseObj):
    """
    The QueryDispatcherRequestsOutput struct is the output structure containing the requests that were returned from
    the corresponding input arguments to the query.
    
    :var queriedRequests: A list of the ETSDispatcherRequests returned from the query within the Teamcenter database.
    """
    queriedRequests: List[BusinessObject] = ()


@dataclass
class QueryDispatcherRequestsResponse(TcBaseObj):
    """
    The QueryDispatcherRequestsResponse struct is the output values for the call to the function
    queryDispatcherRequests.
    
    :var outputObjects: A list of the output data associated with this call.
    :var svcData: The service data needed to pass the above values back.
    """
    outputObjects: List[QueryDispatcherRequestsOutput] = ()
    svcData: ServiceData = None


@dataclass
class UpdateDispatcherRequestArgs(TcBaseObj):
    """
    The UpdateDispatcherRequestArgs is the possible data to be used in updating a Dispatcher Request object.
    
    :var requestToUpdate: The DispatcherRequest to update.  This value MUST be set and cannot be empty.
    :var currentState: The current state of the request.  This value is used as a safety check when setting the
    nextState of the request to make sure we have the current up to date request.
    :var nextState: The next state to assign to the request.
    :var type: type
    :var keyValueArgs: The key/value args to assign to the request.  This will override the current argument if it
    exist or add the new argument to the list.
    :var dataFiles: The data files to assign to the request.  This will override the current data file if it exist or
    add the new data file to the list.
    """
    requestToUpdate: BusinessObject = None
    currentState: str = ''
    nextState: str = ''
    type: str = ''
    keyValueArgs: List[InternalKeyValueArguments] = ()
    dataFiles: List[InternalDataFiles] = ()


@dataclass
class UpdateDispatcherRequestOutput(TcBaseObj):
    """
    The UpdateDispatcherRequestOutput struct is the output structure containing the request that was updated and a
    boolean value stating if the request was updated.
    
    :var requestUpdated: This is the request that was updated and should be the request that the client was previously
    referencing.
    :var wasRequestUpdated: This is a boolean representing whether or not the request was successfully updated.
    """
    requestUpdated: BusinessObject = None
    wasRequestUpdated: bool = False


@dataclass
class UpdateDispatcherRequestResponse(TcBaseObj):
    """
    The UpdateDispatcherRequestResponse struct is the output values for the call to the function
    updateDispatcherRequest.
    
    :var outputObjects: A list of the output data associated with this call.
    :var svcData: The service data needed to pass the above values back.
    """
    outputObjects: List[UpdateDispatcherRequestOutput] = ()
    svcData: ServiceData = None


@dataclass
class CreateDatasetOfVersionArgs(TcBaseObj):
    """
    The CreateDatasetOfVersionArgs is used to carry the data needed to create a dataset of a particular version.  This
    is similar to the core create dataset method with the exception that this method takes a specific version and
    creates the dataset at that version even if it is the first instance of that dataset.
    
    :var itemRevision: The ItemRevision to relate the new Dataset to once created.
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
    The CreateDatasetOfVersionResponse struct is the output values for the call to the function createDatasetOfVersion.
    
    :var createdDatasets: A list of the Datasets created corresponding to the list of input data.
    :var svcData: The service data needed to pass the above values back.
    """
    createdDatasets: List[Dataset] = ()
    svcData: ServiceData = None
