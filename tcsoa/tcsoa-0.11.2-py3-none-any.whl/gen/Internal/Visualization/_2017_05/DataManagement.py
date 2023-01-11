from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanRelation, Dataset
from typing import Dict, List
from tcsoa.gen.Internal.Visualization._2008_06.DataManagement import NamedRefsInDataset
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class Snapshot3DInfoInput2(TcBaseObj):
    """
    Input structure for getting SnapShotViewData Dataset info.
    
    :var clientId: Identifier for client data.
    :var snapshot3DDataset: Object of the input SnapShotViewData Dataset.
    :var getStaticFilesInfo: If true, it will return the static information of this Product View. This may not be
    available if a static representation of the Product View was not saved, or the data model does not support it.
    """
    clientId: str = ''
    snapshot3DDataset: Dataset = None
    getStaticFilesInfo: bool = False


@dataclass
class Snapshot3DInfoOutput2(TcBaseObj):
    """
    Output structure for the info contained in the Product View.
    
    :var namedRefFileInfoList: A list of file info named referenced by the SnapShotViewData Dataset.
    :var relObjList: A list of objects related to SnapShotViewData Dataset via GRM.
    :var snapshot3DVisibleLines: A list of visible lines in the Product View.
    """
    namedRefFileInfoList: List[NamedRefsInDataset] = ()
    relObjList: List[Snapshot3DRelObjInfo2] = ()
    snapshot3DVisibleLines: Snapshot3DVisibleLines2 = None


@dataclass
class Snapshot3DInfoResponse2(TcBaseObj):
    """
    Return structure for Snapshot3DInfo.
    
    :var snapshot3DInfoMap: A map (string, Snapshot3DInfoOutput2) containing client IDs and output structure as
    key/value pairs. The keys corresponding to the clientId specified in the Snapshot3DInfoInput2 and the values are a
    structure of Snapshot3DInfoOutput2 data.
    :var serviceData: Standard ServiceData member
    """
    snapshot3DInfoMap: Snapshot3DInfoOutputMap2 = None
    serviceData: ServiceData = None


@dataclass
class Snapshot3DRelObjInfo2(TcBaseObj):
    """
    List of objects related to SnapShotViewData Dataset via GRM.
    
    :var relType: Currently two values are supported:  TYPE_NamedRef and TYPE_GRM.
    :var relObj: Object Reference attached to the Dataset.
    :var relation: GRM relation on the attached Dataset such as VISTopLevelRef or IMAN_3D_snap_shot. For namedRef, it
    is Root Context representing the top line of the structure that must be loaded in order to display the Product View.
    """
    relType: str = ''
    relObj: BusinessObject = None
    relation: ImanRelation = None


@dataclass
class Snapshot3DVisibleLines2(TcBaseObj):
    """
    List of visible lines in the Product View.
    
    :var uidType: This supports two values: TYPE_CS (cloneStable unique id chain string) and TYPE_APN ( absolute path
    node unique id string).
    :var visibleLinesMap: A map (string, VisibleLine2) of visible BOMLine objects. The key is the parentRef from
    another VisibleLine struct.
    :var relDatasetInfoMap: A map (string, StaticFileInfo2) of the Dataset info related to the visible lines. The
    relDatasetRef string in the VisibleLine references the keys in this map.
    """
    uidType: str = ''
    visibleLinesMap: Snapshot3DVisibleLinesMap2 = None
    relDatasetInfoMap: Snapshot3DRelDatasetInfoMap2 = None


@dataclass
class StaticFileInfo2(TcBaseObj):
    """
    Structure to hold the file info from the static capture of the snapshot.
    
    :var datasetUID: Direct Model dataset UID for the JT part file on the visible line.
    :var imanFileUID: The ImanFile UID for the JT part file on the visible line. If there are multiple files in the
    Dataset, the first one is returned.
    :var originalFileName: Full file name plus extensions.
    """
    datasetUID: str = ''
    imanFileUID: str = ''
    originalFileName: str = ''


@dataclass
class VisibleLine2(TcBaseObj):
    """
    Structure to hold the unique data about the Visible BOMLine.
    
    :var uidString: The UID string of the Visible BOMLine objects, its type is specified by uidType.
    :var relDatasetRef: This is a string mapping to a related Dataset if not empty. Use the string as a key to the
    relDatasetInfo member in Snapshot3DVisibleLines structure.
    :var parentRef: This is the reference ID of the parent visible line (parentRef).
    :var altKeyType: This represents the type of the altKeyValue. Currently the only supported type is TYPE_IDIC.
    :var altKeyValue: Currently the only supported value is "ID in TopLevel context" (IDIC). This value will be
    populated for visible lines.
    """
    uidString: str = ''
    relDatasetRef: str = ''
    parentRef: str = ''
    altKeyType: str = ''
    altKeyValue: str = ''


"""
A map (string, Snapshot3DInfoOutput2) containing client IDs and output structure as key/value pairs. The keys corresponding to the clientId specified in the Snapshot3DInfoInput2 and the values are a structure of Snapshot3DInfoOutput2 data.
"""
Snapshot3DInfoOutputMap2 = Dict[str, Snapshot3DInfoOutput2]


"""
A map (string, StaticFileInfo2) of the Dataset info related to the visible lines. The relDatasetRef string in the VisibleLine references the keys in this map.
"""
Snapshot3DRelDatasetInfoMap2 = Dict[str, StaticFileInfo2]


"""
A map (string, VisibleLine2) of visible BOMLine objects. The key is the parentRef from another VisibleLine struct.
"""
Snapshot3DVisibleLinesMap2 = Dict[str, VisibleLine2]
