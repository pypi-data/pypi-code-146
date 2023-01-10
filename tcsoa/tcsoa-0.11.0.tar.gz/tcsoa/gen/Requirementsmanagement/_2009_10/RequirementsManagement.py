from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0ParamReqmentRevision, Fnd0ListsParamReqments
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetStdNoteParamAndValues(TcBaseObj):
    """
    'GetStdNoteParamAndValues' structure defines the name and value pair of each parameter for
    Fnd0ParamReqmentRevision. Each Parameter has list of values. And 'assignedValue' has the value of parameter for
    Fnd0ParamReqmentRevision when it is in context.
    
    :var parameter: Parameter name. Example-Temperature
    :var values: List of values for given parameter. Example. For above parameter Temperature list of values can be :
    0, 10, 20, 30, 40
    :var assignedValue: Current value of Parameter. Example. From the list of values as mentioned for values elements,
    the assignedValue for any specific context with relation 'Fnd0ListsParamReqments' can be say "10" or "20" for
    selected parameter type.
    """
    parameter: str = ''
    values: List[str] = ()
    assignedValue: str = ''


@dataclass
class OpenStdNoteContents(TcBaseObj):
    """
    OpenStdNoteContents structure contains input structure provided to this operation StdNoteInput, note text of
    Fnd0ParamReqmentRevision object which user want to see/edit, body_text of Fnd0ParamReqmentRevision object, and map
    of the parameter and values for the Fnd0ParamReqmentRevision object.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var inputDetails: 'StdNoteInput' structure given as input this operation.
    :var parametersOnRelation: A list of 'GetStdNoteParamAndValues' which gives the list of parameters and their values
    for Fnd0ParamReqmentRevision object.
    :var noteText: Note Text of Fnd0ParamReqmentRevision object. In this note text user can type any text, and
    parameter, and its value pair in below format
     [<param1 name>: value1, value2,..]
    Example [Temperature:0,10,20,30]
    :var templateText: body_text property of Fnd0ParamReqmentRevision object.
    """
    clientId: str = ''
    inputDetails: StdNoteInput = None
    parametersOnRelation: List[GetStdNoteParamAndValues] = ()
    noteText: str = ''
    templateText: str = ''


@dataclass
class OpenStdNoteResponse(TcBaseObj):
    """
    'OpenStdNoteResponse' structure represents list of 'OpenStdNoteContents' structure along with the ServiceData.
    
    :var openNoteObjectsDetails: A list of 'GetStdNoteParamAndValues' structure that hold the information of
    Fnd0ParamReqmentRevision objects parameter values set in the context, note text, body_text property of
    Fnd0ParamReqmentRevision, and input structure as 'StdNoteInput'.
    :var sreviceData: The Service Data.
    """
    openNoteObjectsDetails: List[OpenStdNoteContents] = ()
    sreviceData: ServiceData = None


@dataclass
class SetStdNoteDetails(TcBaseObj):
    """
    'SetStdNoteDetails' structure represents Standard Note/Parametric Requirement details with note relation object,
    and values to set on Standard note relation.
    
    :var inputNoteDetails: A 'StdNoteInput' structure that hold the information of Standard note object and Standard
    note relation.
    :var values: List of Values to be set on Standard note.
    """
    inputNoteDetails: StdNoteInput = None
    values: List[SetStdNoteParameters] = ()


@dataclass
class SetStdNoteParameters(TcBaseObj):
    """
    'SetStdNoteParameters' structure represents Parameter and its value to be set on Standard Note Relation object.
    
    :var parameter: Name of parameter.
    :var value: Value to be set on parameter from the list of values.
    """
    parameter: str = ''
    value: str = ''


@dataclass
class SetStdNoteResponse(TcBaseObj):
    """
    'SetStdNoteResponse' structure represents list of 'SetStdNoteResult' structure containing Standard Note details
    along with the ServiceData.
    
    :var resultObjects: A list of 'SetStdNoteResult' structure that hold the information of Standard Note objects.
    :var serviceData: The Service Data.
    """
    resultObjects: List[SetStdNoteResult] = ()
    serviceData: ServiceData = None


@dataclass
class SetStdNoteResult(TcBaseObj):
    """
    'SetStdNoteResult' structure defines the output for each note when set Note SOA operation is invoked. It returns
    the new note text value set on parametreized Requirement.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var standardNote: Standard Note/Parametric Requirement Revision object.
    :var noteText: Value of new Note Text on Standard Note/Parametric Requirement Revision object
    """
    clientId: str = ''
    standardNote: Fnd0ParamReqmentRevision = None
    noteText: str = ''


@dataclass
class StdNoteInput(TcBaseObj):
    """
    'StdNoteInput' structure represents the input parameters of setting Standard note values. It includes Standard
    Note/Parametric Requirement Revision object and the object of 'Fnd0ListsParamReqments' relation by which it is
    attached to any Item/ ItemRevision.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var standardNote: Tag of Fnd0ParamReqmentRevision object.
    :var stdNoteRelation: Relation object of type Fnd0ListParamRequirements by which Fnd0ParamReqmentRevision is
    attached to selected object revision.
    """
    clientId: str = ''
    standardNote: Fnd0ParamReqmentRevision = None
    stdNoteRelation: Fnd0ListsParamReqments = None
