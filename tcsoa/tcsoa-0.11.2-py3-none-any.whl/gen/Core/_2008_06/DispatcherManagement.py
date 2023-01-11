from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class KeyValueArguments(TcBaseObj):
    """
    This structure represents the key/value pairs that can be attached to the Dispatcher Request.
    
    :var key: The key of the key/value pair.
    :var value: The value of the key/value pair.
    """
    key: str = ''
    value: str = ''


@dataclass
class CreateDispatcherRequestArgs(TcBaseObj):
    """
    The CreateDispatcherRequestArgs struct is used to pass in multiple sets of data to be used in a single call.  These
    structs are passed in the collection of input arguments to the function createDispatcherRequest.
    
    :var providerName: The primary objects for the request.  This usually refers to a dataset to translate but can be
    any component.
    :var serviceName: The secondary objects for the request.  This usually refers to the Item Revision containing the
    primary objects.
    :var type: The type of this request (USER SPECIFIED)
    :var primaryObjects: The provider name to process the request.
    :var secondaryObjects: The service from the above provider to process the request.
    :var priority: The priority to assign to the request.
    :var startTime: The start time to start the request.
    :var endTime: The end time at which no new requests will be created based on interval setting.  If request is still
    processing, the request WILL be completed and will not be stopped.
    :var interval: The number of times to repeat a given request.
    :var keyValueArgs: The key/value arguments for the request.
    :var dataFiles: The key/file arguments for the request.
    """
    providerName: str = ''
    serviceName: str = ''
    type: str = ''
    primaryObjects: List[BusinessObject] = ()
    secondaryObjects: List[BusinessObject] = ()
    priority: int = 0
    startTime: str = ''
    endTime: str = ''
    interval: int = 0
    keyValueArgs: List[KeyValueArguments] = ()
    dataFiles: List[DataFiles] = ()


@dataclass
class CreateDispatcherRequestResponse(TcBaseObj):
    """
    The CreateDispatcherRequestResponse struct contains the requests that were created as a result of the inputs
    specified in the CreateDispatcherRequestArgs structure above.
    
    :var requestsCreated: The Dispatcher Request objects created.
    :var svcData: The SOA Service Data.
    """
    requestsCreated: List[BusinessObject] = ()
    svcData: ServiceData = None


@dataclass
class DataFiles(TcBaseObj):
    """
    This structure represents the key/file pairs that can be attached to the Dispatcher Request.
    
    :var key: The key of the key/file pair.
    :var file: file
    """
    key: str = ''
    file: ImanFile = None
