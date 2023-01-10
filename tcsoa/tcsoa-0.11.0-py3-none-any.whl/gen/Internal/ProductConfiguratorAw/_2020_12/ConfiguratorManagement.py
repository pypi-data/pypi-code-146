from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject, VariantRule, Cfg0ConfiguratorPerspective
from typing import Dict, List
from tcsoa.gen.Internal.ProductConfiguratorAw._2018_05.ConfiguratorManagement import SelectionsSummary, Violation, VariantExpressionFilters, ViewModelObjectLabelType
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ApplicationConfigExpression(TcBaseObj):
    """
    Structure representing a single variant expression.
    
    :var formula: The persistent configuration formula string.
    :var exprID: The application expression identifier used to distinguish the current expression from other variant
    expressions authored for the same business object.
    :var exprType: Expression type represents expression category and the intent of this expression. The valid values
    are as follows: 9  - Variant Condition, 18 - Variant Rule, 25 &ndash; Applicability,44 &ndash; Subject , 28 -
    Inclusive Constraint,29 - Exclusive Constraint,37 - Default Rule,41 - Availability Rule etc. which are defined in
    cfg_tokens.h file.
    :var configExprSets: A list of 'ConfigExpressionSet' which are relevant to the business object. The variant
    expression sets are combined by OR operator.
    """
    formula: str = ''
    exprID: str = ''
    exprType: int = 0
    configExprSets: List[ConfigExpressionSet] = ()


@dataclass
class ConfigExpressionSection(TcBaseObj):
    """
    Structure defines a Boolean expression to be used for configuration purposes.
    
    :var exprType: Expression type represents expression category and the intent of this expression. The valid values
    are as follows: 9 - Variant Condition, 18 - Variant Rule, 25 &ndash; Applicability, 44 &ndash; Subject, 28 -
    Inclusive Constraint, 29 - Exclusive Constraint, 37 - Default Rule, 41 - Availability Rule. These constants are
    defined in cfg_tokens.h file.
    :var formula: Configuration formula for a 'ConfigExpressionSection'.
    :var subExpressions: A list of sub-expressions in a Boolean variant expression. Either formula or sub expressions
    are populated in a 'ConfigExpressionSection' at a time.
    """
    exprType: int = 0
    formula: str = ''
    subExpressions: List[ConfigSubExpression] = ()


@dataclass
class SetVariantExpressionDataInput(TcBaseObj):
    """
    Input containing the user selections that represent variability to be set on variant configurable objects for e.g
    VariantRule.
    
    :var selectedExpressions: A map (string, list of ApplicationConfigExpressions ) of affected object UID to the list
    of its selected variant expressions. Affected object is any object for which selections are stored. Valid values
    for affected object are UIDs of VariantRule, Awb0Element or any configurable object.
    :var configPerspective: Cfg0ConfiguratorPerspective object is used as communication mechanism for the configuration
    and the valid configurator contexts across the Product Configurator and its consuming applications such as 4G
    Designer, Structure Manager. If it is empty then the config perspective is obtained from the selected objects
    :var requestInfo: Map (string, list of strings ) of request names and value pairs. Allowed names are: 
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
    selectedExpressions: SelectedExpressions = None
    configPerspective: Cfg0ConfiguratorPerspective = None
    requestInfo: StringMap3 = None


@dataclass
class UserSelection(TcBaseObj):
    """
    Structure representing a single user selection contributing a violation. Other information will be populated in
    'ViewModelObjectMap2'.
    
    :var groupUid: UID of the group corresponding to feature contributing to violation.
    :var configExpressionTerm: Holds a single selection. The nodeUid in the 'configExpressionTerm' is the unique ID to
    represent a node in the hierarchy which can be family (Cfg0AbsFamily) or a feature (Cfg0AbsFeature).
    """
    groupUid: str = ''
    configExpressionTerm: ConfigExpressionTerm = None


@dataclass
class ValidateProductConfigsInput(TcBaseObj):
    """
    The input containing the configurator perspective and the SelectedExpressions to validate by applying the
    constraints for the input perspective.
    
    :var configPerspective: Instance of Cfg0ConfiguratorPerspective business object.
    :var applyConstraints: The constraint rules application. The parameter is a bitwise &lsquo;OR&rsquo; of the
    following values: 
    0: Disable configurator constraint evaluation. 
    1: Enable configurator constraint evaluation.
    2: Skip constraints if they only reference unset families.
    4: Skip constraints that don't reference all Expression families.
    8: Report warnings in addition to errors.
    16: Report informational messages.
    64: Treat constraints with warning severity as if they had error severity.
    256: Skip allocation constraints in solve.
    1024: Skip criteria update based on validation rules (For example configurator exclusion rule). If this flag is not
    set then the operation will update the variant criteria after applying validation rules.
    2048: Enable Availability Constraint evaluation. 
    4096: Include Default Rules in the violations.
    :var requestInfo: Map (string, list of strings) of request names and value pairs. 
    
    1.  "profileSetting"  contains the information regarding the setting of different severity information (Error,
    warning, info) in JSON format which is taken into consideration for for the validation.
    :var selectedExpressions: A map (string, list of ApplicationConfigExpressions) containing the expressions in
    PCAGrid format, which needs to be validated.
    """
    configPerspective: Cfg0ConfiguratorPerspective = None
    applyConstraints: int = 0
    requestInfo: StringMap3 = None
    selectedExpressions: SelectedExpressions = None


@dataclass
class ConfigExpressionSet(TcBaseObj):
    """
    Structure containing the collection of variant expressions referred as set for the business
    object. A set collects different type of variant expressions such as applicability and subject. These will be
    joined together by AND operation and evaluated as part of single expression.
    
    :var configExprSections: A list of 'ConfigExpressionSection' structures which are collected as a set for the
    business object. Each structure defines a variant expression which can be used for the configuration purposes.
    """
    configExprSections: List[ConfigExpressionSection] = ()


@dataclass
class ValidateProductConfigsResponse2(TcBaseObj):
    """
    It is the structure containing response of operation validateProductConfiuration2.
    
    :var validateProductConfigurationOutputs: A map (string, ValidateProductConfigurationOutput2) containing the
    Selected object UID to its ValidateProductConfigurationOutput2 response structure.
    :var responseInfo: A map (string, list of strings) containing the additional informations which server wants to
    send about the operation. 
    Following information is sent by the server
    incompleteFamilies &ndash; UID of the families for which no selection is made by the user and system could not
    select any valid value by considering the constraints for the input expression. 
    completenessStatus &ndash; Provide additional information about the completeness of the input expression. Following
    are the valid values.
    ValidAndIncomplete &ndash; Indicates that the current input expression is valid but not every family have been
    selected.
    ValidAndIncomplete &ndash; Indicates that the current input expression is valid and have the selection for every
    family.
    Invalid &ndash; Indicates that the input expression is invalid.
    :var serviceData: ServiceData containing partial exceptions, if any.
    """
    validateProductConfigurationOutputs: AffectedObjectToValidateProductConfiguration = None
    responseInfo: StringMap3 = None
    serviceData: ServiceData = None


@dataclass
class ValidateProductConfigurationOutput2(TcBaseObj):
    """
    It is the structure containing information about the expanded expression and criteria status for the corresponding
    configurable object.
    
    :var criteriaStatus: Indicate if input configuration is valid or not. If true, input configuration is valid;
    otherwise, input configuration is invalid.
    :var valueToViolations: A map (string, Violations) of all violated values. The key is the UID of the feature
    (Cfg0AbsFeature) for the violations are reported by the system.
    :var expression: Expression in PCAGrid format which contains the expanded selections that is in accordance with the
    given input selections and the rules in the context.
    """
    criteriaStatus: bool = False
    valueToViolations: ValueToViolations2 = None
    expression: ApplicationConfigExpression = None


@dataclass
class VariabilityTreeData(TcBaseObj):
    """
    Tree structure representing variant data. This holds list of a structure VariabiltyNode. Each element will
    represent UID of the group, family and feature in the response and list of UIDs of all children. For features, no
    children data is populated.
    This structure will be populated for current scope or for all scopes based on view\mode information received in the
    requestInfo.
    
    In Tree Mode &ndash; Single SVR,  parent and child information of all scopes to be populated.
    In Tree Mode &ndash; Multiple SVR, parent and child information of all scopes to be populated.
    In existing Mode &ndash; Single SVR, parent and child information of current scope to be populated.And only list of
    all other parents is sufficient.
    
    :var variabiltyNodes: Represents UID of and list of UIDs of all children along with other properties to know
    additional information.
    """
    variabiltyNodes: List[VariabiltyNode] = ()


@dataclass
class VariabiltyNode(TcBaseObj):
    """
    Structure representing UID of Object and list of UIDs of all children along with other properties to know
    additional information.
    
    :var nodeUid: The UID of the object to be rendered.
    :var isExpanded: If true, the objects are expanded.
    :var childrenUids: The list of UIDs of children. This can contain value texts in case of free form features.
    :var props: The node specific meta information. For example &ndash; 1. allowed selection states in case of guided
    mode for family as well as feature. 2. For free form family nodeUid will represent information like familyUid and
    prop contains isFreeForm=true, children contains values texts like 10,20.
    """
    nodeUid: str = ''
    isExpanded: bool = False
    childrenUids: List[str] = ()
    props: StringMap3 = None


@dataclass
class VariantConfigurationViewIn2(TcBaseObj):
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
    to be retrieved. If this parameter is empty, then option values from model group (Cfg0AbsFamilyGroup) are retrieved.
    :var selectedExpressions: A map (string, list of 'ApplicationConfigExpressions' ) of affected object UID to the
    list of its selected variant expressions. Affected object is any object for which selections are stored. Valid
    values for affected object are UIDs of VariantRule, Awb0Element or any configurable object.
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
    selectedExpressions: SelectedExpressions = None
    payloadStrings: StringMap3 = None
    requestInfo: StringMap3 = None


@dataclass
class ConfigExpressionTerm(TcBaseObj):
    """
    Structure representing a single selection which will hold variant option and its selection state.
    
    :var nodeUid: The unique ID to represent a node in the hierarchy which can be family (Cfg0AbsFamily) or a feature
    (Cfg0AbsFeature).
    :var valueText: The string value of feature to be used in case of free form families.
    :var family: The UID of the family (Cfg0AbsFamily).
    :var familyId: The unique Object identifier for the Family (Cfg0AbsFamily).
    :var familyNamespace: The family namespace by which the family object is uniquely identified. This is used for
    unconfigured families where no UID is available.
    :var selectionState: The state of object selection. Selection state values are:
    0 - No Selection.
    1 - User positive Selection.
    2 - User negative Selection.
    5 - Default positive Selection by System.
    6 - Default negative Selection by system.
    9 - positive Selection by System. 
    10 - negative Selection by System.
    :var props: A map (string, list of strings) to store meta data about config object. It is used to indicate free
    form, unconfigured selection.
    """
    nodeUid: str = ''
    valueText: str = ''
    family: str = ''
    familyId: str = ''
    familyNamespace: str = ''
    selectionState: int = 0
    props: StringMap3 = None


@dataclass
class VariantConfigurationViewResponse2(TcBaseObj):
    """
    The output containing the available variability for the input list of variant option value selections.
    
    :var configPerspective: The configurator perspective containing all information about the current Configurator
    Context, revision rule and effectivity. All further communications with the server to retrieve variant
    configuration data must use this object.
    :var scopes: UID of the current expanded group or partition.
    :var serviceData: serviceData
    :var variabilityTreeData: Tree structure representing variant data.
    :var viewModelObjectMap: A map (string, 'ViewModelObject2') of object UID to its 'ViewModelObject2'.
    :var selectionsSummary: The summary of all selections in displayable format.
    :var selectedExpressions: A map (string, list of 'ApplicationConfigExpressions') of affected object UID to the list
    of its selected variant expressions. Affected object is any object for which selections are stored. Valid values
    for affected object are UIDs of VariantRule, Awb0Element or any configurable object.
    :var labels: 'ViewModelObjectLabelMap' of labels.
    :var violationCombo: Structure representing a single problem\violation and its contributing user selections as well
    contributing rules.
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
    """
    configPerspective: Cfg0ConfiguratorPerspective = None
    scopes: List[str] = ()
    serviceData: ServiceData = None
    variabilityTreeData: VariabilityTreeData = None
    viewModelObjectMap: ViewModelObjectMap2 = None
    selectionsSummary: SelectionsSummary = None
    selectedExpressions: SelectedExpressions = None
    labels: ViewModelObjectLabelMap2 = None
    violationCombo: List[ViolationCombo] = ()
    payloadStrings: StringMap3 = None
    responseInfo: StringMap3 = None


@dataclass
class VariantExpressionDataInput2(TcBaseObj):
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
    :var requestInfo: Map (string, list of strings ) of request names and value pairs. Allowed names are: 
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
    configContextProvider: BusinessObject = None
    configContext: WorkspaceObject = None
    configPerspective: Cfg0ConfiguratorPerspective = None
    selectedObjects: List[BusinessObject] = ()
    currentExpandedFamilies: List[str] = ()
    filters: VariantExpressionFilters = None
    requestInfo: StringMap3 = None


@dataclass
class VariantExpressionDataResponse2(TcBaseObj):
    """
    Variant expression response for the selected objects.
    
    :var variabilityTreeData: Tree structure representing variant data.
    :var viewModelObjectMap: A map (string, ViewModelObject2) of object UID to its ViewModelObject2 object.
    :var selectedExpressions: A map (string, list of ApplicationConfigExpressions) of affected object UID to the list
    of its selected variant expressions. Affected object is any object for which selections are stored. Valid values
    for affected object are UIDs of VariantRule, Awb0Element or any other object which have variant configurable
    behavior attached.
    :var configPerspective: Output configurator perspective. Configurator Perspective object is used as communication
    mechanism for the configuration and the valid configurator contexts across the Product Configurator and its
    consuming applications such as 4G Designer, Structure Manager.
    :var filters: The filters applied on the output to render the option families and values.
    :var responseInfo: Map (string, list of strings) of response names and value pairs. 
    1. "configurationControlMode" is the configuration control view.
    Supported values are: "guided" and "manual".
    guided: In this mode, configuration is always valid. This mode is used to configure products by optimizing the
    required input by pre-populating choices and at the same time provide maximum flexibility to users to get exactly
    what they want by overriding the system selections.
    manual: Manual mode does not give system selections unless user validates or applies his configuration.
    
    2."severity": This gives information what all violations to be returned.
    Supported values are: "error", "warn" and "info".
    
    3. "viewName": This holds the current configuration view name which decides how to display configuration data.
    Supported values are: "listView" and "treeView".
    listView: In this view Configurator data is displayed in simple list format.
    treeView: In this view Configurator data is displayed in tree format. Families are shown as children of Groups.
    Features are shown as children of respective families.
    :var serviceData: Service Data containing partial errors, if any.
    """
    variabilityTreeData: VariabilityTreeData = None
    viewModelObjectMap: ViewModelObjectMap2 = None
    selectedExpressions: SelectedExpressions = None
    configPerspective: Cfg0ConfiguratorPerspective = None
    filters: VariantExpressionFilters = None
    responseInfo: StringMap3 = None
    serviceData: ServiceData = None


@dataclass
class ViewModelObject2(TcBaseObj):
    """
    The generic object that is used to represent a single user facing object and its properties.
    It encapsulates a model object in server side.
    This object represents each object which is visible on UI like Scope, Feature, OptionFamily.
    
    :var sourceUid: The UID of the object to be rendered. Valid values are either valid UIDs of configurable object
    along with context UIDs.
    :var displayName: The display name of the object.
    :var sourceType: Type of the 'ViewModelObject'2. Valid values are following Business object types:
    Cfg0AbsFamilyGroup, Cfg0PackageOptionValue, Cfg0AbsValue, Cfg0AbsFamily.
    :var props: Map (string, list of strings) of 'ViewModelObject'2 property and value. Valid keys are: "isFreeForm",
    "isMultiSelect", "isPackage"
    """
    sourceUid: str = ''
    displayName: str = ''
    sourceType: str = ''
    props: StringMap3 = None


@dataclass
class ConfigSubExpression(TcBaseObj):
    """
    Structure containing map (string, list of 'ConfigExpressionTerms') of all option values selected by user per
    Cfg0AbsFamily.
    
    :var configExpressionGroupMap: Map (string, list of 'ConfigExpressionTerms') of all option values selected by user
    per family. 
    Here key is the UID of the family (Cfg0AbsFamily). For unconfigured and unassigned families, key is namespace and
    display name of the family.
    """
    configExpressionGroupMap: ConfigExpressionGroup = None


@dataclass
class ViolationCombo(TcBaseObj):
    """
    Structure representing a single problem\violation and its contributing user selections as well contributing rules.
    
    :var userSelections: A list of user selections contributing to violation.
    :var ruleUids: A list of UIDs of contributing rules.  More information is retrieved from 'ViewModelObject2'.
    :var props: A map (string, list of strings) to store meta information about selections or rules. For example, when
    the rule does not have access 'props' contains message as &lsquo;access denied&rsquo;.
    """
    userSelections: List[UserSelection] = ()
    ruleUids: List[str] = ()
    props: StringMap3 = None


"""
It is a map containing information about the result of validate product configuration for the corresponding affected object.
"""
AffectedObjectToValidateProductConfiguration = Dict[str, ValidateProductConfigurationOutput2]


"""
Map (string, list of 'ConfigExpressionTerms') of all option values selected by user per family. 
Here key is the UID of the family (Cfg0AbsFamily). For unconfigured and unassigned families, key is namespace and display name of the family.
"""
ConfigExpressionGroup = Dict[str, List[ConfigExpressionTerm]]


"""
A map (string, Violations) of all violated values.
"""
ValueToViolations2 = Dict[str, Violation]


"""
Map (string, list of ViewModelObjectLabelType) which will hold 'ViewModelObjects' for violations and package.

The valid keys are "violations", "package"
The value is ViewModelObjectLabelType which contains the 'ViewModelObjects' in a map where key names are nodeID and values are corresponding "violation" or "package"' ViewModelObjects'.
"""
ViewModelObjectLabelMap2 = Dict[str, List[ViewModelObjectLabelType]]


"""
Map (string, 'ViewModelObject'2) of all config Objects. 
The key represents the UID of the 'ViewModelObject'2.
This map is useful for the client to obtain 'ViewModelObject'2 properties like its type, display name and other properties.
"""
ViewModelObjectMap2 = Dict[str, ViewModelObject2]


"""
Map (string , list of variant expressions). Here, key is UID of the affected object for which selections are stored. Display name and other properties of affected object are stored in 'ViewModelObjectMap2'.
"""
SelectedExpressions = Dict[str, List[ApplicationConfigExpression]]


"""
Map (string, list of strings) to hold any property and its values.
"""
StringMap3 = Dict[str, List[str]]
