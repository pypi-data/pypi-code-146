from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0ModelViewProxy, ConfigurationContext
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Cad._2016_03.StructureManagement import StructureNodeResults
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FindModelViewsInput(TcBaseObj):
    """
    The set of inputs needed to start a find operation on a given object ('disclosure') or a set of objects
    ('startingScopes') which are structured under the disclosure.
    
    :var searchID: A unique identifier passed by the client in order to identify the find results to continue with when
    calling the continueFindModelViews operation. If a value is not provided, the preference MVFindMinNodeCount will be
    ignored and the find will finish and no followup call to continueFindModelViews can be made.
    :var disclosure: The structure root of the various 'startingScopes'. This structure root must be an ItemRevision or
    Workset (Cpd0Workset).  Required if 'startingScopes' contains more than one object, otherwise it may be left NULL.
    :var startingScopes: A list of one or more structures to search for model view proxy objects. If a single root
    assembly or workset (Cpd0Workset) is given, the entire structure will be searched. If multiple sub-assemblies are
    given, then only those disclosure children under the given sub-assemblies will be searched for proxies. The input
    objects may be any WorkspaceObject sub-type that is expected to own (directly or indirectly) model view proxy
    objects. Most commonly input would be a Workset or WorksetLine, but other ItemRevision or ItemLine objects may be
    given.
    :var configurationContext: The configuration context object used to configure the children of the expanding
    structure by revision rules, effectivity, and variants.
    :var withDisclosureIntents: A list of string values values (such as "Design Review" or "Quality Check" ) to match
    against candidate model view proxies. Only model view proxies that have any of the specified disclosure purpose
    (fnd0DisclosureIntent) attribute values will be returned. If no strings are given or any string is an empty string,
    then all model view proxy objects will be returned.
    :var options: A set of optional flags. Supported options are: "'expandStructureScope'"
    'expandStructureScope': If true, each 'startingScope' will be expanded and their children searched for model views.
    If false, only model view proxies owned by the 'startingScope' objects will be returned. The default is true.
    """
    searchID: str = ''
    disclosure: BusinessObject = None
    startingScopes: List[BusinessObject] = ()
    configurationContext: ConfigurationContext = None
    withDisclosureIntents: List[str] = ()
    options: BoolMap2 = None


@dataclass
class FindModelViewsResponse(TcBaseObj):
    """
    The response contains any found model view proxies (FndModelViewProxy) and the structure location at which they
    were found.
    
    Any errors are returned in the 'serviceData'.
    
    :var modelViewsByStructureNodes: A list of  proxy objects found for various  nodes in the structure - the structure
    nodes may be bomlines, item revisions or design elements depending on the type of structure starting scope and
    disclosure type.
    :var finished: Flag to indicate if the find operation is complete or if there is more content or structure to be
    searched. If false, then the continueFindModelViews operation may be called with the input 'searchID' in order to
    continue to retrieve more model views. If true, the state of the search is cleaned up and the given 'searchID', if
    any, may not be used as input into the continueFindModelViews operation.
    :var structureNodesSearched: Total number of structure nodes ( BomLines or Design Elements) which were so far
    searched for model views. This shows how large the structure is as the search is progressing over multiple calls to
    startFindModelViews and continueFindModelViews.
    :var serviceData: Contains a list of any errors which occurred during the operation.
    """
    modelViewsByStructureNodes: List[StructureNodeResults] = ()
    finished: bool = False
    structureNodesSearched: int = 0
    serviceData: ServiceData = None


@dataclass
class ModelViewProxyReconcileInfo(TcBaseObj):
    """
    This structure contains the reconcile information for each Fnd0ModelViewProxy object found in the
    Fnd0ModelViewPalette. It contains information about the candidate Fnd0ModelViewProxy found, the recommended
    reconciliation action, and a description of the basis on which the candidate Fnd0ModelViewProxy was identified.
    
    :var candidateMVP: The candidate Fnd0ModelViewProxy identified for reconciliation.
    :var reconcileActionEnum: The recommended action for the user to take. Supported values are: 
    - None
    - Replace
    - Remove
    - Resolve Ambiguity
    
    
    :var reconcileAction: The displayable explanation of the action that need to be taken. For example: "Remove Model
    View from Palette"
    :var reconcileReason: The displayable message which describes the basis of candidate identification.  For example,
    "Model View deleted from Owning Model"
    :var candidateStructNodeInfos: A list of 'CandidateModelViewStructNodeInfo' that contains the BOMLine or
    Cpd0DesignElement  on which the candidate Fnd0ModelViewProxy was found.
    """
    candidateMVP: Fnd0ModelViewProxy = None
    reconcileActionEnum: str = ''
    reconcileAction: str = ''
    reconcileReason: str = ''
    candidateStructNodeInfos: List[CandidateModelViewStructNodeInfo] = ()


@dataclass
class NextReconcilePaletteInput(TcBaseObj):
    """
    This structure contains the  information about the  'clientID' that identifies the reconciliation state in the
    server and list of Fnd0ModelViewProxy if they have to be given a higher priority during reconciliation. For
    example, the user may have chosen to apply a Model View on the palette before the palette reconciliation that
    already started was complete.
    
    :var clientID: A unique clientId passed by the client in order to identify the reconciliation of the palette
    between subsequent calls to 'startReconcilePalette 'and' continueReconcilePalette'.
    :var mvProxiesOrMvGroups: List of Fnd0ModelViewProxy  or the  Fnd0ModelViewGroup objects that need to be
    reconciled.  Can be used to do a partial reconciliation or just the ModelViewProxy or Group of interest.
    :var stopReconcile: Flag to stop the reconciliation process.
    """
    clientID: str = ''
    mvProxiesOrMvGroups: List[BusinessObject] = ()
    stopReconcile: bool = False


@dataclass
class PaletteModelViewProxyReconcileInfo(TcBaseObj):
    """
    This structure binds the Fnd0ModelViewProxy in the Fnd0ModelViewPalette to its corresponding reconcile information.
    
    :var paletteMVP: The Fnd0ModelViewProxy on the Fnd0ModelViewPalette that has needs to be reconciled.
    :var reconcileInfos: A list of reconcile information for this Fnd0ModelViewProxy including reasons, actions,
    reconcile candidates, and more. Can be a list if more than one candidate identified.
    """
    paletteMVP: Fnd0ModelViewProxy = None
    reconcileInfos: List[ModelViewProxyReconcileInfo] = ()


@dataclass
class ReconcilePaletteInput(TcBaseObj):
    """
    This structure contains the  information about the  Fnd0ModelViewPalette or the disclosing object that needs to be
    reconciled. It also contains configuration information specified as 'configRecipe'  in the form of BOMLine or
    VisStructureContext object. If BOMLine is specified as 'configRecipe' then the BOMWindow to which the line belongs
    will be used for reconciliation. If the 'configRecipe' is not specified then the configuration information will be
    retrieved from the Fnd0ModelViewPalette if present otherwise the default configuration is used for reconciliation.
    The 'clientID' supplied by the client will be used to identify the reconciliation state in the server to continue
    the reconciliation process during the 'continueReconcilePalette' operation.
    
    :var clientID: A unique clientId passed by the client in order to identify the reconciliation of the palette
    between subsequent calls to 'continueReconcilePalette'.
    :var paletteOrDisclosingObject: The Fnd0ModelViewPalette  or the object to which Fnd0ModelViewPalette  is
    associated using Fnd0DisclosedViewList relation.
    :var mvProxiesOrMvGroups: List of Fnd0ModelViewProxy  or the  Fnd0ModelViewGroup objects that need to be
    reconciled. Can be used to do a partial reconciliation or just the ModelViewProxy or Group of interest.
    :var doEntirePalette: Specify false to indicate whether to reconcile only the Fnd0ModelViewProxy or
    Fnd0ModelViewGroup specified in 'mvProxiesOrMvGroups', or true to continue with reconciliation of the entire
    palette.
    :var configRecipe: The top line (BOMLine) of the disclosing object or a VisStructureContext which has the product
    structure configuration information.
    """
    clientID: str = ''
    paletteOrDisclosingObject: BusinessObject = None
    mvProxiesOrMvGroups: List[BusinessObject] = ()
    doEntirePalette: bool = False
    configRecipe: BusinessObject = None


@dataclass
class ReconcilePaletteResponse(TcBaseObj):
    """
    This structure contains the reconciliation information reponse for each Fnd0ModelViewProxy  on the
    Fnd0ModelViewPalette. The clientID signifies maintains the correlation between multiple calls to the the server. 
    The 'origConfigInfo' and 'reconcileConfigInfo' are returned only if there is a configuration mis-match between the
    configuration associated to Fnd0ModelViewPalette and the one used for reconciliation.
    
    :var palMVPReconcileInfos: A list of 'PaletteModelViewProxyReconcileInfo', one for each Fnd0ModelViewProxy  on the
    Fnd0ModelViewPalette  that has been reconciled.
    :var clientID: A unique clientId passed by the client to correlate multiple subsequent 'continueReconcilePalette'
    operations .
    :var finished: True if the reconciliation is complete.
    :var configurationMisMatch: Returned as true during 'startReconcilePalette' if there is a configuration mismatch
    between the product configuration associated with the Fnd0ModelViewPalette  and the input product configuration.
    Used to warn the user.
    :var origConfigInfo: The configuration information that is associated to the Fnd0ModelViewPalette, presented in a
    form that can be directly displayed to the user.
    :var reconcileConfigInfo: The configuration information for the current structure that is used for reconciliation.
    :var estimatedMVPsLeft: The number of Fnd0ModelViewProxy objects remaining to be reconciled.
    :var percentComplete: The percentage of total Fnd0ModelViewProxy objects on the Fnd0ModelViewPalette where
    reconciliation is complete.
    :var serviceData: 'ServiceData' is used to communicate partial errors to the client.
    """
    palMVPReconcileInfos: List[PaletteModelViewProxyReconcileInfo] = ()
    clientID: str = ''
    finished: bool = False
    configurationMisMatch: bool = False
    origConfigInfo: ConfigurationDisplayInfo = None
    reconcileConfigInfo: ConfigurationDisplayInfo = None
    estimatedMVPsLeft: int = 0
    percentComplete: float = 0.0
    serviceData: ServiceData = None


@dataclass
class CandidateModelViewStructNodeInfo(TcBaseObj):
    """
    The structure contains  BOMLine or  Cpd0DesignElement on which the candidate Fnd0ModelViewProxy was identified. If
    a BOMLine is returned then also the clone stable occ id  chain which identifies BOMLine in a structure is also
    returned.
    
    :var structNode: A BOMLine or Cpd0DesignElement object on which the candidate was identified.  A BOMLine is
    returned only if a BOMLine is sent as 'configRecipe' input.
    :var cloneStableIdChain: List of strings representing a chain of clone stable ids that lead to the 'structNode' in
    the product structure.
    The clone stable occurrence id values are ordered from the top BOMLine incase 'structNode' is a BOMLine with line
    object being ItemRevision. Alternatively, if a the 'csIdContextOccurrence' is a subset in the Workset, and only a
    single cs_id value for the 'structNode' would be needed since a given model element (Mdl0ModelElement) in a subset
    (Cpd0DesignSubsetElement)
    can be identified by such a single clone stable id.
    :var csIdContextOccurrence: Contains either the subset in which the structure node resides (either Cpd0SubsetLine
    or Cpd0DesignSubsetElement.). This object gives context to the associated 'cloneStableIdChain' value(s). In case if
    the 'structNode' is a BOMLine whose line object is ItemRevision then this would be empty since the top line gives
    the context for the 'cloneStableIdChain'.
    """
    structNode: BusinessObject = None
    cloneStableIdChain: List[str] = ()
    csIdContextOccurrence: BusinessObject = None


@dataclass
class ConfigurationDisplayInfo(TcBaseObj):
    """
    This structure contains the configuration information that can be displayed to the user if there is a mis-match
    between the configuration found on the Fnd0ModelViewPalette and the configuration used for palette reconciliation.
    Note: The information returned by this structure should be used only to display configuration information.
    
    :var configWindow: The configuration window (BOMWindow) that represents the configuration.In case when the previous
    configuration information is returned during reconciliation process the BOMWindow is valid until the reconciliation
    is complete.
    :var revisionRule: The RevisionRule used for the configuration.
    :var revRuleConfigEntriesAsStrings: A list of strings describing the configuration entries in the RevisionRule.
    :var configOptions: A list of options that is being used during configuration such as "hide unconfigured lines" etc.
    :var variantRules: A list of VariantRule objects used for the configuration.
    """
    configWindow: BusinessObject = None
    revisionRule: BusinessObject = None
    revRuleConfigEntriesAsStrings: List[str] = ()
    configOptions: List[ConfigurationOptionDisplayInfo] = ()
    variantRules: List[BusinessObject] = ()


@dataclass
class ConfigurationOptionDisplayInfo(TcBaseObj):
    """
    A structure to represent the configuration option and its values. Depending upon the type of option value the
    appropriate values member would be populated. Say for example for the option "Show Unconfigured Variants" the
    'boolValues' would be populated with a single value and the rest of the values member would be empty. The caller
    can determine the type of option value by checking the value memberthat has been populated.
    
    :var optionName: The name of the option use for configuration.
    :var boolValues: A list of boolean values if the option is a boolean.
    :var doubleValues: A list of double values if the option is a double.
    :var intValues: A list of integer values if the option is an integer.
    :var strValues: A list of char or string values if the option is a character or string.
    :var dateValues: A list of date values if the option is a date.
    :var refValues: A list of objects values if the option is a object.
    """
    optionName: str = ''
    boolValues: List[bool] = ()
    doubleValues: List[float] = ()
    intValues: List[int] = ()
    strValues: List[str] = ()
    dateValues: List[datetime] = ()
    refValues: List[BusinessObject] = ()


"""
Generic map of boolean names to values (string, bool). Commonly used to contain selected options from a client.
"""
BoolMap2 = Dict[str, bool]
