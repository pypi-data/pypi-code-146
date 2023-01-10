from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, VariantRule, Variant, BOMWindow, Item
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ApplyBOMVariantRulesResponse(TcBaseObj):
    """
    It contains list of variant rules applied on the window.
    
    :var rules: List of  BOMVariantRuleContents object associated with the BOMWidow
    :var serviceData: Object of service data, that returns partial errors.
    :var window: BOMWindow object on which rules have been applied
    """
    rules: List[BOMVariantRuleContents] = ()
    serviceData: ServiceData = None
    window: BOMWindow = None


@dataclass
class GetBOMVariantRuleInput(TcBaseObj):
    """
    It contains information about window and saved variant rules which user want to add, delete, update or override.
    
    :var window: BOMWindow object for which variant rule is being requested.
    :var variantRule: The variant rule for which the contents are requested.
    :var svrs: List of saved variant rules which user want to add, unset, update or override. It is optional.
    :var clientId: unique identifier for each window. Output will have same identifier, to let caller know, which rule
    list is associated with which window.
    :var svrActionMode: This flag indicates different action mode associated to SVRs which includes  add (add new saved
    variant rule), unset (unset existing saved variant rule), update (update configuration using saved variant rule),
    override (override configuration using saved variant rule). 
    
    0     Set this value, when you want to get variant rule from window(default value).
    1      Set this value, when you want to apply or add new saved variant rule in case of multiple rule scenario
    2      Set this value, when you want to unset existing saved variant rule in case of multiple rule scenario. 
    3     Set this mode, if user wants to override existing option value in saved variant rule.
    4     Set this mode, if user wants to update existing option value in saved variant rule.
    """
    window: BOMWindow = None
    variantRule: VariantRule = None
    svrs: List[BusinessObject] = ()
    clientId: str = ''
    svrActionMode: int = 0


@dataclass
class GetVariantExpressionsMatchInfoResponse(TcBaseObj):
    """
    The response of method getVariantExpressionsMatchInfo.
    
    :var variantExpressionsDetails: The entries in this list corresponds to each input InputBOMLinesSet.
    :var serviceData: The partial errors.
    """
    variantExpressionsDetails: List[VariantExpressionsDetails] = ()
    serviceData: ServiceData = None


@dataclass
class InputBOMLinesSet(TcBaseObj):
    """
    The list of roll up BOMLine objects and non-roll up BOMLine objects.
    
    :var rollUpBOMLines: The list of BOMLine objects for which rolled up variant conditions and rolled up clause lists 
    to be calculated. If this list is empty, then this operation will populate the variant expressions for the
    nonRollUPBOMLines and their corresponding clause lists in the response.
    :var nonRollUpBOMLines: The list of BOMLine objects for which occurrence variant conditions and clause lists to be
    returned. If this list is empty, , then this operation will populate the rolled up variant expressions and
    corresponding clause lists in the response.
    :var doCompare: If true, the comparison will be peformed between all the input bomLines i.e. rollUpBOMLines and
    nonRollUpBOMLines till a mismatch is found.
    """
    rollUpBOMLines: List[BOMLine] = ()
    nonRollUpBOMLines: List[BOMLine] = ()
    doCompare: bool = False


@dataclass
class BOMVariantOptionValueEntry(TcBaseObj):
    """
    It contains details of option, its description and values associated with that particular option.
    
    :var option: Variant object that contains details of option value.
    :var owningItem: Item on which option is set.
    :var optionName: Name of the option associated with Item
    :var optionDesc: Additional information about option
    :var variantOptionValue: List containing options and configuration details
    """
    option: Variant = None
    owningItem: Item = None
    optionName: str = ''
    optionDesc: str = ''
    variantOptionValue: List[VariantOptionValue] = ()


@dataclass
class BOMVariantRuleContents(TcBaseObj):
    """
    BOMVariantRuleContents contains variant rule, the saved variant rules associated with the window,   list of option
    value details and a boolean flag for constraints evaluation status.
      
    In getBOMVariantRules operation , this structure used as output. 
    
    In setBOMVariantRule operation, this structure used as input as well as output. As input, it contains details of
    variant rule, saved variant rule, saved variant rule modification flag and list of options that needs to be set on
    variant rule. As output, it contains details of variant rule with set option values. 
    
    In applyBOMVariantRules operation, this structure used as input as well as output. Typically the variantRule, svr,
    isSVRModified provided as input and  list of BOMVariantOptionValueEntry and isConstraintsEvaluated are part of
    output.  
     
    Constraints (defaults, derived defaults and rule check) will only be evaluated for single variant rule having
    single option value.
    
    
    :var variantRule: VariantRule with which window has been configured. This cannot be NULL
    :var svr: Saved variant rule with which  window has been configured. This will be NULL if window is not configured
    with saved variant rule.
    :var isSVRModified: True, if saved variant rule has been modified.
    :var bomVariantOptionValueEntry: List of options associated with VariantRule 
    :var isConstraintsEvaluated: True, if default, derived default have been evaluated
    """
    variantRule: VariantRule = None
    svr: BusinessObject = None
    isSVRModified: bool = False
    bomVariantOptionValueEntry: List[BOMVariantOptionValueEntry] = ()
    isConstraintsEvaluated: bool = False


@dataclass
class BOMVariantRuleOutput(TcBaseObj):
    """
    BOMVariantRuleOutput contains window and the list of rule associated with window. It has the identifier to map
    input variant rule to output variant rule.
    
    :var window: BOMWindow on which rules are set
    :var rules: List of  BOMVariantRuleContents  objects
    :var clientId: Identifier to map input variant rules to output variant rules.
    """
    window: BOMWindow = None
    rules: List[BOMVariantRuleContents] = ()
    clientId: str = ''


@dataclass
class BOMVariantRulesResponse(TcBaseObj):
    """
    List of varaint rule data associated with window.
    
    :var variantRuleData: List of  BOMVariantRuleOutput  object
    :var serviceData: Object of service data.
    """
    variantRuleData: List[BOMVariantRuleOutput] = ()
    serviceData: ServiceData = None


@dataclass
class SetBOMVariantRuleData(TcBaseObj):
    """
    SetBOMVariantRuleData contains information about window and variant rule that needs to be set on the window. This
    structure will be used as an input and as an output. Input contains details of  window and BOMVariantRuleContents 
    that needs to be set on window . Output contains details of BOMVariantRuleContents  having information about option
    values set on the variant rule.
    
    :var window: BOMWindow object on which variant rules will be set
    :var rules: A list of BOMVariantRuleContents  object which contain details of Variant Rule and list of options and
    values.
    :var clientId: Identifier to map input variant rule to output variant rule
    """
    window: BOMWindow = None
    rules: List[BOMVariantRuleContents] = ()
    clientId: str = ''


@dataclass
class SetBOMVariantRulesResponse(TcBaseObj):
    """
    SetBOMVariantRulesResponse object reference.
    
    :var setBOMVariantRuleData: List of  objects containing setBOMVariantRuleData  object 
    :var serviceData: Object of service data that that returns partial errors
    """
    setBOMVariantRuleData: List[SetBOMVariantRuleData] = ()
    serviceData: ServiceData = None


@dataclass
class VariantExpressionClauseList(TcBaseObj):
    """
    Contains clauseList object and corresponding clause list text.
    
    :var clauseListText: The text representation of the clauseList. If the line does not have the variant condition
    then this list will be empty.
    :var clauseList: The clauseList object of the VarientExpression. If the line does not have the variant condition
    then corresponding entry in this list will be null.
    """
    clauseListText: List[str] = ()
    clauseList: BusinessObject = None


@dataclass
class VariantExpressionsDetails(TcBaseObj):
    """
    The VariantExpressionsDetails represents response for each input InputBOMLinesSet. It contains clause List and
    corresponding clause List text for rollUpBOMLines and nonRollUpBOMLines.
    
    :var rollUpClauseList: The rolled up clause list object and clauseListText for the BOMLine objects in the
    rollUpBomLines list. Each entry in this list corresponds to one BOMLine in rollUpBomLines list.
    :var nonRollUpClauseList: The clause lists for the BOMLines objects in the nonRollUpBomLines list.
    :var isDifferent: True if the input doCompare flag is set and any of the BOMLines of the inputBOMLinesSets are
    different due to variant conditions.
    """
    rollUpClauseList: List[VariantExpressionClauseList] = ()
    nonRollUpClauseList: List[VariantExpressionClauseList] = ()
    isDifferent: bool = False


@dataclass
class VariantOptionValue(TcBaseObj):
    """
    Details of option values.
    
    :var value: Value assigned to option 
    :var howSet: Indicates, how value is set. Possible values are  
    -     Unset  value is unset, 
    -     Unset (potentially derived)  derivable value is unset,
    -     Derived  value is from derived option value  ,
    -     Defaulted  value from default option value, 
    -     Set by User  value is set by user, 
    -     Set by Rule  value is set by rule,
    -     Variant Item  value set by variant item
    
    
    :var howSetInt: It indicates how value is set. It is integer representation of  howSet. 
    Valid values are as follows. 
    0  value is unset, 
    1  derivable value is unset,
    2  value is from derived option value  ,
    3  value from default option value, 
    4  value is set by user, 
    5  value is set by rule,
    8  value set by variant item.
    
    :var whereSet: Name of saved variant rule given by user or name of the owningItem
    :var index: Position of option value in variant revision
    :var isConfiguredOptionValue: If rule is configured with particular option value.
    """
    value: str = ''
    howSet: str = ''
    howSetInt: int = 0
    whereSet: str = ''
    index: int = 0
    isConfiguredOptionValue: bool = False
