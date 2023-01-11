from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Core._2011_06.OperationDescriptor import DeepCopyData
from typing import Dict, List


@dataclass
class GetDeepCopyDataResponse(TcBaseObj):
    """
    getDeepCopyData Response
    
    :var deepCopyInfoMap: Map of the DeepCopy data
    :var serviceData: Creates a list of Datasets and creates the specified relation type between created Dataset and
    input container object.
    """
    deepCopyInfoMap: DeepCopyInfoMap2 = None
    serviceData: ServiceData = None


@dataclass
class DeepCopyDataInput(TcBaseObj):
    """
    Input structure for getDeepCopyData operation
    
    :var operation: This is the operation types such as SaveAs,Revise, etc.
    :var object: object reference to get the deepcopydata
    """
    operation: str = ''
    object: BusinessObject = None


"""
Map contains a list of <name, value> pairs ('BusinessObject, vector<DeepCopyData>').  For each pair, name is the business object and value holds deep copy data for the business object.
"""
DeepCopyInfoMap2 = Dict[BusinessObject, List[DeepCopyData]]
