from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, VisStructureContext, ConfigurationContext
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
    recipe. If not supplied then the output VisStructureContext object will not have its 
    occurrence_list property set. This will be interpreted as the top line was selected BOMLine for this configuration
    recipe.
    
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
    configuration objects
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


@dataclass
class CreateVisSCsFromBOMsInfo(TcBaseObj):
    """
    Input structure used for creating VisStrucutreContext objects based on the given BOMWindows and specific
    occurrenses within those BOMWindows.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var occurrencesList: List of BOMLines representing  the occurrences to be included in the structure recipe.
    :var staticStructureFile: IMANFile reference to the PLMXML static representation of the structure. If  not supplied
    then the associated property of the VisStructureContext will not be set. [optional]
    """
    clientId: str = ''
    occurrencesList: List[BOMLine] = ()
    staticStructureFile: BusinessObject = None


@dataclass
class CreateVisSCsFromBOMsOutput(TcBaseObj):
    """
    The output structure that contains the references to the created VisStructureContext objects along with the
    corresponding 'clientId'.
    
    :var clientId: The unique string supplied by the caller used to match the output to the supplied input.
    :var structureRecipe: VisStructureContext object that records the configuration recipe of the BOMWindow that
    contains the input BOMLines
    """
    clientId: str = ''
    structureRecipe: VisStructureContext = None


@dataclass
class CreateVisSCsFromBOMsResponse(TcBaseObj):
    """
    Response structure for the 'createVisSCsFromBOMs' operation.
    
    :var output: List of 'CreateVisSCsFromBOMsOutput' structures containing the VisStructureContext object that records
    the configuration recipe of the BOMWindow from which the input BOMLines belong.
    
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information.
    """
    output: List[CreateVisSCsFromBOMsOutput] = ()
    serviceData: ServiceData = None
