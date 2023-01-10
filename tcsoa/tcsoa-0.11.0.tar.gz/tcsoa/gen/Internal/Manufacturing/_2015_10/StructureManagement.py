from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AlignmentScopeElement(TcBaseObj):
    """
    Contains the details of a single scope element for alignment.
    
    :var sourceScope: The BOMLine object representing the source scope to align with.
    :var targetScopes: The list of BOMLine objects representing the target scopes to be aligned.
    :var reusedNodes: The list of BOMLine objects under which the target BOMLine objects may have been assigned. All
    BOMLine objects assigned from source structure under this reusedNodes will be considered for alignment if
    alignmentMode is not specified. This list will be empty for single line alignment or  assemblies alignment. For
    reused assemblies alignment, the size of reusedNodes is the same as that of the targetScopes.
    """
    sourceScope: BusinessObject = None
    targetScopes: List[BusinessObject] = ()
    reusedNodes: List[BusinessObject] = ()


@dataclass
class AlignmentSummary(TcBaseObj):
    """
    Contains the summary information for a single alignment input.
    
    :var aligned: The number of successfully aligned lines.
    :var notAlignedWithError: The number of lines not aligned due to errors.
    :var notAlignedUnderReused: The number of lines under reused assemblies.
    """
    aligned: int = 0
    notAlignedWithError: int = 0
    notAlignedUnderReused: int = 0


@dataclass
class GetEquivalentPropValuesElement(TcBaseObj):
    """
    Input structure to provide property names, and original and new ItemRevisions to find equivalent property values
    for.
    
    :var propertyNamesByCategory: List of property names by category to find equivalent property values.
    :var originalItemRevision: The ItemRevision to get equivalent property values from.
    :var newItemRevision: The new ItemRevision for which the equivalent properties are needed.
    """
    propertyNamesByCategory: List[EquivalentPropertyNames] = ()
    originalItemRevision: ItemRevision = None
    newItemRevision: ItemRevision = None


@dataclass
class GetEquivalentPropValuesResp(TcBaseObj):
    """
    The equivalent properties and associated value and equivalent attachments.
    
    :var equivalentPropValuesElements: A list of getEquivalentPropValuesRespElem.
    The size of list is same as size of input to the operation.
    :var serviceData: Service data containing partial errors.
    """
    equivalentPropValuesElements: List[GetEquivalentPropValuesRespElem] = ()
    serviceData: ServiceData = None


@dataclass
class GetEquivalentPropValuesRespElem(TcBaseObj):
    """
    List of equivalent properties and values and equivalent attachments found.
    
    :var propertyCategory: Valid values are:
    - "Item"
    - "ItemRevision"
    - "Item Master"
    - "ItemRevision Master"
    
    
    :var equivalentPropertyValues: List of source and target equivalent properties and associated values.
    :var attachments: List of equivalent attachments found.
    """
    propertyCategory: str = ''
    equivalentPropertyValues: List[PropertyNamePairValue] = ()
    attachments: List[Attachment] = ()


@dataclass
class Attachment(TcBaseObj):
    """
    Description of attachment.
    
    :var relationName: Relation name between Item and attachment.
    :var action: Valid values are:
    - "Ignore" 
    -  "Reference" 
    -  "Clone"
    
    
    :var secondary: Attachment object associated to Item with relationName.
    """
    relationName: str = ''
    action: str = ''
    secondary: BusinessObject = None


@dataclass
class PasteOrReplaceAssemblyInContextInfo(TcBaseObj):
    """
    PasteOrReplaceAssemblyInContextInfo structure contains the input for paste /replace action on a given assembly
    (BOMLine). The structure will comprise of the new ItemRevision object ( needed in case of paste new / replace ),
    the  assembly (BOMLine)  to be pasted/replaced, the parent BOMLine object under which the paste is to be done and
    any additional info required. Currently this additional info is not used.
    
    :var sourceObject: The  BOMLine representing the root of assembly to be pasted/replaced.
    :var targetObject: The BOMLine representing the parent under which the sourceObject need to be pasted. If this is
    null then the sourceObject's item is replaced with newObject.
    :var newObject: The ItemRevision that will get a new BOMViewRevision, child lines, and in context edits duplicated
    from the sourceObject.  It will be pasted to targetObject.  If newObject is null then an ItemRevision of
    sourceObject will be pasted with in context edits duplicated.
    :var additionalInfo: The AdditionalInfo structure. Currently not used.
    """
    sourceObject: BusinessObject = None
    targetObject: BusinessObject = None
    newObject: BusinessObject = None
    additionalInfo: AdditionalInfo = None


@dataclass
class PasteOrReplaceAssemblyInContextResponse(TcBaseObj):
    """
    PasteOrReplaceAssemblyInContextResponse structure contains the ServiceData and AdditionalInfo which is unused
    currently.
    
    :var serviceData: The ServiceData
    :var additionalInfo: The additional info.
    """
    serviceData: ServiceData = None
    additionalInfo: AdditionalInfo = None


@dataclass
class PropertyNamePairValue(TcBaseObj):
    """
    A source and target property name pair that are equivalent and the associated source value.
    
    :var sourcePropName: Property  name of the equivalent property found on the original ItemRevision corresponding to
    the targetPropName.
    :var targetPropName: Equivalent property name for sourcePropName.
    :var sourceValue: The value of sourcePropName from the passed in original ItemRevision.
    """
    sourcePropName: str = ''
    targetPropName: str = ''
    sourceValue: str = ''


@dataclass
class AdditionalInfo(TcBaseObj):
    """
    AdditionalInfo has a list of key value pairs to capture the result.
    
    :var strToDateVectorMap: String to date vector map
    :var strToDoubleVectorMap: String to Double vector map
    :var strToStrVectorMap: String to String vector map
    :var strToObjVectorMap: String to Teamcenter BusinessObject vector map
    :var strToIntVectorMap: String to Integer vector map
    """
    strToDateVectorMap: StringToDateVectorMap = None
    strToDoubleVectorMap: StringToDoubleVectorMap = None
    strToStrVectorMap: StringToStringVectorMap = None
    strToObjVectorMap: StringToObjectVectorMap = None
    strToIntVectorMap: StringToIntegerVectorMap = None


@dataclass
class AlignLinesInBOMData(TcBaseObj):
    """
    Contains the details of an input for alignment.
    
    :var scopeElements: The list of BOMLine objects representing the scopes under which equivalent child BOMLine
    objects are aligned. This list is empty for single line alignment.
    :var equivalentLines: The list of EquivalentLinesPair structures. This list is not empty only for single line
    alignment.
    :var alignmentMode: String representing one of the four alignment modes: "AlignIdInTopLevelContextOnly" - single
    line alignment, "RecursivelyAlignAssemblies" - assemblies alignment, "AlignTransformOnReuseAssemblyOnly" - resued
    assemblies alignment, and "AlignMultipleNodesOfReuseAssm" - align all assigned lines under the reused assembly.
    :var alignProperties: If true, align all occurrence properties of the equivalent lines based on preference
    "MEAlignedPropertiesList".
    :var alignAllAssemblies: Applicable only to alignmentMode "AlignTransformOnReuseAssemblyOnly" or
    "AlignMultipleNodesOfReuseAssm". If true, indicates that in addition to aligning the selected reused assembly, the
    system also aligns the rest of the matching reused assemblies in the MBOM.
    :var additionalInfo: Additional input information; currently not used.
    """
    scopeElements: List[AlignmentScopeElement] = ()
    equivalentLines: List[EquivalentLinesPair] = ()
    alignmentMode: str = ''
    alignProperties: bool = False
    alignAllAssemblies: bool = False
    additionalInfo: AdditionalInfo = None


@dataclass
class AlignLinesInBOMResponse(TcBaseObj):
    """
    Contains the details of the alignment results.
    
    :var logTickets: The list of file tickets for the alignment logs. The size of logTickets is the same as that of the
    alignInputs list.
    :var summaries: The list of AlignmentSummary structures containing the summary information about the alignment. The
    size of summaries is the same as that of the alignInputs list.
    :var serviceData: The ServiceData containing partial errors.
    :var additionalInfo: Additional output information; currently not used.
    """
    logTickets: List[str] = ()
    summaries: List[AlignmentSummary] = ()
    serviceData: ServiceData = None
    additionalInfo: AdditionalInfo = None


@dataclass
class EquivalentLinesPair(TcBaseObj):
    """
    Contains a pair of equivalent BOMLine objects.
    
    :var sourceLine: The source BOMLine object to align with.
    :var targetLine: The target BOMLine object to be aligned.
    """
    sourceLine: BusinessObject = None
    targetLine: BusinessObject = None


@dataclass
class EquivalentPropertyNames(TcBaseObj):
    """
    List of property names and the property category they belong to.
    
    :var propertyCategory: A business object type to which property belong.  Valid values are:
    - Item
    - ItemRevision
    - Item Master
    - ItemRevision Master
    
    
    :var propertyNames: List of property names to find equivalent property values of  original ItemRevision.
    """
    propertyCategory: str = ''
    propertyNames: List[str] = ()


"""
A map of string to list of dates
"""
StringToDateVectorMap = Dict[str, List[datetime]]


"""
A map of string to list of doubles
"""
StringToDoubleVectorMap = Dict[str, List[float]]


"""
A map of string to list of integers
"""
StringToIntegerVectorMap = Dict[str, List[int]]


"""
A map of string to list of Teamcenter BusinessObjects
"""
StringToObjectVectorMap = Dict[str, List[BusinessObject]]


"""
A map of string to list of strings
"""
StringToStringVectorMap = Dict[str, List[str]]
