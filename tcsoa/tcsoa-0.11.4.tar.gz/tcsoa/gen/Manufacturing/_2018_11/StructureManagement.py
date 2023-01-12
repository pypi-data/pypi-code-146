from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RevisionRule
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PasteDuplicateInput(TcBaseObj):
    """
    A structure containing source BOMLine and target BOMLine as input for pasteDuplicateStructure operation.
    
    :var sourceLine: Source BOMLine to be cloned.
    :var targetLine: Target BOMLine under which the cloned source BOMLine is to be pasted
    """
    sourceLine: BusinessObject = None
    targetLine: BusinessObject = None


@dataclass
class PasteDuplicateStructureOutput(TcBaseObj):
    """
    A structure containing the target BOMLine, the new child BOMLine created under this target and the index of
    corresponding source BOMLine in the input.
    
    :var srcLineIndex: Index of the source BOMLine in the input data.
    :var targetLine: Target BOMLine under which the new cloned BOMLine is pasted.
    :var newChildLine: New BOMLine which is cloned from the source BOMLine and is pasted under the target BOMLine.
    """
    srcLineIndex: int = 0
    targetLine: BusinessObject = None
    newChildLine: BusinessObject = None


@dataclass
class PasteDuplicateStructureResponse(TcBaseObj):
    """
    Response for pasteDuplicateStructure operation.
    
    :var pasteDuplicateOutput: The target BOMLine, the new child BOMLine created under this target and the index of
    corresponding source BOMLine in the input.
    :var serviceData: Partial errors as part of the serviceData.
    """
    pasteDuplicateOutput: List[PasteDuplicateStructureOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CopyRecursivelyConfigurationInfo(TcBaseObj):
    """
    Structure containing configuration information.
    
    :var revisionRule: The RevisionRule with which the template BOMWindow is configured for cloning.
    :var variantRules: A list of variant rules to configure the BOMWindow for cloning. List can contain either
    StoredOptionSet or VariantRule. Both type of variant rules are not supported in the same list. If the list is empty
    all the SVRs created on the BOMWindow are carried over to the new BOMWindow.
    :var copySuppressedLines: If true, the  suppressed lines are carried to the cloned structure otherwise not.
    :var copyFutureEffectivities: If true, the furture effectivites are carried to the cloned structure otherwise not.
    :var additionalInfo: A generic structure to be used to capture additional information.
    """
    revisionRule: RevisionRule = None
    variantRules: List[BusinessObject] = ()
    copySuppressedLines: bool = False
    copyFutureEffectivities: bool = False
    additionalInfo: AdditionalInfo2 = None


@dataclass
class CopyRecursivelyInputInfo(TcBaseObj):
    """
    Holds information about the original structure to be cloned, BOMWindow configuration used to clone the structure
    and the information for the cloned structure.
    
    :var templateInfo: Structure with the information about the template and rule to be used for cloning.
    :var configurationInfo: Structure containing configuration information.
    :var newObjectInfo: Structure containing information about the cloned object.
    """
    templateInfo: CopyRecursivelyTemplateInfo = None
    configurationInfo: CopyRecursivelyConfigurationInfo = None
    newObjectInfo: CopyRecursivelyNewObjectInfo = None


@dataclass
class CopyRecursivelyNewObjectInfo(TcBaseObj):
    """
    Structure containing information about the cloned object.
    
    :var newName: The name of cloned BOMLine object.
    :var newDescription: The description of cloned object.
    :var newId: Id of cloned BOMLine object.
    :var newrevId: The revision id of cloned object.
    :var pasteTarget: The target BOMLine object under which the cloned object is created. If NULL, the cloned object is
    created as new root in a new BOMWindow object.
    :var additionalInfo: Any additional information.Reserved for future use.
    """
    newName: str = ''
    newDescription: str = ''
    newId: str = ''
    newrevId: str = ''
    pasteTarget: BusinessObject = None
    additionalInfo: AdditionalInfo2 = None


@dataclass
class CopyRecursivelyResponse(TcBaseObj):
    """
    The response is a structure containing the map of template object and the item revision of cloned object, a fms
    file ticket that captures logs.
    
    :var dataMap: A Map <BusinessObject, BusinessObject> contains the input object which has been cloned as key and the
    item revision of the cloned object as value.
    :var logFileTicket: The FMS ticket for the transient file that captures the log of cloning operation.
    :var serviceData: The standard service data.
    """
    dataMap: OriginalToCloneStructureMap = None
    logFileTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class CopyRecursivelyTemplateInfo(TcBaseObj):
    """
    Structure with the information about the template and rule to be used for cloning.
    
    :var objectToClone: The object to be cloned. The valid object types are: Mfg0BvrPart, Mfg0BvrWorkarea,
    Mfg0BvrProcess and Mfg0BvrOperation.
    :var cloningRule: The preference name holding the list of caluses to be  used for cloning.
    :var referenceWindow: BOMWindow  from where the objects are referred during cloning. If NULL, the objects are
    referred from the template BOMWindow.
    :var additionalInfo: Structure for additional information. Reserved for future use.
    """
    objectToClone: BusinessObject = None
    cloningRule: str = ''
    referenceWindow: List[BusinessObject] = ()
    additionalInfo: AdditionalInfo2 = None


@dataclass
class AdditionalInfo2(TcBaseObj):
    """
    A structure containg the maps to capture the additional information.
    
    :var strToDateVectorMap: A map of string to list of dates.
    :var strToDoubleVectorMap: A map of string to list if doubles.
    :var strToStrVectorMap: A map of string to list if strings.
    :var strToObjVectorMap: A map of string to list of business object.
    :var strToIntVectorMap: A map of string to list of integers.
    """
    strToDateVectorMap: StringToDateVectorMap2 = None
    strToDoubleVectorMap: StringToDoubleVectorMap2 = None
    strToStrVectorMap: StringToStringVectorMap2 = None
    strToObjVectorMap: StringToObjectVectorMap2 = None
    strToIntVectorMap: StringToIntegerVectorMap2 = None


"""
A Map <BusinessObject, BusinessObject> contins the input object which has been cloned as key and the item revision of the cloned object as value.
"""
OriginalToCloneStructureMap = Dict[BusinessObject, BusinessObject]


"""
A map of string to list of dates.
"""
StringToDateVectorMap2 = Dict[str, List[datetime]]


"""
A map of string to list of doubles.
"""
StringToDoubleVectorMap2 = Dict[str, List[float]]


"""
A map of string to list of integers.
"""
StringToIntegerVectorMap2 = Dict[str, List[int]]


"""
A map of string to list of business objects.
"""
StringToObjectVectorMap2 = Dict[str, List[BusinessObject]]


"""
A map of string to list of strings.
"""
StringToStringVectorMap2 = Dict[str, List[str]]
