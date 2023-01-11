from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ChangeTypeInfo(TcBaseObj):
    """
    Structure holds the Change type information.
    
    :var typeName: Name of the Change type.
    :var typeDisplayName: Display name of the Change type.
    """
    typeName: str = ''
    typeDisplayName: str = ''


@dataclass
class ContextDataInput(TcBaseObj):
    """
    The parameters required to find the creatable ChangeItem type.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var object: Context data for creating ChangeItem types. If this input is not specified then the allowed Change
    types will be determined based only on the conditions specified for Change type creation in BMIDE. This input is
    used to determine the Change types that are allowed to be created for creating derive Change objects.
    Note: The calling client is responsible for converting the inputs to a string using the appropriate function(s) in
    the SOA client framework Property class (i.e. Property.toDateString).
    :var baseTypeName: Base type name. If this input is specified then all the Change types in this type hierarchy will
    be evaluated. If not specified then all the change types in ChangeItem hierarchy will be evaluated for determining
    the allowed change types. Valid value for this input is ChangeItem or its sub type.
    :var exclusionTypeNames: A list of Change types to be excluded from the returned list. If this input is specified
    then Change types specified in this list will be excluded while determining the allowed Change types. Valid value
    for this input is ChangeItem or its sub type.
    """
    clientId: str = ''
    object: str = ''
    baseTypeName: str = ''
    exclusionTypeNames: List[str] = ()


@dataclass
class CreatableChangeTypesOut(TcBaseObj):
    """
    This is output of getCreatableChangeTypes operation.
    
    :var clientId: The unmodified value from the ContextDataInput.clientId. This can be used by the caller to indentify
    this data structure with the source input data.
    :var allowedChangeTypes: A list of ChangeTypeInfo representing Change types that are allowed to be created.
    """
    clientId: str = ''
    allowedChangeTypes: List[ChangeTypeInfo] = ()


@dataclass
class CreatableChangeTypesResponse(TcBaseObj):
    """
    This is response Structure of getCreatableChangeTypes operation.
    
    :var output: A list of CreatableChangeTypesOut objects representing ChangeTypeInfo objects.
    :var serviceData: Service data including partial errors that are mapped to the client id.
    """
    output: List[CreatableChangeTypesOut] = ()
    serviceData: ServiceData = None
