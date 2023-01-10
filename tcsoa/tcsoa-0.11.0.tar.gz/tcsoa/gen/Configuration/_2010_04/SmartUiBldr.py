from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.BusinessObjects import TCX_SCConfig
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ForTypePreferences(TcBaseObj):
    """
    The ForTypePreferences structure contains the information such as Classname, Typename and the property of the
    object for which the Smart Code needs to be generated.
    
    :var className: Contains the Class Name of the object for which the Smart Code needs to be generated.
    
    :var typeName: Contains the Type Name of the object for which the Smart Code    needs to be generated.
    
    :var property: Contains the Property of the object for which the Smart Code needs to be generated.
    """
    className: str = ''
    typeName: str = ''
    property: str = ''


@dataclass
class GetPropertiesForSelectionsOutput(TcBaseObj):
    """
    The GetPropertiesForSelectionsOutput structure contains the information about the properties of selected objects
    for which the Smart Code needs to be generated.
    
    :var clientId: Contains a unique string supplied by the caller. This ID is used to identify return data and partial
    errors associated with this input structure. 
    
    :var containerWiseProperties: Contains the container name (any one of "I", "IR", "IM", "IRM") and the properties
    mapped on to this container in the form of key-value pairs.
    """
    clientId: str = ''
    containerWiseProperties: List[ContainerWiseProperties] = ()


@dataclass
class GetPropertiesForSelectionsResponse(TcBaseObj):
    """
    This structure contains the GetPropertiesForSelectionsOutput object and the ServiceData.
    
    :var output: Contains the information about the properties of selected objects for which the Smart Code needs to be
    generated.
    
    :var serviceData: Contains the successful Object ids, partial error mentioned below.
    o    258000    - If an invalid Root Component is passed, this error is added in the ServiceData.
    """
    output: GetPropertiesForSelectionsOutput = None
    serviceData: ServiceData = None


@dataclass
class GetResultForSelectionsOutput(TcBaseObj):
    """
    The GetResultForSelectionsOutput structure contains the clientID, generated Smart Code and the containerwise
    properties.
    
    :var clientId: Contains a unique string supplied by the caller. This ID is used to identify return data and partial
    errors associated with this input structure.
    
    :var resultStrings: Contains the final generated SmartCode.
    :var containerWiseProperties: Contains the container name (any one of "I", "IR", "IM", "IRM") and the properties
    mapped on to this container in the form of key-value pairs.
    """
    clientId: str = ''
    resultStrings: List[str] = ()
    containerWiseProperties: List[ContainerWiseProperties] = ()


@dataclass
class GetResultForSelectionsResponse(TcBaseObj):
    """
    This structure contains GetResultForSelectionsOutput object and the ServiceData.
    
    :var output: Contains the information about the the generated Smart Code for the given Component's Item ID as per
    the given configuration.
    :var serviceData: The successful Object ids, partial error mentioned below.
    o    258000        - If an invalid Root Component is passed, this error is added in the ServiceData.
    """
    output: GetResultForSelectionsOutput = None
    serviceData: ServiceData = None


@dataclass
class GetValuesForComponentOutput(TcBaseObj):
    """
    The structure GetValuesForComponentsOutput contains the clientID and a vector containing the next avialable Smart
    Code values.
    
    :var clientId: Contains a unique string supplied by the caller. This ID is used to identify return data and partial
    errors associated with this input structure.
    
    :var componentValues: Contains the next valid available Smart Code values for Item ID for the  given  component.
    """
    clientId: str = ''
    componentValues: List[str] = ()


@dataclass
class GetValuesForComponentResponse(TcBaseObj):
    """
    This structure contains GetValuesForComponentsOutput object and the ServiceData.
    
    :var output: Contains the information about the next avialable Smart Code values for Item ID for the given
    component.
    
    :var serviceData: The successful Object ids, partial error mentioned below.
    o    258000    -     If an invalid Root Component is passed, this error is added in the ServiceData.
    """
    output: List[GetValuesForComponentOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ListForerunnersForComponentsOutput(TcBaseObj):
    """
    The structure ListForerunnersForComponentsOutput contains the clientID and SCConfig  configuration object.
    
    :var clientId: Contains a unique string supplied by the caller. This ID is used to identify return data and partial
    errors associated with this input structure
    
    :var forerunningComponents: Contains a list of valid Smart Code configuration objects in Teamcenter.
    """
    clientId: str = ''
    forerunningComponents: List[TCX_SCConfig] = ()


@dataclass
class ListForerunnersForComponentsResponse(TcBaseObj):
    """
    The structure ListForerunnersForComponentsResponse contains the object of ListForerunnersForComponentsOutput and
    the ServiceData.
    
    :var output: Contains information about the components explicitly dependent on each of the given component
    
    :var serviceData: Contains the successful Object ids, partial error mentioned below.
    o    258000        - If an invalid Root Component is passed, this error is added in the ServiceData
    """
    output: List[ListForerunnersForComponentsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ListObjectsForComponentsOutput(TcBaseObj):
    """
    The structure ListObjectsForComponentsOutput contains the clientID and a vector of TCX_SCConfig  objects.
    
    :var clientId: Contains a unique string supplied by the caller. This ID is used to identify return data and partial
    errors associated with this input structure.
    
    :var componentsList: Contains the list of components explicitly dependent on the given component.
    """
    clientId: str = ''
    componentsList: List[TCX_SCConfig] = ()


@dataclass
class ListObjectsForComponentsResponse(TcBaseObj):
    """
    The structure contains the  ListObjectsForComponentsOutput object and the ServiceData.
    
    :var output: Contains a list of ListObjectsForComponentsoutput objects. Each object represents the components
    explicitly dependent on the given component.
    
    :var serviceData: Contains the successful Object ids, partial error mentioned below.
    o    258000        - If an invalid Root Component is passed, this error is added in the ServiceData.
    """
    output: List[ListObjectsForComponentsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ListValuesForComponentsOutput(TcBaseObj):
    """
    The structure ListValuesForComponentsOutput contains the clientID and a vector of strings.
    
    :var clientId: Contains a unique string supplied by the caller. This ID is used to identify return data and partial
    errors associated with this input structure.
    :var allowedValues: Contains the list of Smart Code values for Item IDs for the given component as per the Smart
    Code configuration set by the user.
    """
    clientId: str = ''
    allowedValues: List[str] = ()


@dataclass
class ListValuesForComponentsResponse(TcBaseObj):
    """
    The structure ListValuesForComponentsResponse contains a vector of ListValuesForComponentsOutput objects and the
    ServiceData.
    
    :var output: Contains a list of ListValuesForComponentsOutput. Each object contains a list of Smart Code values for
    Item IDs for the given component as mentioned in the Smart Code configuration by the user.
    
    :var serviceData: Contains the successful Object ids, partial error mentioned below.
    o    258000    - If an invalid Root Component is passed, this error is added in the ServiceData.
    """
    output: List[ListValuesForComponentsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ComponentInfo(TcBaseObj):
    """
    The ComponentInfo structure contains the optional clientId and the TCX_SCConfig configuration object.
    
    :var clientId: Contains  a unique identifier supplied by the caller. This ID is used to 
    track the related objects.
    :var component: Contains a valid Smart code configuration object in Teamcenter.
    """
    clientId: str = ''
    component: TCX_SCConfig = None


@dataclass
class ContainerWiseProperties(TcBaseObj):
    """
    ContainerWiseProperties structure contains the container name (any one of "I", "IR", "IM", "IRM") and the
    properties mapped on to this container in the form of key-value pairs.
    
    :var container: Contains the name of the container, which can be any one of the following -  "I", "IR", "IM" or
    "IRM".
    
    :var properties: This map contains the properties and values of Smart Code configuration object.
    """
    container: str = ''
    properties: PropertiesMap = None


"""
This map contains a key value pairs, where key is the Smart Code configuration property and the value is the user selected value for the property.
"""
CurrentSelectionsMap = Dict[str, str]


"""
This map contains the properties and values of Smart Code configuration object.
"""
PropertiesMap = Dict[str, str]
