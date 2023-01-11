from __future__ import annotations

from tcsoa.gen.BusinessObjects import Form, ImanRelation, RevisionRule, Dataset, GeneralDesignElement, GeneralDesignElementLink, MEAppearancePathNode, GDEOccurrence, ItemRevision
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FeatureQueryInfo(TcBaseObj):
    """
    Input to control the QueryPartRelatedFeatures service.
    
    :var clientId: The id string for the operation, used in the return map to specify the return data associated with
    this input set.
    :var itemRevision: The ItemRevision to process
    :var viewType: The  View to be used for PS traversal. If not supplied then the default view will be used.
    :var featureReturnFilter: Information defining the data to be returned.
    """
    clientId: str = ''
    itemRevision: ItemRevision = None
    viewType: str = ''
    featureReturnFilter: FeatureReturnFilter = None


@dataclass
class FeatureReturnFilter(TcBaseObj):
    """
    Filter for how to process.
    
    :var relationTypes: Types of PartToPart relations to process. Required
    :var levelsForward: The number of levels to process PartToPart relations in the primary to secondary direction.
    :var levelsBackward: The number of levels to process PartToPart relations in the secondary to primary direction.
    :var featureTypes: Types of features to be processed, if empty then all.
    :var configurationType: Determines, based on configuration, which item revisions will be processed. 
      All Item Revisions.
      Latest Item Revisions.
      Configured Item Revisions based on configRule.
    :var configRule: Name of a configuration rule to use. REQUIRED when revisionTypes is Configured.
    :var psNotesWanted: A list of names of attributes to retireve from the PSOccurrenceNote attached to the
    GDEOccurrence.
    """
    relationTypes: List[str] = ()
    levelsForward: int = 0
    levelsBackward: int = 0
    featureTypes: List[str] = ()
    configurationType: FeatureConfigurationType = None
    configRule: RevisionRule = None
    psNotesWanted: List[str] = ()


@dataclass
class GDEItem(TcBaseObj):
    """
    GDE Object data
    
    :var gde: The GDE Object.
    :var gdeOccurrence: The GDEOccurrence that references the GDE Object
    :var psOccNotes: The PSOccurrenceNotes for the GDEOccurrence.
    :var apns: The list of APNs associated with the GDE.
    :var featureForm: The FeatureForm associated with the GDE Object, if requested.
    :var numberOfGDELinks: The number of GDE Links that reference the GDE. This may be more than the number of GDELinks
    returned.
    :var gdeLinks: The list of GDELinks that reference the GDE Object,  if requested.
    """
    gde: GeneralDesignElement = None
    gdeOccurrence: GDEOccurrence = None
    psOccNotes: List[GDEOccNote] = ()
    apns: List[MEAppearancePathNode] = ()
    featureForm: Form = None
    numberOfGDELinks: int = 0
    gdeLinks: List[GeneralDesignElementLink] = ()


@dataclass
class GDELinkItem(TcBaseObj):
    """
    Description of a GDELink Object
    
    :var gdeLink: The GDELink Object.
    :var gdeLinkOccurrence: The GDEOccurrence that references the GDELink  Object
    :var psOccNotes: The PSOccurrenceNotes for the GDEOccurrence.
    :var apns: The list of APNs associated with the GDELink.
    :var featureForm: The FeatureForm for the GDELink Object.
    :var numberOfGDEs: The number of GDE referenced by the GDELink. This may be more than the number of GDEs returned.
    :var gdes: The list of GDEs that are referenced by the GDELink Object.
    :var connectedTos: The list of CONNECTED_TO or CF_CONNECTED_TO ImanRelations that the GDELink is in.
    """
    gdeLink: GeneralDesignElementLink = None
    gdeLinkOccurrence: GDEOccurrence = None
    psOccNotes: List[GDEOccNote] = ()
    apns: List[MEAppearancePathNode] = ()
    featureForm: Form = None
    numberOfGDEs: int = 0
    gdes: List[GeneralDesignElement] = ()
    connectedTos: List[ImanRelation] = ()


@dataclass
class GDEOccNote(TcBaseObj):
    """
    A name / value pair for an attribute in an GDEOccurrenceNote.
    
    :var name: The name of the Occurrence Note attribute.
    :var value: The value of the Occurrence Note attribute.
    """
    name: str = ''
    value: str = ''


@dataclass
class PartToPartData(TcBaseObj):
    """
    A PartToPart relation with the primary and secondary objects specified as the comparable item revision.
    
    :var primaryRevision: The equivalent primary ItemRevision in the relationship.
    :var secondaryRevision: The equivalent secondary ItemRevision in the relationship
    :var partToPartRelation: The actual PartToPart IMANRelation.
    """
    primaryRevision: ItemRevision = None
    secondaryRevision: ItemRevision = None
    partToPartRelation: ImanRelation = None


@dataclass
class QueryPartRelatedFeaturesResponse(TcBaseObj):
    """
    Results for the query operations performed.
    
    :var clientIdToFeatureMap: Map of data requested.
    :var serviceData: Service data containing warnings, errors and objects.
    """
    clientIdToFeatureMap: QueryPartRelatedFeaturesMap = None
    serviceData: ServiceData = None


@dataclass
class RevisionData(TcBaseObj):
    """
    The list of item revisions that were processed.
    
    :var itemRevision: The ItemRevision
    :var masterDataset: The UGMaster Datset for the ItemRevision.
    :var gdeItems: The list of GDE Objects owned by the ItemRevision.
    :var gdeLinkItems: The list of GDE Link Objects owned by the ItemRevision
    :var partToPartList: TThe list of PartToPart relations the ItemRevision is part of if the level
    ( i.e. backward or forward count ) has not been reached.
    :var endOfChain: A flag, when true this ItemRevision is at the end of the list as specified by the levels forward
    or backward.
    :var numberOfParents: The number of PartToPart relations where this ItemRevision is the secondary object.
    :var numberOfChildren: The number of PartToPart relations where this ItemRevision is the primary object.
    """
    itemRevision: ItemRevision = None
    masterDataset: Dataset = None
    gdeItems: List[GDEItem] = ()
    gdeLinkItems: List[GDELinkItem] = ()
    partToPartList: List[PartToPartData] = ()
    endOfChain: bool = False
    numberOfParents: int = 0
    numberOfChildren: int = 0


class FeatureConfigurationType(Enum):
    """
    The item revisions to be selected based on configuration.
    """
    All = 'All'
    Configured = 'Configured'
    Latest = 'Latest'


"""
A map of the list of 'RevisionData' from the 'queryPartRelatedFeatures' service. The key is the 'ClientId' supplied in 'FeatureQueryInfo'.
"""
QueryPartRelatedFeaturesMap = Dict[str, List[RevisionData]]
