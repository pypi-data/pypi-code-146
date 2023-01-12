from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awb0ProductContextInfo, VariantRule, RevisionRule
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConfigRuleInput(TcBaseObj):
    """
    The ConfigRuleInput contains Awb0ProductContextInfo, pagination, type to fetch and optionally search criteria to
    filter the result.
    
    :var productContext: Awb0ProductContextInfo containing current product and configuration information.
    :var startIndex: Start index for pagination.
    :var maxToLoad: Maximum number of RevisionRule or VariantRule to be returned. Return everything if 'maxToLoad' is
    -1.
    :var typeToFetch: Internal name of the type to be returned. Valid values are "RevisionRule" and "VariantRule". The
    input is case sensitive.
    :var fetchOnlyPreferredConfiguration: If this is true then return only preferred effectivity information or
    preferred VariantRule owning objects for current RevisionRule.
    :var searchCriteria: Object Name to filter the response objects.
    :var requestPref: Map of preference name and value pairs (string/string).
    """
    productContext: Awb0ProductContextInfo = None
    startIndex: int = 0
    maxToLoad: int = 0
    typeToFetch: str = ''
    fetchOnlyPreferredConfiguration: bool = False
    searchCriteria: str = ''
    requestPref: RequestPreference = None


@dataclass
class ConfigRuleResponse(TcBaseObj):
    """
    ConfigRuleResponse contains RevisionRule and VariantRule information.
    
    :var marker: Number of preferred RevisionRule or VariantRule. Preferred RevisionRule or VariantRule are the one
    which are indexed through structure indexing. The default value is -1.
    :var endIndex: End index of page.
    :var totalFound: Total numbers of RevisionRule or VariantRule found.
    :var globalRevisionRule: Global RevisionRule based on preference "TC_config_rule_name".
    :var revisionRules: List of unique RevisionRule.
    :var preferredEffectivityInfo: Fetch the preferred effectivity information based on prdouct and RevisionRule only
    when 'fetchOnlyPreferredConfiguration' is true.
    :var addOpenObjAsPreferredEndItem: This flag is true. If none of the preferred end item revision or preferred
    VariantRule owninig object points to root.
    :var variantRules: List of VariantRule based on RevisionRule and owning object for VariantRule.
    :var preferredVarRuleOwningObjects: Fetch the list of owning object based on RevisionRule and product only when
    'fetchOnlyPreferredConfiguration' is true.
    :var serviceData: The Service Data.
    """
    marker: int = 0
    endIndex: int = 0
    totalFound: int = 0
    globalRevisionRule: RevisionRule = None
    revisionRules: List[RevisionRule] = ()
    preferredEffectivityInfo: EffectivityInfo = None
    addOpenObjAsPreferredEndItem: bool = False
    variantRules: List[VariantRule] = ()
    preferredVarRuleOwningObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class EffectivityInfo(TcBaseObj):
    """
    EffectivityInfo contains list of effectivity units, effectivity end items and effectivity dates.
    
    :var effectivityUnits: List of effectivity units.
    :var effectivityEndItems: List of effectivity end items.
    :var effectivityDates: List of effectivity dates.
    """
    effectivityUnits: List[int] = ()
    effectivityEndItems: List[BusinessObject] = ()
    effectivityDates: List[datetime] = ()


"""
RequestPreference is a map of preference name and value.
"""
RequestPreference = Dict[str, List[str]]
