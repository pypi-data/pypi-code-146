from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateIn2(TcBaseObj):
    """
    This is input structure for create operation including unique client identifier.
    
    :var clientId: Unique client identifier
    :var createData: Input data for create operation
    :var dataToBeRelated: Additional input data .This data will be related to the created object by the given property.
    User need to pass the data in this key-value pair format: Property - array of data
    :var workflowData: Input data required for workflow creation. User need to pass the data in this key-value pair
    format:submitToWorkflow - true/false.
    NOTE: If the above option is "true" then workflow process template to be used for workflow creation should be
    specified in the preference (TypeName_default_workflow_template ) defined for the created object type.
    :var targetObject: Target to which created object will be pasted
    :var pasteProp: Property to be used to paste the created object to  the target
    """
    clientId: str = ''
    createData: CreateInput2 = None
    dataToBeRelated: PropertyValues = None
    workflowData: PropertyValues = None
    targetObject: BusinessObject = None
    pasteProp: str = ''


@dataclass
class CreateInput2(TcBaseObj):
    """
    CreateInput2 structure used to capture the inputs required for creation of a business object. This is a recursive
    structure containing the CreateInput(s) for any secondary(compounded) objects that might be created (e.g Item also
    creates ItemRevision and ItemMasterForm etc.)
    
    :var boName: Business Object type name
    :var propertyNameValues: Map of property name (key) and property values (values) in string format, to be set on new
    object being created. 
    Note: The calling client is responsible for converting the different property types (int, float, date .etc) to a
    string using the appropriate function(s) in the SOA client framework Property class.
    :var compoundCreateInput: CreateInput for compounded objects
    """
    boName: str = ''
    propertyNameValues: PropertyValues = None
    compoundCreateInput: CreateInputMap = None


@dataclass
class CreateOut2(TcBaseObj):
    """
    This is output structure for create operation including unique client identifier.
    
    :var clientId: Unique client identifier
    :var objects: List of tags representing objects that were created
    """
    clientId: str = ''
    objects: List[BusinessObject] = ()


@dataclass
class CreateResponse2(TcBaseObj):
    """
    This is response object structure for create operation.
    
    :var output: List of output objects representing objects that were created
    :var serviceData: Service data including partial errors that are mapped to the client id
    """
    output: List[CreateOut2] = ()
    serviceData: ServiceData = None


"""
CreateInputMap is a map of reference or relation property name to secondary CreateInput2 objects.
"""
CreateInputMap = Dict[str, List[CreateInput2]]


"""
PropertyValues is a map of property name (key) and property values (values) in string format.
"""
PropertyValues = Dict[str, List[str]]
