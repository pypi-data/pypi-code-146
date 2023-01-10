from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow, VisStructureContext, BusinessObject
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandPSData(TcBaseObj):
    """
    Through this structure, the child BOMLine, the object of the BOMLine and the objects attached to the BOMLine via
    specified relations are returned.
    
    :var bomLine: BOMLine representing a particular occurrence.
    :var objectOfBOMLine: The object that the BOMLine represents.
    :var relatedObjects: List of object references attached to the BOMLine with the given relations.
    """
    bomLine: BOMLine = None
    objectOfBOMLine: BusinessObject = None
    relatedObjects: List[ExpandPSRelatedObjectInfo] = ()


@dataclass
class ExpandPSFromOccurrenceListInfo(TcBaseObj):
    """
    Input structure that defines the occurrences which are to be expanded into the BOM window
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var occurrences: List of occurrences that are to be expanded.
    """
    clientId: str = ''
    occurrences: List[OccurrenceListInfo] = ()


@dataclass
class ExpandPSFromOccurrenceListOutput(TcBaseObj):
    """
    This structure contains the client identifier and the list of 'OccurrenceListResults'.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var occurrenceList: List of 'OccurrenceListResults' structs describing the occurrences that were expanded
    """
    clientId: str = ''
    occurrenceList: List[OccurrenceListResults] = ()


@dataclass
class ExpandPSFromOccurrenceListPref(TcBaseObj):
    """
    A structure that allows for filtering criteria to be specified.
    
    :var wantDatasets: Boolean flag that when true causes the item revision to expand further so that its datasets can
    be found. If the info argument is empty, all the datasets related to the 'objectOfBOMLine' are returned. Otherwise,
    the filtering rules will be honored. If false, no related objects will be returned.
    :var info: Contains the list of relation name and the types of objects of the given relation to return along with
    the children. If no 'RelationAndTypesFilter' is supplied and the 'wantDatasets' is true, then all Datasets related
    to the 'objectOfBOMLines' are returned.
    """
    wantDatasets: bool = False
    info: List[RelationAndTypesFilter] = ()


@dataclass
class ExpandPSFromOccurrenceListResponse(TcBaseObj):
    """
    Response structure for the 'expandPSFromOccurrenceList' operation.
    
    :var output: List of 'ExpandPSFromOccurrenceListOutput' structures containing the objects corresponding to the
    parent and the child BOMLines and their related objects as well.
    :var serviceData: The service data contains the plain objects and the error stack, if any. Error 46061 is returned
    when the related object is unreadable because of access rules and the user does not have read access to the object.
     Error 46063 is returned when the related object is a remote item and not available at the local site.
    """
    output: List[ExpandPSFromOccurrenceListOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ExpandPSNamedReferenceInfo(TcBaseObj):
    """
    This structure is used to identify the reference object corresponding to the named reference.
    
    :var namedReferenceType: The type of the reference object.
    :var namedReferenceName: The name of the reference object.
    :var referenceObject: Object reference corresponding to the named reference.
    :var fileTicket: FMS ticket used to retrieve the file in cases where referenceObject is a file.
    """
    namedReferenceType: str = ''
    namedReferenceName: str = ''
    referenceObject: BusinessObject = None
    fileTicket: str = ''


@dataclass
class ExpandPSParentData(TcBaseObj):
    """
    Through this structure, the parent BOMLine , the object of the bom line and the objects attached to the bom line
    object are returned.
    
    :var bomLine: BOMLine of the parent to be expanded.
    :var objectOfBOMLine: The object that the parent BOMLine represents.
    :var parentRelatedObjects: List of object references attached to the parent with the given relations.
    """
    bomLine: BOMLine = None
    objectOfBOMLine: BusinessObject = None
    parentRelatedObjects: List[ExpandPSRelatedObjectInfo] = ()


@dataclass
class ExpandPSRelatedObjectInfo(TcBaseObj):
    """
    This structure associates a related object, named references and reference objects.
    
    :var relatedObject: This object is the related to the BOMLine by one of the relation specified in the input
    reference.
    :var namedRefList: List of named references and reference objects of the 'relatedObject'.
    """
    relatedObject: BusinessObject = None
    namedRefList: List[ExpandPSNamedReferenceInfo] = ()


@dataclass
class AreRecipesMergableInfo(TcBaseObj):
    """
    Input structure that contains a recipe object (with optional topline) and the
    BOM window to compare against.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements 
     and partial errors associated with this input structure.
    
    :var recipeObj: Object of type ConfigurationContext or StructureContext that records the configuration recipe.
    
    :var topline: Top line object that must be non null if recipeObj is of type ConfigurationContext. This object is
    either the BOMView or BOMViewRevision of the top line.  This argument is not used when the recipeObj is of type
    StructureContext because StructureContext objects contain a reference to their own top line object.
    
    :var bomWindow: The BOMWindow reference.
    """
    clientId: str = ''
    recipeObj: BusinessObject = None
    topline: BusinessObject = None
    bomWindow: BOMWindow = None


@dataclass
class AreRecipesMergableOutput(TcBaseObj):
    """
    The output structure that contains the client identifier and a boolean
    indicating whether or not a merge is allowed.
    
    :var clientId: The unique string supplied by the caller used to match the output to the supplied input.
    :var isMergable: The answer to the question of whether the recipe contained in the configuration object is
    equivalent to the given BOMWindow configuration.
    """
    clientId: str = ''
    isMergable: bool = False


@dataclass
class AreRecipesMergableResponse(TcBaseObj):
    """
    Response structure for the 'areRecipesMergable' operation.
    
    :var output: List of 'AreRecipesMergableOutput' structures containing the Boolean answer as  to whether the recipe
    contained in the configuration object is equivalent to the BOMWIndow configuration.  If true then the ocurrences in
    the configuration object may be merged into the given BOMWindow.
    
    :var serviceData: The Service Data.
    """
    output: List[AreRecipesMergableOutput] = ()
    serviceData: ServiceData = None


@dataclass
class OccurrenceChain(TcBaseObj):
    """
    Input structure that defines a single occurrence uid chain from the topline (but not including topline) to the
    BOMLine that this chains represents.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var occurrenceChainStr: List of occurrence UIDs that make up the chain of UIDs from the parent BOMLine (but not
    including the parent) down to the last occurrence in the chain.
    """
    clientId: str = ''
    occurrenceChainStr: List[str] = ()


@dataclass
class OccurrenceChainList(TcBaseObj):
    """
    Input structure that defines the parent context and a list of occurrence
    chains to expand within that context.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var parentBomLine: BOMLine reference that is to be used as the parent line when the occurrences in the
    'occurrenceList' are expanded.
    
    :var occurrenceList: The list of occurrences to be expanded and the associated BOMLines returned. These occurrences
    are represented as a list of UID strings. The BOMLine property used to originally obtain these UIDs are listed in
    the 'attibuteNames' member of the 'OccurrenceListInfo' structure.
    """
    clientId: str = ''
    parentBomLine: BOMLine = None
    occurrenceList: List[OccurrenceChain] = ()


@dataclass
class OccurrenceChainResult(TcBaseObj):
    """
    This structure contains the client identifier and the list of 'ExpandPSData' structures for each occurrence in a
    given chain.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var occurrenceChain: The list of 'ExpandPSData' structures that describe the occurrences that were expanded in the
    given occurrence chain.
    """
    clientId: str = ''
    occurrenceChain: List[ExpandPSData] = ()


@dataclass
class OccurrenceListInfo(TcBaseObj):
    """
    Input structure that contains the occurrence chains to be expanded and the property names used to construct those
    occurrence chains.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    
    :var attributeNames: List of one or more attribute names that correspond to the values that make up the
    'OccurrenceChainList'. Each attribute name identifies the BOMLine property  that was used to obtain the identifier
    in the occurrence chain at the same  position. The 'attributeNames' and the 'occurrenceChainsByParent' lists are
    parallel in that regard. However, if the 'attributeNames' list length is less than the 'occurrenceChainsByParent'
    length then it is assumed that the last name in the 'attributeNames' list is repeated out until they are of equal
    length.
    
    :var occurrenceChainsByParent: The list of occurrences to be expanded into BOMLines.
    """
    clientId: str = ''
    attributeNames: List[str] = ()
    occurrenceChainsByParent: List[OccurrenceChainList] = ()


@dataclass
class OccurrenceListResults(TcBaseObj):
    """
    This structure records the parent context and the occurrences expanded in that context.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errorsassociated with this input structure.
    
    :var parent: The parent BOMLine and any additionally requested related objects associated with the BOMLine.
    
    :var occurrenceList: List of 'OccurrenceChainResults' that describe the requested occurrences in the context of the
    given parent BOMLine.
    """
    clientId: str = ''
    parent: ExpandPSParentData = None
    occurrenceList: List[OccurrenceChainResult] = ()


@dataclass
class RelatedObjectTypeAndNamedRefs(TcBaseObj):
    """
    This structure contains a related object type and the list of its named references to be processed.
    
    :var relationTypeName: The related object type for which the specified named references will be processed.
    :var namedReferenceNames: Named references to be processed for the object types.
    """
    relationTypeName: str = ''
    namedReferenceNames: List[str] = ()


@dataclass
class RelationAndTypesFilter(TcBaseObj):
    """
    This structure contains a relation name and a list of related object types and its named references
    ('RelatedObjectTypeAndNamedReferences').  Together they are used to filter objects passed back in a product
    structure expand operation.
    
    :var relationName: Name of the relation by which the objects related to the BOMLines are to be filtered.
    :var relatedObjAndNamedRefs: A list of related object types and named references that are related that are to be
    filtered. The objects filtered will have to be related to the BOMLine by the relation of type specified by the
    'relationName' member.
    
    :var namedRefHandler: An enumeration used to identify how named references are processed.
    
    - UseNamedRefsList : The named references as specified in the 'RelatedObjectAndNamedRefs' structure will be
    processed. 
    - NoNamedRefs : No named references are to be processed. This will override the 'namedReferenceNames' specified in
    the 'RelatedObjectAndNamedRefs' structure. Even if the 'namedReferenceNames' has any values in it, no named
    references will be returned for this option.
    - AllNamedRefs : All the named references , related to the BOMLine  will be processed and sent to the client.
    - PreferredJT : The preferred JT named reference will be returned. Please refer to the  Determining JT file
    priorities section in the Administering the product structure topic of the Structure Manager Guide in Teamcenter
    documentation for more details on the preferred JT files. 
    
    """
    relationName: str = ''
    relatedObjAndNamedRefs: List[RelatedObjectTypeAndNamedRefs] = ()
    namedRefHandler: NamedRefHandler = None


@dataclass
class CreateBOMsFromRecipesInfo(TcBaseObj):
    """
    Input structure that defines the BOM recipe object and optional topline.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure. 
    
    :var recipeObj: Object of type ConfigurationContext, Fnd0StructureContext or StructureContext that records the
    configuration recipe.
    :var topline: Top line object that must be non null if recipeObj is of type ConfigurationContext. This object is
    either the BOMView or BOMViewRevision of the top line. If recipeObj is of type StructureContext or
    Fnd0StructureContext then this argument is ignored.
    """
    clientId: str = ''
    recipeObj: BusinessObject = None
    topline: BusinessObject = None


@dataclass
class CreateBOMsFromRecipesOutput(TcBaseObj):
    """
    Output structure that contains the list of created 'BOMWindow' objects.
    
    :var clientId: The unique string supplied by the caller used to match the output to the supplied input.
    :var bomWindow: The 'BOMWindow' object that was created and configured according to the input recipe. 
    If the recipe objects represent a manufacturing composition then the additional composition windows will also have
    been created and attached to this 'BOMWindow'.
    """
    clientId: str = ''
    bomWindow: BOMWindow = None


@dataclass
class CreateBOMsFromRecipesResponse(TcBaseObj):
    """
    Response structure for the 'createBOMsFromRecipes' operation.
    
    :var output: List of 'CreateBOMsFromRecipesOutput' structures containing the BOM Windows that were created and
    configured according to the input recipe objects. One 'CreateBOMsFromRecipesOutput' returned per input recipe
    object.
    
    :var serviceData: The Service Data.
    """
    output: List[CreateBOMsFromRecipesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateVisSCsFromBOMsInfo(TcBaseObj):
    """
    Input structure used for creating VisStrucutreContext objects based on the given
    BOMWindows and specific occurrenses within those BOMs.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements 
     and partial errors associated with this input structure.
    
    :var occurrencesList: List of BOMLines representing  the occurrences to be included in the structure recipe.
    :var staticStructureFile: IMANFile reference to the PLMXML static representation of the structure. If 
     not supplied then the associated property of the VisStructureContext will not be set.
    """
    clientId: str = ''
    occurrencesList: List[BOMLine] = ()
    staticStructureFile: BusinessObject = None


@dataclass
class CreateVisSCsFromBOMsOutput(TcBaseObj):
    """
    The output structure that contains the references to the created VisStructureContext
    objects along with the corresponding clientId.
    
    :var clientId: The unique string supplied by the caller used to match the output to the supplied input.
    :var structureRecipe: VisStructureContext object that records the configuration recipe of the BOMWindow that
    contains the input BOMLines.
    """
    clientId: str = ''
    structureRecipe: VisStructureContext = None


@dataclass
class CreateVisSCsFromBOMsResponse(TcBaseObj):
    """
    Response structure for the createVisSCsFromBOMs() operation.
    
    :var output: List of 'CreateVisSCsFromBOMsOutput' structures containing the VisStructureContext object that records
    the configuration recipe of the BOMWindow from which the input BOMLines belong.
    
    :var serviceData: The Service Data.
    """
    output: List[CreateVisSCsFromBOMsOutput] = ()
    serviceData: ServiceData = None


class NamedRefHandler(Enum):
    """
    An enumeration used to indicate which name reference handler should be used.
    
    - 'UseNamedRefsList' The named references as specified in the 'RelatedObjectAndNamedRefs' structure will be
    processed. 
    - 'NoNamedRefs' No named references are to be processed. This will override the 'namedReferenceNames' specified in
    the 'RelatedObjectAndNamedRefs' structure. Even if the 'namedReferenceNames' has any values in it, no named
    references will be returned for this option.
    - 'AllNamedRefs' All the named references, related to the BOMLine will be processed and sent to the client.
    - 'PreferredJT' The preferred JT named reference will be returned. Please refer to the Determining JT file
    Priorities section in the Administering the product structure topic of the Structure Manager Guide in Teamcenter
    documentation for more details on the preferred JT files.
    
    """
    UseNamedRefsList = 'UseNamedRefsList'
    NoNamedRefs = 'NoNamedRefs'
    AllNamedRefs = 'AllNamedRefs'
    PreferredJT = 'PreferredJT'
