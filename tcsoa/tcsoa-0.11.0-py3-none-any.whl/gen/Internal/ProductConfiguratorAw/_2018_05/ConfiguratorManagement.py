from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject, VariantRule, Cfg0ConfiguratorPerspective
from typing import Dict, List
from tcsoa.gen.Internal.ProductConfiguratorAw._2017_12.ConfiguratorManagement import OptionValueSelection, OptionFamily
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OptionFamily(TcBaseObj):
    """
    A collection of features. It also contains selection state and allowed selection states for the current rendered
    family.
    
    :var selectionInfo: This will hold the nodeID of the Feature and its selection state.
    :var familyObj: ViewModelObject which represents family object information e.g. displayName, type.
    :var features: A list of all allowable selection states for option family based on current option value selections
    and constraint rules. Valid values refer to 1.1.1.10 section.
    :var allowedSelectionStates: A list of all allowable selection states for option value based on current option
    value selections and constraint rules. Following are the valid values:
    
    NoSelection ->0
    User positive Selection->1
    User negative Selection->2
    systemDefault positive Selection->5
    systemDefault negative Selection-> 6
    system positive Selection -> 9
    system negative Selection -> 10
    :var labelInfo: A map (string, vector<string>) of label type and list of nodeID of ViewModelObject.
    Valid keys : "violations", "package"
     Values: nodeID of ViewModelObject
     If key ==  "violation", then:
     Value = list of appropriate nodeID of a ViewModelObject of type "violation".
    """
    selectionInfo: Selection = None
    familyObj: ViewModelObject = None
    features: List[Feature] = ()
    allowedSelectionStates: List[int] = ()
    labelInfo: StringMap = None


@dataclass
class Scope(TcBaseObj):
    """
     Scope stores the collection of variant option families. Scope represents the top level object in the hierarchy of
    configuration data that is displayed in the client.
    
    :var nodeID: The UID of the variant option group or partition.
    :var scopeObj: This ViewModelObject store information of scope object such as nodeID, displayName, internalName.
    :var families: A list of option families within this group.
    """
    nodeID: str = ''
    scopeObj: ViewModelObject = None
    families: List[OptionFamily] = ()


@dataclass
class SelectedExpression(TcBaseObj):
    """
    Structure containing expression selection for the given affected object. If the expression has split then there
    will be more than one SelectedExpression structure with same affectedObject UID.
    
    :var affectedObject: UID of the Affected Object.
    :var displayValue: Display value of the affected object.
    :var userSelections: Represents list of Map (string, OptionValueSelection) of all option values selected by user
    per family.
    :var familySelections: Represents list of Map (string, int) of all families selected by user. Key is UID of
    Cfg0AbsFamily object and value is selection state of the family. 
     0 &ndash; Unselected.
     1 - User selected (equal to).
     2 - Negatively user selected (not equal to).
     3 - System Selected (equal to).
     4 - Negatively system selected (not equal to).
     5 - Default Selected (equal to).
     6 - Negatively default selected (not equal to).
    """
    affectedObject: str = ''
    displayValue: str = ''
    userSelections: UserSelectionMap2 = None
    familySelections: FamilySelectionMap = None


@dataclass
class SelectedExpressions(TcBaseObj):
    """
    Store selections against affected object UID.
    
    :var affectedObject: Object UID for which selection is stored, valid values are UIDs of Awb0Element, VariantRule,
    and Mdl0ModelElement.
    :var columnId: For split cases it will hold the column number for given affected object.
    :var selections: Map of (OptionFamily nodeID and list of Selections) nodeID of OptionFamily or Feature and list of
    Selection.
    """
    affectedObject: str = ''
    columnId: int = 0
    selections: SelectionMap = None


@dataclass
class Selection(TcBaseObj):
    """
    This structure stores nodeID of OptionFamily or Feature along with its selection state.
    
    :var nodeID: The nodeID of the OptionFamily or Feature structures in the response.
    :var selectionState: The state of object selection. The below are given valid values.
    Selection state values are
    NoSelection ->0
    User positive Selection->1
    User negative Selection->2
    systemDefault positive Selection->5
    systemDefault negative Selection-> 6
    system positive Selection -> 9
    system negative Selection -> 10
    """
    nodeID: str = ''
    selectionState: int = 0


@dataclass
class SelectionSummary(TcBaseObj):
    """
    Pair of option family name to selected option value.
    
    :var selectionState: The state of Cfg0AbsValue or Cfg0AbsFamily selection.
    :var familyDisplayName: Display name of the option family (Cfg0AbsFamily) selected. In case of Boolean or multi
    select families, this parameter would contain the option value display name.
    :var valueDisplayName: Display name of the option value (Cfg0AbsValue) selected. In case of Boolean, multi select
    families or family selection, this parameter would be empty.
    """
    selectionState: int = 0
    familyDisplayName: str = ''
    valueDisplayName: str = ''


@dataclass
class SelectionsSummary(TcBaseObj):
    """
    Summary of all selections in displayable format.
    
    :var summaryOfSelections: A list of all selections per family in user friendly displayable format.
    :var requiredFamilies: Information about which families are mandatory.
    :var displayName: Display name of selections summary panel.
    :var internalName: Internal name of selections summary panel. This name is used to identify if user has requested
    to view selections summary panel.
    """
    summaryOfSelections: List[SelectionSummary] = ()
    requiredFamilies: List[SelectionSummary] = ()
    displayName: str = ''
    internalName: str = ''


@dataclass
class ValidateProductConfigResponse(TcBaseObj):
    """
    It is the structure containing response of operation validateProductConfiuration.
    
    :var validateProductConfigurationOutputs: A list of ValidateProductConfigurationOutput structure. The sequence in
    this list is same as the input sequence of SelectedExpression.
    :var serviceData: ServiceData containing partial exceptions, if any. Partial exceptions are added as per index of
    input SelectedExpression in the list.
    """
    validateProductConfigurationOutputs: List[ValidateProductConfigurationOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ValidateProductConfigurationOutput(TcBaseObj):
    """
    It is the structure containing the violations and SelectionMap for each affected object.
    
    :var criteriaStatus: Indicate if input configuration is valid or not. If true, input configuration is valid;
    otherwise, input configuration is invalid.
    :var valueToViolations: A map (string, Violations) of all violated values.
    :var outputSelections: A map (string, list of OptionValueSelection) of expanded selections that is in accordance
    with the given input selections and the rules in the context.
    """
    criteriaStatus: bool = False
    valueToViolations: ValueToViolations = None
    outputSelections: UserSelectionMap2 = None


@dataclass
class VariantConfigurationViewIn(TcBaseObj):
    """
    The input containing the selected context and selections to fetch the available variability.
    
    :var configPerspective: The configurator perspective. When this operation is invoked first time, this parameter
    would be null. But in all subsequent calls, this parameter must be populated with the configurator perspective
    retrieved in the response.
    :var selectedContext: The selected object for which variant configurator context to be retrieved. It can be a
    runtime business object (instance of Awb0Element) or persistent variant configurable business object (instance of
    Mdl0ConditionalElement). This parameter is ignored if configPerspective is passed in input.
    :var activeVariantRules: An optional list of active VariantRule whose expression can be used as input selections
    for computing next valid selections. The parameter is ignored if the &lsquo;selections&rsquo; is populated.
    :var scopes: A list of UIDs of Scope (Cfg0AbsFamilyGroup, Ptn0Partition) for which the next valid selections must
    to be retrieved. If this parameter is empty, then option values from model group (Cfg0AbsFamilyGroup) are are
    retrieved.
    :var selections: List of all user and system selections for the custom configuration or the configurable object.
    :var payloadStrings: A map (string, list of strings) represents the payload that is transferred between client and
    server for the current session. The operation would use the payload as the state information to process the request.
    The client should pass the same payloadStrings that is returned by previous call if the state information is to be
    maintained for the current request.
    Valid map:
    "violation" -> { "list of nodeIDs of viewModelObject which hold the violation" }
    :var requestInfo: Map (string, string) of request names and value pairs. Allowed names are: 
    -"requestType" : This gives the operation to be handled for the SOA call.   
    [ "requestType" -> { ("viewPackage") | ("selectPackage") | ("addPackage") | ("cancelPackage") | ("getConfig") |
    ("validate") | ("switchToManual") | ("expand") }]
    - "selectedPackage" : nodeID of selected package feature object. This is required in case of requestType is one of
    "viewPackage", "selectPackage", "cancelPackage", "addPackage".
    - "configurationControlMode" is the configuration view mode in manual mode invalid selections are allowed.
    ["configurationControlMode" -> { "guided" | "manual" }]
    - "severity" : This will give information what all violations you want to show.
    ["severity" &#61672; { "error" | "warn" | "info" }]
    -"viewName" : This will hold the current configuration view name.
    [" viewName" &#61672; { "guidedConfig" | "manualWithError" | "manualWithExpand" | "package"}]
    """
    configPerspective: Cfg0ConfiguratorPerspective = None
    selectedContext: BusinessObject = None
    activeVariantRules: List[VariantRule] = ()
    scopes: List[str] = ()
    selections: List[SelectedExpressions] = ()
    payloadStrings: StringMap = None
    requestInfo: StringMap = None


@dataclass
class VariantConfigurationViewResponse(TcBaseObj):
    """
    The output containing the available variability for the input list of variant option value selections.
    
    :var configPerspective: The configurator perspective containing all information about the current Configurator
    Context, revision rule and effectivity. All further communications with the server to retrieve variant
    configuration data must use this object.
    :var scopes: UID of the current expanded group or partition.
    :var allScopes: The list of all variant option groups available in the current Configurator Context.
    :var selections: A list of SelectedExpressions strutures.
    :var selectionsSummary: The summary of all selections in displayable format.
    :var labels: ViewModelObjectLabelMap of labels.
    :var payloadStrings: A map (string, list of strings) represents the payload that is transferred between client and
    server for the current session. The operation would use the payload as the state information to process the request.
    :var responseInfo: Map (string, string) of response names and value pairs. Allowed names are:
    -"requestType" : This gives the operation to be handled for the SOA call.   
    [ "requestType" -> { ("viewPackage") | ("selectPackage") | ("addPackage") | ("cancelPackage") | ("getConfig") |
    ("validate") | ("switchToManual") | ("expand") }]
    - "selectedPackage" : nodeID of selected package feature object. This is required in case of requestType is one of
    "viewPackage", "selectPackage", "cancelPackage", "addPackage".
    - "configurationControlMode" is the configuration view mode in manual mode invalid selections are allowed.
    ["configurationControlMode" -> { "guided" | "manual" }]
    - "severity" : This will give information what all violations you want to show.
    ["severity" &#61672; { "error" | "warn" | "info" }]
    :var serviceData: Contains the list of all BusinessObjects that make up the output, as well as any errors that
    might have occurred as part of the service invocation.
    """
    configPerspective: Cfg0ConfiguratorPerspective = None
    scopes: List[str] = ()
    allScopes: List[Scope] = ()
    selections: List[SelectedExpressions] = ()
    selectionsSummary: SelectionsSummary = None
    labels: ViewModelObjectLabelMap = None
    payloadStrings: StringMap = None
    responseInfo: StringMap = None
    serviceData: ServiceData = None


@dataclass
class VariantExpressionDataInput(TcBaseObj):
    """
    The input structure for the getVariantExpressionData operation containing either the selected objects or current
    expanded families and optionally containing configurator context, configurator perspective, and variant expression
    filters.
    
    :var configContextProvider: The configurator context provider object. It is optional. If not null, it is used to
    find configurator context object. Valid input types are ItemRevision, Awb0Element and Mdl0ConditionalElement. This
    parameter is ignored if configContext or configPerspective parameters are passed.
    :var configContext: The variant configurator context. Valid input types are Item or ItemRevision. This parameter is
    ignored if the configPerspective parameter is passed.
    :var configPerspective: Input Cfg0ConfiguratorPerspective. It is optional. Cfg0ConfiguratorPerspective object is
    used as communication mechanism for the configuration and the valid configurator contexts across the Product
    Configurator and its consuming applications such as 4G Designer, Structure Manager. If it is empty then the config
    perspective is obtained from the selected objects.
    :var selectedObjects: The list of selected business objects. If this parameter is empty then
    currentExpandedFamilies and configPerspective should be provided. The supported business object types are
    Awb0Element, Mdl0ConditionalElement and variant configurable business objects - BOMLine, VariantRule.
    :var currentExpandedFamilies: The list of expanded option families. If the input contains only
    currentExpandedFamilies and configPerspective as non-empty input then operation will return only the Option values
    of the provided families.
    :var filters: The input filters that govern the option family and value response. For instance input filter may
    contain option filter (&lsquo;showCurrentElements&rsquo;, &lsquo;showFamilies&rsquo; ) or intent filters (from
    Cfg0ObjectIntentions List Of Values).
    """
    configContextProvider: BusinessObject = None
    configContext: WorkspaceObject = None
    configPerspective: Cfg0ConfiguratorPerspective = None
    selectedObjects: List[BusinessObject] = ()
    currentExpandedFamilies: List[str] = ()
    filters: VariantExpressionFilters = None


@dataclass
class VariantExpressionDataResponse(TcBaseObj):
    """
    Variant expression response for the selected objects.
    
    :var optionFamilies: List of option Families.
    :var selectedExpression: The list of selections of all option values that form the expression on the input object.
    If the expression has split then there will be more than one SelectedExpression structure with same affectedObject
    UID.
    :var configPerspective: Output configurator perspective. Configurator Perspective object is used as communication
    mechanism for the configuration and the valid configurator contexts across the Product Configurator and its
    consuming applications such as 4G Designer, Structure Manager.
    :var filters: The filters applied on the output to render the option families and values.
    :var serviceData: Service Data containing partial errors, if any.
    """
    optionFamilies: List[OptionFamily] = ()
    selectedExpression: List[SelectedExpression] = ()
    configPerspective: Cfg0ConfiguratorPerspective = None
    filters: VariantExpressionFilters = None
    serviceData: ServiceData = None


@dataclass
class VariantExpressionFilters(TcBaseObj):
    """
    Variant expression filter structure containing intent filters and option filter.
    
    :var intentFilters: Represents the list of Intent filters. The valid values are the Cfg0ObjectIntentions List Of
    Values.
    :var optionFilter: Option output filter. Valid values are &lsquo;showCurrentElements&rsquo;,
    &lsquo;showFamilies&rsquo;.
    """
    intentFilters: List[str] = ()
    optionFilter: str = ''


@dataclass
class ViewModelObject(TcBaseObj):
    """
    The generic object that is used in this SOA request and response.
    User facing object that is used by the client of this SOA. It encapsulates a model object in server side.
    This object represent each object which is visible on UI like Scope, Feature, OptionFamily.
    
    :var wsObject: WorkspaceObject to be rendered.
    :var sourceUid: The UID of the object to be rendered. Valid values are either valid UIDs of configurable object
    along with context UIDs.
    :var displayName: The display name of the object.
    :var sourceType: Type of the ViewModelObject. Valid values are following Business object types: Cfg0AbsFamilyGroup,
    Cfg0PackageOptionValue, Cfg0AbsValue, Cfg0AbsFamily.
    :var props: Map of (string, list of strings) ViewModelObject property and value.
    Valid keys: "isFreeForm", "isMultiSelect", "isPackage".
    """
    wsObject: WorkspaceObject = None
    sourceUid: str = ''
    displayName: str = ''
    sourceType: str = ''
    props: StringMap = None


@dataclass
class ViewModelObjectLabelType(TcBaseObj):
    """
    ViewModelObjectLabelType will be used in ViewModelObjectLabelMap to get the violation and package information.
    
    :var nodeMap: Map of string, vector<ViewModelObject> ViewModelObject.
    """
    nodeMap: ViewModelObjectMap = None


@dataclass
class Violation(TcBaseObj):
    """
    This structure contains list of severities and messages for violations.
    
    :var severities: A list of severities of violations found during validation.
    :var messages: A list of messages of violations found during validation.
    """
    severities: List[int] = ()
    messages: List[str] = ()


@dataclass
class Feature(TcBaseObj):
    """
    Feature stores the information for the Variant feature to be displayed to the user. This contains the current
    selection state of the feature and labels such as violations.
    
    :var selectionInfo: This will hold the nodeID of the Feature and its selection state.
    :var featureObject: ViewModelObject which represents feature object information.
    :var allowedSelectionStates: A list of all allowable selection states for option value based on current option
    value selections and constraint rules. Following are the valid values:
    
    NoSelection ->0
    User positive Selection->1
    User negative Selection->2
    systemDefault positive Selection->5
    systemDefault negative Selection-> 6
    system positive Selection -> 9
    system negative Selection -> 10
    :var labelInfo: A map (string, list of strings) of label type and list of nodeID of ViewModelObjects.
    nodeIDViewModelObjectIf key == "violation", then:
       Value = list of appropriate nodeID of a ViewModelObjects of type "violation".
    """
    selectionInfo: Selection = None
    featureObject: ViewModelObject = None
    allowedSelectionStates: List[int] = ()
    labelInfo: StringMap = None


@dataclass
class FilterPanelDataResponse(TcBaseObj):
    """
    Filter Panel Data response for the selected object.
    
    :var featureParameters: The details of feature filter parameter Current Elements, Show Families and their selection
    state. Current Elements and Show Families are display name defined in text server locale file.
    :var intentParameters: The details of Intents filter parameter Manufacturing, Marketing, and Technical. These
    intents will be retrieve from LOV Cfg0ObjectIntentions.
    """
    featureParameters: List[FilterParameter] = ()
    intentParameters: List[FilterParameter] = ()


@dataclass
class FilterParameter(TcBaseObj):
    """
    Filter parameter details and its selection state.
    
    :var internalName: Internal name of the filter parameter.
    :var displayName: Display name of the filter parameter.
    :var isSelected: If true the parmeter is selected.
    """
    internalName: str = ''
    displayName: str = ''
    isSelected: bool = False


"""
Map(string, OptionValueSelection) of all option values selected by user per family.
"""
UserSelectionMap2 = Dict[str, List[OptionValueSelection]]


"""
A map (string, Violations) of all violated values.
"""
ValueToViolations = Dict[str, Violation]


"""
Map of string, and list of ViewModelObjectLabelType which will hold ViewModelObjects for violations and package.

The valid keys are "violations", "package"
The value is ViewModelObjectLabelType which contains the ViewModelObjects in a map where key names are nodeID and values are corresponding "violation" or "package" ViewModelObjects.
"""
ViewModelObjectLabelMap = Dict[str, List[ViewModelObjectLabelType]]


"""
Map of string and list of ViewModelObject. The key represents the nodeID of the ViewModelObject.
This map is useful for the client to obtain ViewModelObject from labels structure given a nodeID.
For example: The server will send the response of labelInfo Map in Feature structure containing violations in the following format, 
labelInfo["violations"] = [ "nodeID1", "nodeID3", "nodeID5" ]
The client will use the nodeIDs list and look into the ViewModelObjectMap of the "violations" label and fetch the corresponding ViewModelObject for the given nodeID.
"""
ViewModelObjectMap = Dict[str, List[ViewModelObject]]


"""
Map(string, int) of all family selected by user.
"""
FamilySelectionMap = Dict[str, int]


"""
Map of OptionFamily nodeID and list of Selections.
Map key will hold the nodeID of the OptionFamily and values contain the Selection list for features of the family.
"""
SelectionMap = Dict[str, List[Selection]]


"""
Map of string and list of strings.
"""
StringMap = Dict[str, List[str]]
