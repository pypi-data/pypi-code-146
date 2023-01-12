from __future__ import annotations

from tcsoa.gen.Classification._2007_01.Classification import ClassificationProperty
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class SaveClassificationObjectsResponse(TcBaseObj):
    """
    Holds the classification objects returned by the saveClassificationObjects operation.
    
    :var clsObjs: A list of created or updated Classification objects.
    :var data: Any failures will be returned in the service data list of partial errors.
    """
    clsObjs: List[ClassificationObjectInfo] = ()
    data: ServiceData = None


@dataclass
class ClassificationObjectInfo(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var clsObjUid: UID of Classification object.
    :var instanceId: Alphanumeric ID of the Classification object.
    :var classId: Unique Alphanumeric ID of the Classification class where this object was created.
    :var unitBase: Unit system of measure in which the Classification object is stored in.
    :var wsoId: Reference of the WorkspaceObject (WSO) that is associated by this Classification object. This can be
    empty.
    :var properties: Array of Classification attributes references that store the properties of this Classification
    object.
    :var relationUid: UID of IMAN_classification relation.
    :var lastModDate: Last modified date of the Classified WorkspaceObject.
    """
    clsObjUid: str = ''
    instanceId: str = ''
    classId: str = ''
    unitBase: UnitSystem = None
    wsoId: WorkspaceObject = None
    properties: List[ClassificationProperty] = ()
    relationUid: str = ''
    lastModDate: str = ''


class UnitSystem(Enum):
    """
    US_UNSPECIFIED: Both or no unit system of measure.
    US_METRIC: Metric unit system of measure.
    US_NON_METRIC: Non-metric unit system of measure.
    """
    US_UNSPECIFIED = 'US_UNSPECIFIED'
    US_METRIC = 'US_METRIC'
    US_NON_METRIC = 'US_NON_METRIC'
