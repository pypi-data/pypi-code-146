from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awb0ProductContextInfo, VariantRule, RevisionRule
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_06.OccurrenceConfiguration import EffectivityInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OptionValuesCursor(TcBaseObj):
    """
    OptionValuesCursor is a cursor that is returned for use in subsequent calls to get next page of results.
    
    :var startReached: If true, the first page of the results has been reached.
    :var endReached: If true, the last page of the results has been reached.
    :var startIndex: The Cursor start position for the result returned so far.
    :var endIndex: The Cursor end position for the result returned so far.
    :var pageSize: The maximum number of results that can be returned in one service call.
    :var isForward: If true scrolling is done in forward direction.
    """
    startReached: bool = False
    endReached: bool = False
    startIndex: int = 0
    endIndex: int = 0
    pageSize: int = 0
    isForward: bool = False


@dataclass
class RevisionRuleInfo(TcBaseObj):
    """
    'RevisionRuleInfo' contains list of RevisionRule objects along with their serialized strings.
    
    :var revisionRule: The RevisionRule.
    :var serializedRevRule: A string representing transient RevisionRule.This string is system generated which holds an
    information about name , description and all clauses in the RevisionRule as per the precedence order.Format of the
    string is encoded and it is for internal use only.
    """
    revisionRule: RevisionRule = None
    serializedRevRule: str = ''


@dataclass
class VariantContent(TcBaseObj):
    """
    Contains variant rule, the saved variant rules associated with the window, list of option value details. This
    structure is used for both getClassicVariants as well as createOrUpdateClassicVariantRule.
    
    :var variantRule: A VariantRule with which the current product is configured. This can be NULL
    :var variantOptionValueEntry: A list of options associated with VariantRule.
    """
    variantRule: VariantRule = None
    variantOptionValueEntry: List[VariantOptionValueEntry] = ()


@dataclass
class VariantOptionFilterData(TcBaseObj):
    """
    Option details for which option values are to be returned.
    
    :var optionUID: UID of the Variant that contains details of options and values.
    :var owningItemUID: UID of the Item on which option is set.
    """
    optionUID: str = ''
    owningItemUID: str = ''


@dataclass
class VariantOptionValue(TcBaseObj):
    """
    Contains options and configuration details.
    
    :var optionValue: Value assigned to an option.
    :var howset: It indicates how value is set. Valid values are as follows. 
    0: value is unset, 
    4: value is set by user.
    """
    optionValue: str = ''
    howset: int = 0


@dataclass
class VariantOptionValueEntry(TcBaseObj):
    """
    Options associated with VariantRule
    
    :var optionUID: UID of the Variant that contains details of options and values.
    :var owningItemUID: UID of the Item on which option is set.
    :var optionName: Name of the option associated.
    :var optionDesc: Description of the option.
    :var variantOptionValue: A list containing options and configuration details.
    """
    optionUID: str = ''
    owningItemUID: str = ''
    optionName: str = ''
    optionDesc: str = ''
    variantOptionValue: List[VariantOptionValue] = ()


@dataclass
class ClassicVariantsData(TcBaseObj):
    """
    Input for variant data request.
    
    :var productContext: Awb0ProductContextInfo of the product for which Variant information to be retrieved.
    :var variantRule: VariantRule for which option and value information are to be retrieved. This input is optional.
    If provided in the input, the option values returned will have a flag indicating option values set in the
    VariantRule.
    :var optionFilter: Option details for which option values are to be returned. An empty string value in this input
    element will return all options and their associated values.
    :var optionValuesCursor: A cursor that is returned for use in subsequent calls to get next page of results.
    """
    productContext: Awb0ProductContextInfo = None
    variantRule: VariantRule = None
    optionFilter: VariantOptionFilterData = None
    optionValuesCursor: OptionValuesCursor = None


@dataclass
class ClassicVariantsResp(TcBaseObj):
    """
    List of options and their values.
    
    :var productContext: Awb0ProductContextInfo for the product for which Variant information is retrieved.
    :var variantContent: Options and values associated with the product.
    :var serviceData: The service data containing updated object(s).
    """
    productContext: Awb0ProductContextInfo = None
    variantContent: VariantContent = None
    serviceData: ServiceData = None


@dataclass
class ConfigRuleResponse2(TcBaseObj):
    """
    ConfigRuleResponse2 contains RevisionRule and VariantRule information.
    
    :var marker: Number of preferred RevisionRule or VariantRule. Preferred RevisionRule or VariantRule are the one
    which are indexed through structure indexing. The default value is -1.
    :var endIndex: End index of page.
    :var totalFound: Total numbers of RevisionRule or VariantRule found.
    :var globalRevisionRule: Global RevisionRule based on preference "TC_config_rule_name".
    :var revisionRules: List of unique RevisionRule objects along with serialized string.
    :var preferredEffectivityInfo: Fetch the preferred effectivity information based on prdouct and RevisionRule only
    when 'fetchOnlyPreferredConfiguration' is true.
    :var addOpenObjAsPreferredEndItem: If true, none of the preferred effectivity end item 
    revision  or preferred VariantRule owninig object is opened product and the client will use the opened product as
    preferred end item or VariantRule owninig object .
    :var variantRules: List of VariantRule based on RevisionRule and owning object for VariantRule.
    :var preferredVarRuleOwningObjects: Fetch the list of owning object based on RevisionRule and product only when
    'fetchOnlyPreferredConfiguration' is true.
    :var serviceData: The Service Data.
    """
    marker: int = 0
    endIndex: int = 0
    totalFound: int = 0
    globalRevisionRule: RevisionRule = None
    revisionRules: List[RevisionRuleInfo] = ()
    preferredEffectivityInfo: EffectivityInfo = None
    addOpenObjAsPreferredEndItem: bool = False
    variantRules: List[VariantRule] = ()
    preferredVarRuleOwningObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateClassicVariantRuleData(TcBaseObj):
    """
    Input containing Awb0ProductContextInfo, user selected options and values and an optional saved VariantRule.
    
    :var productContext: Awb0ProductContextInfo of the product for which option and values are to be set.
    :var variantRuleName: Name of the VariantRule to be created.
    :var variantContent: A list of options and values provided by the user with an optional VariantRule. The input
    options and values are applied to the currently opened product.
    :var saveRule: If true, the input VariantRule will be updated. If false, input VariantRule will not be updated.
    Access checks will be applied during updation of the VariantRule.
    """
    productContext: Awb0ProductContextInfo = None
    variantRuleName: str = ''
    variantContent: VariantContent = None
    saveRule: bool = False
