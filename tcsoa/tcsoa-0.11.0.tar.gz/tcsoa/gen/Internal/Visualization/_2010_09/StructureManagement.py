from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, VisStructureContext, ConfigurationContext
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateVisSCInfo(TcBaseObj):
    """
    Input structure used for creating VisStrucutreContext objects based on the given inputs.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var configContext: A reference to an existing ConfigurationContext object that contains a portion of the
    configuration to be used by the output VisStructureContext object.
    
    :var topLine: Object reference of type BOMView or BOMViewRevision that is the topline of the configuration.
    
    :var occurrencesList: List of UID chain strings representing  the occurrences to be included in the structure
    recipe. If not supplied then the output VisStructureContext object will not have its occurrence_list property set.
    This will be interpreted as the top line of the BOMWindow was selected for this configuration recipe.
    
    :var staticStructureFile: IMANFile reference to the PLMXML static representation of the structure, (optional).
    """
    clientId: str = ''
    configContext: ConfigurationContext = None
    topLine: BusinessObject = None
    occurrencesList: List[str] = ()
    staticStructureFile: BusinessObject = None


@dataclass
class CreateVisSCOutput(TcBaseObj):
    """
    The output structure that contains the references to the created VisStructureContext object along with the
    corresponding 'clientId'.
    
    :var clientId: The unique string supplied by the caller used to match the output to the supplied input.
    :var structureRecipe: VisStructureContext object that records the configuration recipe based on the input
    configuration objects.
    """
    clientId: str = ''
    structureRecipe: VisStructureContext = None


@dataclass
class CreateVisSCResponse(TcBaseObj):
    """
    Response structure for the 'createVisSC' operation.
    
    :var output: List of 'CreateVisSCOutput' structures containing the VisStructureContext objects created based on the
    input configuration objects.
    
    :var serviceData: The Service Data.
    """
    output: List[CreateVisSCOutput] = ()
    serviceData: ServiceData = None
