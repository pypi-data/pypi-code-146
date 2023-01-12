from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from typing import List
from tcsoa.gen.Internal.StructureManagement._2012_02.StructureVerification import PartialMatchCriteria2
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindReviewStatusDetails(TcBaseObj):
    """
    The review status details for a list of impacted target scopes.
    
    :var inputIndex: Corresponds to the index of the input list.
    :var statusDetails: Corresponds to the details of the review status associated with impacted target scopes. This
    list is in parallel with the changedObjects list in FindReviewStatusIn.
    """
    inputIndex: int = 0
    statusDetails: List[FindSingleReviewStatusDetail] = ()


@dataclass
class FindReviewStatusIn(TcBaseObj):
    """
    Input object that contains the changed line, the change identifier, and the impacted target scopes.
    
    :var changedLine: The changed BOMLine object.
    :var changedObjects: The changed objects, which can be IncrementalChangeElement, ItemRevision, or PSOccurrence
    objects.
    :var impactedScopes: A list of BOMLine objects representing the impacted target scopes.
    """
    changedLine: BOMLine = None
    changedObjects: List[BusinessObject] = ()
    impactedScopes: List[BOMLine] = ()


@dataclass
class FindReviewStatusResponse(TcBaseObj):
    """
    The response that contains the review status details for a list of impacted target scopes.
    
    :var statusDetails: The review status details information. Each FindReviewStatusDetails object in the statusDetails
    list represents the status details for a single FindReviewStatusIn object in the input list.
    :var serviceData: Will contain the client ID and partial errors.
    """
    statusDetails: List[FindReviewStatusDetails] = ()
    serviceData: ServiceData = None


@dataclass
class FindSingleReviewStatusDetail(TcBaseObj):
    """
    Review status detail for an impacted target scope.
    
    :var resultantScope: The scope object whose review status is used. It can be any of the following: the top most
    scope object which has a review status, the target scope itself if it has a review status, a child scope if this is
    the only child which has a review status, or null if the target scope has multiple children with a review status.
    :var resultantStatus: The review status from the resultantScope.
    :var evaluatedScopes: In case there is a review status on multiple sub-scopes, this field will contain the
    sub-scope objects.
    :var evaluatedStatus: In case there is a review status on multiple sub-scopes, this field will contain the status
    of each sub-scope object.
    :var setByUser: Indicates if this review status is explicitly set by the user.
    """
    resultantScope: BusinessObject = None
    resultantStatus: str = ''
    evaluatedScopes: List[BusinessObject] = ()
    evaluatedStatus: List[str] = ()
    setByUser: bool = False


@dataclass
class GetPropPropagationDetailsRespElem(TcBaseObj):
    """
    The getPropertyPropagationStatusDetails response element. Contains property details and propagation status details
    for each input line.
    
    :var propagationStatusDetails: A list of review status detail elements.
    
    :var propertyDetails: A list of  property details for each line.
    :var additionalInfo: Future Use
    """
    propagationStatusDetails: List[FindReviewStatusDetails] = ()
    propertyDetails: List[PropertyDetail2] = ()
    additionalInfo: PartialMatchCriteria2 = None


@dataclass
class GetPropPropagationStatusDetailsIn(TcBaseObj):
    """
    A list of changed lines, the reason for the change and a potential list of candidate impacted lines.
    
    :var changedLines: List of changed BOMLine objects.
    :var impactedLines: List of propagation candidate BOMLine objects.
    :var objectsDescribingChange: List of property changed objects, which can be  IncrementalChangeElement, 
    ItemRevision, or 
    PSOccurrence.
    
    :var additionalInfo: Future Use
    """
    changedLines: List[BusinessObject] = ()
    impactedLines: List[BusinessObject] = ()
    objectsDescribingChange: List[BusinessObject] = ()
    additionalInfo: PartialMatchCriteria2 = None


@dataclass
class GetPropPropagationStatusDetailsResp(TcBaseObj):
    """
    List of property and propagation status details for each input line.
    
    :var details: A list of property and propagation status details.
    :var serviceData: Service data capturing partial errors using the input array index as client id.
    """
    details: List[GetPropPropagationDetailsRespElem] = ()
    serviceData: ServiceData = None


@dataclass
class GetStructureChangeDetailsResponse(TcBaseObj):
    """
    The GetStructureChangeDetailsResponse is returned by the getStructureChangeDetails method.  The response is the
    details of a changed line that was changed by IC, revision, occurrence effectivity or time period.  The details
    returned are the value that was requested in the original call to getStructureChangeDetails.  The response has two
    main element that are:
    
    -     serviceData - Service data capturing partial errors using the input array index as client id.
    -     details - list of StructureChangeDetailsResponseElement
    
    
    
    :var serviceData: Service data capturing partial errors using the input array index as client id.
    :var details: The details of a changed value of the configured input line.
    """
    serviceData: ServiceData = None
    details: List[StructureChangeDetailsResponseElement] = ()


@dataclass
class GetStructureChangeImpactedLinesInfo(TcBaseObj):
    """
    The GetStructureChangeImpactedLinesInfo contains impacted lines and associated line info that were found in the
    input target structure.  The impacted lines are lines chosen in the target structure due to changes in a source
    structure.  The type of changes in the source structure that are supported are:
    
    - Incremental changes
    - Revision effectivity changes
    - Occurrence effectivity changes
    - Time period changes
    
    
    
    :var icImpactedLinesInfo: Impacted lines and associated information found in the target structure that were
    impacted in the source structure through incremental change.  This field is a generic map, currently the following
    key/value pairs are returned:
    
    The PartialMatchCriteria is a structure of maps as follows:
    struct PartialMatchCriteria2
    { 
        StringToIntVectorMap2 intMap,
        StringToDblVectorMap2 dblMap,
        StringToStrVectorMap2 strMap,
        StringToObjVectorMap2 objMap,
        StringToDateVectorMap2 dateMap
    };
    
    Elements:
    - intMap map of string to list of integers. 
    - dblMap map of string to list of doubles. 
    - strMap map of string to list of strings. 
    - objMap map of string to list of objects. 
    - dateMap map of string to list of dates 
    
    
    
    strMap entries:
    
    Key: ChangeType
    Value: One of the following case sensitive strings:
    
    - Add
    - Remove
    - Move
    - Property
    - Attachment
    - Predecessor
    
    
    
    Key: AttributeName (Required for Property Change)
    Value: Internal name of affected value
    
    Key: AttributeValue (Required for Property Change)
    Value: Value that changed   (Aligned with AttributeName list)
    
    Key: PredecessorName (Required for Predecessor Change Type)
    Value: name of predecessor
    
    Key:PredecessorSequence (Required for Predecessor Change Type)
    Value: sequence number of predecessor     
    
    objMap entries:
    
    Key: ChangedLine        Value: BOMLine in the source structure that changed
    
    Key: AffectedObject (Required for Attachment Change)
    Value: An object of one of the following types (not a complete list):
    - PSOccurrence
    - Datasets
    - Folders
    - Forms
    - Activities
    - AbsOccData
    
    
    
    End of the details for the icImpactedLinesInfo PartialMatchCriteria2 structure.
    
    
    
    - findImpactedLinesByRevisionEff    Currently not supported
    - findImpactedLinesByOccEff        Currently not supported
    - findImpactedLinesByPeriod        Currently not supported
    
    
    :var revisionImpactedLinesInfo: Impacted lines and associated information found in the target structure that were
    impacted in the source structure through revision effectivity change. Currently not supported.
    :var occEffImpactedLinesInfo: Impacted lines and associated information found in the target structure that were
    impacted in the source structure through occurrence effectivity change.  Currently not supported.
    :var periodImpactedLinesInfo: Impacted lines and associated information found in the target structure that were
    impacted in the source structure through time period change.  Currently not supported.
    """
    icImpactedLinesInfo: PartialMatchCriteria2 = None
    revisionImpactedLinesInfo: PartialMatchCriteria2 = None
    occEffImpactedLinesInfo: PartialMatchCriteria2 = None
    periodImpactedLinesInfo: PartialMatchCriteria2 = None


@dataclass
class GetStructureChangeImpactedLinesResponse(TcBaseObj):
    """
    The GetStructureChangeImpactedLinesResponse is returned by the getStructureChangeImpactedLines method.  The
    response contains partial errors or impacted lines and associated line information.  Impacted lines are lines in a
    target structure that are affected by changes in a source structure. The following errors may be returned:
    - 214522 The End item specified for the Unit Effectivity is invalid.
    - 214523 No incremental change contexts can be found based on search criteria.
    - 214524 Invalid units specified for searching.
    - 214525 Invalid dates specified for searching.
    - 200451 The incremental change criteria are invalid.
    
    
    
    :var impactedLinesInfo: The impacted lines and associated line info found in the input target structure based on
    changes made to the source structure.  Impacted lines are lines in a target structure that are potentially affected
    by changes in a source structure.
    
    The PartialMatchCriteria is a structure of maps as follows:
    struct PartialMatchCriteria2
    { 
        StringToIntVectorMap2 intMap,
        StringToDblVectorMap2 dblMap,
        StringToStrVectorMap2 strMap,
        StringToObjVectorMap2 objMap,
        StringToDateVectorMap2 dateMap
    };
    
    Elements:
    - intMap map of string to list of integers. 
    - dblMap map of string to list of doubles. 
    - strMap map of string to list of strings. 
    - objMap map of string to list of objects. 
    - dateMap map of string to list of dates 
    
    
    
    strMap entries:
    
    Key: ChangeType
    Value: One of the following case sensitive strings:
    
    - Add
    - Remove
    - Move
    - Property
    - Attachment
    - Predecessor
    
    
    
    Key: AttributeName (Required for Property Change)
    Value: Internal name of affected value
    
    Key: AttributeValue (Required for Property Change)
    Value: Value that changed   (Aligned with AttributeName list)
    
    Key: PredecessorName (Required for Predecessor Change Type)
    Value: name of predecessor
    
    Key:PredecessorSequence (Required for Predecessor Change Type)
    Value: sequence number of predecessor     
    
    objMap entries:
    
    Key: ChangedLine        Value: BOMLine in the source structure that changed
    
    Key: AffectedObject (Required for Attachment Change)
    Value: An object of one of the following types (not a complete list):
    - PSOccurrence
    - Datasets
    - Folders
    - Forms
    - Activities
    - AbsOccData
    
    
    
    End of the details for the icImpactedLinesInfo PartialMatchCriteria2 structure.
    
    
    
    - findImpactedLinesByRevisionEff    Currently not supported
    - findImpactedLinesByOccEff        Currently not supported
    - findImpactedLinesByPeriod        Currently not supported
    
    
    :var serviceData: The partial errors indexed by the input vector.
    """
    impactedLinesInfo: List[GetStructureChangeImpactedLinesInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ImpactedLinesCriteria(TcBaseObj):
    """
    This data structure is used by the getImpactedLinesForStructureChange method.  The data structure provides criteria
    for finding impacted lines in the designated target structure due to changes in a related but different structure. 
    The data structure supports four types of structure changes:  
    
    - Incremental change
    - Revision effectivity - Currently not supported
    - Occurrence effectivity - Currently not supported
    - Time period - Currently not supported
    
    
    
    :var findImpactedLinesByICInfo: This structure contains changed lines under incremental change that will be used to
    find equivalent impacted lines in the input target structure.  This element is a generic map that currently
    supports the following name/value pairs:
    
    strMap entries:
    
    Key: ChangeType
    Value: One of the following case sensitive strings:
    
    - Add
    - Remove
    - Move
    - Property
    - Attachment
    - Predecessor
    
    
    
    objMap entries:
    
    Key: ChangedLine
    Value: BOMLine in the source structure that changed
    
    Key: AffectedObject
    Value: An object of one of the following types (not a complete list):
            PSOccurrence
            Datasets
            Folders
            Forms
            Activities
            AbsOccData
    :var findImpactedLinesByRevisionEff: This structure contains changed lines by revision effectivity that will be
    used to find equivalent impacted lines in input target structure.
    :var findImpactedLinesByOccEff: This structure contains changed lines by occurrence effectivity that will be used
    to find equivalent impacted lines in input target structure.
    :var findImpactedLinesByPeriod: This structure contains changed lines by time period that will be used to find
    equivalent impacted lines in input target structure.
    """
    findImpactedLinesByICInfo: PartialMatchCriteria2 = None
    findImpactedLinesByRevisionEff: PartialMatchCriteria2 = None
    findImpactedLinesByOccEff: PartialMatchCriteria2 = None
    findImpactedLinesByPeriod: PartialMatchCriteria2 = None


@dataclass
class PropagationDetail(TcBaseObj):
    """
    The propagation status for a target line.
    
    :var status: The propagation status.
    :var targetContext: The target line. (MEAppearancePathNode)
    """
    status: str = ''
    targetContext: BusinessObject = None


@dataclass
class PropertyDetail2(TcBaseObj):
    """
    Index and list of property details for one element in the input array.
    
    :var index: Index into the input array.
    :var propertyDetails: List of property details
    """
    index: int = 0
    propertyDetails: List[PropertyDetailsElement2] = ()


@dataclass
class PropertyDetailsElement2(TcBaseObj):
    """
    Internal version of PropertyDetailsElement.
    Contains property name and isDifferent elements.
    
    :var propertyName: The property name
    :var isDifferent: Set true if property is different between the two lines
    """
    propertyName: str = ''
    isDifferent: bool = False


@dataclass
class ReviewStatusInfo(TcBaseObj):
    """
    The status to be set on this target scope.
    
    :var impactedScopeLine: The BOMLine object representing an impacted target scope.
    :var status: The status that needs to be set on this impacted target scope.
    """
    impactedScopeLine: BOMLine = None
    status: str = ''


@dataclass
class StructureChangeDetailsElement(TcBaseObj):
    """
    The StructureChangeDetailsElement contains the changed line, the changed value and the configuration information
    for which detailed information is required about the change.  The main elements of the structure are:
    -     searchContext    The search context that was used to find the original changed lines
    -     icChangesInfo    The changed lines found by incremental change critieria
    -     revisionChangesInfo    The changed lines found by revision criteria (Currently not supported)
    -     occEffChangesInfo    The changed lines found by occurrence effectivity (Currently not supported)
    -     periodChangesInfo    The changed lines found by period changes (Currently not supported)
    
    
    
    :var searchContext: The search context that was used to find the original changed lines.
    
    For Vector entries where only one value is needed always use the first vector position.
    Either 'Date' or 'Unit' effectivity entries are required.
    
    The PartialMatchCriteria2 is a structure of maps as follows:
    struct PartialMatchCriteria2
    { 
        StringToIntVectorMap2 intMap,
        StringToDblVectorMap2 dblMap,
        StringToStrVectorMap2 strMap,
        StringToObjVectorMap2 objMap,
        StringToDateVectorMap2 dateMap
    };
    
    Elements:
    intMap map of string to vector or integers. 
    dblMap map of string to vector of doubles. 
    strMap map of string to vector of strings. 
    objMap map of string to vector of objects. 
    dateMap map of string to vector of dates 
    
     
    Entries for the strMap:
    Key: OwningUser        Value: userid as String
    Key: Statuses            Value: A list of statuses - one status for each element of the vector
    Key: ICIntents            Value: A list of IC intents - one for each element of the vector
    
    
    
    Entries for the intMap:
    Key: IsUnitEffectivity            Value: 0 == false, 1 == true
    Key: IsDateEffectivity        Value: 0 == false, 1 == true
    Key: AlreadyReviewedUnit    Value: already reviewed unit number as int
    Key: ToReviewUnit            Value: to review unit number as int
    
    
    Entries for the dateMap:
    Key: AlreadyReviewedDate        Value: date
    Key: ToReviewDate                Value: date
    Key: StatusSinceDate            Value: status since date
    
    
    Entries for the objMap:
    Key :EndItemComp (Required if Unit Effectivity)    Value: End Item of IC Unit effectivity 
    Key: ScopeLines (Required)            Value: Selected BOMLine objects in the original search 
    
        
        
    
    :var icChangesInfo: The changed lines found by incremental change critieria
    The PartialMatchCriteria2 structure of maps has the following entries:
    For vector entries where only one value is needed always use the first vector position.
    Entries for the objMap:
    
    Key: ChangedLine (Required)        Value: The changed BOMLine
    Key: ICRev (Required)            Value: ItemRevision representing the Incremental Change object 
    Key: ICE (Required)            Value: IncrementalChangeElement associated with the changed line.
    
    Key: AffectedObject            Value: An object of one of the following types (not a complete list):
    - PSOccurrence
    - Datasets
    - Folders
    - Forms
    - Activities
    - AbsOccData
    
    
    
    Entries for the strMap:
    Key: ChangeType (Required)        Value: One of the following case sensitive strings:
    - Add
    - Remove
    - Move
    - Property
    - Attachment
    - Predecessor
    
    
     
    Key: HowConfigured                                                    Value: the incremental change how configured
    string
           
    Key:AttributeName (Required for Property Change Type)    Value: internal name of the attribute for
    attribute/property changes
           
    Key:AttributeValue (Required for Property Change Type)    Value: value of the attribute from incremental    change 
          
          
    Key: PredecessorName (Required for Predecessor Change Type)        Value: name of predecessor
    
    Key:PredecessorSequence (Required for Predecessor Change Type)    Value: sequence number of predecessor     
     
    Key:UnitRangeText (Required for unit effectivity)                                Value: unit range text
    
    Key:DateRangeText (Required for date effectivity)                            Value: date range text
    :var revisionChangesInfo: This field is currently not supported.
    :var occEffChangesInfo: This field is currently not supported.
    :var periodChangesInfo: This field is currently not supported.
    """
    searchContext: PartialMatchCriteria2 = None
    icChangesInfo: PartialMatchCriteria2 = None
    revisionChangesInfo: PartialMatchCriteria2 = None
    occEffChangesInfo: PartialMatchCriteria2 = None
    periodChangesInfo: PartialMatchCriteria2 = None


@dataclass
class StructureChangeDetailsResponseElement(TcBaseObj):
    """
    The StructureChangeDetailsResponseElement is returned from the getStructureChangeDetails method.   The main
    components of the structure are the following:
    
    - icChangeDetails - the details of a changed line from IC related change
    - revisionChangeDetails - the details of a changed line from revision related change     (Currently not supported) 
              
    - occEffChangeDetails - the details of a changed line from occurrence effectivity change (Currently not supported) 
                  
    - periodChangeDetails - the details of a changed line from period related change (Currently not supported)
    
    
                    
    
    :var icChangeDetails: The details of a changed line from IC related change 
    The PartialMatchCriteria2 is a structure of maps as follows:
    struct PartialMatchCriteria2
    { 
        StringToIntVectorMap2 intMap,
        StringToDblVectorMap2 dblMap,
        StringToStrVectorMap2 strMap,
        StringToObjVectorMap2 objMap,
        StringToDateVectorMap2 dateMap
    };
    
    Elements:
    intMap map of string to vector or integers. 
    dblMap map of string to vector of doubles. 
    strMap map of string to vector of strings. 
    objMap map of string to vector of objects. 
    dateMap map of string to vector of dates 
    Entries for the objMap:
    
    Key: ChangedLine (Required)    Value: The changed BOMLine
    
    Key: ICRev (Required)        Value: ItemRevision representing the Incremental Change object 
    
    Key: ICE (Required)        Value: IncrementalChangeElement associated with the changed line.
    
    Key: AffectedObject
    Value: An object of one of the following types (not a complete list):
    -         PSOccurrence
    -         Datasets
    -         Folders
    -         Forms
    -         Activities
    -         AbsOccData
    
    
    
    Entries for the strMap:
    
    Key: ChangeType (Required)
    Value: One of the following case sensitive strings:
        Add
        Remove
        Move
        Property
        Attachment
        Predecessor
     
    Key: HowConfigured    Value: the incremental change how configured string
           
    Key:AttributeName (Required for Property Change Type)
    Value: internal name of the attribute for attribute/property changes
           
    Key:AttributeValue (Required for Property Change Type)      
    Value: value of the attribute from incremental change        
          
    Key: PredecessorName (Required for Predecessor Change Type)
    Value: name of predecessor
    
    Key:PredecessorSequence (Required for Predecessor Change Type)
    Value: sequence number of predecessor     
     
    Key:UnitRangeText (Required for unit effectivity)
    Value: unit range text
    
    Key:DateRangeText (Required for date effectivity)
    Value: date range text
         
    :var revisionChangeDetails: This field is not currently supported.
    :var occEffChangeDetails: This field is not currently supported.
    :var periodChangeDetails: This field is not currently supported.
    """
    icChangeDetails: PartialMatchCriteria2 = None
    revisionChangeDetails: PartialMatchCriteria2 = None
    occEffChangeDetails: PartialMatchCriteria2 = None
    periodChangeDetails: PartialMatchCriteria2 = None


@dataclass
class TargetCreateOrUpdateParams(TcBaseObj):
    """
    Criteria for a target line that needs propagation status created or updated. In case a selected target line is to
    be moved from one parent to another, two such structures will be needed: one for the selected target line and the
    other for the suggested parent line. The structure for the selected target line will have a regular status value
    (e.g., "Handled") in its status field; and the structure for the suggested target line will have a special value
    "BDF3D5F9-1330-4ED0-A290-E6C1B5250DFF:MoveTo" in its status field.
    
    :var targetLine: The target line.
    :var incrementalChangeElement: Incremental change element (Optional)
    :var status: Propagation status
    """
    targetLine: BOMLine = None
    incrementalChangeElement: BusinessObject = None
    status: str = ''


@dataclass
class CreateOrUpdatePropagationDetailsIn(TcBaseObj):
    """
    The input criteria describing which target lines need propagation status updated or created.
    
    :var changedLine: The changed line.
    :var changedObject: The changed object, which can be IncrementalChangeElement,  ItemRevision, or PSOccurrence.
    :var changeType: The change type
    :var targets: The target info to create or update propagation statuses.    
    """
    changedLine: BOMLine = None
    changedObject: BusinessObject = None
    changeType: str = ''
    targets: List[TargetCreateOrUpdateParams] = ()


@dataclass
class CreateOrUpdatePropagationDetailsResp(TcBaseObj):
    """
    Propagation status response.
    
    :var details: List of propagation details elements.
    :var serviceData: Handle partial errors and return propagation statuses.
    """
    details: List[CreateOrUpdatePropagationDetailsRespElem] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdatePropagationDetailsRespElem(TcBaseObj):
    """
    List of propagation details.
    
    :var propagationDetails: List of propagation details.
    """
    propagationDetails: List[PropagationDetail] = ()


@dataclass
class CreateOrUpdateReviewStatusDetails(TcBaseObj):
    """
    Review status details set on a list of impacted target scopes.
    
    :var inputIndex: Corresponds to the index of the input list.
    :var statusDetails: Corresponds to the details of the review status associated with specific impacted target
    scopes. This list is in parallel with the impactedScopeStatus list in CreateOrUpdateReviewStatusIn.
    """
    inputIndex: int = 0
    statusDetails: List[CreateOrUpdateSingleReviewStatusDetail] = ()


@dataclass
class CreateOrUpdateReviewStatusIn(TcBaseObj):
    """
    Review status to be set on a list of impacted target scopes.
    
    :var changedLine: The changed BOMLine object.
    :var changedObject: The changed object, which can be IncrementalChangeElement, ItemRevision, or PSOccurrence.
    :var changeType: The type of the change.
    :var impactedScopeStatus: The review status for a list of impacted target scopes.        
    """
    changedLine: BOMLine = None
    changedObject: BusinessObject = None
    changeType: str = ''
    impactedScopeStatus: List[ReviewStatusInfo] = ()


@dataclass
class CreateOrUpdateReviewStatusResponse(TcBaseObj):
    """
    The review status details set on a list of impacted target scopes for every input.
    
    :var statusDetails: The review status details information. Each CreateOrUpdateReviewStatusDetails object in the
    statusDetails list represents the status details for a single CreateOrUpdateReviewStatusIn object in the input list.
    :var serviceData: Contains the client ID and partial errors.
    """
    statusDetails: List[CreateOrUpdateReviewStatusDetails] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateSingleReviewStatusDetail(TcBaseObj):
    """
    The review status set on a single impacted target scope.
    
    :var impactedScopeObject: The impacted scope object whose review status is set. It can be any of the following: the
    top most scope object which has a review status, the target scope itself if it has a review status, a child scope
    if this is the only child which has a review status, or null if the target scope has multiple children with a
    review status.
    :var reviewStatus: The review status from the statusScope.
    """
    impactedScopeObject: BusinessObject = None
    reviewStatus: str = ''
