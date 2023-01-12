from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile, PSBOMViewRevision, Fnd0BOMLineLite, Dataset, BOMWindow
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ArrAbsOccDataOverride(TcBaseObj):
    """
    The data structure contains occurrence override data for an arrangement&rsquo;s occurrence. If there are no
    overrides for the occurrence (possible in the case of a base arrangement), the override type is 0. 
    There can be only one transform override on an occurrence per arrangement, and only one suppression override. If
    the occurrence is a subassembly, there may also be at most one used arrangement identified.
    For a base arrangement, there may be multiple transform overrides and there may be multiple geometry (jt) overrides.
    
    :var occurrenceThreadPath: A list of occurrence thread UID strings representing the occurrence path. Beginning with
    the specified occurrence up to the occurrence immediately under the context PSBOMViewRevision (i.e. the input
    PSBOMViewRevision.)
    :var overrideTypes: The type of data held in the structure. Values as a bitmask: 0=No override, 1=Transform,
    2=Suppression, 4=Arrangement, 8=JT. For example, if there is both a transform and suppression override, the type
    value is 3.
    :var absTransform: Transformation (positioning) override data of the PSOccurrence.
    Transformation data is provided in a matrix in eXT format of
    { R00 R10 R20 P0 R01 R11 R21 P1 R02 R12 R22 P2 T0 T1 T2 S }
    where the components of this matrix are:
    A general rotation submatrix, comprising
       x-axis (R00, R01, R02),
       y-axis (R10, R11, R12),
       z-axis (R20, R21, R22).
    A perspective (P0, P1, P2).
    A translation (T0, T1, T2).
    A scaling factor (S).
    :var suppression: The occurrence suppression setting, in the context of the arrangement.
    If true, the occurrence is not displayed.
    :var usedArrangement: Identifier for an arrangement used by a child subassembly.
    :var jtOverride: The geometry (jt) data override in context of the input PSBOMViewRevision.
    """
    occurrenceThreadPath: List[str] = ()
    overrideTypes: int = 0
    absTransform: List[float] = ()
    suppression: bool = False
    usedArrangement: ArrangementID = None
    jtOverride: ArrJtOverride = None


@dataclass
class ArrJtOverride(TcBaseObj):
    """
    The data structure contains information about the absolute occurrence override of geometry (jt) data.
    
    :var jtDataset: The dataset object reference of the geometry (jt) information.
    :var jtFile: The file object reference of the geometry (jt) information
    :var jtFileName: Original filename.
    :var fileTicket: FMS ticket to use in file upload.
    """
    jtDataset: Dataset = None
    jtFile: ImanFile = None
    jtFileName: str = ''
    fileTicket: str = ''


@dataclass
class ArrOccurrenceData(TcBaseObj):
    """
    The data structure contains occurrence and override data for an occurrence of the arrangement. The relative
    transformation information is only provided for base arrangements. In a base arrangement, the override data is not
    in context of any "named" arrangement.
    
    :var occurrenceThread: The occurrence thread UID string.
    :var occTransform: Transformation (positioning) override data of the PSOccurrence. 
    Transformation data is provided in a matrix in eXT format of
    { R00 R10 R20 P0 R01 R11 R21 P1 R02 R12 R22 P2 T0 T1 T2 S }
    where the components of this matrix are:
    A general rotation submatrix, comprising
       x-axis (R00, R01, R02),
       y-axis (R10, R11, R12),
       z-axis (R20, R21, R22).
    A perspective (P0, P1, P2).
    A translation (T0, T1, T2).
    A scaling factor (S).
    :var absOccOverrides: List of override data from the AbsOccData for an absolute occurrence.
    """
    occurrenceThread: str = ''
    occTransform: List[float] = ()
    absOccOverrides: List[ArrAbsOccDataOverride] = ()


@dataclass
class ArrangementData(TcBaseObj):
    """
    The data structure contains data of the "base" arrangement or of a single AssemblyArrangement, for a specified
    product structure.  For a base arrangement, the arrangement ID is empty, and the occurrence data list contains
    elements for each immediate child of the product structure.
    
    :var arrangeType: The type of arrangement. Supported values are: 0=Base, 1=Default, 2=As_Saved, and 3=Named.
    :var arrangeID: Data to uniquely identify an AssemblyArrangement of the structure.
    :var occData: List of occurrence and override information for each occurrence in an arrangement.
    """
    arrangeType: int = 0
    arrangeID: ArrangementID = None
    occData: List[ArrOccurrenceData] = ()


@dataclass
class ArrangementID(TcBaseObj):
    """
    The data structure contains information to uniquely identify an arrangement of a structure.
    
    :var arrangeName: Name of AssemblyArrangement. (May be empty.)
    :var arrangeSubfileid: External UID of AssemblyArrangement.
    """
    arrangeName: str = ''
    arrangeSubfileid: str = ''


@dataclass
class GetProductStructureArrangementsResp(TcBaseObj):
    """
    The data structure contains output corresponding to the input list of product structures 
    (identified by PSBOMViewRevisions or Fnd0BOMLineLite lines), along with the ServiceData of the operation.
    
    :var arrOutput: List of ProductStructureArrOutput objects.
    :var serviceData: Contains PartialErrors.
    """
    arrOutput: List[ProductStructureArrOutput] = ()
    serviceData: ServiceData = None


@dataclass
class LWBStructureInput(TcBaseObj):
    """
    Identifies the structures for which to return arrangement data, in the LWB (Light Weight BOM) scenario.
    
    :var lwbWindow: Window in which the product structure is expanded
    :var lwbLines: List of lines contained in lwbWindow from which to obtain arrangement data.
    """
    lwbWindow: BOMWindow = None
    lwbLines: List[Fnd0BOMLineLite] = ()


@dataclass
class ProductStructureArrOutput(TcBaseObj):
    """
    The data structure contains arrangement data for the specified product structures.
    
    :var psArrOutput: List of arrangement data from all the structures&rsquo; arrangements.
    """
    psArrOutput: List[ProductStructureArrangementsOutput] = ()


@dataclass
class ProductStructureArrangementInput(TcBaseObj):
    """
    Identifies the product structures for which to return arrangement data. The expected input is either a list of
    specific PSBOMViewRevisions; or a BOMWindow and list of corresponding Fnd0BOMLineLite lines.
    
    :var bvrs: List of PSBOMViewRevisions from which to obtain arrangement data.
    :var lwbStructures: Identifies the product structures from which to return arrangement data.
    """
    bvrs: List[PSBOMViewRevision] = ()
    lwbStructures: LWBStructureInput = None


@dataclass
class ProductStructureArrangementsOutput(TcBaseObj):
    """
    The data structure contains arrangement data for the specified product structure, identified by either bvr or line.
    The base arrangement is the first element in the arrangement list.
    
    :var bvr: The PSBOMViewRevision to which the arrangement data belongs, it is the "parent context".
    :var line: The Fnd0BOMLineLite line to which the arrangement data belongs, it is the "parent context".
    :var arrangeData: List of arrangement data from each of the structure&rsquo;s arrangements.
    """
    bvr: PSBOMViewRevision = None
    line: Fnd0BOMLineLite = None
    arrangeData: List[ArrangementData] = ()
