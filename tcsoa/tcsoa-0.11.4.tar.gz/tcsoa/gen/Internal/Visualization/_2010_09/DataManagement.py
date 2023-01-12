from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, ImanRelation, Dataset
from tcsoa.gen.Internal.Visualization._2008_06.DataManagement import NamedRefsInDataset, DatasetInfo, NamedRefUploadOrUpdateInfo
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindNodesInProductViewResultResponse(TcBaseObj):
    """
    Returns the nodes present in the product view.
    
    :var outputNodes: Nodes which are present in the product view out of the input node vector.The nodes can be either
    BOM line(s), BOP line(s) or an Item(s).
    :var serviceData: Standard service data to handle partial errors.
    """
    outputNodes: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class FindProductViewForNodesResult(TcBaseObj):
    """
    Hold the result of the search.
    
    :var productView: The product view which contains the nodes or set of the nodes which the user is searching for.
    :var nodesPresentInPv: This is the set of nodes out of the input nodes which are present in the product view.The
    nodes can be either BOM line(s), BOP line(s) or an Item(s).
    :var pvAttachedTo: The line(BOM or BOP) in the product or process structure to which the PV is attached.
    """
    productView: Dataset = None
    nodesPresentInPv: List[BusinessObject] = ()
    pvAttachedTo: BusinessObject = None


@dataclass
class FindProductViewForNodesResultRespose(TcBaseObj):
    """
    Contains the result and the errors of the product view search
    
    :var productViews: Returns the result of the search.
    :var serviceData: This is standard service data which contains the partial errors
    """
    productViews: List[FindProductViewForNodesResult] = ()
    serviceData: ServiceData = None


@dataclass
class GatherSnapshot3DInput(TcBaseObj):
    """
    Input structure for GatherSnapshot3DInput
    
    :var clientId: Client specified identifier to help keep track of the objects returned.
    :var bomLine: Object reference of the input BOMLine object.  Typically the top line object is specified, but caller
    can also include lines where Product Views may be attached depending on the filtering behavior desired.
    :var refType: GRM relation type to be followed from the specified bomline for finding the SnapShotViewData
    datasets.  The VisTopLevelRef refType should be specified for the topline to find all Product Views authored in
    this context.  The IMAN_3D_snap_shot relation should be specified along with a bomline where a Product View must be
    attached in order to filter by attachment location.
    """
    clientId: str = ''
    bomLine: BOMLine = None
    refType: RefType = None


@dataclass
class GatherSnapshot3DListOutputPreview(TcBaseObj):
    """
    A List of Snapshot3DPreview objects.
    
    :var snapshotList: A List of Snapshot3DPreview objects.
    """
    snapshotList: List[Snapshot3DOutput] = ()


@dataclass
class GatherSnapshot3DListResponse(TcBaseObj):
    """
    Response containing a map between BOMLine and 'Snapshot3DPreviewList' which provides the minimum information
    necessary to populate the gallery about the snapshots found.
    
    :var snapshot3DOutputMap: A map between 'BOMLineUid' string and 'GatherSnapshot3DListOutputPreview'.
    :var serviceData: Standard  ServiceData member.
    """
    snapshot3DOutputMap: GatherSnapshot3DListOutputMap = None
    serviceData: ServiceData = None


@dataclass
class NewSnapshot3DInput(TcBaseObj):
    """
    Input structure for the 'createSnapshot3D' operation that creates the Product View (SnapShotViewData) Dataset.
    
    :var clientId: Identifier that helps the client to track the objects returned.
    :var attachToBOMLine: 'BOMLineInput' object reference to attach the new Product View Dataset.
    :var datasetInfo: Object of 'DatasetInfo', containing Dataset creation info.
    :var visibleLinesList: A list of visible BOMLine objects.
    :var createStructureFile: True if structure PLMXML file is to be generated.
    :var namedRefFileUpdateInfoList: (Optional) List of 'nameRefFiles' to be attached to Product View Dataset at the
    time of creation.  (named references in the Dataset).
    """
    clientId: str = ''
    attachToBOMLine: BOMLine = None
    datasetInfo: DatasetInfo = None
    visibleLinesList: List[BOMLine] = ()
    createStructureFile: bool = False
    namedRefFileUpdateInfoList: List[NamedRefUploadOrUpdateInfo] = ()


@dataclass
class SearchCriteria(TcBaseObj):
    """
    This contains all the required inputs for the product search
    
    :var searchScope: Scope lines within which the search will be performed. The scope lines can be either BOM or BOP
    lines.
    :var nodesToSearch: A list of nodes for which user is interested to find in the product views which are associated
    with the search scope. The scope lines can be either BOM lines , BOP lines ot Items.
    :var nodeCombination: Allows the user to specify the combination of node for the search. Currently only two value
    are upported : OR and AND. If the value is OR,  the use wants to find the PVs which include any of the node from
    the above node list. If it is AND, the user is intended to find the PVs which include all the nodes from the above
    list.If the user has not provided any input, the nodeCombination parameter value will be OR.
    """
    searchScope: List[BusinessObject] = ()
    nodesToSearch: List[BusinessObject] = ()
    nodeCombination: str = ''


@dataclass
class Snapshot3DInfoInput(TcBaseObj):
    """
    Input structure for getting SnapShotViewData Dataset info.
    
    :var clientId: Identifier for client data.
    :var snapshot3DDataset: Tag of the input SnapShotViewData Dataset.
    :var getStaticFilesInfo: If true, it will return the static information of this Product View.  This may not be
    available if a static representation of the Product View was not saved, or the data model does not support it.
    """
    clientId: str = ''
    snapshot3DDataset: Dataset = None
    getStaticFilesInfo: bool = False


@dataclass
class Snapshot3DInfoOutput(TcBaseObj):
    """
    Output structure for the info contained in the Snapshot 3D.
    
    :var namedRefFileInfoList: List of file info named referenced by the SnapShotViewData.
    :var relObjList: List of objects related to SnapShotViewData via GRM.
    :var snapshot3DVisibleLines: List of visible lines in the Product View.
    """
    namedRefFileInfoList: List[NamedRefsInDataset] = ()
    relObjList: List[Snapshot3DRelObjInfo] = ()
    snapshot3DVisibleLines: Snapshot3DVisibleLines = None


@dataclass
class Snapshot3DInfoResponse(TcBaseObj):
    """
    Return structure for 'Snapshot3DInfo'.
    
    :var snapshot3DInfoMap: A map containing client ids and output structure as key/value pairs. The keys corresponding
    to the clientId specified in the 'Snapshot3DInfoInput'. The values are a struct of 'Snapshot3DInfoOutput' data.
    :var serviceData: Standard 'ServiceData' member.
    """
    snapshot3DInfoMap: Snapshot3DInfoOutputMap = None
    serviceData: ServiceData = None


@dataclass
class Snapshot3DOutput(TcBaseObj):
    """
    Output structure for the info contained in the snapshot3D dataset.
    
    :var snapshot3DDataset: The Snapshot3D dataset object gathered.
    :var namedRefFileInfoList: Named References in dataset; only thumbnail file and preview file named references will
    be returned in case of gatherSnapshot3DList SOA call.
    """
    snapshot3DDataset: Dataset = None
    namedRefFileInfoList: List[NamedRefsInDataset] = ()


@dataclass
class Snapshot3DRelObjInfo(TcBaseObj):
    """
    List of objects related to SnapShotViewData via GRM.
    
    :var relType: The relationship type namedRef or GRM.
    :var relObj: Object Reference attached to the Dataset.
    :var relation: GRM relation on the attached Dataset such as VISTopLevelRef or IMAN_3D_snap_shot. For namedRef, it
    is RootContext.
    """
    relType: RelType = None
    relObj: BusinessObject = None
    relation: ImanRelation = None


@dataclass
class Snapshot3DStructureFilesInput(TcBaseObj):
    """
    Input Structure for updating the PLMXML structure file.
    
    :var clientId: Identifier for client data
    :var snapshot3DDataset: SnapshotDataset3D Dataset for which strucuture file to be updated.
    :var visibleLinesList: The list of visible BOMLine objects.  The ConfigurationContext object will be updated if
    needed.
    """
    clientId: str = ''
    snapshot3DDataset: Dataset = None
    visibleLinesList: List[BOMLine] = ()


@dataclass
class Snapshot3DUpdateInput(TcBaseObj):
    """
    Input structure for updating the SnapShotViewData Dataset.
    
    :var clientId: A unique ID used to help the client keep track of the SnapShotViewData Datasets in the output when
    using the call in batch mode when multiple Datasets are submitted at once.  If more than one Dataset tag is used,
    it is important to use unique 'clientId' strings in the input since they are used as keys in the return output map.
     If the same 'clientId' string is used, information will be lost.
    :var snapshot3DDataset: Tag of the  SnapShotViewData Dataset to be updated.
    :var attachToBOMLine: 'BOMLineInput' object reference that controls where (to which ItemRevision) the updated
    SnapShotViewData Dataset is attached.  If not specified the update operation will attach the Dataset to the same
    place the previous Dataset was attached.
    :var createStructureFile: A Boolean used to control whether or not a new structure PLMXML file is exported.  True
    to generate updated PLMXML, False if not.  If PLMXML is already in the original Dataset, it will be removed if
    there are visible lines sent with this call.
    :var updateVisibleLinesList: Set to True to force the Visible Lines to get updated.  This allows the special case
    where a snapshot is updated with no visible lines.
    :var visibleLinesList: Used if 'updateVisibleLinesList' is set to True.  Results in reexport of the structure
    PLMXML and update of it in Dataset if 'createStructureFile' is true.  If 'createStructureFile' is false, the old
    PLMXML will still be removed.  The ConfigurationContext object will be updated if needed.
    :var namedRefFileInfoList: List of 'FileInfo' for named referenced by 'snapshot3D'.  All the old named ref files
    will be removed, and completely replaced with these which may result in fewer named ref files.  If the old named
    ref should be kept (e.g. an old image preview that was not regenerated) it must be passed in this list.
    """
    clientId: str = ''
    snapshot3DDataset: Dataset = None
    attachToBOMLine: BOMLine = None
    createStructureFile: bool = False
    updateVisibleLinesList: bool = False
    visibleLinesList: List[BOMLine] = ()
    namedRefFileInfoList: List[NamedRefUploadOrUpdateInfo] = ()


@dataclass
class Snapshot3DUpdateResponse(TcBaseObj):
    """
    Object containing list of Snapshot3DInfo objects of updated Product View Dataset.
    
    :var snapshot3DUpdateOutputMap: A map between 'clientIds' and  'Snapshot3DUpdateOutput'.
    :var serviceData: Standard service data member.
    """
    snapshot3DUpdateOutputMap: Snapshot3DUpdateOutputMap = None
    serviceData: ServiceData = None


@dataclass
class Snapshot3DUpdateStructureFilesResponse(TcBaseObj):
    """
    SOA Response containing the map between 'clientids' and SnapshotDataset3D Datasets.
    
    :var snapshot3DStrFilesOutputMap: A map between 'clientIds' and SnapshotDataset3D Datasets.
    :var serviceData: Standard  ServiceData member.
    """
    snapshot3DStrFilesOutputMap: Snapshot3DUpdateStructureFilesOutputMap = None
    serviceData: ServiceData = None


@dataclass
class Snapshot3DVisibleLines(TcBaseObj):
    """
    List of visible lines in the Product View.
    
    :var uidType: Type of the return uid string list.
    :var visibleLinesMap: Map of visible BOMLines.  The key is the 'parentRef' from another 'VisibleLine' struct.
    :var relDatasetInfoMap: This will hold the Dataset info related to the visible lines. The 'relDatasetRef' string in
    the VisibleLine references the keys in this map.
    """
    uidType: UIDType = None
    visibleLinesMap: Snapshot3DVisibleLinesMap = None
    relDatasetInfoMap: Snapshot3DRelDatasetInfoMap = None


@dataclass
class StaticFileInfo(TcBaseObj):
    """
    Structure to hold the file info from the static capture of the snapshot.
    
    :var datasetUID: Direct Model dataset UID for the visible line
    :var imanFileUID: Iman file UID.  If there are multiple files in the dataset, return the first one.
    :var originalFileName: Full file name plus extensions.
    """
    datasetUID: str = ''
    imanFileUID: str = ''
    originalFileName: str = ''


@dataclass
class VisibleLine(TcBaseObj):
    """
    Structure to hold the unique data about the Visible BOMLine.
    
    :var uidString: UID string of the Visible BOMLines, its type is specified by 'uidType'.
    :var relDatasetRef: This is a string mapping to a related Dataset if not empty. Use the string as a key to the
    'relDatasetInfo' member in 'Snapshot3DVisibleLines' structure.
    :var parentRef: This is the ID of the parentRef.
    """
    uidString: str = ''
    relDatasetRef: str = ''
    parentRef: str = ''


@dataclass
class CreateSnapshot3DResponse(TcBaseObj):
    """
    Response structure returned by the 'CreateSnapshot3D' operation that consists primarily of a mapping between
    Dataset UIDs and client IDs. Also contains error information in the 'serviceData'.
    
    :var snapshot3DOutputMap: A map containing client_id (std::string) and Product View Dataset (std::string) output
    structure as key/value pairs.
    :var serviceData: Standard ServiceData member.
    """
    snapshot3DOutputMap: CreateSnapshot3DOutputMap = None
    serviceData: ServiceData = None


class RefType(Enum):
    """
    GRM relation type to be followed to gether 3D snapshot datasets.
    Ref_Snapshot3d = IMAN_3D_snap_shot
    Ref_VisTopLevel = VISTopLevelRef
    """
    Ref_Snapshot3d = 'Ref_Snapshot3d'
    Ref_VisTopLevel = 'Ref_VisTopLevel'


class RelType(Enum):
    """
    The relationship type namedRef or GRM.
    """
    TYPE_NamedRef = 'TYPE_NamedRef'
    TYPE_GRM = 'TYPE_GRM'


class UIDType(Enum):
    """
    Type of the return uid string list.
    """
    TYPE_APN = 'TYPE_APN'
    TYPE_CS = 'TYPE_CS'


"""
A map between clientIds (std::string) and Snapshot3D Dataset as key/value pairs.
"""
CreateSnapshot3DOutputMap = Dict[str, Dataset]


"""
A map between BOMLineUid string and Snapshot3DPreviewList
"""
GatherSnapshot3DListOutputMap = Dict[str, GatherSnapshot3DListOutputPreview]


"""
A map containing client ids and output structure as key/value pairs. The keys corresponding to the clientId specified in the Snapshot3DInfoInput. The values are a struct of Snapshot3DInfoOutput data.
"""
Snapshot3DInfoOutputMap = Dict[str, Snapshot3DInfoOutput]


"""
This will hold the Dataset info related to the visible lines. The relDatasetRef string in the VisibleLine struct references the keys in this map.
"""
Snapshot3DRelDatasetInfoMap = Dict[str, StaticFileInfo]


"""
A map between clientIds and  Snapshot3DOutput.
"""
Snapshot3DUpdateOutputMap = Dict[str, Snapshot3DOutput]


"""
A map between clientIds and snapshot3D datasets
"""
Snapshot3DUpdateStructureFilesOutputMap = Dict[str, Dataset]


"""
Map of visible BOMLines.  The key is the parentRef from another VisibleLine struct.
"""
Snapshot3DVisibleLinesMap = Dict[str, VisibleLine]
