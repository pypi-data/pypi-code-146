from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ImanFile, BusinessObject, Dataset, BOMWindow
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FlaggedCell(TcBaseObj):
    """
    The cellids for which the occurrence information has to be determined and criteria applied.
    
    :var iCellId: The id of the spatial cell that need to be rendered.
    :var iBitMask: The bits represented by the integer indicates the position of the cursor in the
    'SpatialHierCellInfo::vCursorOptions' vector.  For example value 0x0003 indicates the first and second cursors
    should be enabled for this cell.
    If a cursor with empty search scope is enabled for a cell then all occurrences in the cell are configured.
    Otherwise the cell is configured only if it is within the scope of the cursors that are enabled for this cell.
    """
    iCellId: int = 0
    iBitMask: int = 0


@dataclass
class GetNodeBBoxIn(TcBaseObj):
    """
    The input structure that specifies the node object information for which bbox information is to be retrieved.
    
    :var sSpatialHierDataset: The UID of the spatial hierarchy dataset based on which the assembly is rendered using
    MMV technology.
    :var vPathObjs: The list of assembly nodes represented as occurrence thread paths for which the Bounding box
    extents need to be fetched.
    """
    sSpatialHierDataset: str = ''
    vPathObjs: List[OccurrenceThreadPath] = ()


@dataclass
class GetNodeBBoxResponse(TcBaseObj):
    """
    The response structure containing the Bounding Box extents for the supplied input nodes.
    
    :var vNodeBBox: A list of node bounding boxes that is parallel to the input node array. If any input assembly node
    is invalid or does not have a valid bounding box associated with it then its returned 'NodeBBox' is empty.
    :var serviceData: The 'ServiceData' through which the errors are communicated to the client.
    """
    vNodeBBox: List[NodeBBox] = ()
    serviceData: ServiceData = None


@dataclass
class GetSpatialCellsReadTicketsResponse(TcBaseObj):
    """
    The response structure contains the file information of the Jt files in the cells, occurrence information
    (transform, BOMLine) and cell information to be able to map the input cell id and scope with the occurrence
    information.
    
    :var vSpatialFileInfos: Vector containing the required file information for all unique files associated with the
    input cells.
    :var vOccurrenceInfos: Vector of occurrence information associated with the input cells.
    :var vSpatialCellOccInfos: Vector containing the index offsets into 'vOccurrenceInfos' for the input cells. This
    helps to map the input cell with its associated occurrence information and file information.
    :var serviceData: The 'ServiceData' through which the errors are communicated to the client.
    """
    vSpatialFileInfos: List[SpatialFileInfo] = ()
    vOccurrenceInfos: List[SpatialOccurrence] = ()
    vSpatialCellOccInfos: List[SpatialCellOccInfo] = ()
    serviceData: ServiceData = None


@dataclass
class IsSpatialHierarchyIn(TcBaseObj):
    """
    The input structure contains a set of dataset versions on which the existence of latest version check is to be
    performed.
    
    :var vpSpatialHierDatasetUids: A list of Fnd0SpatialHierarchy dataset uids on which the existence of latest version
    is to be checked.
    """
    vpSpatialHierDatasetUids: List[str] = ()


@dataclass
class IsSpatialHierarchyLatestResponse(TcBaseObj):
    """
    The response structure containing the verdict on the availabilty of newer dataset versions for the input
    Fnd0SpatialHierarchy dataset versions.
    
    :var vbLatestVersionFlags: A list of boolean values parallel to the input 'vpSpatialHierDatasetUids' indicating if
    a newer version of the dataset is available or not.
    :var serviceData: The 'ServiceData' through which the errors are communicated to the client.
    """
    vbLatestVersionFlags: List[bool] = ()
    serviceData: ServiceData = None


@dataclass
class MmvCursorOptions(TcBaseObj):
    """
    The options to be applied on the cursor.
    
    :var pMmvCursor: Reference to the cursor object that contains the scope information.
    """
    pMmvCursor: BusinessObject = None


@dataclass
class NodeBBox(TcBaseObj):
    """
    The bbox description for a node.
    
    :var vdBBox: An array of bounding boxes, in the form of xmin ymin zmin xmax ymax zmax. Multiple boxes can be
    returned for a path. The array length is always a product of number of boxes and 6.
    """
    vdBBox: List[float] = ()


@dataclass
class OccurrenceThreadPath(TcBaseObj):
    """
    Strcuture to hold the occurrence thread path chains.
    
    :var vsThreadUIDs: A list of of occurrence thread path chains. The 0th element pointing to the top thread.
    """
    vsThreadUIDs: List[str] = ()


@dataclass
class ReleaseSpatialHierarchyIn(TcBaseObj):
    """
    The input contains a set of Fnd0SpatialHierarchy dataset version uids for which the view locks are to be released.
    
    :var vsSpatialHierUids: The uids of the Fnd0SpatialHierarchy dataset versions for which the view locks are to be
    released.
    """
    vsSpatialHierUids: List[str] = ()


@dataclass
class SearchScope(TcBaseObj):
    """
    The SearchScope specifies the scope of a search.
    
    :var pBOMWindow: The BOMWindow context in which the occurrence thread path scope is specified.
    :var vsPathScopes: The list of occurrence thread paths that serve as scope qualifier.
    """
    pBOMWindow: BOMWindow = None
    vsPathScopes: List[OccurrenceThreadPath] = ()


@dataclass
class SpatialCellOccInfo(TcBaseObj):
    """
    The information regarding the file occupied in the given cell id.
    
    :var iCellId: The spatial cell id.
    :var viOccIdx: Index position of the spatial occurrences in 'vOccurrenceInfos' for the spatial cell id.
    """
    iCellId: int = 0
    viOccIdx: List[int] = ()


@dataclass
class SpatialFileInfo(TcBaseObj):
    """
    The information about the file contained in the spatial cell.
    
    :var sOrigFilename: The value of the original_file_name attribute on the Teamcenter file object.
    :var sFMSRTicket: The FMS  read ticket for the TcFile.
    :var pDataSet: The dataset to which the TcFile is associated. This is used if the client needs to refresh the file
    tickets.
    :var pTcFile: The pointer to the File. This is used if the client needs to refresh the file tickets.
    """
    sOrigFilename: str = ''
    sFMSRTicket: str = ''
    pDataSet: Dataset = None
    pTcFile: ImanFile = None


@dataclass
class SpatialHierCellInfo(TcBaseObj):
    """
    Structure containing the spatial hierarchy dataset and the cells in it for which theconfiguration, file
    information, read tickets are to be obtained.
    
    :var pBOMWindow: The BOMWindow of the structure that is currently being viewed.
    :var sSpatialHierDataset: The uid of the Fnd0SpatialHierarchy dataset version that is currently used for rendering.
    :var vCursorOptions: The cursor information for which the cells are to checked if they are within the its scope.
    :var vFlaggedCells: The information about the cell that need to be configured and the cursor
    information(represented as bits that index into 'vCursorOptions') for which the cells are checked for scope.
    """
    pBOMWindow: BOMWindow = None
    sSpatialHierDataset: str = ''
    vCursorOptions: List[MmvCursorOptions] = ()
    vFlaggedCells: List[FlaggedCell] = ()


@dataclass
class SpatialOccurrence(TcBaseObj):
    """
    Information about an occurrence row in the occurrence table.
    
    :var vdXForms: 16 doubles that represent the transform of this occurrence path in row major order.
    :var sOccPartKey: The uid of spatial cell index object in which the spatial occurrence is represented.
    :var occThreadPath: The occurrence thread chain of the configured occurrence.
    :var pBOMLine: The leaf BOMLine of the spatial occurrence.
    :var iFileIdx: Index position in 'vSpatialFileInfos' where file information can be found (used only if 'bHasFile'
    is true).
    :var iBitMask: The bit mask which represents the positions of cursors in 'vCursorOptions'. The spatial occurrence
    is within the scope of the cursors represented by this bit mask.
    :var bHasFile: Boolean information to indicate if the file information is returned for this spatial occurrence.
    :var sRefSetName: The reference set name as pointed by the note type UG REF SET, to be used by the viewer to decide
    which geometry to display.
    """
    vdXForms: List[float] = ()
    sOccPartKey: str = ''
    occThreadPath: OccurrenceThreadPath = None
    pBOMLine: BOMLine = None
    iFileIdx: int = 0
    iBitMask: int = 0
    bHasFile: bool = False
    sRefSetName: str = ''


@dataclass
class AcquireSpatialHierarchyIn(TcBaseObj):
    """
    The structure contains a set of  BomLines for which the latest version of the Fnd0SpatialHierarchy  dataset is to
    be acquired and locked for viewing.
    
    :var vpBOMLines: A list of BOMLines for which Fnd0SpatialHierarchy datasets are to be acquired and locked for
    viewing.
    """
    vpBOMLines: List[BOMLine] = ()


@dataclass
class AcquireSpatialHierarchyResponse(TcBaseObj):
    """
    The response structure contains the returned spatial hierarchy versions, the Fnd0SpatialTree named reference(*.mmv)
    file objects and its original file names and read tickets.  It also contains an index vector that maps the dataset
    array to the bomline array in the input structure.
    
    :var vpSpatialHierDatasets: A list of latest spatial hier dataset version acquired for the input bomlines.
    :var vpTcFiles: A list of file objects parallel to dataset version list.
    :var vsOrigFilenames: A list of file names parallel to dataset version list.
    :var vsFileTickets: A list of file tickets for the named reference (*.mmv file) parallel to dataset version list.
    :var viIndexVector: A list of indices parallel to the dataset version list to indicate the corresponding index in
    the input bomline array.
    :var serviceData: The 'ServiceData' through which the errors are communicated to the client.
    """
    vpSpatialHierDatasets: List[Dataset] = ()
    vpTcFiles: List[ImanFile] = ()
    vsOrigFilenames: List[str] = ()
    vsFileTickets: List[str] = ()
    viIndexVector: List[int] = ()
    serviceData: ServiceData = None


@dataclass
class CreateMmvCursorResponse(TcBaseObj):
    """
    The response structure containing a reference to the Fnd0MMVCursor object created.
    
    :var pMmvCursor: Cursor object that holds the current visibility scope.
    :var serviceData: The 'ServiceData' through which the errors are communicated to the client.
    """
    pMmvCursor: BusinessObject = None
    serviceData: ServiceData = None
