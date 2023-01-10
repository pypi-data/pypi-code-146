from __future__ import annotations

from tcsoa.gen.BusinessObjects import GDEbvr, Form, RevisionRule, GeneralDesignElement, GeneralDesignElementLink, GDEOccurrence, ItemRevision
from typing import Dict, List
from tcsoa.gen.Cad._2007_01.StructureManagement import OccNote
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FeatureQueryData(TcBaseObj):
    """
    Contains processing information for 'queryRelatedFeatures' operation.
    
    :var itemRevision: Item revision, starting point for retrieving related features.
    :var occNote: Occurrence data for selection of the featureTypes to process, if null then all will be processed.
    :var featureTypes: Types of features related to the ItemRevision to process, if empty then all will be processed.
    :var gdeOccurrence: Feature occurrence, starting point for retrieving related features. If supplied, the above data
    is ignored.
    :var gdeBVR: The GDE BOM View Revision for the Item Revision.
    """
    itemRevision: ItemRevision = None
    occNote: OccNote = None
    featureTypes: List[str] = ()
    gdeOccurrence: GDEOccurrence = None
    gdeBVR: GDEbvr = None


@dataclass
class FeatureQueryInfo(TcBaseObj):
    """
    Contains 'clientId', 'featureQueryData' and 'featureReturnFilter' information.
    
    :var clientID: Unique string to identify the input data, required input.
    :var featureQueryData: Structure contains the input data for querying the features.
    :var featureReturnFilter: Structure contains the filter criteria.
    """
    clientID: str = ''
    featureQueryData: FeatureQueryData = None
    featureReturnFilter: FeatureReturnFilter = None


@dataclass
class FeatureReturnFilter(TcBaseObj):
    """
    Contains filter information for queryRelatedFeatures operation.
    
    :var returnFeatureForms: Flag to specify if the Feature forms for the GDE and GDELinks returned are to be returned
    also.
    :var relatedItems: Flag to specify if the related ItemRevisions are to be returned.
    :var returnGDEs: Flag to specify if the GDEs that pass the filter for ItemRevisions returned are to be returned
    also.
    :var returnGDELinks: Flag to specify if the GDELinks that pass the filter for ItemRevisions returned are to be
    returned also.
    :var recursive: Flag to specify if the reference and referenced GDEs are to be returned( only used if relatedItems
    flag is set to true ).
    :var featureTypes: Types of features to be processed, if empty then all.
    :var configRule: Name of a configuration rule to use, if none specified then user's default is used.
    """
    returnFeatureForms: bool = False
    relatedItems: bool = False
    returnGDEs: bool = False
    returnGDELinks: bool = False
    recursive: bool = False
    featureTypes: List[str] = ()
    configRule: RevisionRule = None


@dataclass
class GDEItem(TcBaseObj):
    """
    Contains gdelink, gde and feature form information.
    
    :var gde: The GDE referenced by the Item Revision.
    :var gdeLinks: GDELinks referencing the GDE if requested.
    :var featureForm: The Feature form for the GDE if requested
    """
    gde: GeneralDesignElement = None
    gdeLinks: List[RefedGDELinkItem] = ()
    featureForm: Form = None


@dataclass
class GDELinkItem(TcBaseObj):
    """
    Contains gdelink, gde and feature form information.
    
    :var gdeLink: The GDELink referenced by the Item Revision.
    :var gdes: GDEs referenced by the GDELink if requested.
    :var featureForm: The Feature form for the GDELink if requested
    """
    gdeLink: GeneralDesignElementLink = None
    gdes: List[RefedGDEItem] = ()
    featureForm: Form = None


@dataclass
class QueryRelatedFeaturesOutput(TcBaseObj):
    """
    Contains the output data for queryRelatedFeatures operation, which contains itemrevision, gdeItem and gdeLink item.
    
    :var itemRevision: The ItemRevision of the feature for which query is being made.
    :var gdeItems: GDE items owned by this Item Revision if requested.
    :var gdeLinkItems: GDELinks owned by this Item Revision if requested.
    """
    itemRevision: ItemRevision = None
    gdeItems: List[GDEItem] = ()
    gdeLinkItems: List[GDELinkItem] = ()


@dataclass
class QueryRelatedFeaturesResponse(TcBaseObj):
    """
    Contains the response structure for queryRelatedFeatures
    
    :var returnQueryRelatedFeature: returnQueryRelatedFeature
    :var serviceData: serviceData
    """
    returnQueryRelatedFeature: ClientIdToFeatureMap = None
    serviceData: ServiceData = None


@dataclass
class RefedGDEItem(TcBaseObj):
    """
    Contains item revision, gde and feature form information for queryRelatedFeatures operation.
    
    :var itemRevision: itemRevision
    :var gde: gde
    :var featureForm: featureForm
    :var gdeLinks: gdeLinks
    """
    itemRevision: ItemRevision = None
    gde: GeneralDesignElement = None
    featureForm: Form = None
    gdeLinks: List[RefedGDELinkItem] = ()


@dataclass
class RefedGDELinkItem(TcBaseObj):
    """
    Contains item revision, gde, gdeLinks and feature form information for queryRelatedFeatures operation.
    
    :var itemRevision: The ItemRevision that owns the GDELink.
    :var gdeLink: The GDELink referenced by the ItemRevision.
    :var featureForm: The FeatureForm for the GDELink if requested
    :var gdes: GDEs referenced by the GDELink if recursive.
    """
    itemRevision: ItemRevision = None
    gdeLink: GeneralDesignElementLink = None
    featureForm: Form = None
    gdes: List[RefedGDEItem] = ()


"""
Map of input client id to feature values ('QueryRelatedFeaturesOutput').
"""
ClientIdToFeatureMap = Dict[str, QueryRelatedFeaturesOutput]
