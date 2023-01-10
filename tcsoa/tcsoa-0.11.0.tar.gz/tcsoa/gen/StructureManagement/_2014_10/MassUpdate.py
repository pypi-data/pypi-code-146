from __future__ import annotations

from enum import Enum
from tcsoa.gen.BusinessObjects import Fnd0MarkupChange, POM_object, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandOneLevelSearchScopeInput(TcBaseObj):
    """
    This operation expands the given parent product structure node to fetch its immediate children. A call to this
    operation is made when defining a search scope for impacted object search.
    
    :var operation: Type of mass update operation being performed. 
    Following are the valid values:
    129 - Replace Realization Source
    
    :var parentNode: Node in a product structure to be expanded.
    :var type: Type of child node
    :var revRule: Revision rule using which the expanded structure is to be configured with.
    """
    operation: int = 0
    parentNode: POM_object = None
    type: POM_object = None
    revRule: str = ''


@dataclass
class ExpandOneLevelSearchScopeOutput(TcBaseObj):
    """
    This is an output structure containing information about child nodes for a given parent node
    
    :var parentNode: Parent node of a product structure for which list of child nodes are requested.
    :var childNodes: List of child nodes for a given input parent node.
    """
    parentNode: POM_object = None
    childNodes: List[POM_object] = ()


@dataclass
class ExpandOneLevelSearchScopeResponse(TcBaseObj):
    """
    This is a structure containing information about child nodes for a given input parent node and partial errors
    occured during an operation.
    
    :var output: List of structure containing information about list of child nodes for a given input parent node of a
    product structure.
    :var serviceData: Standard service data to handle partial errors.
    """
    output: List[ExpandOneLevelSearchScopeOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetMarkupChangesForUpdateOutput(TcBaseObj):
    """
    Structure containing information about Fnd0MarkupChange objects per input ChangeItemRevision.
    
    :var changeItemRev: ChangeItemRevision whose markup changes are to be executed for mass update operation.
    :var markupChangeUIDs: List of unprocessed and/or previously failed Fnd0MarkupChange UIDs referenced by Fnd0Markup
    object associated with changeItemRev
    """
    changeItemRev: ItemRevision = None
    markupChangeUIDs: List[str] = ()


@dataclass
class GetMarkupChangesForUpdateResponse(TcBaseObj):
    """
    Response structure containing information about Fnd0MarkupChange objects per input ChangeItemRevision and standard
    service data for partial errors.
    
    
    :var output: List of structure containing information about Fnd0MarkupChange objects per input ChangeItemRevision.
    :var serviceData: Standard service data for partial errors.
    """
    output: List[GetMarkupChangesForUpdateOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetRevisionRulesResponse(TcBaseObj):
    """
    This operation returns the list of valid revision rules applicable for specific mass update operation type.
    
    :var revRuleNames: List of valid revision rules applicable for mass update operation type.
    :var serviceData: Standard service data for partial errors.
    """
    revRuleNames: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class ImpactedObjectDetailsInput(TcBaseObj):
    """
    This is a structure containing information required to get mass update specific details
    
    :var operation: Mass update operation type being performed. 
    Following are the valid values:
    129 - Replace Realization Source
    
    :var impactedObjectUIDs: This is a list of impacted object UIDs for which mass update specific details are required.
    :var processedImpactedUIDs: This is an optional list of impacted object UIDs for which mass update specific details
    were already fetched previously. Objects corresponding to these UIDs will be unloaded from the server since they
    are no longer needed.
    :var change: Change ItemRevision to record mass update results.
    """
    operation: int = 0
    impactedObjectUIDs: List[str] = ()
    processedImpactedUIDs: List[str] = ()
    change: ItemRevision = None


@dataclass
class ImpactedObjectDetailsOutput(TcBaseObj):
    """
    This is a structure containing information like whether the impacted object is selectable for performing an update,
    if not selectable then the reason for it being non-selectable, whether the impacted object is out of date etc.
    
    :var impactedObject: This is an impacted object in respect of which mass update specific details are fetched.
    :var isSelectable: Indicates whether the impacted object is selectable for update.
    :var isOutOfDate: Indicates whether the impacted object is out of date
    :var nonSelectableReason: This text informs why the impacted object is not selectable. For selectable impacted
    objects, this text is empty.
    """
    impactedObject: POM_object = None
    isSelectable: bool = False
    isOutOfDate: bool = False
    nonSelectableReason: str = ''


@dataclass
class ImpactedObjectDetailsResponse(TcBaseObj):
    """
    This is a structure containing mass update specific impacted object information and service data to hold partial
    errors.
    
    :var output: List of structure containing mass update specific impacted object information.
    :var serviceData: Standard service data to handle partial errors
    """
    output: List[ImpactedObjectDetailsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ImpactedObjectStatusOutput(TcBaseObj):
    """
    This is a structure containing information about impacted object Save/Remove operation status and the text
    information describing the reason for the failure if any.
    
    :var impactedObject: This is an impacted object added to or removed from change ItemRevision
    :var status: Success/failure status for Save/Remove operation
    :var statusComment: This text informs why the operation on impacted object has failed. If the operation is
    successful then this text is empty.
    """
    impactedObject: POM_object = None
    status: bool = False
    statusComment: str = ''


@dataclass
class ImpactedObjectsQueryInput(TcBaseObj):
    """
    This is a structure containing information about inputs required to query impacted objects.
    
    :var operation: Mass update operation type being performed. This is used to identify type of filtering to use when
    searching for impacted objects. 
    Following are the valid values:
    129 - Replace Realization Source
    
    :var target: Target ItemRevision whose impacted objects are to be searched.
    :var change: Change ItemRevision to record mass update results.
    :var searchScope: Search scope for searching the impacted objects. If no search scope is provided, impacted object
    search is performed in all available product structures.
    """
    operation: int = 0
    target: ItemRevision = None
    change: ItemRevision = None
    searchScope: SearchScope = None


@dataclass
class ImpactedObjectsQueryOutput(TcBaseObj):
    """
    This is an output structure containing information about list of impacted UIDs per input target ItemRevision.
    
    :var target: Target ItemRevision whose impacted objects are queried for performing mass update operation.
    :var impactedObjectUIDs: List of all impacted object UIDs for a given target ItemRevision.
    """
    target: ItemRevision = None
    impactedObjectUIDs: List[str] = ()


@dataclass
class ImpactedObjectsQueryResponse(TcBaseObj):
    """
    This is a structure containing information about impacted object UIDs per target ItemRevision and service data for
    partial errors.
    
    :var output: List of structure containing impacted object UIDs information.
    :var serviceData: Standard service data to handle partial errors.
    """
    output: List[ImpactedObjectsQueryOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ManageImpactedObjectUpdateInput(TcBaseObj):
    """
    This is a structure containing information data required to manage impacted objects using markup 
    
    :var operation: Mass update operation type being executed
    Following are the valid values:
    129 - Replace Realization Source
    
    :var executionMode: This defines the change ItemRevision specific mass update operation being performed. Following
    are the valid values
    murAddImpactedObjectToMarkup
    murRemoveImpactedObjectFromMarkup
    :var target: Target ItemRevision whose impacted objects are to be searched for mass update
    :var replacement: The new replacement ItemRevision
    :var change: The change ItemRevision object to record mass update results in
    :var addToProblem: Whether to add the target ItemRevision to the problem folder 
    :var addToSolution: Whether to add the target ItemRevision to solution folder
    
    :var markupChange: The markup change correponding to an impacted object to be removed from the markup object and
    the impacted folder of change ItemRevision object
    :var impactedObjects: A list of impacted objects that needs to be managed on change ItemRevision
    """
    operation: int = 0
    executionMode: ManageUpdateOperationType = None
    target: ItemRevision = None
    replacement: ItemRevision = None
    change: ItemRevision = None
    addToProblem: bool = False
    addToSolution: bool = False
    markupChange: Fnd0MarkupChange = None
    impactedObjects: List[POM_object] = ()


@dataclass
class ManageImpactedObjectUpdatesResponse(TcBaseObj):
    """
    This is a structure containing status information about impacted object manage update operations.
    
    :var output: List of structure containing information about impacted object Save/Remove operation status
    :var serviceData: Standard service data for partial errors
    """
    output: List[ImpactedObjectStatusOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ProductScope(TcBaseObj):
    """
    This is a structure containing information about product level search scope.
    
    :var product: Top level product node to be included in the impacted object search scope.
    :var childScope: List of structure containing child scope information for searching the impacted objects.
    :var revRule: Revision rule to configure the impacted object search result.
    """
    product: POM_object = None
    childScope: List[ChildScope] = ()
    revRule: str = ''


@dataclass
class SearchScope(TcBaseObj):
    """
    This is a structure containing information about search scope for searching impacted objects.
    
    :var productScope: List of structure containing product scope information for searching the impacted objects.
    :var propNames: List of impacted object property names based on which the impacted objects are filtered.
    :var propValues: List of impacted object property values based on which the impacted objects are filtered.
    :var defaultRevRule: Default Revision rule to be applied on resultant impacted objects.
    """
    productScope: List[ProductScope] = ()
    propNames: List[str] = ()
    propValues: List[str] = ()
    defaultRevRule: str = ''


@dataclass
class UpdateImpactedObjectEndResponse(TcBaseObj):
    """
    Contains information about whether the cleanup activity is performed successfully or not.
    
    :var isCleanupSuccessful: A list of flags indicating whether the cleanup activity is performed succesfully for each
    input.
    :var serviceData: Standard service data for partial errors.
    """
    isCleanupSuccessful: List[bool] = ()
    serviceData: ServiceData = None


@dataclass
class UpdateImpactedObjectInput(TcBaseObj):
    """
    This is a structure containing information required to update impacted object for mass update operation.
    
    :var operation: Mass update operation type being executed. 
    Following are the valid values:
    129 - Replace Realization Source
    
    :var target: Target ItemRevision whose impacted objects are to be searched for mass update
    :var replacement: The new replacement ItemRevision
    :var change: The change ItemRevision object to record mass update results in
    :var addToProblem: Add the target ItemRevision to the problem folder
    :var addToSolution: Add the replacement ItemRevision to solution folder
    :var impactedObjects: A list of impacted objects to be updated
    :var isSelected: A list of boolean values that indicates whether the impacted objects are selected for mass update
    operation
    """
    operation: int = 0
    target: ItemRevision = None
    replacement: ItemRevision = None
    change: ItemRevision = None
    addToProblem: bool = False
    addToSolution: bool = False
    impactedObjects: List[POM_object] = ()
    isSelected: List[bool] = ()


@dataclass
class UpdateImpactedObjectResponse(TcBaseObj):
    """
    This is a structure containing information about impacted object update status for every object selected for mass
    update operation. It also contains partial error information in ServiceData.
    
    :var output: List of structure containing information about impacted object update operation status.
    :var serviceData: Standard service data for partial errors.
    :var updateRequestId: Unique Identifier per update request initiated from the 'Mass Update Realization' wizard. If
    the update is being performed in batches then this Identifier is same for all the batches. 
    """
    output: List[ImpactedObjectStatusOutput] = ()
    serviceData: ServiceData = None
    updateRequestId: str = ''


@dataclass
class UpdateImpactedObjectStartResponse(TcBaseObj):
    """
    Response structure containing update request identifier and standard service data for partial errors.
    
    
    :var updateRequestId: Unique Update Request Identifier per update request initiated by user while performing 'Mass
    Update Realization'. If the update is being performed in batches then this Identifier is same for all the batches.
    :var serviceData: Standard service data for partial errors.
    
    Note: Member 'serviceData' available as part of this structure is not being used presently. This member has been
    added to this structure for Future use case.
    """
    updateRequestId: str = ''
    serviceData: ServiceData = None


@dataclass
class ValidateChangeObjectForMassUpdateOutput(TcBaseObj):
    """
    This is a structure containing information whether the input ChangeItemRevision is valid for Mass Update type.
    
    :var changeItemRev: Input ChangeItemRevision.
    :var isValid: This flag is set to true if the corresponding input Change Item revision is valid for Mass Update
    type.
    -If API is called with input massUpdateType="massUpdate", this flag is set to false if Fnd0MarkupChange object
    associated with input ChangeItemRevision is found with mass update operation value = 129
    -If API is called with input massUpdateType="massUpdateRealization", this flag is set to false if Fnd0MarkupChange
    object associated with input ChangeItemRevision is found with mass update operation value != 129
    """
    changeItemRev: ItemRevision = None
    isValid: bool = False


@dataclass
class ValidateChangeObjectForMassUpdateResponse(TcBaseObj):
    """
    This is a structure that contains the information whether the input ChangeItemRevision is valid for Mass Update
    type. It also holds the standard service data for partial errors.
    
    :var output: List of structure containing information whether the input ChangeItemRevision is valid for Mass Update
    operation.
    :var serviceData: Standard service data for partial errors.
    """
    output: List[ValidateChangeObjectForMassUpdateOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ChildScope(TcBaseObj):
    """
    This is a structure containing information about a child node and a boolean flag indicating whether this child node
    has to be included recursively in the search scope of impacted objects.
    
    :var child: Child node to be included in the impacted object search scope.
    :var recurse: Indicates whether the child nodes are to be included recursively for the impacted object search scope.
    """
    child: POM_object = None
    recurse: bool = False


@dataclass
class ExecuteMarkupChangeInput(TcBaseObj):
    """
    Input structure containing information about Change Item revision and it's Fnd0MarkupChange object UIDs to be
    executed.
    
    :var changeItemRev: ChangeItemRevision whose associated Fnd0MarkupChange objects are to be executed.
    :var markupChangeUIDs: List of Fnd0MarkupChange object UIDs associated with ChangeItemRevision
    """
    changeItemRev: ItemRevision = None
    markupChangeUIDs: List[str] = ()


@dataclass
class ExecuteMarkupChangeOutput(TcBaseObj):
    """
    This is a structure containing information about an update status and the list of updated Fnd0MarkupChange objects
    per input ChangeItemRevision.
    
    :var changeItemRev: ChangeItemRevision whose associated Fnd0MarkupChange objects are executed
    :var markupChangeObjs: A list of Fnd0MarkupChange objects that are executed
    :var isUpdateSuccessful: This flag is set to true only if all the input Fnd0MarkupChange objects executes
    succesfully.
    """
    changeItemRev: ItemRevision = None
    markupChangeObjs: List[Fnd0MarkupChange] = ()
    isUpdateSuccessful: bool = False


@dataclass
class ExecuteMarkupChangeResponse(TcBaseObj):
    """
    This is a response structure containing update status information about Fnd0MarkupChange objects per input
    ChangeItemRevision and standard service data for partial errors.
    
    :var output: List of structure containing update status and updated Fnd0MarkupChange objects per input
    ChangeItemRevision.
    
    :var serviceData: Standard service data for partial errors.
    """
    output: List[ExecuteMarkupChangeOutput] = ()
    serviceData: ServiceData = None


class ManageUpdateOperationType(Enum):
    """
    Defines enum values for manage update operation types
    """
    murAddImpactedObjectToMarkup = 'murAddImpactedObjectToMarkup'
    murRemoveImpactedObjectFromMarkup = 'murRemoveImpactedObjectFromMarkup'
