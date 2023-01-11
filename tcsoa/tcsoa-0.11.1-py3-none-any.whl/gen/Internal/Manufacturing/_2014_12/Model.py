from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExternalNodeInfo(TcBaseObj):
    """
    This structure holds BOPLine objects along with their UI location and corresponding BOPLine objects connected via
    scope flows relationship.
    
    :var externalNode: The BOPLine object corresponding to absolute occurrence stored in Mfg0UILocationForm attached to
    the input BOPLine. The type of BOPLine objects can be Mfg0BvrOperation, Mfg0BvrProcess, Mfg0BvrProcessArea, and
    Mfg0BvrWorkarea.
    :var uiLocation: UI location of the BOPLine object. This is MEUILocation property of BOMLine persisted in the form
    attached to the contextLine. It is comma separated list of x-coordinate, y-coordinate, height and width
    representing externalNode position. e.g. "27, 24, 84, 43".
    :var connectedNodes: A list of BOPLine objects connected via scope flow relationship to the BOPLine object whose
    absolute occurrence is stored in the Mfg0UILocationForm attached to the input BOPLine. The type of BOPLine objects
    can be Mfg0BvrOperation, Mfg0BvrProcess, Mfg0BvrProcessArea, and Mfg0BvrWorkarea.
    """
    externalNode: BusinessObject = None
    uiLocation: str = ''
    connectedNodes: List[BusinessObject] = ()


@dataclass
class LABatchDetails(TcBaseObj):
    """
    Schedule timing information deciding when and how many times the operation is to be executed.
    
    :var identifier: Operation identifier string (Valid value: laAsyncResolve)
    :var mode: The mode in which the asynchronous operation is to be executed. Valid values are background, inprocess
    and blocking.
    :var site: The multisite site id on which the asynchronous operation is to be executed.
    :var priority: Priority of the asynchronous operation. Valid values 1(low) -3 (high).
    :var startTime: Start time of the asynchronous operation.
    :var endTime: End time of the asynchronous operation.
    :var daysOfWeek: A list of boolean values which represent each day of the week. The value is set to true for the
    days that you want the operation to be executed. The week starts on Sunday.
    :var endAfterOccurrences: Stop executing the operation after these many executions Valid values are positvie
    integers, a value of 0 indicates no repetition.
    :var primaryObjects: List of Teamcenter objects taking part in the asynchronous operation.  These objects are
    required by the dispatcher service to show in the user interface and also for post operation handling.
    :var secondaryObjects: List of Teamcenter objects taking part in the asynchronous operation.  These objects are
    required by the dispatcher service to show in the user interface and also for post operation handling.
    """
    identifier: str = ''
    mode: str = ''
    site: int = 0
    priority: int = 0
    startTime: datetime = None
    endTime: datetime = None
    daysOfWeek: List[bool] = ()
    endAfterOccurrences: int = 0
    primaryObjects: List[BusinessObject] = ()
    secondaryObjects: List[BusinessObject] = ()


@dataclass
class LAResolveAsyncData(TcBaseObj):
    """
    This data structure contains the scope for which the logical assignments are to be resolved, the products to
    resolve them and also whether to resolve them recursively. All the parameters are mandatory.
    
    :var scopeLines: Process(es) and/or Operation(s) of type Mfg0BvrProcess and Mfg0BvrOperation respectively. These
    lines are from Enterprise Bill of Process (EBOP) stucture for which logical assignments are to be resolved.
    :var products: Products to use for resolving the logical assignments. Top BOMLine(s) of product structure(s).
    :var resolveRecursively: If true, the scopeLines are resolved recursively i.e their children are resolved and so on.
    """
    scopeLines: List[BusinessObject] = ()
    products: List[BusinessObject] = ()
    resolveRecursively: bool = False


@dataclass
class ScopeFlowInfo(TcBaseObj):
    """
    This structure holds the predecessor and the successor BOPLine object of Mfg0BvrScopeFlow object to be deleted.
    
    
    :var predecessor: The predecessor BOPLine of the Mfg0BvrScopeFlow object.
    :var successor: The successor BOPLine of the Mfg0BvrScopeFlow object.
    """
    predecessor: BusinessObject = None
    successor: BusinessObject = None


@dataclass
class UILocationInfo(TcBaseObj):
    """
    This structure holds input BOPLine object and corresponding BOPLine objects & UI locations stored in the form
    attached to it. The type of BOPLine objects can be Mfg0BvrProcess, Mfg0BvrOperation, Mfg0BvrProcessArea, and
    Mfg0BvrWorkarea.
    
    :var contextLine: The input BOPLine object. The type of BOPLine objects can be Mfg0BvrOperation, Mfg0BvrProcess,
    Mfg0BvrProcessArea or Mfg0BvrWorkarea.
    :var externalNodesInfo: A list of BOPLine objects along with their UI location and corresponding BOPLine objects
    connected via scope flows relationship.
    """
    contextLine: BusinessObject = None
    externalNodesInfo: List[ExternalNodeInfo] = ()


@dataclass
class UILocationsInfoResponse(TcBaseObj):
    """
    This structure holds the BOPLine objects and UI locations of these BOPLine objects corresponding to the values of
    absolute occurrence and UI location property in Mfg0UILocationForm attached to the input context BOPLine objects
    along with service data which may contain following partial errors:
    251001 - An internal MFGBVR error has occurred. Please contact your system administrator.
    46110 - Unable to find Parent for 'Proc1'.
    
    
    :var uiLocationsInfo: A list of data containing input BOPLine objects and corresponding BOPLine objects & UI
    locations stored in the form attached to it. The type of BOPLine objects can be Mfg0BvrProcess, Mfg0BvrOperation,
    Mfg0BvrProcessArea, and Mfg0BvrWorkarea.
    :var serviceData: Standard service data.
    """
    uiLocationsInfo: List[UILocationInfo] = ()
    serviceData: ServiceData = None
