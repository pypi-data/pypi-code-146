from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Cfg0AbsValue, WorkspaceObject, VariantRule, Cfg0ConfiguratorPerspective
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OptionFamily(TcBaseObj):
    """
    A collection of option values.
    
    :var family: The UID of the variant option family.
    :var familyDisplayName: The display name of the variant option family.
    :var familyType: The data type of option values within this family.
    :var isThumbnailDisplay: If true, option values are displayed as tile with thumbnail. If false, option values are
    displayed as simple text. 
    Value of this parameter is governed by preference PCA_Display_Thumbnail.
    :var familyOptions: A map (string, boolean) indicating the various decorations for this family like, if the family
    is complete, single/multi-select, freeform etc. Valid keys are:
    - isComplete: Indicating if at least one option value has been selected in mandatory family.  If true, option
    family is complete. If false, option family is considered incomplete. Optional families are always considered
    complete.
    - isSingleSelect: Indicate if multiple option values in a family allowed to be selected. If true, multiple
    selections are not allowed. If false, multiple selections are allowed.
    
    
    :var optionValues: The list of option values within this family.
    """
    family: str = ''
    familyDisplayName: str = ''
    familyType: str = ''
    isThumbnailDisplay: bool = False
    familyOptions: FamilyOptionMap = None
    optionValues: List[OptionValue] = ()


@dataclass
class OptionGroup(TcBaseObj):
    """
    Collection of variant option families.
    
    :var optGroup: The UID of the variant option group.
    :var groupDisplayName: The display name of the variant option group.
    :var isComplete: Indicates if all required option value selections are complete within this group.
    :var families: The list of option families within this group.
    """
    optGroup: str = ''
    groupDisplayName: str = ''
    isComplete: bool = False
    families: List[OptionFamily] = ()


@dataclass
class OptionValue(TcBaseObj):
    """
    The Variant option value.
    
    :var optValue: The variant option value object. The value is populated when Thumbnail display is ON.
    :var optValueStr: The UID of the variant option value. The value is popouated when Thumbnail display is off.
    :var valueDisplayName: The display name of the variant option value.
    :var selectionState: The state of value selection. 0 - Unselected, 1 - Selected (equal to), and 2 - Negatively
    selected (not equal to).
    :var allowedSelectionStates: A list of all allowable selection states for option value based on current option
    value selections and constraint rules. Valid values in array are 0 - Unselected, 1 - Selected (equal to), and 2 -
    Negatively selected (not equal to). If all states are allowed for an option value, the list will be empty.
    """
    optValue: Cfg0AbsValue = None
    optValueStr: str = ''
    valueDisplayName: str = ''
    selectionState: int = 0
    allowedSelectionStates: List[int] = ()


@dataclass
class OptionValueSelection(TcBaseObj):
    """
    Option value and its selection state as selected by a user.
    
    :var optionValue: The UID of the variant option value ( Cfg0AbsValue ).
    :var selectionState: Variant option value (Cfg0AbsValue) selection state. 0 - Unselected, 1 - Selected (equal to),
    and 2 - Negatively selected (not equal to)
    """
    optionValue: str = ''
    selectionState: int = 0


@dataclass
class SelectionSummary(TcBaseObj):
    """
    Pair of option family name to selected option value.
    
    :var selectionState: Variant option value (Cfg0AbsValue) selection state. Valid values are 1 - Selected (equal to),
    or 2 - Negatively selected (not equal to).
    :var familyDisplayName: Display name of the option family selected. In case of Boolean or multi select families,
    this parameter would contain the option value display name.
    :var valueDisplayValue: Display name of the option value selected. In case of Boolean or multi select families,
    this parameter would be empty.
    """
    selectionState: int = 0
    familyDisplayName: str = ''
    valueDisplayValue: str = ''


@dataclass
class SelectionsSummary(TcBaseObj):
    """
    Summary of all selections in displayable format.
    
    :var summaryOfSelections: The list of all selections per family in user friendly displayable format.
    :var displayName: Display name of selections summary panel.
    :var internalName: Internal name of selections summary panel. This name is used to identify if user has requested
    to view selections summary panel.
    """
    summaryOfSelections: List[SelectionSummary] = ()
    displayName: str = ''
    internalName: str = ''


@dataclass
class VariantConfigurationDataInput(TcBaseObj):
    """
    The input containing the configurator context and variant option value selections to fetch the available
    variability.
    
    :var configContext: The variant configurator context. Valid input types are Item or ItemRevision. This parameter is
    ignored if the 'configPerspective' parameter is passed as not null.
    :var configPerspective: The configurator perspective. When this operation is invoked first time, this parameter
    would be null. But in all subsequent calls, this parameter must be populated with the configurator perspective
    retrieved in the response.
    :var selectedObject: The selected object for which variant configurator context to be retrieved. It can be a
    runtime business object (e.g. instance of Awb0Element) or persistent variant configurable business object (e.g.
    instance of Mdl0ConditionalElement). This parameter is ignored if either configContext or configPerspective is
    passed in input.
    :var optionGroup: The UID of group for which the next valid selections must to be retrieved. If this parameter is
    empty, then option values from model group would be retrieved.
    :var initialVariantRule: An optional initial VariantRule whose expression can be used as input selections for
    computing next valid selections. The parameter is ignored if the 'optionValueSelectionMap' is populated
    :var userSelections: Map(string, OptionValueSelection) of all option values selected by user per family.
    :var guidedConfigurationMode: The configuration mode choice.
    If true, the next valid selections within a group are retrieved after applying configurator constraints. This is
    the Guided configuration mode.
    If false, the next selections within a group are retrieved without applying constraints. This is the Manual
    configuration mode.
    :var switchingToGuidedMode: Flag indicating if we are switching to Guided configuration mode from Manual
    configuration mode. if true, input selections are validated against all constraints. If false, no validation is
    performed.
    """
    configContext: WorkspaceObject = None
    configPerspective: Cfg0ConfiguratorPerspective = None
    selectedObject: BusinessObject = None
    optionGroup: str = ''
    initialVariantRule: VariantRule = None
    userSelections: UserSelectionMap = None
    guidedConfigurationMode: bool = False
    switchingToGuidedMode: bool = False


@dataclass
class VariantConfigurationDataResponse(TcBaseObj):
    """
    The output containing the available variability for the input list of variant option value selections.
    
    :var currentGroup: The variant option group for which the valid selections are retrieved.
    :var allGroups: The list of all variant option groups available in the current Configurator Context.
    :var selectionsSummary: The summary of all selections in displayable format.
    :var isValidConfiguration: Indicates if selections in userSelections map are valid configuration or not. This
    parameter is relevant only when guidedConfigurationMode is true.
    :var configPerspective: The configurator perspective containing all information about the current Configurator
    Context, revision rule and effectivity. All further communications with the server to retrieve variant
    configuration data must use this object.
    :var userSelections: Map(string, OptionValueSelection) of all option values selected by user per family.This map is
    populated from selected option values from initialVariantRule. If initialVariantRule is passed null, this parameter
    would be empty.
    :var serviceData: ServiceData containing partial exceptions, if any.
    """
    currentGroup: str = ''
    allGroups: List[OptionGroup] = ()
    selectionsSummary: SelectionsSummary = None
    isValidConfiguration: bool = False
    configPerspective: Cfg0ConfiguratorPerspective = None
    userSelections: UserSelectionMap = None
    serviceData: ServiceData = None


@dataclass
class CreateCustomVariantRuleResponse(TcBaseObj):
    """
    The output containing custom variant rule.
    
    :var customVariantRule: The adhoc custom variant rule created or updated.
    :var serviceData: ServiceData containing partial exceptions, if any.
    """
    customVariantRule: VariantRule = None
    serviceData: ServiceData = None


"""
Map(string, OptionValueSelection) of all option values selected by user per family.
"""
UserSelectionMap = Dict[str, List[OptionValueSelection]]


"""
A map of ( std::string, bool ) indicating various family options and their values.
"""
FamilyOptionMap = Dict[str, bool]
