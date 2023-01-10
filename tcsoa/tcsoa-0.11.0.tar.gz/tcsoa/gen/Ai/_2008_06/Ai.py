from __future__ import annotations

from tcsoa.gen.Ai._2006_03.Ai import ApplicationRef
from tcsoa.gen.BusinessObjects import BOMWindow, RequestObject, ConfigurationContext
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateScopedMultipleStructure2Response(TcBaseObj):
    """
    GenerateScopedMultipleStructure2Response struct
    
    :var ticket: The transient file ticket to be used for downloading the generated plmxml
    :var data: partial failures are returned - along with object ids for each plmxml data could not be generated.
    """
    ticket: str = ''
    data: ServiceData = None


@dataclass
class GenerateScopedSyncRequest2Response(TcBaseObj):
    """
    GenerateScopedSyncRequest2Response struct
    
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
    :var refContexts: If passing process object, this parameter can be used to specify how to
    setup the reference Product/Plant structure for that Process. If unused,
    pass an empty vector.
    """
    apprefs: List[ApplicationRef] = ()
    config: Configuration = None
    refContexts: List[ReferenceContext] = ()


@dataclass
class ReferenceContext(TcBaseObj):
    """
    structure to specify the reference structure, in the case of process element like MEProcessRevision,
    MEOpRevision, a process APN etc.
    
    :var topLineObject: ApplicationRef specifying the object to be set as the topline of the reference structure.
    It is optional if config structure's configuringObject is an StructureContext object.
    If not needed - pass an empty ApplicationRef.
    :var config: configuration to be used to construct the reference window.
    """
    topLineObject: ApplicationRef = None
    config: Configuration = None


@dataclass
class CompareConfigurationContextsResponse(TcBaseObj):
    """
    CompareConfigurationContextsResponse struct
    
    :var compareResults: bool array pointing to the result in the compares. Only successful (true/false) are returned
    here.
    :var serviceData: any partial errors are reported here. For example: if any pair comparison fails -
    that failed index with the failed message will be reported like this.
    """
    compareResults: List[bool] = ()
    serviceData: ServiceData = None


@dataclass
class Configuration(TcBaseObj):
    """
    Configuration structure.
    
    :var existingWindow: BOMWindow representing the window from which target application was launched. Must be
    initialized to NULL by client if unused.
    :var useDefaultRevisionRule: If true use default RevisionRule. Used if none of the above options are provided.
    :var revRuleName: Name of RevisionRule. Used if existingWindow and configuringObject are not provided.
    :var variantRule: ApplicationReference representing classic VariantRule.Used in case existingWindow is not provided
    and other options do not yield a VariantRule.
    :var configuringObject: A CollaborationContext or StructureContext object.Used if existingWindow is not provided.
    """
    existingWindow: BOMWindow = None
    useDefaultRevisionRule: bool = False
    revRuleName: str = ''
    variantRule: ApplicationRef = None
    configuringObject: ApplicationRef = None


@dataclass
class ConfigurationContextPair(TcBaseObj):
    """
    ConfigurationContextPair struct
    
    :var src: src configurationcontext object to use in compare
    :var other: target configurationcontext object to use in compare.
    """
    src: ConfigurationContext = None
    other: ConfigurationContext = None
