from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile, AssemblyArrangement, Fnd0ProductSessionData, RevisionRule, Folder, CFMOverrideEntry, BOMWindow, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NamedReferenceInfo(TcBaseObj):
    """
    'NamedReferenceInfo' structure contains the reference object corresponding to the named reference. If the
    referenced object is ImanFile then the FMS file ticket for it is returned.
    
    :var namedReferenceType: The type of reference object.
    :var namedReferenceName: The 'NamedReference' name of the object.
    :var referenceObject: The object reference corresponding to the named reference.
    :var fileTicket: The FMS ticket used to retrieve the file in the cases where 'referenceObject' is a file.
    """
    namedReferenceType: str = ''
    namedReferenceName: str = ''
    referenceObject: BusinessObject = None
    fileTicket: str = ''


@dataclass
class OpenSavedSessionFilter(TcBaseObj):
    """
    'OpenSavedSessionFilter' enables the client application to control the output returned during opening a session.
    
    :var relAndTypesFilter: A list of type filter to be applied on the objects that are associated to the session.
    :var productStructureFilter: The filter to control the product structures returned by the operation. This structure
    can be empty in which case the default values as mentioned in the 'ProductStructureFilter' description will be used.
    :var productSessionDataFilter: Product Session Data Filter
    """
    relAndTypesFilter: List[RelationAndTypesFilter] = ()
    productStructureFilter: ProductStructureFilter = None
    productSessionDataFilter: ProductSessionDataFilter = None


@dataclass
class OpenSessionOutput(TcBaseObj):
    """
    'OpenSessionOutput' contains the launched session object,  the associated product structures and objects.
    
    :var sessionObject: The session Fnd0AppSession object that was opened from the client.
    :var sessionProductStructures: A list of associated product structures that were associated to the session.
    Typically, it contains the BOMWindow object.
    :var relatedObjectInfos: A list of 'RelatedObjectInfo' that contains information about the objects that were
    related to the session object.
    :var productSessionDataObjects: A list of Fnd0ProductSessionData that are associated to the session.
    """
    sessionObject: BusinessObject = None
    sessionProductStructures: List[SessionProductStructureInfo] = ()
    relatedObjectInfos: List[RelatedObjectInfo] = ()
    productSessionDataObjects: List[ProductSessionDataObjectInfo] = ()


@dataclass
class OpenSessionResponse(TcBaseObj):
    """
    'OpenSessionResponse' contains a list of 'OpenSessionOutput' which has the objects and product structures
    associated to the session. Stable Id that identifies the associated objects and product structures are also
    returned which could be used for further references to update the session.
    
    :var sessionOutputs: A list of objects and product structures that were associated to the session.
    :var serviceData: 'ServiceData' that contains the partial errors if any.
    """
    sessionOutputs: List[OpenSessionOutput] = ()
    serviceData: ServiceData = None


@dataclass
class OverrideInfo(TcBaseObj):
    """
    This contains information about the override RevisionRule Entry.
    
    :var ruleEntry: Refers to the CFMOverrideEntry of RevisionRule object.
    :var folder: A Folder containing ItemRevision that are to be considered while evaluating the RevisionRule.
    """
    ruleEntry: CFMOverrideEntry = None
    folder: Folder = None


@dataclass
class ProductSessionDataAttachInfo(TcBaseObj):
    """
    'ProductSessionDataAttachInfo' is a structure which enables to create or update an object of type
    Fnd0ProductSessionData and attach it to the session.
    
    :var clientId: The input 'clientId' sent by the client application which will enable the client to map the output
    with the input.
    :var sessionData: Fnd0ProductSessionData that has to be created or updated and attached to the session object.
    """
    clientId: str = ''
    sessionData: CreateOrUpdateObjectInfo = None


@dataclass
class ProductSessionDataFilter(TcBaseObj):
    """
    'ProductSessionDataFilter' is a structure in which the application can specify the Fnd0ProductSessionData types
    that are associated to the session. The application can either specify the Fnd0ProductSessionData by their stable
    Ids or by their type names.
    
    :var stableIds:  A list of stable Ids that identifies the association of Fnd0ProductSessionData to the session.
    :var productSessionDataTypeNames:  A list of Fnd0ProductSessionData type names. The instances of the given type
    which are associated to the session that are to be retrieved.
    """
    stableIds: List[str] = ()
    productSessionDataTypeNames: List[str] = ()


@dataclass
class ProductSessionDataObjectInfo(TcBaseObj):
    """
    'ProductSessionDataObjectInfo' has the information about Fnd0ProductSessionData that are associated to the session.
    
    :var stableId: The identifier that enables the client to identify the association of the opened object with the
    session.
    :var productSessionDataObject: Fnd0ProductSessionData object associated to the session.
    """
    stableId: str = ''
    productSessionDataObject: Fnd0ProductSessionData = None


@dataclass
class ProductStructureFilter(TcBaseObj):
    """
    This structure enables the client to control how and what product structures are to returned in the response.
    
    :var productStructure: A string used to identify what product structure associated to the session are to be
    returned. 
    Valid values are:
     "'AllProducts'" &ndash; Return all product structures associated to the session.
    
    "'UseList'"-Returned the product structures that are identified by the ids in  'relativeToSessionStableIds'.
    
    "'NoProducts'" &ndash; Don&rsquo;t return any product structures.
    Note: Default value is 'AllProducts'.
    :var outputFilters: A map('string,string') that specifies various options that need to be applied when returning
    the session product structure contents. Valid values are
    "'RecipeObjectsOnly = true'" -  When true, the product structure BOMWindow is not returned and instead the recipe
    object of the product structure which is usually a StructureContext that can be opened outside the session context
    is returned. Default value is false.
    "'WantStaticStructureFileTicket = true'" -  When true, the file ticket of the static product structure file is
    returned. Default value is false.
    :var relativeToSessionStableIds: A list of stable Ids that identifies the association of  product structures to the
    session. This parameter is applicable only if parameter' productStructure' equals 'UseList'
    :var additionalPropsOnBOMWindow: A map('string,PropertyValues)' that specifies additional options that need to be
    set on the BOMWindow while returning the session product structure contents.
    """
    productStructure: str = ''
    outputFilters: StringMap = None
    relativeToSessionStableIds: List[str] = ()
    additionalPropsOnBOMWindow: PropertyValuesMap = None


@dataclass
class ProductStructureRecipe(TcBaseObj):
    """
    'ProductStructureRecipe' contains product, configuration and subset information.
    Note: During update of existing product structure information associated to the session the complete information
    like 'occurrenceLists', 'searchRecipe' and 'staticStructureFile' has to be passed
    
    :var structureContextIdentifier: The product and the configuration information.
    :var occurrenceLists: A list of filtered product structure results.
    :var searchRecipe: This is Fnd0SearchRecipe type BusinessObject which defines the search filters that were applied
    on the product structure
    :var staticStructureFile: The ImanFile object that represents the static product structure as expanded during the
    creation of session.
    """
    structureContextIdentifier: StructureContextIdentifier = None
    occurrenceLists: List[StructureSubsetInfo] = ()
    searchRecipe: BusinessObject = None
    staticStructureFile: ImanFile = None


@dataclass
class PropertyValues(TcBaseObj):
    """
    'PropertyValues' is a structure using which the property values that need to be set on objects are sent. Scalar
    property values are also sent via this structure.
    Note: In case to set a char property, populate the 'stringValues' as shown in example. Example
    To set a single char value say Y- provide 'stringValues[0][0]' = Y
    To set an array of char values YES - provide 'stringValues[0]' = YES
    
    :var intValues: List of integer values.
    :var boolValues: List of boolean values.
    :var dateValues: List of date values.
    :var stringValues: List of string values.
    :var floatValues: List of float values.
    :var doubleValues: List of double values.
    :var tagValues: List of object values.
    """
    intValues: List[int] = ()
    boolValues: List[bool] = ()
    dateValues: List[datetime] = ()
    stringValues: List[str] = ()
    floatValues: List[float] = ()
    doubleValues: List[float] = ()
    tagValues: List[BusinessObject] = ()


@dataclass
class RelatedObjectInfo(TcBaseObj):
    """
    'RelatedObjectInfo' structure contains an object associated to session, named references and reference objects.
    
    :var stableId: The identifier that enables the client to identify the association of the opened object with the
    session.
    :var relatedObject: The resulting related object by following a relation specified in the 'OpenSavedSessionFilter'.
    :var bomWindow: This is  only populated when the 'relatedObject' is associated with Fnd0AppSession with
    VisManagedDocument relation. The BOMWindow is constructed using 'fnd0Recipe' property on the relation.
    :var recipeObject: The recipe object of the structure which can be opened outside the context of the session.
    Typically it is the a VisStructureContext object but it could be any object which is capable of reconstructing the
    BOMWindow and hence the client should not assume the type of object to particular type. This is only populated when
    the 'relatedObject' is associated with Fnd0AppSession with VisManagedDocument relation and the relation has the
    'fnd0Recipe' property populated.
    :var relationProperties: A map('string,PropertyValues') on the relation that associated the session and the object.
    This has information about position, order, parent in case a document was inserted into another.
    Whe the the 'relatedObject' is associated with Fnd0AppSession with VisManagedDocument relation.
    The following information is returned.
    'fnd0InsertOrder' of type Integer - Indicates the order at which the 'relatedObject' was inserted into its parent.
    'fnd0ParentStableId' of type string - Indicates the parent object into whcih the 'relatedObject' was inserted.
    'fnd0Xform' of type string - Indicates the transformation of the  'relatedObject' in the co-ordinate system of
    parent.
    :var namedRefList: A List of named reference and reference object if the 'relatedObject' is a Dataset.
    """
    stableId: str = ''
    relatedObject: BusinessObject = None
    bomWindow: BOMWindow = None
    recipeObject: BusinessObject = None
    relationProperties: PropertyValuesMap = None
    namedRefList: List[NamedReferenceInfo] = ()


@dataclass
class RelatedObjectTypeAndNamedRefs(TcBaseObj):
    """
    This structure contains a related object type and the list of its named references to be processed.
    
    :var objectTypeName: Secondary object type based on which the results are to be filtered down.
    :var namedReferenceNames: Name of the named references in case the 'objectTypeName' is of Dataset type.
    """
    objectTypeName: str = ''
    namedReferenceNames: List[str] = ()


@dataclass
class RelationAndTypesFilter(TcBaseObj):
    """
    This structure contains a relation name and a list of related object types and its named references
    ('RelatedObjectTypeAndNamedRefs'). Together they are used to filter objects passed back in a session open operation.
    
    :var stableId: Stable ID that associates the object with the session.
    :var relationName: The name of the relation. Accepts a wild card "*" to consider all relation names. In case of
    'stableId' is provided this parameter is ignored.
    :var relatedObjAndNamedRefs: A list of related object types and named references.
    :var namedRefHandler: A string used to identify how named references will be processed. 
    Valid values are: 
    "'NoNamedRefs'" -- No named references are to be processed. The input '"relatedObjAndNamedRefs"' will be ignored. 
    "'AllNamedRefs'" -- All named references are to be processed. The input '"relatedObjAndNamedRefs"' will be ignored. 
    "'UseNamedRefsList'" -- Only the named references listed in the input '"relatedObjAndNamedRefs"' struct are
    processed.
    """
    stableId: str = ''
    relationName: str = ''
    relatedObjAndNamedRefs: List[RelatedObjectTypeAndNamedRefs] = ()
    namedRefHandler: str = ''


@dataclass
class RevisionRuleConfigInfo(TcBaseObj):
    """
    'RevisionRuleConfigInfo' is a structure which enables client to pass configuration information for RevisionRule and
    configuration parameters.
    
    :var revRule: The RevisionRule to be used for configuration.
    :var unitNo: Unit number. The client must pass -1 if unit number is not used for configuration.
    :var date: Effectivity date.
    :var today: Effectivity date to use today as the date.
    :var endItem: End Item.
    :var endItemRevision: End ItemRevision.
    :var overrideFolders: A list of Overriding Folder objects.
    """
    revRule: RevisionRule = None
    unitNo: int = 0
    date: datetime = None
    today: bool = False
    endItem: Item = None
    endItemRevision: ItemRevision = None
    overrideFolders: List[OverrideInfo] = ()


@dataclass
class BaseObjectAttachInfo(TcBaseObj):
    """
    'BaseObjectAttachInfo' is a structure which enables to create or update an object and attach it to the session. If
    relation is used to attach object to the session additional properties that are to be set on the relation can be
    passed as input.
    
    :var clientId: The input 'clientId' sent by the client application which will enable the client to map the output
    with the input.
    :var baseObjectToCreateOrUpdate: The input that has information to create an object or update an object associated
    to the session.
    :var relationName: The relation name used to associate the base object to the session. Typically, the ImanRelation
    name.
    :var additionalProps: A map ('string, PropertyValues') of property name and values pairs that need to be set on the
    ImanRelation specified via  'relationName'.
    Note: Incase the 'relationName' is VisManagedDocument, the 'clientId' of 'BaseObjectAttachInfo' can be passed as
    'fnd0ParentStableId' to indicate which document is the parent of this document, if this document was inserted into
    another in the session. The operation would first check if any 'BaseObjectAttachInfo' has the 'clientId' value same
    as the provided as 'fnd0ParentStableId' value, if yes then the 'stableId' of the 'BaseObjectAttachInfo' is stored
    as 'fnd0ParentStableId' otherwise the given string provided is stored as 'fnd0ParentStableId'.
    :var recipe: In case where the 'relationName' is VisManagedDocument, the structure configuration information that
    need to be set on 'fnd0Recipe' property of the relation.
    """
    clientId: str = ''
    baseObjectToCreateOrUpdate: CreateOrUpdateObjectInfo = None
    relationName: str = ''
    additionalProps: PropertyValuesMap = None
    recipe: ProductStructureRecipe = None


@dataclass
class BaseObjectAttachInfoOutput(TcBaseObj):
    """
    'BaseObjectAttachInfoOutput' holds information about the object that was associated to the session.
    
    :var clientId: The input 'clientId' sent by the client application which will enable the client to map the output
    with the input.
    :var stableId: The identifier that enables the client to identify the association of the opened object with the
    session.
    :var baseObject: The object that was associated to the session.
    """
    clientId: str = ''
    stableId: str = ''
    baseObject: BusinessObject = None


@dataclass
class SessionInfo(TcBaseObj):
    """
    'SessionInfo' is a structure which enables to create or update a session. The client can pass information to create
    a session or update a session by passing 'sessionToCreateOrUpdate' . During creation of session the client
    populates 'attachObjectsToSession', 'productSessionDataAttachInfos' with objects it has opened and populates
    'productAndConfigsToCreateOrUpdate' with product structure that were opened. The client can detach the closed
    documents and product structures by populating 'detachObjectOrProductsFromSession'. 
    Note: If an existing product structure which was associated to the session is opened in the context of the session,
    its configuration was changed or recipe was changed, and session is saved, the client application has to remove the
    original product and configuration from the session identifying it by 'stableId' and add the changes as new product
    structure configuration with same  or different 'stableId'.
    
    :var clientId: The input 'clientId' sent by the client application which will enable the client to map the output
    with the input.
    :var sessionToCreateOrUpdate: The input that has information to create a session BusinessObject. Since the session
    object is a Fnd0AppSession the required properties for object creation like 'object_name' and the BusinessObject
    type name can be passed.  Inorder to update, the object itself is passed.
    :var attachObjectsToSession: A list of information about the opened objects that are to be attached to the session.
    This would typically include any Dataset or Form that were opened in the application session.
    :var productAndConfigsToCreate: A list of information about the opened product structures that are to be attached
    to the session. This would typically include any BOMLine, VisStructureContext or Item, ItemRevision, BOMView,
    BOMViewRevision with configuration information.
    :var productAndConfigsToUpdate: A list of information about the product structures information attached to the
    session that are to be updated.
    Note: In order to update the configuration and search recipe the client has to remove the existing product
    structure information and re-associate the new product structure configuration.
    :var productSessionDataAttachInfos: A list of Fnd0ProductSessionData objects that are to be created or updated and
    attached to the session.
    :var detachObjectOrProductsFromSession: A list of stable Id of the product structure or objects associated with the
    session that must be detached.
    Note: This is considered only during the update case.
    """
    clientId: str = ''
    sessionToCreateOrUpdate: CreateOrUpdateObjectInfo = None
    attachObjectsToSession: List[BaseObjectAttachInfo] = ()
    productAndConfigsToCreate: List[StructureRecipeOfOpenedProduct] = ()
    productAndConfigsToUpdate: List[StructureRecipeRelatedInfo] = ()
    productSessionDataAttachInfos: List[ProductSessionDataAttachInfo] = ()
    detachObjectOrProductsFromSession: List[str] = ()


@dataclass
class SessionProductStructureInfo(TcBaseObj):
    """
    'SessionProductStructureInfo' holds information about the product structure associated to session.
    
    :var stableId: The identifier that enables the client to identify the association of the opened product structure
    with the session.
    :var bomWindow: The BOMWindow of the product structure that was associated to the session. This is populated only
    if  ProductStructureFilter.RecipeObjectsOnly is false.
    :var recipeObject: The recipe object of the structure which can be opened outside the context of the session.
    Typically it is the a VisStructureContext object but it could be any object which is capable of reconstructing the
    BOMWindow and hence the client should not assume the type of object to particular type.
    :var relationProperties: A map(string,PropertyValues) on the relation that associated the session  and the product
    structure . This has information about position, order and parent in case these properties were stored on the
    IMAN_CCContext relation. This map is only populated when the  IMAN_CCContext  relation that associates
    Fnd0AppSession and product structure has this information. 
    The following information is returned.
    'fnd0InsertOrder' of type Integer - Indicates the order at which the product structure was inserted into its parent.
    'fnd0ParentStableId' of type string - Indicates the parent product structure into which the product structure was
    inserted.
    'fnd0Xform' of type string - Indicates the transformation of the product structure in the co-ordinate system of
    parent
    :var staticStructureFileTicket: The static structure file ticket if the product structure was represented as a
    static file during the creation of session.
    Note: This is populated only if  'ProductStructureFilter.WantStaticStructureFileTicket' is true.
    :var relatedObjectInfos: A list of 'RelatedObjectInfo' that contains information about the objects that were
    related to the product structure information associated to session object.
    :var productSessionDataObjects: A list of Fnd0ProductSessionData that are associated to product structure
    information present in the session.
    """
    stableId: str = ''
    bomWindow: BOMWindow = None
    recipeObject: BusinessObject = None
    relationProperties: PropertyValuesMap = None
    staticStructureFileTicket: str = ''
    relatedObjectInfos: List[RelatedObjectInfo] = ()
    productSessionDataObjects: List[ProductSessionDataObjectInfo] = ()


@dataclass
class StructureContextIdentifier(TcBaseObj):
    """
    'StructureContextIdentifier' is a structure in which the application can provide information about the 'product'
    and its configurations that were opened. Using this structure an existing product and configuration is provided in
    the following forms. 
    - product: this could be an Item, ItemRevision, BOMView, BOMViewRevision or BOMLine or VisStructureContext or
    recipe object. If a BOMLine or VisStructureContext or any recipe object is passed then the configInfo need not be
    provided.
    
    
    
    :var product: This is either an Item, ItemRevision, BOMView, BOMViewRevision, BOMLine or StructureContext. The
    following is list the behaviour based on the type of object
    BOMLine - 'configInfo' need not be provided. If 'configInfo' is provided it will be ignored.
    Item or BOMView - The BOMWindow will be created using the ItemRevision by applying the 'configInfo' if provided
    otherwise by applying global RevisionRule on the Item.
    BOMViewRevision - The BOMWindow will be created using the ItemRevision of the BOMViewRevision.
    VisStructureContext  or any recipe object- If the object is already associated to the session nothing is done
    otherwise a copy of the recipe is created and associated to session.The 'configInfo' is ignored.
    :var bomViewType: The PSBOMView type that is to be used to create the BOMWindow. This is used only if Item or
    ItemRevision is supplied as product. If empty the default view type is used.
    :var configInfo: The configuration information for the product. This is used only if Item, ItemRevision, BOMView,
    BOMViewRevision are supplied as product.
    :var configOptions: A map ('string', 'PropertyValues') of property name and values pairs that need to be set on the
    BOMWindow.
    """
    product: BusinessObject = None
    bomViewType: BusinessObject = None
    configInfo: ConfigurationInfo = None
    configOptions: PropertyValuesMap = None


@dataclass
class StructurePathIdentifiers(TcBaseObj):
    """
    'StructurePathIdentifiers' is a structure describes the information that need to be used to traverse a BOMLine path.
    
    :var identifierPropertyName: The name of the property that is used to identify the BOMLine in the path.
    :var resultPathIdentifiers: A list of property values to match when the BOMLine path is traversed.
    """
    identifierPropertyName: str = ''
    resultPathIdentifiers: List[str] = ()


@dataclass
class StructureRecipeOfOpenedProduct(TcBaseObj):
    """
    'StructureRecipeOfOpenedProduct' is a structure in which the application can provide information about the product
    and its configurations that were opened. Using this structure, the subsets or product structures that were added,
    updated or removed to the existing product structure that is associated to session can be updated.
    
    :var clientId: The input 'clientId' sent by the client application which will enable the client to map the output
    with the input.
    :var objsAttachInfos: A list of information about the opened objects that are to be associated to the products
    opened in the context of the session. This would typically include any Dataset or Form that are to associated to
    the product structure in the context of session.
    :var productSessionDataAttachInfos: A list of Fnd0ProductSessionData objects that are to be created or updated and
    attached to the product structure in the context of the session.
    :var structureRecipe: Object of type 'ProductStructureRecipe' which contains product, configuration and subset
    information.
    :var structureRecipeProps: A map ('string', 'PropertyValues') of property name and values pairs that need to be set
     or updated on the ImanRelation that associates the product structure to the session.
    Note':' If the client would like to re-use the same stableId of a detached product structure, then it can be
    accomplished by passing the stable id as value for 'fnd0CopyStableId' property.
    """
    clientId: str = ''
    objsAttachInfos: List[BaseObjectAttachInfo] = ()
    productSessionDataAttachInfos: List[ProductSessionDataAttachInfo] = ()
    structureRecipe: ProductStructureRecipe = None
    structureRecipeProps: PropertyValuesMap = None


@dataclass
class StructureRecipeOfProductOutput(TcBaseObj):
    """
    'StructureRecipeOfOpenedOutput' holds information about the product structure that was associated to the session.
    
    :var clientId: The input 'clientId' sent by the client application which will enable the client to map the output
    with the input.
    :var relativeToSessionStableId: The identifier that enables the client to identify the association of the opened
    product structure with the session.
    :var recipeObject: The recipe object which can be opened outside the context of the session. Typically it&rsquo;s a
    VisStructureContext object but the client application should not assume the type of the object. The type of the
    object returned could be changed in the future. The object is solely returned so that the object can be passed to
    operations that supports creation of BOMWindow using this object.
    :var baseObjectAttachOutputs: A list of 'BaseObjectAttachInfoOutput' which has information about the objects that
    were associated to product structure information in the session.
    :var productSessionDataAttachOutputs: A list of Fnd0ProductSessionData objects that were created or updated and
    attached to the product structure information in the session.
    """
    clientId: str = ''
    relativeToSessionStableId: str = ''
    recipeObject: BusinessObject = None
    baseObjectAttachOutputs: List[BaseObjectAttachInfoOutput] = ()
    productSessionDataAttachOutputs: List[BaseObjectAttachInfoOutput] = ()


@dataclass
class StructureRecipeRelatedInfo(TcBaseObj):
    """
    'StructureRecipeRelatedInfo' contains the product structure information that is associated to the session which is
    to be updated.
    
    :var stableId: The stableId of existing product structure information.
    :var objsAttachInfos: A list of information about the opened objects that are to be associated to the product
    structures opened in the context of the session. This would typically include any Dataset or Form that are to
    associated to the product structure in the context of session.
    :var productSessionDataAttachInfos: A list of Fnd0ProductSessionData objects that are to be created or updated and
    attached to the product structure information in the context of the session.
    :var detachObjects: A list of stable Id of the objects associated with the product structure information in the
    context of the session that must be detached.
    :var structureRecipeProps: A map ('string, PropertyValues') of property name and values pairs that need to be set
    or updated on the ImanRelation that associates the product structure to the session.
    """
    stableId: str = ''
    objsAttachInfos: List[BaseObjectAttachInfo] = ()
    productSessionDataAttachInfos: List[ProductSessionDataAttachInfo] = ()
    detachObjects: List[str] = ()
    structureRecipeProps: PropertyValuesMap = None


@dataclass
class StructureSubsetInfo(TcBaseObj):
    """
    'StructureSubsetInfo' is a structure that has the results of product structure filter which needs to be saved in
    the session.
    
    :var resultContext: Context of the 'resultObjects'. This can be one of following values 
    - 'fnd0bg_occurrences
    - fnd0sel_bg_occurrences
    - fnd0sel_target_occurrences
    - fnd0target_occurrences'
    - 'occurrence_list'
    
    
    If empty default value is assumed as 'occurrence'_lis't'
    :var resultObjects: Results of the product structure filter.
    """
    resultContext: str = ''
    resultObjects: SubsetLinesInfo = None


@dataclass
class SubsetLinesInfo(TcBaseObj):
    """
    'SubsetLinesInfo' is a structure using which the result lines of a search can be persisted along with the subset.
    The lines could be identified as BOMLine object or using an identifier.
    
    :var lines: Result BOMLine that are part of the subset.
    :var compositePathIdentifiers: Result BOMLine identified by path identifiers.
    """
    lines: List[BusinessObject] = ()
    compositePathIdentifiers: List[CompositePathIdentifiers] = ()


@dataclass
class CompositePathIdentifiers(TcBaseObj):
    """
    'CompositePathIdentifiers' is a structure in which the application can provide information about how the BOMLine
    can be identified using identifiers. The identifiers can be of composite in nature which means traverse the BOMLine
    path up to certain level using a particular BOMLine property and then the rest of the path using different
    property. For example, with input like:
    
    'pathIdentifiers[0].identifierPropertyName = "bl_topline_absocc_id"
    pathIdentifiers[0]. resultPathIdentifiers[0] = "absOccUId"
    pathIdentifiers[1].identifierPropertyName = "bl_clone_stable_occurrence_id"
    pathIdentifiers[1].resultPathIdentifiers[0] = "ABC"
    pathIdentifiers[1].resultPathIdentifiers[1] = "CAD"
    pathIdentifiers[1].resultPathIdentifiers[2] = "XYZ"'
    
    While traversing from top BOMLine, the BOMLine that has the property bl_topline_absocc_id=absOccUId will be
    searched followed by the property  'bl_clone_stable_occurrence_id' for traversing the hierarchy. Currently only '
    bl_clone_stable_occurrence_id' is supported to identify the entire BOMLine path.
    
    :var pathIdentifiers: A list of identifiers that identifies the BOMLine in a structure.
    """
    pathIdentifiers: List[StructurePathIdentifiers] = ()


@dataclass
class ConfigurationInfo(TcBaseObj):
    """
    'ConfigurationInfo' is a structure which enables client to pass configuration information for product structures.
    
    :var revRuleConfigInfo: The RevisionRule and the configuration entry parameters.
    :var variantRulesOrOptionSets: A list of VariantRule or StoredOptionSet to be used for configuration.
    :var activeAssemblyArrangement: AssemblyArrangement to be used for configuration.
    :var configContext: Configuration object to be used for configuration. If used then 'revRuleConfigInfo',
    'variantRulesOrOptionSets' and 'activeAssemblyArrangement' are ignored.
    :var bomWinPropFlagMap: A map ('string', 'PropertyValues') of property name and values pairs that need to be set on
    the BOMWindow.
    :var effGrpRevList: A list of Fnd0EffectivityGrp objects, 'effGrpRevList' is used along with BOMWindow  to
    configure.
    """
    revRuleConfigInfo: RevisionRuleConfigInfo = None
    variantRulesOrOptionSets: List[BusinessObject] = ()
    activeAssemblyArrangement: AssemblyArrangement = None
    configContext: BusinessObject = None
    bomWinPropFlagMap: PropertyValuesMap = None
    effGrpRevList: List[ItemRevision] = ()


@dataclass
class CreateInput(TcBaseObj):
    """
    'CreateInput' is a structure used to capture the inputs required for creation of a business object. This is a
    recursive structure containing the 'CreateInput'(s) for any secondary (compounded) objects that might be created
    (e.g. Item also creates ItemRevision and ItemMasterForm).
    
    :var boName: Business Object name.
    :var propertyNameValues: A map ('string, PropertyValues') of property name and values pairs that need to be part of
    create input.
    :var compoundCreateInput: Compounded create input in case the business object needs secondary object to be created.
    """
    boName: str = ''
    propertyNameValues: PropertyValuesMap = None
    compoundCreateInput: CreateInputMap = None


@dataclass
class CreateObjectInfo(TcBaseObj):
    """
    'CreateObjectInfo' is a structure which provides input to create an object.
    
    :var creInp: The 'CreateInput' to create the object.
    :var relationName: The relation to be used to associate the created object to the 'relateToObject'. If this is not
    provided and 'relateToObject' is provided then the relation type is determined using the preference
    <Primary>_<Secondary>_default_relation. For example, if relateToObject is of type ItemRevision and boName is
    DirectModel then preference 
    ItemRevision_DirectModel_default_relation used. If not found, then ItemRevision_default_relation will be searched
    for and used.
    :var relateToObject: The object to which the created object is to be related with the given 'relationName'. 
    Special cases -
    1. Folder object without 'relationName' is passed then the created object is added as a folder content.
    2. BOMLine is passed then the system creates an attachment line.
    """
    creInp: CreateInput = None
    relationName: str = ''
    relateToObject: BusinessObject = None


@dataclass
class CreateOrUpdateObjectInfo(TcBaseObj):
    """
    'CreateOrUpdateObjectInfo' is a structure which provides input to either create or update an object.
    'Note:' If 'objectToUpdate' is provided then 'objectToCreate' will be ignored.
    
    :var objectToCreate: The 'CreateInput' to create the object. In case a Dataset is requested to be created then the
    default values for' tool_used', 'dataset_type' and 'format_used' will be assumed.
    :var objectToUpdate: The object to be updated.
    :var lmdOfObject: Last modified date of the input object. If this input date is different than the current last
    modified date and the 'overwriteForLastModDate' preference is false, the input will be ignored, and processing will
    continue with the next input. In this scenario, error 215033 will be returned. If the dates are different and the
    'overwriteForLastModDate' preference is true, processing will continue with the current input. In this scenario,
    error 215034 will be returned.
    :var overwriteForLastModDate: Flag to check whether the object needs to be updated if the input last modified date
    is different from the current last modified date of the object in Teamcenter.
    :var objectPropsToUpdate: A map ('string', 'PropertyValues') of property name and values pairs that need to be set
    on the created or updated object.
    """
    objectToCreate: CreateObjectInfo = None
    objectToUpdate: BusinessObject = None
    lmdOfObject: datetime = None
    overwriteForLastModDate: bool = False
    objectPropsToUpdate: PropertyValuesMap = None


@dataclass
class CreateOrUpdateSessionOutput(TcBaseObj):
    """
    'CreateOrUpdateSessionOutput' contains the session object and a list of objects and product structures that were
    associated to the session.
    
    :var clientId: The input 'clientId' sent by the client application which will enable the client to map the output
    with the input.
    :var sessionObject: Fnd0AppSession that represents the session.
    :var baseObjectAttachOutputs: A list of 'BaseObjectAttachInfoOutput' which has information about the objects that
    were associated to session.
    :var recipeOfOpenedProductOutputs: A list of 'StructureRecipeOfProductOutput' that contains information about the
    product structures that were associated to session.
    :var productSessionDataAttachOutputs: A list of Fnd0ProductSessionData objects that were created or updated and
    attached to the session object.
    """
    clientId: str = ''
    sessionObject: BusinessObject = None
    baseObjectAttachOutputs: List[BaseObjectAttachInfoOutput] = ()
    recipeOfOpenedProductOutputs: List[StructureRecipeOfProductOutput] = ()
    productSessionDataAttachOutputs: List[BaseObjectAttachInfoOutput] = ()


@dataclass
class CreateOrUpdateSessionResponse(TcBaseObj):
    """
    'CreateOrUpdateSessionResponse' contains a list of 'CreateOrUpdateSessionOutput'
    Each of which has the session object along with it are the objects and product structures that were associated to
    it. Stable Id that identifies the associated objects is also returned which could be used during opening the
    session or referencing them from within the CAD files.
    
    :var sessionOutputs: A list of objects that were associated to the session.
    :var serviceData: 'ServiceData' that contains the partial errors if any.
    """
    sessionOutputs: List[CreateOrUpdateSessionOutput] = ()
    serviceData: ServiceData = None


"""
'Map'('string', 'PropertyValues') of property name to property values.
"""
PropertyValuesMap = Dict[str, PropertyValues]


"""
'StringMap'(string, string) is a map of string to string.
"""
StringMap = Dict[str, str]


"""
'CreateInputMap'('string', list of 'CreateInput') is a map of reference or relation property name to secondary 'CreateInput' objects.
"""
CreateInputMap = Dict[str, List[CreateInput]]
