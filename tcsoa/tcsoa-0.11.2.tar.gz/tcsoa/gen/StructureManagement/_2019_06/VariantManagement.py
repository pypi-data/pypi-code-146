from __future__ import annotations

from tcsoa.gen.StructureManagement._2013_05.VariantManagement import BOMVariantOptionValueEntry
from tcsoa.gen.BusinessObjects import BOMWindow, BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ApplyBOMVariantRulesResponse2(TcBaseObj):
    """
    It contains list of variant rules applied to a BOM window.
    
    :var rules: A list of BOMVariantRuleContents2 object associated with the BOMWidow
    :var serviceData: Object of service data, that returns partial errors.
    :var window: BOMWindow object on which rules have been applied
    """
    rules: List[BOMVariantRuleContents2] = ()
    serviceData: ServiceData = None
    window: BOMWindow = None


@dataclass
class BOMVariantRuleContents2(TcBaseObj):
    """
    Contains variant rule, the saved variant rules associated with the window, list of option value details and a
    boolean flag for constraints evaluation status.
    
    In getBOMVariantRules2 operation, this structure used as output. 
    
    In setBOMVariantRule2 operation, this structure used as input as well as output. As input, it contains details of
    variant rule, saved variant rule, saved variant rule modification flag and list of options that needs to be set on
    variant rule. As output, it contains details of variant rule with set option values. 
    
    In applyBOMVariantRules2 operation, this structure used as input as well as output. Typically the variantRule, svr,
    isSVRModified provide input and list of BOMVariantOptionValueEntry and isConstraintsEvaluated are used for output. 
    
    Constraints (defaults, derived defaults and rule check) will only be evaluated for single variant rule having
    single option value.
    
    :var variantRule: VariantRule with which window has been configured. This cannot be NULL.
    :var svr: Saved variant rule with which window has been configured. This will be NULL if window is not configured
    with saved variant rule.
    :var isSVRModified: True, if saved variant rule has been modified.
    :var bomVariantOptionValueEntry: List of options associated with VariantRule.
    :var isConstraintsEvaluated: True, if default, derived default have been evaluated.
    """
    variantRule: BusinessObject = None
    svr: BusinessObject = None
    isSVRModified: bool = False
    bomVariantOptionValueEntry: List[BOMVariantOptionValueEntry] = ()
    isConstraintsEvaluated: bool = False


@dataclass
class BOMVariantRuleOutput2(TcBaseObj):
    """
    Contains window and the list of rule associated with window. It has the identifier to map input variant rule to
    output variant rule.
    
    :var window: The BOMWindow on which rules are set.
    :var rules: A list of BOMVariantRuleContents2 objects.
    :var clientId: Identifier to map input variant rules to output variant rules.
    """
    window: BOMWindow = None
    rules: List[BOMVariantRuleContents2] = ()
    clientId: str = ''


@dataclass
class BOMVariantRulesResponse2(TcBaseObj):
    """
    List of varaint rule data associated with window.
    
    :var variantRuleData: A list of BOMVariantRuleOutput2 object.
    :var serviceData: Object of service data.
    """
    variantRuleData: List[BOMVariantRuleOutput2] = ()
    serviceData: ServiceData = None


@dataclass
class SetBOMVariantRuleData2(TcBaseObj):
    """
    Contains information about window and variant rule that needs to be set on the window. This structure will be used
    as an input and as an output. Input contains details of window and BOMVariantRuleContents2 that needs to be set on
    window. Output contains details of BOMVariantRuleContents2 having information about option values set on the
    variant rule.
    
    :var window: A BOMWindow object on which variant rules are to be set.
    :var rules: A list of BOMVariantRuleContents2 object which contain details of Variant Rule and list of options and
    values.
    :var clientId: Identifier string to map input variant rule to output variant rule.
    """
    window: BOMWindow = None
    rules: List[BOMVariantRuleContents2] = ()
    clientId: str = ''


@dataclass
class SetBOMVariantRulesResponse2(TcBaseObj):
    """
    SetBOMVariantRulesResponse2 object reference.
    
    :var variantRuleData: A list of objects containing SetBOMVariantRuleData2 object.
    :var serviceData: Object of service data that that returns partial errors.
    """
    variantRuleData: List[SetBOMVariantRuleData2] = ()
    serviceData: ServiceData = None
