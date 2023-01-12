from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from tcsoa.gen.Core._2010_04.DataManagement import BusinessObjectHierarchy
from tcsoa.gen.Core._2014_10.DataManagement import DeepCopyData
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDeepCopyDataResponse(TcBaseObj):
    """
    Structure that contains the DeepCopyData embedded within which is a recursive data structure. The DeepCopyData
    contains information about how the secondary objects (related and referenced objects) are to be copied (reference,
    copy as object, no copy).
    
    :var selectedBOIsDuplicated: This indicates whether the 'selectedBO' from the method input already has DeepCopyData
    in deepCopyDatas from the method input or not.
    :var deepCopyDatas: A list of DeepCopyData for the 'selectedBO' from the method input. The DeepCopyData object
    contains all the information about how the attached objects are to be copied (Copy as Object, Copy as Reference,
    NoCopy, etc.). DeepCopyData is a recursive data structure that contains the details for the attached objects at the
    next level.
    :var serviceData: Service data containing errors, etc. The plain object list of the Service data is populated with
    the target objects which are to be copied as part of the saveAs/revise operation. If there is an error retrieving
    Business Object for the business object name corresponding to the target object, it is added to the error stack of
    the ServiceData as a partial error.
    """
    selectedBOIsDuplicated: bool = False
    deepCopyDatas: List[DeepCopyData] = ()
    serviceData: ServiceData = None


@dataclass
class GetDomainInput(TcBaseObj):
    """
    Input structure for getDomainOfObjectOrType operation.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var inputDesignArtifact: Design artifact for which domain information is to be identified and returned. Design
    artifact is of type WorkspaceObject.
    :var typName: Type name  of BusinessObject for which domain information is to be identified and returned. If
    inputDesignArtifact is empty then only  typName will be processed.
    """
    clientId: str = ''
    inputDesignArtifact: WorkspaceObject = None
    typName: str = ''


@dataclass
class LocalizedPropertyValuesInfo2(TcBaseObj):
    """
    This data structure contains business object tag and a list of NameValueLocaleStruct
    
    :var businessObject: The business object
    :var propertyValues: A list of NameValueLocaleStruct that holds property name, value and locale information.
    """
    businessObject: BusinessObject = None
    propertyValues: List[NameValueLocaleStruct2] = ()


@dataclass
class LocalizedPropertyValuesResponse(TcBaseObj):
    """
    This structure contains a list of output localized property value info and partial error.
    
    :var output: A list of structure LocalizedPropertyValuesInfo2 to keep the localized property values info.
    :var partialErrors: Used for storing partial error and standard service data.
    """
    output: List[LocalizedPropertyValuesInfo2] = ()
    partialErrors: ServiceData = None


@dataclass
class NameValueLocaleStruct2(TcBaseObj):
    """
    This data structure contains localization related information for property values.
    
    :var name: Property name (internal)
    :var values: A list of property values
    :var locale: The name of the locale
    :var seqNum: Sequence number
    :var status: A list of localization status values.
    The status must be one of the following values:
    
    For the approved status: "A", "Approved" or the version of the "Approved" string for the client/server log-in
    locale.
    For the in-review status: "R", "In Review", "In-Review", "InReview" or the version of the "In Review" string for
    the client/server log-in locale.
    For the pending status: "P", "Pending" or the version of the "Pending" string for the client/server log-in locale.
    For the invalid status: "I", "Invalid" or the version of the "Invalid" string for the client/server log-in locale.
    For the master status: "M", "Master" or the version of the "Master" string for the client/server log-in locale.
    :var internalStatus: A list of internal values of the status.
    The status must be one of the following values:
    "approved" for the approved status: "A"
    "in review" for the in-review status: "R" 
    "pending" for the pending status: "P" 
    "invalid" for the invalid status: "I" 
    "master" for the master status: "M"
    :var statusDesc: A list of descriptions of statuses used for tooltip on the user interface.
    :var master: Master value indication
    """
    name: str = ''
    values: List[str] = ()
    locale: str = ''
    seqNum: int = 0
    status: List[str] = ()
    internalStatus: List[str] = ()
    statusDesc: List[str] = ()
    master: bool = False


@dataclass
class PropertyNamingruleInfo(TcBaseObj):
    """
    This operation generates values for the given properties of an object(s) during create/revise/save as action based
    on the user exits or naming rules configured on those properties.Customer user exits are given priority over the
    naming rules if both of them are configured on the same property. The counter has to be set active on the naming
    rule in order to generate the next value for a property. This operation also performs naming rule and multi field
    key validation on the generated values and return appropriate partial errors if the validation fails.
    
    For user exit support, an existing user exit will be called to generate values. Right now we support below given
    user exits for corrosponding Objest type.
    
    Object: Item
    User exit name: USER_new_item_id
    Property: item_id
    
    Object: ItemRevision
    User exit name: USER_new_revision_id, USER_new_revision_id_from_alt_rule(Baseline)
    Property: item_revision_id
    
    Object: Dataset
    User exit name: USER_new_dataset_id
    Property: pubr_object_id
    
    Object: Dataset
    User exit name: USER_new_dataset_rev
    Property: rev
    
    Object: Identifier
    User exit name: IDFR_new_alt_id, IDFR_new_rev_id(In Revise case)
    Property: idfr_id
    
    Object: CPD Objects
    User exit name: USER_new_cpd_id
    Property: CPD Objects related property
    
    These each user exits need some specific inputs which are required by them to generate ids. These inputs are part
    of "generateNextValuesIn" structure and are described in details in its description.
    
    
    :var clientId: The unmodified value from the PropertyNamingruleInfo. This can be used by the caller to identify
    this data structure with the source input data. 
    
    
    :var operationType: The type of the operation for which the values are to be generated. 
    1-CREATE
    2-REVISE
    3-SAVEAS.
    
    An error 74007 is returned by the generateNextValues operation if the operationType value is not in any of the
    above. 
    
    :var businessObjectTypeName: The business object type name (for e.g. Item, Dataset or Form etc)   for which unique
    ID generation is required.
    :var propertyNameAttachedPattern: A map of property name and naming rule pattern pairs( string/string ).The key is
    the property name for which the value is to be generated and the value is the naming rule pattern string selected
    for that property. If no pattern is selected for the property the pattern string should be empty string. The caller
    should only pass the properties that are autoassignable.
    :var propertyValuesMap: A map of property name and values list(string/vector) of all the properties that are
    provided as inputs to create/revise/save as action of an object excluding the properties whose values are needed to
    be generated.If a multi field key is configured on the object ,the values of the constituent properties of the
    multi field key other than the ones for which the values are currently being generated are obtained from this map
    in order to perform the validation.
    The entries in this map are also used to generate values for the autoassignable properties of some business objects.
    
    Eg:
    Identifier: "idContext" value is needed to generate "idfr_id" property value
    
    An error 74032 is returned if any of the above property values are not provided .
    
    The values of the properties are to be provided as strings. For non string type properties use the
    Property.toXXXString functions (ie. toDateString) to covert the actual values to a string.
    
    :var additionalInputMap: A map of extra information which is required by user exits to generate values.
    A map where the key (string) is a parameter name and the value (string) is the parameter value.
    
    Valid parameters are:
    
    "ruleSuffix":
    This is only used when Baseline action to be performed. 'PDR' should be passed as ruleSuffix in case of Baseline
    action. An error 74030 is returned if invalid ruleSuffix is supplied.
    
    "sourceObject":
    The object that is being revised/saved or the parent object during Dataset creation . Its value should be passed as
    the object UID. An error 74031 is returned if this parameter is not provided during revise/save as action. It is
    optional in case of Dataset creation .
    
    Object Name        |        Operation                |            Value                    |
    ============================================|
        ITEM                |        Create                    |        NULLTAG                |
                            |        SaveAs                    |        Source tag                |
                            |                                    |                                    |
        ITEM Revision    |        Create/SaveAs            |        NULLTAG                |
                            |        Revise                    |        Source tag                |
                            |        Baseline                    |        Source tag                |
                            |                                    |                                     |
        Identifier            |            Create                |            NULLTAG             |    
                            |        Revise/SaveAs            |         Source tag             |
                            |                                    |                                     |
        Dataset            |         Create                    |         Source tag             |
                            |         SaveAs                |            NULLTAG             |
                            |                                    |                                     |
        CPD Objects    |    Create/Revise/SaveAs    |         Source tag             |
                            |                                    |                                     |
    ============================================|
    
    Any parameter other than the above will not be considered. 
    
    :var compoundObjectInput: Map for compound property.
    A map where the key (string) is a compound property name and the value (vector) is vector of PropertyNamingruleInfo
    type.
    
    By using this map user can generate values for its own properties and also values for any of its compound objects's
    propert. Provided property is autoassignable.
    
    For example user can generate value for "item_id" on item Object and value for "item_revision_id" property also
    using its compound pbject ItemRevision using this map.
    
    :var propertyNameContextListMap: This contains key as property name and value as a list of substituted context list.
    """
    clientId: str = ''
    operationType: int = 0
    businessObjectTypeName: str = ''
    propertyNameAttachedPattern: PropertyAttachedPatternMap = None
    propertyValuesMap: PropertyListOfValuesMap = None
    additionalInputMap: PropertyNamingRuleHelperMap = None
    compoundObjectInput: CompoundPropertyAttachedPatternMap = None
    propertyNameContextListMap: PropertyContextListMap = None


@dataclass
class CreatableBusinessObjectsOut(TcBaseObj):
    """
    This structure contains a list of creatable business object names under a given business object (hierarchy of
    creatable sub business objects).
    
    :var boName: Name of the business object
    :var creatableBONames: Creatable business object hierarchy
    """
    boName: str = ''
    creatableBONames: List[BusinessObjectHierarchy] = ()


@dataclass
class CreatableSubBONamesInput(TcBaseObj):
    """
    Represents the parent business object name, exclusion preference and/or exclusion business object names, and the
    context using which the sub business object names are to be retrieved.
    
    :var boName: The primary business object name for which creatable sub business object names are to be returned. If
    all creatable sub business object names are needed, then "BusinessObject" should be passed as input.
    :var exclusionPreference: Name of the preference to be used to exclude the sub business object names from the
    output. Preference needs to be a multi-valued to specify the names of the business objects to be excluded. This
    parameter is optional.
    :var exclusionBONames: List of business object namess (and their secondary business objects) to be excluded from
    returned list. This parameter is optional.
    :var context: Context based on which server returns the creatable business object names. If there is no value
    specified for the context, all the creatable sub business objects for the business object will be returned.
    Supported contexts:
    legacy: Returns sub business object names from sub classes of the given primary business object, if the primary
    business object name is listed in the TYPE_DISPLAY_RULES_list_types_of_subclasses site preference.
    Please see the Preferences and Environment Variables Reference documentation for more information on preference
    TYPE_DISPLAY_RULES_list_types_of_subclasses.
    """
    boName: str = ''
    exclusionPreference: str = ''
    exclusionBONames: List[str] = ()
    context: str = ''


@dataclass
class CreatableSubBONamesResponse(TcBaseObj):
    """
    This structure holds the list of creatable business objects and their display names
    
    :var output: List of output objects representing the creatable business objects displayable in the Create dialog
    :var serviceData: Service data including the partial errors that are mapped to the input primary business objects
    """
    output: List[CreatableBusinessObjectsOut] = ()
    serviceData: ServiceData = None


@dataclass
class CreateIn2(TcBaseObj):
    """
    This is an input structure for create operation including unique client identifier.
    
    :var clientId: Unique client identifier.
    :var createData: Input data for create operation.
    :var dataToBeRelated: Additional input data. This data (string/list of strings) will be related to the created
    object by the given property.
    :var workflowData: Input data (string/list of strings) required for workflow creation.
    submitToWorkflow - true/false
    NOTE: If the above option is "true" then workflow process template to be used for workflow creation should be
    specified in the preference (<TypeName>_default_workflow_template) defined for the created object type.
    :var targetObject: Target to which the created object will be pasted.
    :var pasteProp: Property to be used to paste the created object to the target.
    """
    clientId: str = ''
    createData: CreateInput2 = None
    dataToBeRelated: PropertyValuesMap2 = None
    workflowData: PropertyValuesMap2 = None
    targetObject: BusinessObject = None
    pasteProp: str = ''


@dataclass
class CreateInput2(TcBaseObj):
    """
    CreateInput2 is a structure used to capture the inputs required for creation of a business object. This is a
    recursive structure containing the CreateInput2 (s) for any secondary (compounded) objects that might be created
    (e.g Item also creates ItemRevision and ItemMasterForm etc.).
    
    :var boName: Business Object type name.
    :var propertyNameValues: Map (string/list of strings)  of property name (key) and to property values (values) in
    string format, to be set on new object being created. Note: The calling client is responsible for converting the
    different property types (int, float, date .etc) to a string using the appropriate function(s) in the client
    framework Property class (i.e. Property.toDateString).
    :var compoundCreateInput: CreateInput2 (s) for compounded objects.
    """
    boName: str = ''
    propertyNameValues: PropertyValuesMap2 = None
    compoundCreateInput: CreateInputMap2 = None


@dataclass
class DeepCopyDataInput(TcBaseObj):
    """
    Input structure for getDeepCopyData operation
    
    :var operation: This is the one of the operation types
    - SaveAs
    - Revise
    
    
    :var targetObject: The target business object which user wants to do save-as/or revise.
    :var deepCopyDatas: This contains the list of DeepCopyData for 'targetObject' which is the object User wants to do
    "saveAs"/"revise".
    :var parentDeepCopyData: This contains parent DeepCopyData of' selctedBO'. It also stores the nested deep copy data
    at the next level.
    :var selectedBO: This is the business object which User wants to change copy action.
    """
    operation: str = ''
    targetObject: BusinessObject = None
    deepCopyDatas: List[DeepCopyData] = ()
    parentDeepCopyData: DeepCopyData = None
    selectedBO: BusinessObject = None


@dataclass
class DomainOfObjectOrTypeResponse(TcBaseObj):
    """
    The identified domain information for the design artifact or type name will be returned.
    
    :var output: The domain information output.
    :var serviceData: Holds any partial errors occurred during the operation.
    """
    output: List[DomainOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DomainOutput(TcBaseObj):
    """
    The identified domain information for input object or type name.
    
    :var clientId: Identifier that helps the client to track the input.
    :var domain: The application domain information identified for the input object or type.
    """
    clientId: str = ''
    domain: str = ''


"""
CreateInputMap is a map of reference or relation property name to secondary CreateInput2 objects.
"""
CreateInputMap2 = Dict[str, List[CreateInput2]]


"""
A map of property name and naming rule pattern pairs( string/string ).The key is the property name for which the value is to be generated and the value is the naming rule pattern string selected for that property. If no pattern is selected for the property the pattern string should be empty string. The caller should only pass the properties that are autoassignable.
"""
PropertyAttachedPatternMap = Dict[str, str]


"""
This is a map contains information required to substitute  the text for a given list of properties. Key is property name and value is substituted text.
The value is a list that needs to be substituted for given pattern for each U, u or D character occurring in naming rule pattern. For example:
Namign Rule Pattern created in  BMIDE is  UuD"-"NNN then valid substitute text value can be "XyB, AbC, ReQ or any Upper Case letter (represented by U in a pattern) followed by lower case letter ( represented by u in a pattern) followed by upper or lower case letter (represented by D in a pattern).

"""
PropertyContextListMap = Dict[str, List[str]]


"""
This map is of property name (as key) and property values (as value) in string format. Each value is a list of strings to support both single valued and multi valued properties of types. The calling client is responsible for converting the different property types (like integer, double, date, etc) to a string using the appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class. 


"""
PropertyListOfValuesMap = Dict[str, List[str]]


"""
A map of extra information which is required by user exits to generate values.
A map where the key (string) is a parameter name and the value (string) is the parameter value.

Valid parameters are:

"ruleSuffix":
This is only used when Baseline action to be performed. 'PDR' should be passed as ruleSuffix in case of Baseline action. An error 74030 is returned if invalid ruleSuffix is supplied.

"sourceObject":
The object that is being revised/saved or the parent object during Dataset creation . Its value should be passed as the object UID. An error 74031 is returned if this parameter is not provided during revise/save as action. It is optional in case of Dataset creation .

"""
PropertyNamingRuleHelperMap = Dict[str, str]


"""
Map (string/list of strings) of property name to property values in string format, to be set on new object being created. Note: The calling client is responsible for converting the different property types (int, float, date, etc) to a string using the appropriate function(s) in the client framework Property class (i.e. Property.toDateString).
"""
PropertyValuesMap2 = Dict[str, List[str]]


"""
Map for compound property.
A map where the key (string) is a compound property name and the value (vector) is vector of GenerateNextValuesIn type.

By using this map user can generate values for its own properties and also values for any of its compound objects's propert. Provided property is autoassignable.

For example user can generate value for "item_id" on item Object and value for "item_revision_id" property also using its compound pbject ItemRevision using this map.

"""
CompoundPropertyAttachedPatternMap = Dict[str, List[PropertyNamingruleInfo]]
