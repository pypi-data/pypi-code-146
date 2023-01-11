from __future__ import annotations

from tcsoa.gen.Ai._2006_03.Ai import ApplicationRef
from typing import List
from tcsoa.gen.BusinessObjects import RequestObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateScopedMultipleStructureResponse(TcBaseObj):
    """
    GenerateScopedMultipleStructureResponse struct
    
    :var ticket: The transient file ticket to be used for downloading the generated plmxml
    :var data: partial failures are returned - along with object ids for each plmxml data could not be generated.
    """
    ticket: str = ''
    data: ServiceData = None


@dataclass
class GenerateScopedSyncRequestResponse(TcBaseObj):
    """
    GenerateScopedSyncRequestResponse struct
    
    :var request: request
    :var data: partial failures are returned - object ids for each sync data could not be created.
    """
    request: RequestObject = None
    data: ServiceData = None


@dataclass
class ObjectsWithConfig(TcBaseObj):
    """
    structure to specify multiple objects with each set potentially having it's own configuration
    
    :var apprefs: vector of ApplicationRefs specifying the objects to be included in the plmxml generation
    :var config: configuration to be used for the above set of objects.
    """
    apprefs: List[ApplicationRef] = ()
    config: Configuration2 = None


@dataclass
class Configuration2(TcBaseObj):
    """
    Configuration structure.
    
    :var useDefaultRevisionRule: if true - the Teamcenter preferences are used to pick up the rev rule. Overrides
    everything if present.
    :var revRuleName: if id is NULLTAG, then used to specify the revisionrule by name.
    :var variantRule: ApplicationRef of a variantrule - only needed if revrule is being specified elsewhere.
    :var configuringObject: revisionrule object or structurecontext
    :var relatedContexts: vector of ApplicationRefs specifying the structure contexts to help create the linked windows
    """
    useDefaultRevisionRule: bool = False
    revRuleName: str = ''
    variantRule: ApplicationRef = None
    configuringObject: ApplicationRef = None
    relatedContexts: List[ApplicationRef] = ()
