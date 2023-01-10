from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMWindow, BusinessObject, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FileTicketDetails(TcBaseObj):
    """
    File ticket details.
    
    :var filename: The name of the log file.
    :var fileTicket: The file management server ticket of the file.
    """
    filename: str = ''
    fileTicket: str = ''


@dataclass
class GetClusterDetails(TcBaseObj):
    """
    in
    
    :var clusters: GetClusterDetails structure contains  the elements that are obtained initially by calling the
    operation searchForClusters. These elements contain BOMLine objects for which properties need to be obtained.
    """
    clusters: List[SearchForClustersElement] = ()


@dataclass
class SearchForClusters(TcBaseObj):
    """
    The input element specifying the parameters to be used for searching for patterns.
    
    :var mbomModelAssemblyNode: The mbom assembly node that is to be used a template for finding the candidates forming
    the set for pattern matching in ebom. Currently, must be a BOMLine object.
    :var ebomContext: The ebom context below which to search for patterns. Currently, the context must be a BOMLine
    object.
    """
    mbomModelAssemblyNode: BusinessObject = None
    ebomContext: BusinessObject = None


@dataclass
class SearchForClustersElement(TcBaseObj):
    """
    SearchForClustersElement structure contains the BOMLine object, its ID in Context (Top Level)  and whether it is a
    basis for formulating a pattern.
    
    :var line: The BOMLine.
    :var isBasis: If true, indicates that it was an element used as a basis to compute the rest of the transforms in
    the pattern list.
    :var idic: The ID in Context (Top Level) of the BOMLine.
    """
    line: BusinessObject = None
    isBasis: bool = False
    idic: str = ''


@dataclass
class SearchForClustersResponse(TcBaseObj):
    """
    SearchForClustersResponse structure contains the response elements (patterns) that match the model assembly in
    MBOM, basis occurrence chain - which is the chain of occurrence threads for the model assembly BOMLine object used
    as a basis for computing the relative transforms, the nodes assigned to the model assembly in MBOM and potentially
    unassigned nodes. The response will also return ServiceData.
    
    :var basisOccurrenceChain: The chain of occurrence threads for the model assembly   BOMLine object used as a basis
    for computing relative transforms. This is computed by concatenating a chain of clone stable ID property value from
    the model assembly down to the basis line (the basis line is the BOMLine object which occurs the least number of
    times in the model assembly in MBOM among the BOMLine objects assigned from the EBOM).
    :var nodesAssignedInModelAssembly: The nodes represented by BOMLine objects assigned in  the model assembly in the
    MBOM.
    :var patterns: A list of patterns. Each pattern is represented by SearchForResponseClusterElement. Each such
    element contains nodes that form the pattern. Each node is of type SearchForClusterElement.
    :var unassignedModelAssemblyNodes: The potentially unassigned model assembly nodes (BOMLine objects) in the model
    assembly.
    :var serviceData: Service data capturing partial errors using the input array index as clientId. ServiceData for
    this operation will not have any data related to properties of BOMLine objects returned, because it is not
    necessary to return properties in this operation, they could be returned from another operation getClusterDetails.
    Also it will be expensive to return properties in this call itself.
    """
    basisOccurrenceChain: str = ''
    nodesAssignedInModelAssembly: List[BusinessObject] = ()
    patterns: List[SearchForClustersResponseElement] = ()
    unassignedModelAssemblyNodes: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class SearchForClustersResponseElement(TcBaseObj):
    """
    SearchForClustersResponseElement structure contains the collection of objects of type SearchForClustersElement.
    
    :var patternNodes: A list of pattern nodes. Each pattern node is represented by struct SearchForClustersElement and
    it comprises of the BOMLine object, the ID in Context (Top Level) of the BOMLine object and the Find number of the
    BOMLine object.
    :var owningModelAssemblies: A list of owning model assemblies ( currently,  BOMLine objects ) below which the
    pattern nodes appear. The same pattern nodes may appear under multiple model assemblies.
    """
    patternNodes: List[SearchForClustersElement] = ()
    owningModelAssemblies: List[BusinessObject] = ()


@dataclass
class ConfigurationsInfo(TcBaseObj):
    """
    Configuration Info Object
    
    :var window: The BOMWindow of the structure.
    :var rootLine: The root BOMLine or BOPLine of the structure. The type of BOPLine object can be Mfg0BvrProcess.
    :var saveCC: The CollaborationContext object being saved, if NULL it will not be saved.
    :var revisionRule: The RevisionRule object.
    :var variantRule: The BOMVariantRule object.
    :var effGrpRevisions: List of Fnd0EffectvtyGrpRevision objects to be applied to the window.
    :var showUnconfigVariants: Show or hide the BOMLine or BOPLine objects configured by the variant configuration on
    the BOMWindow. If true, the configured-out lines are visible; otherwise those are hidden.
    :var showUnconfigOccEffectivity: Show or hide the BOMLine or BOPLine objects configured-out by the occurrence
    effectivity configuration on the BOMWindow. If true, the configured-out lines are visible; otherwise those are
    hidden.
    :var showSupressedOccurrences: Show or hide the suppressed BOMLine or BOPLine objects in the BOMWindow. If true,
    the suppressed lines are visible; otherwise those are hidden.
    :var showUnconfigICs: Show or hide the BOMLine or BOPLine objects configured-out by the configuration of the
    incremental change(IC) context on the BOMWindow. If the value is true, the configured-out lines are visible;
    otherwise those are hidden
    :var showUnconfigAssignedOccs: Show or hide the BOMLine or BOPLine objects which are assigned occurrences from the
    associated BOMLine structure. If true, the assigned lines are visible; otherwise those are hidden.
    """
    window: BOMWindow = None
    rootLine: BusinessObject = None
    saveCC: BusinessObject = None
    revisionRule: BusinessObject = None
    variantRule: BusinessObject = None
    effGrpRevisions: List[ItemRevision] = ()
    showUnconfigVariants: bool = False
    showUnconfigOccEffectivity: bool = False
    showSupressedOccurrences: bool = False
    showUnconfigICs: bool = False
    showUnconfigAssignedOccs: bool = False


@dataclass
class ConfigureMultipleStructuresResponse(TcBaseObj):
    """
    ConfigureMultipleStructuresResponse object.
    
    :var serviceData: Standard service data.
    :var logFileTicket: The details about the file management server ticket of the log file.
    """
    serviceData: ServiceData = None
    logFileTicket: FileTicketDetails = None


@dataclass
class CreateReuseAssembly(TcBaseObj):
    """
    CreateReuseAssembly structure contains the input for creating new assemblies under given parent BOMLine objects.
    
    :var parentNodes: The  BOMLine objects in the MBOM under which new assemblies matching the model assembly will be
    created.
    :var modelAssemblyNode: The BOMLine representing the model assembly in MBOM.
    :var basisOccurrenceChain: The occurrence chain obtained from a prior call to searchForClusters representing the
    chain for the node used as a basis for computing relative transforms.
    :var nodesAssignedInModelAssembly: The currently assigned BOMLine objects under model assembly in the MBOM. These
    are obtained from the response of a prior call to searchFor operation.
    :var clusterElements: The cluster elements represented by SearchForClustersElement returned by prior call to
    searchForClusters operation.
    """
    parentNodes: List[BusinessObject] = ()
    modelAssemblyNode: BusinessObject = None
    basisOccurrenceChain: str = ''
    nodesAssignedInModelAssembly: List[BusinessObject] = ()
    clusterElements: List[SearchForClustersElement] = ()


@dataclass
class CreateReuseAssemblyResp(TcBaseObj):
    """
    A list of created nodes ( currently, BOMLine objects ), one per input parentNode. Can be NULL if there is a failure.
    
    :var nodes: A list of created nodes ( currently, BOMLine objects ), one per input parentNode.
    :var serviceData: serviceData
    """
    nodes: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class AlignAssemblyData(TcBaseObj):
    """
    An element representing the data to be used for aligning a node ( Currently, a BOMLine object ) in source assembly
    to a node in target assembly.
    
    :var sourceNode: The  BOMLine object in the source structure which needs to be aligned with a BOMLine object in the
    target structure.
    :var targetNode: The BOMLine object in the target structure with which the BOMLine object in the source structure
    needs to be aligned.
    :var reuseAssemblyNode: The BOMLine object under which the target BOMLine object may have been assigned. All
    BOMLine objects assigned from source structure under this reuseAssemblyNode will be considered for alignment if
    alignMode is not specified.
    :var alignMode: The alignMode can take one of the values from :
    a)    "AlignIdInTopLevelContextOnly" - used to align the ID in Context (Top Level ) only.
    b)    "AlignOccurrenceProperties" - used to align all occurrence proerpties and ID in Context (Top Level) based on
    the preference "MEAlignedPropertiesList".
    c)    "AlignTransformOnReuseAssemblyOnly" - used to adjust the transform on the parent and stamp ID in Context(Top
    Level) on the source and target BOMLine objects. This is the case where ID in Context (Top Level) is there but they
    need to be paired and the Absolute Transformation Matrix property needs to be adjusted on the model assembly.
    c) "AlignAllModelAssemblies" - used to indicate that on aligning one model assembly, search for others with the
    same item id and align those also.
    d)    An empty value - In this case the pattern defined by the reuseAsemblyNode is searched for in the source
    structure and a new BOMLine object is created that matches the reuseAssemblyNode. Then  all occurrrence properties
    of all BOMLine objects under the new BOMLine object will be adjusted.
    """
    sourceNode: BusinessObject = None
    targetNode: BusinessObject = None
    reuseAssemblyNode: BusinessObject = None
    alignMode: str = ''
