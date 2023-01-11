from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GenerateContextIDsInput(TcBaseObj):
    """
    This structure is the input sructure for the generateContextSpecificIDs service.
    This contains the informanion of context name and number of IDs to be generated for that context name.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify returned
    GenerateContextIDResponse elements and Partial Errors associated with this input GenerateContextIDsInput.
    :var contextName: Name of the context for which IDs to be generated. A context name is a string that can be up to
    256 characters long. This string should not be empty, in order to generate IDs, an error is returned if user tries
    to generate ID for a empty context name.
    :var numberOfIDs: Represents number of IDs to be generated for a given context name. This is a mandatory field and
    should not be 0 or any negative number to generate IDs. An error is returned, if user tries to generate ID for a
    context name with invalid value (0 or negative number) for this field.
    """
    clientID: str = ''
    contextName: str = ''
    numberOfIDs: int = 0


@dataclass
class GenerateContextSpecificIDsResponse(TcBaseObj):
    """
    Contains the returned information of generateContextSpecificIDs service.
    
    :var serviceData: Partial Errors are returned in the ServiceData when service generateContextSpecificIDs fails to
    generate IDs of any of the context name. Errors are mapped back to input context name based on the client ID field
    provided in structure GenerateContextIDsInput.
    :var generatedContextIDValues: A list of GeneratedContextIDs, which contains each of the context names and IDs
    generated for it by service generateContextSpecificIDs.
    """
    serviceData: ServiceData = None
    generatedContextIDValues: List[GeneratedContextIDs] = ()


@dataclass
class GeneratedContextIDs(TcBaseObj):
    """
    Contains the combination of context name and its generated IDs based on the user input.
    
    :var contextName: Name of the context for which IDs has been generated. This value is provided by the user in
    GenerateContextIDsInput for generating IDs.
    :var generatedIDs: List of generated IDs for a given context name. This contains one or more generated IDs for a
    given context name based on the user input in input structure GenerateContextIDsInput.
    """
    contextName: str = ''
    generatedIDs: List[str] = ()


@dataclass
class PropData(TcBaseObj):
    """
    This structure holds information about Teamcenter business object, its last saved date when exported to client and
    list of property name/value pair information.
    
    :var businessObject: The business object for which the properties to be set. All business object types are
    supported.
    :var vecPropNameVal: List of property name/value pair information.
    :var lastSavedDateExportedToClient: Last saved date of the object when object was exported to client.
    """
    businessObject: BusinessObject = None
    vecPropNameVal: List[PropertyNameValuesStruct] = ()
    lastSavedDateExportedToClient: datetime = None


@dataclass
class PropertyNameValuesStruct(TcBaseObj):
    """
    This structure contains property name, list of old values for the property and list of new values to be set for the
    property.
    
    :var propertyName: Name of the property
    :var oldValues: A vector of old values of the property for comparison with the latest database values to indentify
    any overwrite before saving. The calling client is responsible for converting the different property types (int,
    float, date etc.) to a string using the appropriate toXXXstring functions in the SOA client framerwork&rsquo;s
    Property class.
    :var newValues: A vector of new values of the property to save. The calling client is responsible for converting
    the different property types (int, float, date etc.) to a string using the appropriate toXXXstring functions in the
    SOA client framerwork&rsquo;s Property class.
    """
    propertyName: str = ''
    oldValues: List[str] = ()
    newValues: List[str] = ()


@dataclass
class SetPropsAndDetectOverwriteResponse(TcBaseObj):
    """
    Response structure for setPropertiesAndDetectOverwrite operation. It returns the information about overwritten
    objects and the properties/objects which are not saved due to conflict.
    
    :var data: This is the service data. It contains the updated objects and their properties.
    :var overwriteDetectedObjPropMap: The  map ( business object / list of string ) contains the objects and properties
    list for which overwrite condition has been detected.
    """
    data: ServiceData = None
    overwriteDetectedObjPropMap: ObjectPropertiesMap = None


"""
This map has information about object and its properties.
"""
ObjectPropertiesMap = Dict[BusinessObject, List[str]]


"""
This map has information about the name of the options and its values.
"""
OptionsMap = Dict[str, List[str]]
