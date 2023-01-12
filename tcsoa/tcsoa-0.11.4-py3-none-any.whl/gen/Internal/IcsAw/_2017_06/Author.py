from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ClassificationObject(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var clsObject: The Classification object. If this is NULLTAG; a new classification object will be created
    otherwise existing classification object represented by clsObject will be updated.
    :var workspaceObject: The WorkspaceObject (WSO) that is associated by this Classification object. If this is
    NULLTAG, then a standalone classification object is created or updated. Allowed WSO types will be defined by the
    preference 'ICS_allowable_types'.
    :var properties: List of properties containing attribute Ids and their values.
    """
    clsObject: BusinessObject = None
    workspaceObject: WorkspaceObject = None
    properties: List[ClassificationProperty] = ()


@dataclass
class ClassificationProperty(TcBaseObj):
    """
    Structure representing Classification Property which holds attribute ids and their values.
    
    :var attributeId: The unique identifier of classification attribute or internal identifier for classification
    header properties like class Id, unit system etc.
    :var values: A list of values for this attribute in the context of a Classification object.
    For regular properties it's just one value. In case of VLA (variable length array) properties each value has its
    own entry.
    """
    attributeId: int = 0
    values: List[str] = ()


@dataclass
class CreateOrUpdateClsObjectsResponse(TcBaseObj):
    """
    Holds the classification objects returned by the createOrUpdateClassificationObjects operation.
    
    :var clsObjects: A list of created or updated Classification objects.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    clsObjects: List[ClassificationObject] = ()
    serviceData: ServiceData = None
