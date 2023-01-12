from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Manufacturing._2009_10.StructureSearch import MFGSearchRefinementSet
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetAssignmentRecipesResp(TcBaseObj):
    """
    GetAssignmentRecipesResp structure contains a list of AdditionalInfo elements, the size of which matches the input
    recipeAnchor list. It also includes the standard serviceData object.
    
    :var info: A list of AdditionInfo structures. If the recipe is found objMap member will have the key "Recipe" and
    the Mfg0MEMBOMRecipe objects as the values, the strMap will have "Name" for key and the corresponding names of the
    recipes, the objMap will have "Anchor" to indicate the BOMLine object owning the recipe.
    :var serviceData: Service data capturing partial errors using the input array index as client id.
    """
    info: List[AdditionalInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AssignmentRecipeSearchCriteria(TcBaseObj):
    """
    search criteria
    
    :var objectTypes: the types of objects to search.
    :var logicalDesignator: name, value attributes of logicalDesignator
    :var refinements: refinements on the search
    :var absoccAttributes: KeyValue Pairs for each attribute on AbsOccurrence to be used in search.
    """
    objectTypes: List[BusinessObject] = ()
    logicalDesignator: KeyValuePair = None
    refinements: List[MFGSearchRefinementSet] = ()
    absoccAttributes: List[KeyValuePair] = ()


@dataclass
class KeyValuePair(TcBaseObj):
    """
    A generic name/value pair construct.
    
    :var name: name of a key
    :var value: property value.
    """
    name: str = ''
    value: str = ''


@dataclass
class ResolveAssignmentRecipeInputElement(TcBaseObj):
    """
    Element decribing the input for resolveAssignmentRecipe.
    
    :var recipeAnchor: The object on or below which the recipe should be resolved. Currently, only BOMLine objects are
    supported.
    :var recipeObjs: A list of recipe objects that are a subset of recipes attached to recipeAnchor. If this list is
    not empty there is no search performed on recipeAnchor to get any recipe objects for resolve. Currently, this
    object must be of type Mfg0MEMBOMRecipe.
    :var searchScopes: The Engineering BOM (EBOM) scopes to resolve the objects to be assigned to skeletal
    Manufacturing BOM (MBOM). Currently, only the root scope ( EBOM root ) BOMLine is supported.
    :var reResolve: If true force resolve by eliminating previous result. Should be true unless, already resolved lines
    are being asked for.
    :var removePreviouslyResolved: If true, any previously resolved lines are removed.
    :var recursive: If true, recursively resolve under the given recipe anchor
    :var generateLog: If true, generates a log file with details of the resolved lines for given recipe under a parent
    line.
    :var appKey: The application key to decide which resolver to use. Currently, only key supported is
    Mfg0AssignmentRecipe.
    """
    recipeAnchor: BusinessObject = None
    recipeObjs: List[BusinessObject] = ()
    searchScopes: List[BusinessObject] = ()
    reResolve: bool = False
    removePreviouslyResolved: bool = False
    recursive: bool = False
    generateLog: bool = False
    appKey: str = ''


@dataclass
class ResolveAssignmentRecipeResp(TcBaseObj):
    """
    ResolveAssignmentRecipeResp structure contains a list of AdditionalInfo elements, the size of which matches the
    input element list. It also includes the standard serviceData object.
    
    :var info: A list of AdditionInfo structures. The names of the resolved recipes appear under the "Recipe" key of
    strMap. Each value in this strMap is a further key into objMap and the values for those are the resolved BOMLine
    objects. Any BOMLine objects that are manually assigned from EBOM to MBOM appear under the objMap key "Manual",
    with the values being the BOMLine objects that were manually assigned. If "generateLog" is true in the input then a
    file ticket is generated under the "LogFileTicket" key of strMap of the first element in this list.
    :var serviceData: serviceData to caputre partial errors.
    """
    info: List[AdditionalInfo] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateAssignmentRecipeInputElem(TcBaseObj):
    """
    An element defining the content and context for attaching the recipe to be used to populating child nodes.
    
    :var name: name of the recipe.
    :var recipeAnchorOrRecipe: The anchor to which the recipe definition will be attached after creation of recipe, or
    the recipe to be updated.
    :var searchContextSC: The object containing the details of search fields supported by cacheless search. Currently,
    this must be a StructureSearchContext with details of cacheless search attributes.
    :var additionalSearchCriteria: additional search criteria with manufacturing aspects.
    :var appKey: A unique key used for choosing the right resolver object. Currently, only supports Mfg0AssignmentRecipe
    """
    name: str = ''
    recipeAnchorOrRecipe: BusinessObject = None
    searchContextSC: BusinessObject = None
    additionalSearchCriteria: AssignmentRecipeSearchCriteria = None
    appKey: str = ''


@dataclass
class CreateOrUpdateAssignmentRecipeResp(TcBaseObj):
    """
    CreateOrUpdateAssignmentRecipeResp structure contains a list of AdditionalInfo elements, the size of which matches
    the input element list. It also includes the standard serviceData object. Each element contains the recipe object (
    stringToObjVector with key "CreatedObject"  or "UpdatedObject" and value being the Mfg0MEMBOMRECIPE). In case there
    is a failure - the element content will be empty - and the serviceData will have the details of the failure for
    that particular element.
    
    
    :var info: A list of AdditionalInfo structures. If recipe is created, the objMap member will have the key
    "CreatedObject" with the value being the Mfg0MEMBOMRecipe object. If recipe is updated the objMap member will have
    the key "UpdatedObject". The strMap member will have the "Name" key with the value being a element of size one
    having the name of the recipe.
    :var serviceData: serviceData
    """
    info: List[AdditionalInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AdditionalInfo(TcBaseObj):
    """
    a generic structure to capture additional information.
    - intMap    A map of string to a list of integers. 
    - dblMap    A map of string to a list of doubles. 
    - strMap    A map of string to a list of strings. 
    - objMap    A map of string to a list of BusinessObjects.
    - dateMap    A map of string to a list of dates.
    
    
    
    :var intMap: A map (string/list of integers) of generic key to integer values.
    :var dblMap: A map (string/list of doubles) of generic key to double values.
    :var strMap: A map (string/list of strings) of generic key to string values.
    :var objMap: A map (string/list of BusinessObjects) of generic key to  BusinessObject values.
    :var dateMap: A map (string/list of dates) of generic key to date values.
    """
    intMap: StringToIntVectorMap = None
    dblMap: StringToDblVectorMap = None
    strMap: StringtoStrVectorMap = None
    objMap: StringToObjVectorMap = None
    dateMap: StringToDateVectorMap = None


"""
a map of string to vector of dates
"""
StringToDateVectorMap = Dict[str, List[datetime]]


"""
String to vector of doubles map.
"""
StringToDblVectorMap = Dict[str, List[float]]


"""
map of string to vector of integers.
"""
StringToIntVectorMap = Dict[str, List[int]]


"""
a map of string to vector of objects.
"""
StringToObjVectorMap = Dict[str, List[BusinessObject]]


"""
A map of string to vector of strings.
"""
StringtoStrVectorMap = Dict[str, List[str]]
