from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Visualization._2008_06.DataManagement import DatasetInfo, NamedRefUploadOrUpdateInfo
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class NewSnapshot3DInput(TcBaseObj):
    """
    New input structure for creating SnapShotViewData dataset, where user can specify relation to be used and generic
    objects are used.
    
    :var clientId: Identifier that helps the client to track the objects returned.
    :var attachToInfo: SnapShotViewData attachment information
    :var datasetInfo: Dataset creation information
    :var visibleLinesList: A list of visible objects
    :var createStructureFile: If true, a static structure file is created on the server. For legacy purposes only.
    :var variantName: Variant information. It can be empty.
    :var namedRefFileUpdateInfoList: List of named reference files to be attached to SnapShotViewData dataset at time
    of creation.
    """
    clientId: str = ''
    attachToInfo: Snapshot3DAttachToInfo = None
    datasetInfo: DatasetInfo = None
    visibleLinesList: List[BusinessObject] = ()
    createStructureFile: bool = False
    variantName: str = ''
    namedRefFileUpdateInfoList: List[NamedRefUploadOrUpdateInfo] = ()


@dataclass
class Snapshot3DAttachToInfo(TcBaseObj):
    """
    Object and relation attachment information.
    
    :var attachToObject: BusinessObject input object to which SnapShotViewData dataset is to be attached to. Currently
    only ItemRevision objects are supported. 
    :var relationName: Relation name for attaching SnapShotViewData dataset
    """
    attachToObject: BusinessObject = None
    relationName: str = ''
