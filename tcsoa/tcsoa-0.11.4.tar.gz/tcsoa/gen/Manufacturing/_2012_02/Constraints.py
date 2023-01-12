from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetPrecedenceConstraintPathsInputs(TcBaseObj):
    """
    Input structure for the getPrecedenceConstraintPaths operation.
    
    :var startNode: The process/operation line at the start of the precedence chain.
    This member can hold BOs of type Mfg0BvrProcess and Mfg0BvrOperation.
    :var endNode: The operation/process line at the end of the precedence chain
    This member can hold BOs of type Mfg0BvrProcess and Mfg0BvrOperation.
    """
    startNode: BusinessObject = None
    endNode: BusinessObject = None


@dataclass
class GetPrecedenceConstraintPathsResponse(TcBaseObj):
    """
    Response structure for the getPrecedenceConstraintPaths operation.
    
    :var results: A list of result structures that contain the paths for each start and end node pair specfied in the
    input structures.
    :var serviceData: The ServiceData object for the matching GetPrecedenceConstraintPathsInputs structure.
    """
    results: List[GetPrecedenceConstraintPathsResult] = ()
    serviceData: ServiceData = None


@dataclass
class GetPrecedenceConstraintPathsResult(TcBaseObj):
    """
    The result structure for the getPrecedenceConstraintPaths operation.
    
    :var paths: The list of paths that connect the respective start and end node.
    """
    paths: List[PrecedenceConstraintPath] = ()


@dataclass
class GetPrecedenceConstraintsIn(TcBaseObj):
    """
    The input structure for the getPrecedenceConstraints service operation
    
    :var predecessorLevel: The integer indicating the number of predecessor levels to be processed in the precedence
    chain
    :var successorLevel: The integer indicating the number of successor levels to be processed in the precedence chain
    :var inputObject: The input object (Mfg0BvrProcess / Mfg0BvrOperation)
    """
    predecessorLevel: int = 0
    successorLevel: int = 0
    inputObject: BusinessObject = None


@dataclass
class GetPrecedenceConstraintsResponse(TcBaseObj):
    """
    The response structure of the getPrecedenceConstraints service operation. Contains the predecessor and successor
    maps.
    
    :var predecessorMap: The map of objects to their predecessors
    :var successorMap: The map of objects to their successors
    :var serviceData: The ServiceData structure
    """
    predecessorMap: AdjacentObjectsMap = None
    successorMap: AdjacentObjectsMap = None
    serviceData: ServiceData = None


@dataclass
class PrecedenceConstraintPath(TcBaseObj):
    """
    Defines a specific path for the GetPrecedenceConstraintPaths API
    
    :var components: A list of structures that hold the nodes and constraints that make up the path to the end node.
    :var endNode: The end node itself. The Business Object  is of type Mfg0BvrProcess or Mfg0BvrOperation.
    """
    components: List[PrecedenceConstraintPathComponent] = ()
    endNode: BusinessObject = None


@dataclass
class PrecedenceConstraintPathComponent(TcBaseObj):
    """
    A component of a constraint path for structure PrecedenceConstraintPath
    
    :var predecessor: A node which is part of the path (type Mfg0BvrProcess or Mfg0BvrOperation).
    :var constraint: The constraint that connects the node of this component structure to the next, or, in case this is
    the last component in the path, to the end node. Note that the predecessor of the constraint is different from the
    predecessor member in case the constraint is inherited.The same applies to the successor of the constraint: it does
    not necessarily have to be the successor in the path. This member is of type Mfg0BvrPrecedenceConstraint.
    :var constraintIsInherited: Indicates whether the constraint is directly connected to the predecessor and successor
    nodes in the path or whether it has been inherited from a parent node:
    """
    predecessor: BusinessObject = None
    constraint: BusinessObject = None
    constraintIsInherited: bool = False


@dataclass
class ValidateConstraintConsistencyError(TcBaseObj):
    """
    Describes a problem detected by the validateConstraintConsistency operation.
    
    :var constraintType: The type of the constraint that is violated. This is the ImanType of the runtime constraint
    object, for example Mfg0BvrPrecedenceConstraint for precedence constraints.
    :var message: A localized message explaining the detected inconsistency.
    :var objects: The list of operations/processes that participate in the constraints that are inconsistent. The list
    contains business objects of type Mfg0BvrOperation and Mfg0BvrProcess.
    :var constraints: The constraint objects which are inconsistent.These objects are of type Mfg0BvrConstraint.
    """
    constraintType: BusinessObject = None
    message: str = ''
    objects: List[BusinessObject] = ()
    constraints: List[BusinessObject] = ()


@dataclass
class ValidateConstraintConsistencyInputs(TcBaseObj):
    """
    Input structure for the validateConstraintConsistency operation.
    
    :var constraintTypes: The constraint types to check. Each entry in this vector is of type ImanType; it corresponds
    to the type of the runtime object for the constraint (e.g. Mfg0BvrPrecedenceConstraint for precedence constraints
    or Mfg0BvrPrecedenceConstraint for group constraints; customer defined derived types are accepted as well). If the
    vector is empty, all constraints are checked.
    :var rootNodes: The list of BOMLines from the BOP window that define the root nodes of the sub structures to check.
     The objects must be of type Mfg0BvrProcess or Mfg0BvrOperation. All lines must be associated with the same window.
    """
    constraintTypes: List[BusinessObject] = ()
    rootNodes: List[BusinessObject] = ()


@dataclass
class ValidateConstraintConsistencyResponse(TcBaseObj):
    """
    Response structure of the validateConstraintConsistencyResponse operation.
    
    :var results: The list of result structures that holds one entry for each input structure.
    :var serviceData: The ServiceData object for this request.
    """
    results: List[ValidateConstraintConsistencyResult] = ()
    serviceData: ServiceData = None


@dataclass
class ValidateConstraintConsistencyResult(TcBaseObj):
    """
    Result structure for the validateConstraintConsistency operation.
    
    :var errors: The  list of validation errors, if any.
    """
    errors: List[ValidateConstraintConsistencyError] = ()


@dataclass
class ValidateProcessAreaAssignmentsError(TcBaseObj):
    """
    A structure that contains information about an problem detected in the ValidateProcessAreaAssignments operation.
    In the case of a precedence constraint violation, the objectsOfContextOfConstraint vector will contain the
    predecessor and the sucessor operation or process whose order is conflicting with the order of the process areas
    they are assigned to, if a Product BOP is given. The objectsOfContextToValidate member will contain their
    respective counterparts in the Plant BOP, and processAreas will contain the associated process areas. In case of a
    precedence constraint violations the constraints vector will be empty, since the constraints themselves are
    meaningless without the intermittent operations/processes. In order to obtain the paths of processes/operations and
    constraints that define the precedence of the start and end node, the GetPrecedenceConstraintPathsAPI may be used.
    Currently one possible type of error may arise when precedence constraints are violated. The format of the error
    message is similar to the following:
    <Node A> is assigned to <Process Area X> while its successor <Node B> is assigned to <Process Area Y>  which is a
    predecessor of  <Process Area X>.
    
    :var constraintType: The type of the constraint that is violated. Corresponds to the ImanType of the constraint
    object. See also the constraintTypes member of struct ValidateProcessAreaAssignmentsInputs.
    :var message: A localized message explaining the validation error.
    :var objectsOfContextOfConstraint: The list of operations and/or processes that violate the constraints. These
    objects belong to the contexts passed via the contextOfConstraints parameter i.e. the Product BOPs. The vector will
    be empty if the contextOfConstraints vector is empty. The list contains business objects of type Mfg0BvrOperation
    and Mfg0BvrProcess.
    :var objectsOfContextToValidate: The list of assigned nodes from the contextToValidate parameter. In case only a
    single Product BOP exists, the vector will hold the same number of objects as the objectsOfContextOfConstraint
    member. The business objects are of type Mfg0BvrOperation and Mfg0BvrProcess.
    :var processAreas: The list of process areas associated with the Product BOP objects. The objects are of type
    Mfg0BvrProcessArea and belong to the context passed in contextToValidate.
    :var constraints: The constraint objects which are violated. These objects are of type Mfg0BvrConstraint. Note that
    depending on the type of violation the constraints list may be empty. This is the case for example for precedence
    constraints.
    """
    constraintType: BusinessObject = None
    message: str = ''
    objectsOfContextOfConstraint: List[BusinessObject] = ()
    objectsOfContextToValidate: List[BusinessObject] = ()
    processAreas: List[BusinessObject] = ()
    constraints: List[BusinessObject] = ()


@dataclass
class ValidateProcessAreaAssignmentsInputs(TcBaseObj):
    """
    Input structure for the validateProcessAreaAssignments operation.
    
    :var constraintTypes: The constraint types to check. Each entry in this vector is of type ImanType; it corresponds
    to the type of the runtime object for the constraint (e.g. Mfg0BvrPrecedenceConstraint for precedence constraints
    or Mfg0BvrGroupConstraint for group constraints). The types vector may also contain customized types derived from
    the base constraint types. If the vector is empty, all constraints are checked.
    :var contextToValidate: The context of the process area structure. This is the top line of the window that holds
    the Plant BOP structure (the object is of type Mfg0BvrPlantBOP).
    :var contextOfConstraints: A list of contexts that describes the processes and operations whose assignments are to
    be validated. If empty it is assumed that the context of the process area structure is to be used. Currently only
    one single is accepted that represents the topline of the Product BOP structure (this object must be of type
    Mfg0BvrProductBOP).
    :var rootProcessAreas: The list of BOMLines from the Plant BOP window that define the substructure whose
    allocations are examined If the list is empty, the whole Plant BOP loaded into the Plant BOP window will be
    checked. The Business Objects are of type Mfg0BvrProcessArea.
    :var maxErrors: The maximum number of errors to return. Can be set to 0 in order not to impose any limit. Otherwise
    the value must be greater than 0.
    """
    constraintTypes: List[BusinessObject] = ()
    contextToValidate: BusinessObject = None
    contextOfConstraints: List[BusinessObject] = ()
    rootProcessAreas: List[BusinessObject] = ()
    maxErrors: int = 0


@dataclass
class ValidateProcessAreaAssignmentsResponse(TcBaseObj):
    """
    Response structure for the validateProcessAreaAssignments operation.
    
    :var results: The list of result structures that holds one entry for each input structure.
    :var serviceData: The ServiceData object for this request.
    """
    results: List[ValidateProcessAreaAssignmentsResult] = ()
    serviceData: ServiceData = None


@dataclass
class ValidateProcessAreaAssignmentsResult(TcBaseObj):
    """
    Result structure for the validateProcessAreaAssignments operation.
    
    :var errors: The  list of validation errors, if any.
    """
    errors: List[ValidateProcessAreaAssignmentsError] = ()


@dataclass
class AdjacentObjectInfo(TcBaseObj):
    """
    The structure representing an adjacent object (either the predecessor or the successor) along with the constraint
    object
    
    :var constraintObject: The constraint object (Mfg0BvrPrecedenceConstraint)
    :var adjacentObject: The preceding or succeeding object (Mfg0BvrProcess / Mfg0BvrOperation)
    """
    constraintObject: BusinessObject = None
    adjacentObject: BusinessObject = None


"""
The map containing a BusinessObject as key and its list of adjacent objects (predecessor/successor) as the value
"""
AdjacentObjectsMap = Dict[BusinessObject, List[AdjacentObjectInfo]]
