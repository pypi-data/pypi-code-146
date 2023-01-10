from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ClassificationObjectResponse(TcBaseObj):
    """
    Holds information on created, updated or deleted classification objects.
    
    :var jsonResponse: This is a JSON string containing information about the created, updated, retrieved or deleted
    classification objects.
    Any failures occurred during the operation will be specified in the JSON string under the 'ErrorDetails' container.
    The response structure will follow the JSON schema defined in the file:
    TC_DATA\classification\json\1.0.0\schema\Response.schema.json.
    Refer the following sample responses for operations on classification objects:
    Save and Retrieve:- TC_DATA\classification\json\1.0.0\samples\GetClassificationObjects_Response_sample.json
    Delete:- TC_DATA\classification\json\1.0.0\samples\DeleteClassificationObjects_Response_sample.json
    Error:- TC_DATA\classification\json\1.0.0\samples\SaveClassificationObjects_Error_Response_sample.json
    :var serviceData: This is a placeholder for future use. All information about the created, updated and deleted
    classification objects and any errors, occurred during the operation, will be returned in the JSON response string.
    """
    jsonResponse: str = ''
    serviceData: ServiceData = None
