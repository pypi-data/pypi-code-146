from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, FND_TraceLink
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateInput(TcBaseObj):
    """
    CreateInput structure used to capture the inputs required for creation of a business object. This is a recursive
    structure containing the CreateInput(s) for any secondary(compounded) objects that might be created (e.g Item also
    creates ItemRevision and ItemMasterForm etc.)
    
    :var boName: The type name of the Business Object.
    :var propertyNameValues: Map of property name (key) and property values (values) in string format, to be set on new
    object being created. The calling client is responsible for converting the different property types (int, float,
    date .etc) to a string using the appropriate function(s) in the SOA client framework Property class.
    :var compoundCreateInput: CreateInput structure used to capture the inputs required for creation of a business
    object. This is a recursive structure containing the CreateInput(s) for any secondary(compounded) objects that
    might be created (e.g Item also creates ItemRevision and ItemMasterForm etc.)
    """
    boName: str = ''
    propertyNameValues: PropertyValues = None
    compoundCreateInput: CreateInputMap = None


@dataclass
class CreateTracelinksInputData(TcBaseObj):
    """
    Structure represents the parameters required to create a tracelink between the given set of objects.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var tracelinkCreateInput: The Create Input structure which holds the necessary information to create an object of
    type FND_TraceLink or its subtypes.
    :var primaryObj: The business object which represents the Defining end of the tracelink. If it is Occurrence,
    FND_TraceLink object will be created with its underlying ItemRevision or AbsoluteOccurrence object depending on the
    input preference.
    :var secondaryObj: The business object which represents the Complying end of the tracelink. If it is Occurrence,
    FND_TraceLink object will be created with its underlying ItemRevision or AbsoluteOccurrence object depending on the
    input preference.
    :var requestPref: A map of preferences and their values (string/string). For e.g. keys could be
    createComplyingTracelinkWithOccurrence, createDefiningTracelinkWithOccurrence, createTracelinkWithOccurrences etc.
    and values could be true or false and are case sensitive.
    """
    clientId: str = ''
    tracelinkCreateInput: CreateInput = None
    primaryObj: BusinessObject = None
    secondaryObj: BusinessObject = None
    requestPref: RequestPreference2 = None


@dataclass
class CreateTracelinksResponse(TcBaseObj):
    """
    Structure represents the output parameters of the operation.
    
    :var output: A list of CreateTracelinksResponseData structures.
    :var serviceData: The Service Data.
    """
    output: List[CreateTracelinksResponseData] = ()
    serviceData: ServiceData = None


@dataclass
class CreateTracelinksResponseData(TcBaseObj):
    """
    Structure represents the output of the operation.
    
    :var clientId: The clientId from the input CreateTracelinksInputData element. This value is unchanged from the
    input, and can be used to identify this response element with the corresponding input element.
    :var tracelinkObject: The FND_TraceLink object.
    """
    clientId: str = ''
    tracelinkObject: FND_TraceLink = None


"""
PropertyValues is a map of property name (key) and property values (values) in string format.
"""
PropertyValues = Dict[str, List[str]]


"""
A map of preferences and their values. Current supported key values are createTracelinkWithOccurrences, createComplyingTracelinkWithOccurrence, createDefiningTracelinkWithOccurrence. The supported values are "true" and "false". Keys and their values both are case sensitive. 
If createComplyingTracelinkWithOccurrence is "true", the complying object for the created tracelink will be the occurrence.
If createDefiningTracelinkWithOccurrence is "true", the defining object for the created tracelink will be the occurrence. 
If createTracelinkWithOccurrences is "true", the defining and complying object for the created tracelink will be the occurrence.
"""
RequestPreference2 = Dict[str, str]


"""
CreateInputMap is a map of reference or relation property name to secondary CreateInput objects.
"""
CreateInputMap = Dict[str, List[CreateInput]]
