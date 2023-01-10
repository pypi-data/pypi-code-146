from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject, Dataset
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Internal.StructureManagement._2013_05.StructureExpansionLite import ChildLineInfo


@dataclass
class ExpansionResponse2(TcBaseObj):
    """
    'ExpansionResponse2' contains a map with key as parent Fnd0BOMLineLite or BOMLine and values as 'ChildLineInfo'.
    Additionally it also contains 'DatasetInfo2', uids of undelivered Fnd0BOMLineLite or BOMLine objects and its
    parent. 
    
    :var parentChildInfo: Map with key as parent Fnd0BOMLineLite or BOMLine and values as 'ChildLineInfo'.
    :var datasetInfo: 'DatasetInfo2' contains name of GRM relation through which underlying object of Fnd0BOMLineLite
    or BOMLine is attached to Dataset, Dataset object and list of 'NamedRefInfo2'.
    :var parentUndeliveredChildrenUids: Parent BOMLine or Fnd0BOMLineLite and its children uids which are yet to be
    transferred to client.
    :var serviceData: The service data containing partial errors.
    """
    parentChildInfo: ParentLineToChildLineInfo2 = None
    datasetInfo: List[DatasetInfo2] = ()
    parentUndeliveredChildrenUids: ParentLineToChildrenLineUidValues = None
    serviceData: ServiceData = None


@dataclass
class NamedRefInfo2(TcBaseObj):
    """
    Contains details of named reference object of Dataset.
    
    :var name: Name of reference object in Dataset. For example, JTPART.
    :var type: The type of the named reference object.
    :var originalFileName: The 'original_file_name' attribute value of the file in case the named reference object is a
    file.
    :var object: Object reference corresponding to the named reference.
    :var fileTicket: FMS ticket used to retrieve the file in case.
    """
    name: str = ''
    type: str = ''
    originalFileName: str = ''
    object: BusinessObject = None
    fileTicket: str = ''


@dataclass
class DatasetInfo2(TcBaseObj):
    """
    'DatasetInfo2' describes GRM relation name through which Dataset is attached with underlying object of
    Fnd0BOMLineLite or BOMLine. It also contains 'NamedRefInfo2' for Dataset requested through
    'DatasetTypeAndNamedRefs'.
    
    :var relationName: Name of GRM relation through which underlying object of Fnd0BOMLineLite or BOMLine is related to
    Dataset object.
    :var dataset: Dataset attached to Fnd0BOMLineLite or BOMLine.
    :var namedRefInfo: Named reference objects details for Dataset.
    """
    relationName: str = ''
    dataset: Dataset = None
    namedRefInfo: List[NamedRefInfo2] = ()


"""
Map with key as Fnd0BOMLineLite or BOMLine and 'ChildLineInfo' as values.
"""
ParentLineToChildLineInfo2 = Dict[RuntimeBusinessObject, List[ChildLineInfo]]


"""
Map with key as Fnd0BOMLineLite or BOMLine and uids of the children lines as values.
"""
ParentLineToChildrenLineUidValues = Dict[RuntimeBusinessObject, List[str]]
