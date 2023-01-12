from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, PSBOMViewRevision, ChangeItem, ChangeItemRevision, BOMWindow, BOMSupersedure, BOMEdit
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateChangeItemInputs(TcBaseObj):
    """
    Input structure for holding create change item input.
    
    :var clientID: Tracking client invoking this method this information not persisted, Optional
    :var iD: iD
    :var revisionID: The revision ID that will be set on the new object, Required
    :var name: Name that will be used on the new object, Required
    :var description: Description that will be used on the new object, Required
    :var type: This will be used to determine what type of change item that is to be created, Required
    :var relationshipData: The list of objects and their relations to the change item, Optional
    :var extendedData: The list of additional attributes that might be passed from a client, Optional
    """
    clientID: str = ''
    iD: str = ''
    revisionID: str = ''
    name: str = ''
    description: str = ''
    type: str = ''
    relationshipData: List[RelationshipData] = ()
    extendedData: List[ExtendedAttributes] = ()


@dataclass
class CreateChangeItemsOutput(TcBaseObj):
    """
    Output structure for createChangeItems operation
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var changeItem: Change item object reference that was created.
    :var itemRev: change item revision that is created.
    """
    clientId: str = ''
    changeItem: ChangeItem = None
    itemRev: ChangeItemRevision = None


@dataclass
class CreateChangeItemsResponse(TcBaseObj):
    """
    Response structure for createItems operation
    
    :var output: A list of CreateChangeItemsOutput
    :var serviceData: Standard ServiceData member
    """
    output: List[CreateChangeItemsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateSupercedureInput(TcBaseObj):
    """
    Input structure for createSupercedures operation
    
    :var clientID: A unique client identifier. This is a unique string supplied by the caller. This ID 
    is used to identify return data elements and partial errors associated with this input structure.
    
    :var solutionBvr: This parameter represents a reference to the solution item BOM View Revision 
    (BVR) and is a required parameter. A solution item is a new component that replaces an old component in the parent
    assembly. Solution items are supplementary components that are involved in the solution the change is bringing
    about and the affected item represents the final assembly product containing the solution items.
    
    :var isTransferred: This required parameter determines if the Supercedure created is a transfer type 
    Supercedure and takes in a boolean true or false value. Transfer Supercedures are generated when a component is
    moved from one assembly to another.
    
    :var bomAdds: A list of BOM Adds which represents the additions made to the assembly. It is a 
    required input element.
    
    :var bomCancels: A list of BOM Cancels which denotes the deletions made from the assembly and 
    is a required input parameter.
    
    :var extendedAttributes: A placeholder for additional attributes and this is an optional parameter. i.e it can be
    empty.
    """
    clientID: str = ''
    solutionBvr: PSBOMViewRevision = None
    isTransferred: bool = False
    bomAdds: List[BusinessObject] = ()
    bomCancels: List[BusinessObject] = ()
    extendedAttributes: ExtendedAttributes = None


@dataclass
class CreateSupercedureOutput(TcBaseObj):
    """
    Output structure for createSupercedures operation
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var supercedure: List of tags to the supercedure reference that was created
    """
    clientId: str = ''
    supercedure: List[BusinessObject] = ()


@dataclass
class CreateSupercedureResponse(TcBaseObj):
    """
    Response structure containing list of Supercedure objects and partial errors.
    
    :var output: This represents a list of created Supercedure objects.
    :var serviceData: The SOA framework object containing Supercedure objects that were created 
    based on the input and error information returned based on validations performed.
    """
    output: List[CreateSupercedureOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ConfigureChangeSearchData(TcBaseObj):
    """
    'ConfigureChangeSearchData' structure represents all the details of a Change Home folder.
    
    :var name: Name of the folder
    :var visible: Indicates if the folder is visible or not visible.
    :var queryName: Indicates the name of the query.
    :var savedSearchName: Indicates the name of the saved search name.
    :var queryCriteria: Indicates saved query criterias.
    :var queryValues: Indicates saved query values.
    :var isFolderSiteLevel: Indicates folder is site level or user level and default is user level which is false.
    :var operation: Indicates folder to be added or removed to add value should be Add and to delete value should be
    Remove.
    """
    name: str = ''
    visible: bool = False
    queryName: str = ''
    savedSearchName: str = ''
    queryCriteria: List[str] = ()
    queryValues: List[str] = ()
    isFolderSiteLevel: bool = False
    operation: str = ''


@dataclass
class ExtendedAttributes(TcBaseObj):
    """
    Input structure for createItems operation to support setting attribute values on the created Item,
    ItemRevision, or corresponding master forms that may be created with the objects.
    
    :var attributeName: The name of the attribte to modify or change or update.
    :var values: Values for the attribute ateast must have one value.
    """
    attributeName: str = ''
    values: List[str] = ()


@dataclass
class FindContextDataInputs(TcBaseObj):
    """
    'FindContextDataInputs' structure contains an object reference to a change revision, a pair of object references to
    any Business Object type, and a context string which determines what and how the input objects will be used to
    obtain the desired output objects.
    
    :var changeRev: An object reference to a change revision.
    :var primaryContextInputData: An object reference to any BO type.
    :var secondaryContextInputData: An object reference to any BO type.
    :var contextRelName: A context string.
    """
    changeRev: ChangeItemRevision = None
    primaryContextInputData: BusinessObject = None
    secondaryContextInputData: BusinessObject = None
    contextRelName: str = ''


@dataclass
class FindContextDataOutput(TcBaseObj):
    """
    'FindContextDataOutput' structure contains an object reference that can be used to point to a change revision, a
    list that can be used to hold any number of returned business objects, and a list of counts to help sort out the
    Adds and the Cancels from the returned object list.
    
    :var changeRev: A reference to change revision. Can be empty.
    :var contextOutputData: A list to hold any number of returned business objects.
    :var vBomEditCount: A list of counts used to sort out the Adds and the Cancels.
    """
    changeRev: ChangeItemRevision = None
    contextOutputData: List[BusinessObject] = ()
    vBomEditCount: List[int] = ()


@dataclass
class FindContextDataResponse(TcBaseObj):
    """
    'FindContextDataResponse' structure contains a list of 'FindContextDataOutput' structures and a service data.
    
    :var output: A list of 'FindContextDataOutput' structures.
    :var serviceData: A service data.
    """
    output: List[FindContextDataOutput] = ()
    serviceData: ServiceData = None


@dataclass
class FindSupersedureOutput(TcBaseObj):
    """
    Output structure find supercedure.
    
    :var findsupercedure: A list of reference to supersedure.
    :var bomedit: A reference to BOMEdit to which a supersedure is associated to.
    """
    findsupercedure: List[BOMSupersedure] = ()
    bomedit: BOMEdit = None


@dataclass
class FindSupersedureResponse(TcBaseObj):
    """
    Output structure for list of BOMSupersedure and ServiceData.
    
    :var supersedureOutput: A reference to list of supersedures.
    :var serviceData: The SOA framework object containing Supercedure objects that were 
    returned based on the input and error information returned based on validations performed.
    """
    supersedureOutput: List[FindSupersedureOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetAllChangeHomeFolderResponse(TcBaseObj):
    """
    'GetAllChangeHomeFolderResponse' structure encapsulates the list of returned Change Home folders as a vector of
    'ConfigureChangeSearchData' structures, in addition to the standard mandatory 'ServiceData' structure.
    
    :var output: A vector of 'ConfigureChangeSearchData' structures which represent the details of change home folders
    :var serviceData: Standard ServiceData member
    """
    output: List[ConfigureChangeSearchData] = ()
    serviceData: ServiceData = None


@dataclass
class GetBOMEditInput(TcBaseObj):
    """
    'GetBOMEditInput' structure represents a set of criteria for finding any existing BOMEdit object(s) that satisfy
    the criteria.  It is possible that none satisfies the input criteria.
    
    :var changeRev: A reference to the revision of the change item, Required.
    :var affectedBvr: Reference to PSBOMViewRevision of the affected item, Required
    :var bomEditType: The type of this BOMEdit valid integer values are 1 to 10. BOM_Add=1,BOM_Cancel=2,
    BOM_Quantity_Change=3, BOM_Move=4,BOM_Reshape=5,BOM_Note_Change=6,BOM_Variant_Change=7,LBOM_Add=8,LBOM_Cancel=9,
    and LBOM_Quantity_Change=10
    """
    changeRev: ChangeItemRevision = None
    affectedBvr: PSBOMViewRevision = None
    bomEditType: int = 0


@dataclass
class GetBOMEditOutput(TcBaseObj):
    """
    GetBOMEditOutput structure contains a list of BOMEdit objects and the associated change revision object. The list
    contains the BOMEdit objects that satisfy the input criteria as represented by the corresponding GetBOMEditInput
    structure, and it can be empty.
    
    :var bomEdits: The BOMEdit objects that satisfy the input criteria as represented by the corresponding
    GetBOMEditInput structure. This can be empty.
    :var changeRev: The change revision associated with the returned BOMEdit object(s).
    """
    bomEdits: List[BOMEdit] = ()
    changeRev: ChangeItemRevision = None


@dataclass
class GetBOMEditResponse(TcBaseObj):
    """
    'GetBOMEditResponse' structure contains a list of 'GetBOMEditOutput' structures and a standard ServiceData.
    
    :var bomEditOutput: A vector of 'GetBOMEditOutput' structures.  See 'GetBOMEditOutput' section below for more
    details.  This can be empty.
    :var serviceData: Standard ServiceData member
    """
    bomEditOutput: List[GetBOMEditOutput] = ()
    serviceData: ServiceData = None


@dataclass
class RelationshipData(TcBaseObj):
    """
    Input structure for holding relationship data.
    
    :var tags: List of object references used to hold the objects to put in the relationship, Required
    :var relTypeName: Name of relationship to be created, Required
    :var operation: Flag indicating weather to add or remove relationship, Required
    """
    tags: List[BusinessObject] = ()
    relTypeName: str = ''
    operation: str = ''


@dataclass
class UpdateChangeProperties(TcBaseObj):
    """
    Input structure for updateChangeItems operation
    
    :var chgRev: A reference to the revision of the change item  that to be updated, Required
    :var newPropertyValues: A vector of the property values, Optional
    :var newRelationshipData: A vector of  of relationship data , Optional
    """
    chgRev: ChangeItemRevision = None
    newPropertyValues: List[ExtendedAttributes] = ()
    newRelationshipData: List[RelationshipData] = ()


@dataclass
class UpdateSupercedureData(TcBaseObj):
    """
    Structure for 'updateSupercedures' operation.
    
    :var bomAddOrCancleFlag: A flag value indicating if the update operation is to be carried out on 
    BOMAdds or BOMCancels. This parameter uses Change Management BOM_ADD or BOM_CANCEL constants.
    
    :var operation: A flag indicating whether to add or remove components from the 
    Supercedure. The parameter uses Change Management constants OPERARTION_TYPE_ADD or OPERATION_TYPE_CANCEL.
    
    :var tags: A list of tag values to be added or removed.
    :var supTag: This input element represents the tag for the Supercedure to be updated.
    """
    bomAddOrCancleFlag: str = ''
    operation: str = ''
    tags: List[BusinessObject] = ()
    supTag: BusinessObject = None


@dataclass
class CreateBOMEditInput(TcBaseObj):
    """
    'CreateBOMEditInput' structure contains the object reference to the associated change revision, and the object
    references to the two BOM windows.  The referenced objects will provide the necessary details to create a number of
    BOMEdit objects that represents the whole BOM Change.
    
    :var changeRev: A reference to the revision of the change item.
    :var firstWindow: A reference to the BOM window containing the BOM view Revision of Solution Item Revision for the
    given change objects.
    :var secondWindow: A reference to the BOM window containing the BOM view Revision of Impacted Item Revision for the
    given change objects.
    """
    changeRev: ChangeItemRevision = None
    firstWindow: BOMWindow = None
    secondWindow: BOMWindow = None


@dataclass
class CreateBOMEditResponse(TcBaseObj):
    """
    CreateBOMEditResponse structure contains an empty output, and a standard ServiceData.
    
    :var output: A reference to list of BOMEdits.
    :var serviceData: Standard ServiceData member
    """
    output: List[BOMEdit] = ()
    serviceData: ServiceData = None
