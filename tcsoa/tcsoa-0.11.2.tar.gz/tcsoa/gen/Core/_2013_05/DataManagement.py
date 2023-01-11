from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateNextValuesIn(TcBaseObj):
    """
    The input required to generate the next values.
    
    :var clientId: A unique string supplied by the caller.
    :var operationType: The type of the operation for which the values are to be generated.
    1-CREATE
    2-REVISE
    3-SAVEAS.
    
    An error 74007 is returned by the generateNextValues operation if the operationType value is not in any of the
    above. 
    :var businessObjectName: The name of the business object for which the property values are to be generated. An
    error 39007 is returned by the generateNextValues operation if the type name is not valid.
    :var propertyNameWithSelectedPattern:  A map of  property name and  naming rule pattern  pairs( string/string ).The
    key is the property name for which the value is to be generated and the value is the naming rule pattern string
    selected for  that property. If no pattern is selected for the property  the pattern string  should be empty
    string. The caller should only pass the properties that are autoassignable.
    :var propValues: A map of property name and values list(string/vector) of all the properties that are provided as
    inputs to create/revise/save as action of an object excluding the properties whose values are needed to be
    generated.If a multi field key is configured on the object ,the values of the constituent properties of the multi
    field key other than the ones for which the values are currently being generated are obtained from this map in
    order to perform the validation.
    The entries in this map are also used to generate values for the autoassignable properties of some business objects.
    
    Eg:
    Identifier: "idContext" value is needed to generate "idfr_id" property value
    
    An error  74032 is returned if any of the above property values are not provided .
    
    The values of the properties are to be provided as strings. For non string type properties use the
    Property.toXXXString functions (ie. toDateString) to covert the actual values to a string.
    
    :var additionalInputParams: A map of extra information which is required by user exits to generate values.
    A map where the key (string) is a parameter name and the value (string) is the parameter value.
    
    Valid parameters are:
    
    "ruleSuffix":
    This is only used when Baseline action to be performed. 'PDR'  should be passed  as ruleSuffix  in case of Baseline
    action. An error 74030 is returned if invalid ruleSuffix is supplied.
    
    "sourceObject":
    The object that is being revised/saved  or  the parent object  during  Dataset creation . Its value should be
    passed as the object UID. An error 74031 is returned if this parameter is not provided during revise/save as
    action.  It is optional in case of  Dataset creation .
    
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
                            |        Revise/SaveAs            |           Source tag             |
                            |                                    |                                     |
        Dataset            |           Create                    |           Source tag             |
                            |           SaveAs                |            NULLTAG             |
                            |                                    |                                     |
        CPD Objects    |    Create/Revise/SaveAs    |           Source tag             |
                            |                                    |                                     |
    ============================================|
    
    Any parameter other than the above will not be considered. 
    
    :var compoundObjectInput: Map for compound property.
    A map where the key (string) is a compound property name and the value (vector) is vector of GenerateNextValuesIn
    type.
    
    By using this map user can generate values for its own properties and also values for any of its   compound
    objects's propert. Provided property is autoassignable.
    
    For example user can generate value for "item_id" on item Object and value for "item_revision_id" property also
    using its compound pbject ItemRevision using this map.
    """
    clientId: str = ''
    operationType: int = 0
    businessObjectName: str = ''
    propertyNameWithSelectedPattern: PropertyNameWithSelectedPatternMap = None
    propValues: PropValuesMap = None
    additionalInputParams: AdditionalInputParamsMap = None
    compoundObjectInput: CompoundObjectInputMap = None


@dataclass
class GenerateNextValuesResponse(TcBaseObj):
    """
    This output structure contains service data with partial errors and a list of GeneratedValuesOutput each for an
    entry in the generateNextValuesIn input list.
    
    :var data: The Service Data with partial errors for each GenerateNextValuesInput and identified by  its clientId.
    :var generatedValues: A list of GeneratedValuesOutput one for each entry in generateNextvaluesIn input list and 
    identified by its clientId.
    """
    data: ServiceData = None
    generatedValues: List[GeneratedValuesOutput] = ()


@dataclass
class GeneratedValue(TcBaseObj):
    """
    This structure contains the  generated value for the input property. It also contains the information whether or
    not the generated values can be modified in the user interface.
    
    :var errorCode: The error encountered during the generation of value.
    :var nextValue: The  value generated based on the user exit/naming rule configured on the property.If the property
    has multiple naming rule patterns with counters  and if the selected pattern is passed as empty string, the value
    is generated based on the first pattern configured on the naming rule. An error 74006 is returned if the generated
    value does not match the naming rule pattern configured on the property and the nextValue is set to empty string.
    An error 74006 is returned if the generated value does not match the naming rule pattern configured on the property
    and the nextValue is set to empty string.
    :var isModifiable: True if the user can modify the generated value.If isModifiable is false the attempts to change
    the generated value shall be prevented at the user interface.
    """
    errorCode: int = 0
    nextValue: str = ''
    isModifiable: bool = False


@dataclass
class GeneratedValuesOutput(TcBaseObj):
    """
    This structure contains the values generated for each of the properties supplied in  the
    propertyNameWithSelectedPattern map of corresponding PropertyValuesInput structure.
    
    :var clientId: Identifying string from the source GenerateNextValuesInput.
    :var generatedValues: This contains map of property name and its values.
    :var generatedValuesOfSecondaryObjects: Field contains value for generated secondary object property values.
    """
    clientId: str = ''
    generatedValues: GeneratedValuesMap = None
    generatedValuesOfSecondaryObjects: GeneratedValuesOfSecondaryObjectsMap = None


@dataclass
class GetChildrenInputData(TcBaseObj):
    """
    This structure defines the object for which to retrieve children and optionally the propertyNames from which to
    retrieve those children.  If propertyNames is undefined, then the Teamcenter <Type>_DefaultChildProperties
    preference is used.
    
    :var clientId: Identifier used to track the input object.  Primarily this is used to identify which PartialError
    corresponds to which input object.
    :var obj: The object for which to retrieve children.
    :var propertyNames: The properties to use to retrieve children.  Only the properties defined in this list are used.
    If this list is empty, then the children are returned based on the <Type>_DefaultChildProperties and
    <Type>_PseudoFolders preferences.  Please see the Preferences and Environment Variables Reference and the
    RichClient Interface Guide for information on configuring there preferences
    """
    clientId: str = ''
    obj: BusinessObject = None
    propertyNames: List[str] = ()


@dataclass
class GetChildrenOutput(TcBaseObj):
    """
    This structure contains the children output for the defined property name.
    
    :var children: This is the list of Teamcenter business object children which exist within this property name.
    :var propertyName: The property the child belongs to in the parent input object.
    """
    children: List[BusinessObject] = ()
    propertyName: str = ''


@dataclass
class GetChildrenResponse(TcBaseObj):
    """
    Output structure for the getChildren operation.
    
    :var serviceData: The service data contains any partial errors which may have been encountered during processing. 
    All business objects which are returned are added to the serviceData's plain objects list.
    :var objectWithChildren: A map of requested objects and a list of children(business
    object/vector<GetChildrenOutput>).
    """
    serviceData: ServiceData = None
    objectWithChildren: GetChildrenOutputMap = None


@dataclass
class GetPasteRelationsInputData(TcBaseObj):
    """
    Object input structure of getPasteRelations operation.
    
    :var clientId: Identifier used to track the input object.  Primarily this is used to identify which PartialError
    corresponds to which input object.
    :var obj: The parent object for which to get the paste relations.
    :var childTypeName: The child type name for which the paste relations will be retrieved.
    """
    clientId: str = ''
    obj: BusinessObject = None
    childTypeName: str = ''


@dataclass
class GetPasteRelationsOutput(TcBaseObj):
    """
    Output structure of getPasteRelations operation.  This structure contains all the paste relations for a given
    business object.
    
    :var pasteRelationsInfo: This is the list of paste relation names and other info for the given business object.
    :var indexOfPreferred: The zero-based index of the preferred paste relation in the list of paste relation names.
    """
    pasteRelationsInfo: List[PasteRelationsInfo] = ()
    indexOfPreferred: int = 0


@dataclass
class GetPasteRelationsResponse(TcBaseObj):
    """
    Response of getPasteRelations operation.  This structure contains the servicedata and the outputMap to look up the
    paste relations for a given business object.
    
    :var serviceData: The service data contains any partial errors which may have been encountered during processing. 
    All business objects which are returned are added to the serviceData&apos;s plain objects list.
    :var outputMap: A map of input parent object to a vector of GetPasteRelationsOutput objects.
    """
    serviceData: ServiceData = None
    outputMap: GetPasteRelationsOutputMap = None


@dataclass
class PasteRelationsInfo(TcBaseObj):
    """
    Object output structure of getPasteRelations operation.
    
    :var pasteRelationName: The paste relation name.
    :var isExpandable: A flag indicating whether the relation will enable the children to be shown under the parent
    when expanded.
    """
    pasteRelationName: str = ''
    isExpandable: bool = False


@dataclass
class ReviseIn(TcBaseObj):
    """
    Input structure for 'reviseObjects' operation of any revisable object.
    
    :var targetObject: Target object being revised 
    :var reviseInputs: Map of property name(key) and property values(values) in string format, to be set on new object
    being created with revise. The calling client is responsible for converting the different property types (int,
    float, date .etc) to a string using the appropriate toXXXString functions in the SOA client framework Property
    class.
    :var deepCopyDatas: Relevant information regarding applicable deep copy rules for the objects attached to the
    targetobject.
    """
    targetObject: BusinessObject = None
    reviseInputs: PropertyValues = None
    deepCopyDatas: List[DeepCopyData] = ()


@dataclass
class ReviseObjectsResponse(TcBaseObj):
    """
    Output structure of 'reviseObjects' operation have information of new resultant objects created and error
    information if any.
    
    :var output: The target object and the newly created revised objects.
    :var reviseTrees: List corresponding to the input target objects that holds mapping between the original objects
    and the copied objects.
    :var serviceData: Data containing created objects, errors, etc.
    """
    output: List[ReviseOut] = ()
    reviseTrees: List[ReviseTree] = ()
    serviceData: ServiceData = None


@dataclass
class ReviseOut(TcBaseObj):
    """
    Member of Output structure of 'reviseObjects' operation, having information of original and newly created objects.
    
    :var targetObject: Original object being revised.
    :var objects: List of newly created objects during revise operation.
    """
    targetObject: BusinessObject = None
    objects: List[BusinessObject] = ()


@dataclass
class ReviseTree(TcBaseObj):
    """
    Member of Output structure of 'reviseObjects' operation, having information of attached objects and newly created
    objects from them.
    
    :var originalObject: Original object.
    :var objectCopy: Object copy after Revise. This could be NULL if no copy was made or same as original object if the
    copy is a reference to the original.
    :var childReviseNodes: List of child revise nodes for next level of the tree.
    """
    originalObject: BusinessObject = None
    objectCopy: BusinessObject = None
    childReviseNodes: List[ReviseTree] = ()


@dataclass
class SubTypeNamesInput(TcBaseObj):
    """
    The parent business object type name and context for which the sub business object type names are to be retrieved.
    
    :var typeName: The business object type name for which sub business object type names are to be returned. If all
    sub business object type names are needed then pass BusinessObject as input.
    :var contextName: Context name based on which server returns the business object type names.
    
    Supported contexts:
    
    subtypes: Returns all sub business object type names.
    :var exclusionPreference: Name of the preference to be used to exclude the sub business object type names from the
    output. Preference needs to be a multi-valued to specify the names of the business object types to be excluded.
    
    This is optional. It could be empty string.
    """
    typeName: str = ''
    contextName: str = ''
    exclusionPreference: str = ''


@dataclass
class SubTypeNamesOut(TcBaseObj):
    """
    This is the output structure which holds list of sub business object type names for a given business object type
    based on the context specified.
    
    :var typeName: The parent business object type name.
    :var contextName: Name of the context for which  the typeName represents.
    :var exclusionPreference: Name of the preference to be used to exclude the sub business object type names from the
    output. Preference needs to be a multi-valued to specify the names of the business object types to be excluded.
    
    This is optional. It could be empty string.
    :var subTypeNames: List of sub business object type names based on the context name.
    :var displayableSubTypeNames: List of sub business object type displayable names based on the context name.
    """
    typeName: str = ''
    contextName: str = ''
    exclusionPreference: str = ''
    subTypeNames: List[str] = ()
    displayableSubTypeNames: List[str] = ()


@dataclass
class SubTypeNamesResponse(TcBaseObj):
    """
    The returned business object type names based on the context for each input business object type.
    
    :var output: List of  business object type names.
    :var serviceData: The Service data.
    """
    output: List[SubTypeNamesOut] = ()
    serviceData: ServiceData = None


@dataclass
class ValidateInput(TcBaseObj):
    """
    This structure contains the necessary input for the 'validateValues' operation to support generic property
    validation while retaining support for some existing user exits for specific properties.  The 'validateValues'
    operation details legacy user exit support.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.
    :var operationType: The operation type for which the input values are to be validated. Valid values are:
    
    - 0 for create
    - 1 for revise
    - 2 for saveas
    - 3 for generic validation
    
    
    :var businessObjectName: The name of the business object for which the property values are to be validated. 
    :var propValuesMap: A map where the key (string) is a property name and the value (string) is the property value to
    be validated.  The value input is a list to support multi-value properties. The values of the properties are to be
    provided as strings.
    :var compoundObjectInput: A map where the key (string) is a property name and the value ('ValidateInput') is input
    for the property. This contains the property values of the secondary objects.
    """
    clientId: str = ''
    operationType: int = 0
    businessObjectName: str = ''
    propValuesMap: PropertyValues = None
    compoundObjectInput: CompoundValidateInputMap = None


@dataclass
class ValidateValuesResponse(TcBaseObj):
    """
    The response from the 'validateValues' operation.
    
    :var validationResults: A map where the key (string) is the 'clientId' and the value ('ValidationResults') is a
    list of validation results for the properties.
    :var serviceData: Service data containing errors that occurred during the operation.
    """
    validationResults: ValidationResultsMap = None
    serviceData: ServiceData = None


@dataclass
class ValidationResults(TcBaseObj):
    """
    This structure holds the property validation results for 'validateValues' operation.
    
    :var uniqueID: If true, the MFK value is unique.  If false, the MFK value is not unique.
    :var validationStatus: A list of ValidationStatus, which contains the validation status for each input property
    value.
    """
    uniqueID: bool = False
    validationStatus: List[ValidationStatus] = ()


@dataclass
class ValidationStatus(TcBaseObj):
    """
    This structure holds the validation status for a property.
    
    :var propName: The property name.
    :var valueStatus: The status of the property value validation. The possible values are:
    
    - 0 for valid - The input value is valid for use as-is.
    - 1 for invalid - The input value is not valid and cannot be used.
    - 2 for override - The input value cannot be used, but should be replaced by the value in the modifiedValue field.
    - 3 for duplicate - The input value is not valid because it is considered a duplicate and cannot be used.
    
    
    :var modifiedValue: The modified property value if the input value is modified by the user exit or by naming rule
    validation according to naming rule pattern and case specification. The modified property value should be used for
    subsequent create, saveAs and revise operation. It will hold value if property value validation status is override
    i.e. valueStatus = 2 otherwise it will be empty.
    This is a list to support multi-value properties.
    """
    propName: str = ''
    valueStatus: int = 0
    modifiedValue: List[str] = ()


@dataclass
class DeepCopyData(TcBaseObj):
    """
    The 'DeepCopyData' data structure holds the relevant information regarding applicable deep copy rules.
    
    :var attachedObject: Other side object.
    :var propertyName: Name of relation type or reference property for which DeepCopy rule is configured.
    :var propertyType: If 'Relation', it represents Relation type property. If 'Reference', it represents Reference
    property.
    :var copyAction: DeepCopy action [NoCopy, CopyAsReference, CopyAsObject or Select].
    :var isTargetPrimary: If true the target object is processed as primary, otherwise it is processed as a secondary
    object.
    :var isRequired: If true, the copy action can not be modified. If false, the copy action can be changed different
    action by the user. In this case, the copy action field in the revise dialog is editable.
    :var copyRelations: If true, the custom properties on the source relation object are copied over to the
    newly-created relation. If false, custom properties are not copied.
    :var operationInputTypeName: OperationInput type name.
    :var childDeepCopyData: List of DeepCopy data for the secondary objects on the other side.
    :var operationInputs: OperationInput field to capture property values of attached object, to apply on copied object
    of attached object. Map of property name(key) and property values(values) in string format of attached object, to
    be set on copied object of attached object. The calling client is responsible for converting the different property
    types (int, float, date .etc) to a string using the appropriate toXXXString functions in the SOA client  framework
    Property class.
    """
    attachedObject: BusinessObject = None
    propertyName: str = ''
    propertyType: str = ''
    copyAction: str = ''
    isTargetPrimary: bool = False
    isRequired: bool = False
    copyRelations: bool = False
    operationInputTypeName: str = ''
    childDeepCopyData: List[DeepCopyData] = ()
    operationInputs: PropertyValues = None


"""
A map of property name and GeneratedValue list.
"""
GeneratedValuesMap = Dict[str, GeneratedValue]


"""
A map of property name and list of  GeneratedValues.
"""
GeneratedValuesOfSecondaryObjectsMap = Dict[str, List[GeneratedValuesOutput]]


"""
This is a map of input BusinessObject to a vector of GetChildrenOutput objects.  It is used to look up the output for a given input BusinessObject.
"""
GetChildrenOutputMap = Dict[BusinessObject, List[GetChildrenOutput]]


"""
This is a map of input to a vector of GetPasteRelationOutput objects. It is used to look up the output for a given input business object.
"""
GetPasteRelationsOutputMap = Dict[BusinessObject, GetPasteRelationsOutput]


"""
Additional parameters needed to generate the next values.
"""
AdditionalInputParamsMap = Dict[str, str]


"""
A map of property name and values list.
"""
PropValuesMap = Dict[str, List[str]]


"""
A map of  property name and  naming rule pattern  pairs.
"""
PropertyNameWithSelectedPatternMap = Dict[str, str]


"""
Map of property name(key) and property values(values) in string format.
"""
PropertyValues = Dict[str, List[str]]


"""
A map where the key is the 'clientId' and the value is a list of 'ValidationResults' for the properties.
"""
ValidationResultsMap = Dict[str, ValidationResults]


"""
A map of property name and PropertyValuesInput list.
"""
CompoundObjectInputMap = Dict[str, List[GenerateNextValuesIn]]


"""
A map where the key is the property name and the value is a list of 'ValidateInput'.  This map contains the property values of the secondary objects.
"""
CompoundValidateInputMap = Dict[str, List[ValidateInput]]
