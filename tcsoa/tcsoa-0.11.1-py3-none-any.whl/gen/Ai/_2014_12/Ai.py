from __future__ import annotations

from tcsoa.gen.BusinessObjects import AppInterface
from tcsoa.gen.Ai._2006_03.Ai import ApplicationRef
from tcsoa.gen.Ai._2008_06.Ai import Configuration
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetMappedAppRefsInput(TcBaseObj):
    """
    GetMappedAppRefsInput structure contains a Application Reference representing the object for which Application
    References of different Application name are needed, the Configuration to be used if Application Reference is of
    Teamcenter PSOccurrenceThread chain, and a list of Application names.
    
    :var configuration: A optional element only used if the appRef is of "Teamcenter" application and is a
    PSOccurrenceThread chain. If not used, the useDefaultRevistionRule member should be set to false and existingWindow
    should be set to NULL.
    :var appRefs: A list of 3-tuple each consisting of application name, label string and version string to represent
    the objects for which Application References are needed. For each Application Reference in the list, there will be
    appNames number of Application References.
    :var appNames: A list of strings representing the names of Applications for which the "appRef" values are needed.
    Atleast one value must be provided. Valid value for Teamcenter is "Teamcenter".
    """
    configuration: Configuration = None
    appRefs: List[ApplicationRef] = ()
    appNames: List[str] = ()


@dataclass
class GetMappedAppRefsResponse(TcBaseObj):
    """
    GetMappedAppRefsResponseElement returns the Application References for each input appref for each input appname.
    The vector is laid out sequencially - all the apprefs for each appName following each other.
    
    :var appRefs: A list of GetMappedRefsResponseElement structures.
    :var serviceData: Service data capturing partial errors using the input array index as client id.
    """
    appRefs: List[GetMappedAppRefsResponseElement] = ()
    serviceData: ServiceData = None


@dataclass
class GetMappedAppRefsResponseElement(TcBaseObj):
    """
    Element corresponding to each element in the input containing the details of the desired Application Reference. The
    layout of the vector corresponds to appRef values for each appName in sequence.
    
    :var appRefs: A list of Application Reference elements corresponding to the Application names specified in the
    input element.
    """
    appRefs: List[ApplicationRef] = ()


@dataclass
class CreateAppInterfaceRecordInput(TcBaseObj):
    """
    CreateAppInterfaceRecordInput structure contains a AppInterface object and PLMXML labels for which corresponding
    RecordObjects are to be created and associated with the MasterRecord of the input AppInterface object.
    
    :var ai: The ApplicationInterface object whose MasterRecord is to be modified with the newly created RecordObjects
    based on the labels.
    :var labels: A list of strings in the label format of PLMXML Application Reference element.
    """
    ai: AppInterface = None
    labels: List[str] = ()


@dataclass
class CreateAppInterfaceRecordOutput(TcBaseObj):
    """
    CreateAppInterfaceRecordOutput returns the PLMXML style labels for which the RecordObjects could not be created and
    the corresponding reason for failure.
    
    :var failedLabels: A list of labels for which  RecordObjects could not be created.
    :var reasons: A list of strings each indicating the reason for failure.
    """
    failedLabels: List[str] = ()
    reasons: List[str] = ()


@dataclass
class CreateAppInterfaceRecordsResponse(TcBaseObj):
    """
    CreateAppInterfaceRecordsResponse structure contains a vector of CreateAppInterfaceRecordOutput, the size of which
    matches the input vector. It also includes the standard serviceData object.
    
    :var output: A list of CreateAppInterfaceRecordOutput structures.
    :var serviceData: Service data capturing partial errors using the input array index as client id.
    """
    output: List[CreateAppInterfaceRecordOutput] = ()
    serviceData: ServiceData = None
