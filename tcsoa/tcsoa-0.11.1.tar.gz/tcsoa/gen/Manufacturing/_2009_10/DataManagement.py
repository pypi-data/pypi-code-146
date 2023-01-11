from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateIn(TcBaseObj):
    """
    Input for create operation including unique client identifier
    
    :var clientId: Unique client identifier
    :var context: The context for the new created object
    :var target: The target  to connect to
    :var relationName: The name of the relation to use to connect to the target. If the string is empty then the
    relation defined as default will be used.
    :var data: Input data for create operation
    """
    clientId: str = ''
    context: BusinessObject = None
    target: BusinessObject = None
    relationName: str = ''
    data: CreateInput = None


@dataclass
class CreateInput(TcBaseObj):
    """
    CreateInput structure used to capture the inputs required for creation of a business object. This is a recursive
    structure containing the CreateInput(s) for any secondary (compounded) objects that might be created (e.g Item also
    creates ItemRevision and ItemMasterForm, etc.)
    
    :var type: Business Object type name
    :var stringProps: Map containing string property values
    :var boolArrayProps: Map containing string array property values
    :var dateProps: Map containing DateTime property values
    :var dateArrayProps: Map containing DateTime array property values
    :var tagProps: Map containing string property values
    :var tagArrayProps: Map containing string array property values
    :var compoundCreateInput: CreateInput for compounded objects
    :var stringArrayProps: Map containing string array property values
    :var doubleProps: Map containing string property values
    :var doubleArrayProps: Map containing string array property values
    :var floatProps: Map containing string property values
    :var floatArrayProps: Map containing string array property values
    :var intProps: Map containing string property values
    :var intArrayProps: Map containing string array property values
    :var boolProps: Map containing string property values
    """
    type: str = ''
    stringProps: StringMap = None
    boolArrayProps: BoolVectorMap = None
    dateProps: DateMap = None
    dateArrayProps: DateVectorMap = None
    tagProps: TagMap = None
    tagArrayProps: TagVectorMap = None
    compoundCreateInput: CreateInputMap = None
    stringArrayProps: StringVectorMap = None
    doubleProps: DoubleMap = None
    doubleArrayProps: DoubleVectorMap = None
    floatProps: FloatMap = None
    floatArrayProps: FloatVectorMap = None
    intProps: IntMap = None
    intArrayProps: IntVectorMap = None
    boolProps: BoolMap = None


@dataclass
class CreateOut(TcBaseObj):
    """
    Output for create operation including unique client identifier
    
    :var clientId: Unique client identifier
    :var objects: Vector of tags representing objects that were created
    """
    clientId: str = ''
    objects: List[BusinessObject] = ()


@dataclass
class CreateResponse(TcBaseObj):
    """
    Response object for create operation
    
    :var output: Vector of output objects representing objects that were created
    :var serviceData: Service data including partial errors that are mapped to the client id
    """
    output: List[CreateOut] = ()
    serviceData: ServiceData = None


@dataclass
class DisconnectInput(TcBaseObj):
    """
    Input for disconnect operation
    
    :var clientId: Unique client identifier
    :var object: The object to disconnect
    :var disconnectFrom: The object to disconnect from
    :var relationName: The relation to disconnect in case 2 objects are connected by more than one relation
    """
    clientId: str = ''
    object: BusinessObject = None
    disconnectFrom: BusinessObject = None
    relationName: str = ''


"""
CreateInputMap
"""
CreateInputMap = Dict[str, List[CreateInput]]


"""
DateMap
"""
DateMap = Dict[str, datetime]


"""
DateVectorMap
"""
DateVectorMap = Dict[str, List[datetime]]


"""
DoubleMap
"""
DoubleMap = Dict[str, float]


"""
DoubleVectorMap
"""
DoubleVectorMap = Dict[str, List[float]]


"""
FloatMap
"""
FloatMap = Dict[str, float]


"""
FloatVectorMap
"""
FloatVectorMap = Dict[str, List[float]]


"""
IntMap
"""
IntMap = Dict[str, int]


"""
IntVectorMap
"""
IntVectorMap = Dict[str, List[int]]


"""
StringMap
"""
StringMap = Dict[str, str]


"""
BoolMap
"""
BoolMap = Dict[str, bool]


"""
StringVectorMap
"""
StringVectorMap = Dict[str, List[str]]


"""
BoolVectorMap
"""
BoolVectorMap = Dict[str, List[bool]]


"""
TagMap
"""
TagMap = Dict[str, BusinessObject]


"""
TagVectorMap
"""
TagVectorMap = Dict[str, List[BusinessObject]]
