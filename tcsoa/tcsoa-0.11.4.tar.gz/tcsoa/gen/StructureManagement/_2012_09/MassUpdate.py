from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0MarkupChange, Fnd0Markup, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MassUpdateAffectedInput(TcBaseObj):
    """
    This structure provides a set of input values for the massGetAffectedParents operation.
    
    :var target: Item Revision to base the where used search on.
    :var change: The change item revision object to record mass update results in.
    :var operation: Operation type used to help identify type of filtering to use when searching for impacted parent
    parts.
    """
    target: ItemRevision = None
    change: ItemRevision = None
    operation: int = 0


@dataclass
class MassUpdateAffectedOutput(TcBaseObj):
    """
    This structure provides a set of output values for the massGetAfectedParents operation.
    
    :var parent: This is the impacted parent part that references the target part.
    :var selectable: This indicates if the impacted parent part is selectable for mass update or not.
    :var selectableComment: This text informs why the impacted parent part is not selectable.
    """
    parent: ItemRevision = None
    selectable: bool = False
    selectableComment: str = ''


@dataclass
class MassUpdateAffectedResponse(TcBaseObj):
    """
    This structure contains all the results from the massGetAffectedParents operation.
    
    :var massUpdateAffectedOutputs: This is a vector of MassUpdateAffectedOutput structures.
    :var serviceData: Standard service data to handle partial errors.
    """
    massUpdateAffectedOutputs: List[MassUpdateAffectedOutput] = ()
    serviceData: ServiceData = None


@dataclass
class MassUpdateExecuteECNoutput(TcBaseObj):
    """
    This structure provides a set of output values for the massUpdateExecutionECN operation.
    
    :var changeItemRev: Change item revision used for mass update execution on the ECN change management process.
    :var markup: Markup on ChangeItemRev that was processed during the ECN CM process.
    :var markupChanges: This is a vector of markup changes that was processed during the ECN CM process.
    """
    changeItemRev: ItemRevision = None
    markup: Fnd0Markup = None
    markupChanges: List[Fnd0MarkupChange] = ()


@dataclass
class MassUpdateExecuteECNresponse(TcBaseObj):
    """
    This structure provides output for the massUpdateExecutionECN operation.
    
    :var outputs: This is a vector of MassUpdateExecuteECNoutput structures.
    :var serviceData: Standard service data for partial errors.
    """
    outputs: List[MassUpdateExecuteECNoutput] = ()
    serviceData: ServiceData = None


@dataclass
class MassUpdateExecuteECRinput(TcBaseObj):
    """
    This structure provides a set of input values for the massUpdateExecutionECR operation.
    
    :var executionMode: This defines the ECR execution being performed 1=one time execute, 2=save as markup and
    3=remove markup.
    :var operation: The mass update operation type being executed.
    :var target: Part that is being replaced or removed.
    :var addToProblem: Add the target part to the problem folder.
    :var addToSolution: Add the newItem to solution folder.
    :var newItem: The part that is doing the replacing or being added.
    :var change: The change item revision object to record mass update results in.
    :var markupChange: The markup change to remove from the markup and the change item revision object impacted folder.
    :var parents: A vector of impacted parent parts that reference the target part.
    :var sParents: A vector of bools that indicate if the impacted parent parts are selectable or not for mass update.
    """
    executionMode: int = 0
    operation: int = 0
    target: ItemRevision = None
    addToProblem: bool = False
    addToSolution: bool = False
    newItem: ItemRevision = None
    change: ItemRevision = None
    markupChange: Fnd0MarkupChange = None
    parents: List[ItemRevision] = ()
    sParents: List[bool] = ()


@dataclass
class MassUpdateExecuteECRoutput(TcBaseObj):
    """
    This structure provides a set of output values for the massUpdateExecutionECR operation.
    
    :var parent: The impacted parent part that references the target part.
    :var status: This indicates if the impacted parent part was successful or not during the massUpdateExecutionECR
    operation.
    :var statusComment: Detailed status text on why the impacted parent part succeded or failed to process correctly.
    """
    parent: ItemRevision = None
    status: int = 0
    statusComment: str = ''


@dataclass
class MassUpdateExecuteECRresponse(TcBaseObj):
    """
    This structure provides output for the massUpdateExecutionECR operation.
    
    :var outputs: This is a vector of MassUpdateExecuteECRoutput structures.
    :var serviceData: Standard service data for partial errors.
    """
    outputs: List[MassUpdateExecuteECRoutput] = ()
    serviceData: ServiceData = None
