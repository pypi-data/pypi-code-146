from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DeepCopyData(TcBaseObj):
    """
    Holds the relavent information regarding applicable deep copy rules.
    
    :var otherSideObjectTag: This is a tag representing object on which the deep copy action need to be performed.
    :var relationTypeName: This is a string representing the name the relation that need to be deep copied.
    :var newName: This is a string representing the new name for the new copy of the object represented by
    'otherSideObjectTag'. The value for the 'newName' will be 'NULL' if the 'action' is not 'CopyAsObject' or
    'ReviseAndRelateToLatest'.
    :var action: This is an integer representing the action to be performed on the object represented by
    'otherSideObjectTag'. The values for action are: 'CopyAsObjectType = 0, CopyAsRefType = 1, DontCopyType =2,
    RelateToLatest = 3, ReviseAndRelateToLatest = 4'.
    :var isTargetPrimary: Boolean representing whether the given item revision is a primary object in the relation that
    need to be deep copied.
    :var isRequired: Boolean representing whether the deep information is from a mandatory deep copy rule configured by
    the administrator or not.
    :var copyRelations: Boolean representing whether the Properties on  the Relation if any in the Relation that exists
    between the Primary and the Secondary should be carried forward or not.
    """
    otherSideObjectTag: BusinessObject = None
    relationTypeName: str = ''
    newName: str = ''
    action: int = 0
    isTargetPrimary: bool = False
    isRequired: bool = False
    copyRelations: bool = False


@dataclass
class DeepCopyInfoKey(TcBaseObj):
    """
    Holds the ItemRevision object tag ('itemRevisionTag') and the operation name for which the deep copy information
    should be obtained.
    
    :var itemRevisionTag: The ItemRevision object on which the operation is being performed.
    :var operation: The string representing the operation name (i.e., 'Revise' or 'SaveAs' ).
    """
    itemRevisionTag: ItemRevision = None
    operation: str = ''


@dataclass
class DeepCopyInfoKeyValue(TcBaseObj):
    """
    Store key and value pair for DeepCopyData.
    
    :var key: Structure representing the key for the Deep Copy Info.
    :var deepCopyInfos: The resultant 'deepCopyInfo' values are returned as a list.
    """
    key: DeepCopyInfoKey = None
    deepCopyInfos: List[DeepCopyData] = ()


@dataclass
class DeepCopyInfoResponse(TcBaseObj):
    """
    Holds the response for the 'getDeepCopyInfo' method.
    
    :var values: The resultant 'deepCopyInfo' values are returned as a list.
    :var serviceData: Contains the status of the operation. This operation does not return any error code but
    propagates the error code from lower level functions.
    """
    values: List[DeepCopyInfoKeyValue] = ()
    serviceData: ServiceData = None
