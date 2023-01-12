from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateAndPasteInputInfo(TcBaseObj):
    """
    CreateAndPasteInputInfo structure represents the information necessary to create a new object and paste the same.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data     elements and
    partial errors associated     with this input structure.
    :var opType: createAndPaste - use in cases where create     and paste both are needed
    pasteOnly    - use in cases where paste alone     is needed.newObject should have valid value     in this case.
    
    :var createData: Input data for create operation.
    :var newObject: The object to paste in pasteTarget in case of pasteOnly else it is NULL.
    
    :var pasteTarget: The target object onto which the newly created object is to be pasted.
    :var pasteRelation: The relation to create between the object     being pasted and paste target.If no value is    
    specified the default relation is used.
    """
    clientId: str = ''
    opType: str = ''
    createData: CreateInput = None
    newObject: BusinessObject = None
    pasteTarget: BusinessObject = None
    pasteRelation: str = ''


@dataclass
class CreateAndPasteOutput(TcBaseObj):
    """
    This structure represents the details of the output of CreateAndPaste operation.
    
    :var clientID: The clientId from the input CreateAndPasteInputInfo element.This value is unchanged from the input,
    and can be used to identify this response elementwith the corresponding input element.
    :var pasteResultObject: Runtime object resulting from the paste of newly created object.This can be null in some
    cases.E.g: Paste in a Folder object.
    :var newObject: Newly created object.
    """
    clientID: str = ''
    pasteResultObject: BusinessObject = None
    newObject: BusinessObject = None


@dataclass
class CreateAndPasteResponse(TcBaseObj):
    """
    The structure represents the output of CreateAndPaste operation.It contains the CreateAndPasteOutput object and
    ServiceData.
    
    :var output: CreateAndPasteOutput objects containing information about the newly created object and paste result
    object.
    :var serviceData: The ServiceData.
    """
    output: List[CreateAndPasteOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateConnectionPortsAndConnectInputInfo(TcBaseObj):
    """
    This structure contains the details required for creating, pasting port and connection objects and establishing
    connection between them.
    
    :var clientId: A unique string supplied by the caller. This ID is used  to identify return data elements and
    partial errors associated with this input structure.
    :var inputMap: A map of key input data (string/CreateAndPasteInputInfo) valid keys are PORT1,PORT2,CONNECTION
    :var connectCase: It can be one of the following values 
    - create2PortsConxAndConnToPorts -  Use this to create    two ports, connection and establish connection between
    them.
    - create1PortConxAndConnToPorts - Uset this to create one    port, connection and establish connection between the 
      existing port,newly created port and connection.
    - createConxConnectToPorts - Use this to create a connection and connect it to existing ports.
    - create2PortsConxExistsConnToPorts- Use this to create two ports and connect the existing connection to these
    ports.
    - create1PortConxExistsConnToPorts - Use this to create a    single port and then connect the existing connection
    to this port and existing port.
    - createConxConnToBlocks- Use this to establish connection between blocks [preference connected_ToRules should also
    allow this]
    
    
    :var objectsToConnectTo: Ports / Blocks to connect the connection.
    :var connectionObject: The Connection object if already exists.
    """
    clientId: str = ''
    inputMap: ConnectInputDataMap = None
    connectCase: str = ''
    objectsToConnectTo: List[BusinessObject] = ()
    connectionObject: BusinessObject = None


@dataclass
class CreateConnectionPortsAndConnectResponse(TcBaseObj):
    """
    This structure represents the output of createConnectionPortsAndConnect operation. It contains ConnectOutputDataMap
    object[s] and ServiceData.
    
    :var output: A map of key output data (string/ CreateAndPasteOutput) .Valid keys are PORT1,PORT2,CONNECTION
    :var serviceData: ServiceData
    """
    output: List[ConnectOutputDataMap] = ()
    serviceData: ServiceData = None


@dataclass
class CreateInput(TcBaseObj):
    """
    The parameters required to create the Business Object.
    
    :var boName: Business Object type name
    :var propertyNameValues: Map of property name (key) and property values (values) in string format, to be set on new
    object being created. Note: The calling client is responsible for converting the different property types (int,
    float, date .etc) to a string using the appropriate function(s) in the SOA client framework Property class.
    :var compoundCreateInput: CreateInput for compounded objects.
    """
    boName: str = ''
    propertyNameValues: PropNameValueMap = None
    compoundCreateInput: CreateInputMap = None


"""
Map of reference or relation property name to secondary CreateInput objects.
"""
CreateInputMap = Dict[str, List[CreateInput]]


"""
This map contains the property name and its values.
"""
PropNameValueMap = Dict[str, List[str]]


"""
Map of reference or relation property name to CreateAndPasteInputInfo     objects.
"""
ConnectInputDataMap = Dict[str, CreateAndPasteInputInfo]


"""
Map of reference or relation property name to secondary CreateAndPasteOutput    objects
"""
ConnectOutputDataMap = Dict[str, CreateAndPasteOutput]
