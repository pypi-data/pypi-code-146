from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2009_10.DataManagement import CreateInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ApplyConfigInput(TcBaseObj):
    """
    Structure containing the configuration information and the context on which configuration needs to be applied.
    
    :var configObj: Object holding the configuration information that needs to be applied
    :var context: The context to which the configuration needs to be applied.
    """
    configObj: BusinessObject = None
    context: BusinessObject = None


@dataclass
class CreateConfigInput(TcBaseObj):
    """
    Object containing input information for createOrUpdateConfigObjects action.
    
    :var data: CreateInput structure used to capture the inputs required for creation of a business object.
    :var modifyObject: Object to be modified.
    :var basedOn: Top line of the BOMWindow object in case of StructureContext or ConfigurationContext, Null in case of
    CollaborationContext.
    :var internalConfigData: Internal related config objects. For a CC, this would be a vector of SCs. For an SC, this
    would be a Config Context. For ConfigContext, this would be null.
    """
    data: CreateInput = None
    modifyObject: BusinessObject = None
    basedOn: BusinessObject = None
    internalConfigData: List[CreateConfigInput] = ()


@dataclass
class CreateConfigOutput(TcBaseObj):
    """
    Object containing information related to createOrUpdateConfigObjects action.
    
    :var object: Configuration object created or modified as per input.
    :var context: The context based on which configuration object is created.
    :var internalConfigData: Data regarding created and updated internal nested configuration objects.
    """
    object: BusinessObject = None
    context: BusinessObject = None
    internalConfigData: List[CreateConfigOutput] = ()


@dataclass
class CreateConfigResponse(TcBaseObj):
    """
    Response for createOrUpdateConfigObjects action.
    
    :var output: Object of CreateConfigOutput.
    :var serviceData: Service data including partial errors.
    """
    output: List[CreateConfigOutput] = ()
    serviceData: ServiceData = None
