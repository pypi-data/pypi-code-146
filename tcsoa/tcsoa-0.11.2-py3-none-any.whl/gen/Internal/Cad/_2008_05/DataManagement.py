from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, CadAttrMappingDefinition
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class MappedDatasetAttrPropertyInfoForNX(TcBaseObj):
    """
    Contains the resolved attribute information.
    
    :var cadAttrMappingDefinition: 'CadAttributeMappingDefinition' object reference associated with the resolved
    property object.
    :var resolvedObject: Object reference of object holding mapped attribute value.
    :var resolvedPropertyName: The property name of the mapped object holding the attribute value of interest resulting
    from evaluation of a dataset CAD attribute mapping definition.
    """
    cadAttrMappingDefinition: CadAttrMappingDefinition = None
    resolvedObject: BusinessObject = None
    resolvedPropertyName: str = ''


@dataclass
class NxFrozenAndModifiableInfo(TcBaseObj):
    """
    Contains additional NX-specific information about the "frozen" and "modifiable" values of the resolved attributes.
    
    :var isModifiable: Whether the mapped Teamcenter property is modifiable in the NX specific semantics.
    :var isFrozen: Whether the mapped Teamcenter property is frozen in the NX specific semantics.
    """
    isModifiable: bool = False
    isFrozen: bool = False


@dataclass
class NxResolvedConstOrPrefAttrInfo(TcBaseObj):
    """
    Contains additional NX specific information for attributes whose mapping definitions are of ATTRMAP_preference or
    ATTRMAP_constant type.
    
    
    :var isFrozen: Whether the mapped Teamcenter property is frozen in the NX specific semantics.
    :var value: mapped attr value.
    """
    isFrozen: bool = False
    value: str = ''


@dataclass
class ResolveAttrMappingsForNXResponse(TcBaseObj):
    """
    Contains the response for 'resolveAttrMappingsForNX'
    
    :var resolvedMappingsMap: This is a map containing the successfully mapped property information. The keys are the
    input 'clientIds' and the values are the output 'MappedNxDatasetAttrPropertyInfo' structures.
    :var frozenAndModifiableInfoMap: This is a map containing the NX specific frozen and modifiable value of
    successfully resolved attributes. The keys are the input 'clientIds' and the values are the output
    'NxFrozenAndModifiableInfo' structures.
    :var resolvedConstOrPrefAttrInfoMap: This is a map containing the NX specific frozen value and the resolved value
    for attributes whose mappinge definitions are of ATTRMAP_preference or ATTRMAP_constant type.
    The keys are the input 'clientIds' and the values are the output 'NxResolvedConstOrPrefAttrInfo' structures.
    :var serviceData: Service data contains all objects returned by the service. Also contains error messages. . If no
    entry is found in the returned maps then an error may have occurred. The client should look for it mapped to a
    Partial Error. Look for a Partial error with with an id of NX: + clientId for error occurs in NX specific
    processing. If none of the above exists, locate a Partial Error, this indicates that the processing of the dataset
    or the item revision (where the attribute belongs) failed. Iterate through the input indexes of the list of
    ResolveAttrMappingsInfo and look for index mapped to the Partial Errors of the Service Data.
    Error reported by this service :
    215119 No Dataset or Item Revision specified
    215074 Invalid Dataset
    215075 Invalid Item Revision
    215076 Invalid CadAttrMappingDefinitionInfo object
    215200 No clientId specified
    215201 Duplicate clientId specified
    """
    resolvedMappingsMap: ResolveAttrMappingsOutputMapForNX = None
    frozenAndModifiableInfoMap: NxFrozenAndModifiableInfoMap = None
    resolvedConstOrPrefAttrInfoMap: NxResolvedConstOrPrefAttrInfoMap = None
    serviceData: ServiceData = None


"""
Map of string client ids to 'NxFrozenAndModifiableInfo' values (string, 'NxFrozenAndModifiableInfo').
"""
NxFrozenAndModifiableInfoMap = Dict[str, NxFrozenAndModifiableInfo]


"""
Map of string client ids to 'NxResolvedConstOrPrefAttrInfo' values (string, 'NxResolvedConstOrPrefAttrInfo').
"""
NxResolvedConstOrPrefAttrInfoMap = Dict[str, NxResolvedConstOrPrefAttrInfo]


"""
Map of string client ids to 'MappedDatasetAttrPropertyInfoForNX' values (string, 'MappedDatasetAttrPropertyInfoForNX').
"""
ResolveAttrMappingsOutputMapForNX = Dict[str, MappedDatasetAttrPropertyInfoForNX]
