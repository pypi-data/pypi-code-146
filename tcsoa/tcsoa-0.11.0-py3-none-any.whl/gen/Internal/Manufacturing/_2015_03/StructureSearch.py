from __future__ import annotations

from tcsoa.gen.Manufacturing._2014_12.StructureSearch import AdditionalInfo, KeyValuePair
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetSearchCrieriaFromRecipeResp(TcBaseObj):
    """
    GetSearchCriteriaFromRecipeResp structure contains the details of search critieria necessary for resolving
    Engineering BOM (EBOM) lines under the MBOM node with the recipe.
    
    :var criteriaElements: A list of SearchCriteriaElement elements, each of which captures the output data for a
    Mfg0MEMBOMRecipe object in the input list. The size of this list matches that of the input recipes.
    :var additionalInfo: A list of AdditionalInfo structures. Currently, not used.
    :var serviceData: Service data capturing partial errors using the input list index as client id.
    """
    criteriaElements: List[SearchCriteriaElement] = ()
    additionalInfo: AdditionalInfo = None
    serviceData: ServiceData = None


@dataclass
class SearchCriteriaElement(TcBaseObj):
    """
    SearchCriteriaElement structure contains the details of search critieria for a single Mfg0MEMBOMRecipe object in
    the input recipes.
    
    :var featureType: The feature type. If not empty, relatedObjs list will have the list of
    SearchCriteriaRelatedObject elements. Currently supported values are: "General", "WeldPoint", "DatumPoint", and
    "ArcWeld".
    :var logicalOperator: The logical operator associated with the feature type. Currently only "AND" and "OR" are
    supported.
    :var relatedObjs: The details of the connected objects for which the feature is being queried.
    :var searchCriteria: A list of KeyValuePair elements representing search criteria names and values.
    """
    featureType: str = ''
    logicalOperator: str = ''
    relatedObjs: List[SearchCriteriaRelatedObject] = ()
    searchCriteria: List[KeyValuePair] = ()


@dataclass
class SearchCriteriaRelatedObject(TcBaseObj):
    """
    SearchCriteriaRelatedObject structure contains the details of connected objects.
    
    :var conditionType: Indicate how the parts are connected to the feature. Currently only supported value is
    "Connected to".
    :var connectedObjs: The connected ItemRevision objects for which the feature is being queried.
    :var matchType: Currently four match types are supported: FullMatch (all parts are connected to the feature),
    PartialMatch (any of the parts is connected to the feature), NoMatch (none of the parts is connected to the
    feature), and NotApplicable (used in cases where match type is ignored).
    :var withHierarchy: If true, indicate traversal below the connectedObjs.
    """
    conditionType: str = ''
    connectedObjs: List[BusinessObject] = ()
    matchType: str = ''
    withHierarchy: bool = False
