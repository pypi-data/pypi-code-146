from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0ModelViewProxy
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindModelViewsInStructureResponse(TcBaseObj):
    """
    The response contains any found model view proxies ( FndModelViewProxy) and the structure location at which they
    were found. Also, if the "compareWithMVList" option is set to true, then an additional list of model view proxies
    that are currently disclosed but appear to no longer be relevant is returned.
    Any errors are returned in the 'serviceData'.
    
    :var modelViewsByStructureNodes: A list of proxy objects found for various nodes in the structure - the structure
    nodes may be bomlines, item revisions or design elements depending on the type of structure starting scope and
    disclosure type.
    :var unfoundFromModelViewList: The model view proxy objects (Fnd0ModelViewProxy) that are currently associated to
    the specified disclosure but are not found in the given 'startingScope'. Note that if the 'startingScope' is not
    the disclosure, that the missing proxy objects may still be present in a disclosure elsewhere in its structure.
    This list is only populated if the compareWithMVList option is set to true.
    :var possibleMatching: Map (Fnd0ModelViewProxy, Fnd0ModelViewProxy) of possible matching proxies that are
    equivalent. The keys are proxies in an associated MVList (associated to the input structure object or disclosure)
    that are no longer precisely in the structure with the given configuration. The values are the system suggested new
    proxies that are equivalent. This map is only populated if compareWithMVList option is set to true.
    :var serviceData: Contains a list of any errors which occurred during the operation.
    """
    modelViewsByStructureNodes: List[StructureNodeResults] = ()
    unfoundFromModelViewList: List[Fnd0ModelViewProxy] = ()
    possibleMatching: BoToBoMap = None
    serviceData: ServiceData = None


@dataclass
class StructureNodeResults(TcBaseObj):
    """
    Identifies a list (containing at least one) of model view proxies (Fnd0ModelViewProxy) that were found for a
    particular structure node. Assisting context information ('csIdContextOccurrence') may be provided to help locate
    the structure node.
    
    :var structureNode: A node of the structure for which model views have been found. The structure node could either
    be a BOMLine or for some cases of Workset structure, a model element (Mdl0ModelElement).
    :var resultingViews: List of model view proxies (Fnd0ModelViewProxy) found for the particular structure node.
    :var csIdContextOccurrence: Contains either the subset in which the structure node resides (either Cpd0SubsetLine
    or Cpd0DesignSubsetElement.) or the 'startingScope' ItemRevision or BOMLine if multiple 'startingScope' values were
    provided. This object gives context to the associated 'clonestableIdChain' value(s).
    :var clonestableId: A list of one or more clone stable occurrence id values used to help locate the 'structureNode'
    within the 'csIdContextoccurrence'. The clone stable occurrence id values are may be ordered from a given
    'startingScope' - which is repeated in the 'StructureNodeResults' as the 'csIdContextOccurrence'. 
    
    Alternatively, if a Workset is given as a 'startingScope', the 'csIdContextOccurrence' may be a subset in the
    Workset, and only a single cs_id value for the 'structureNode' would be needed since a given model element
    (Mdl0ModelElement) in a subset (Cpd0DesignSubsetElement) can be identified by such a single clone stable id.
    
    Also, if the 'resultingViews' are found directly off a 'startingScope', then the 'csIdContextOccurrence' and
    'structureNode' will both be the 'startingScope' and the 'clonestableIdChain' will be empty as no expansion was
    used to find the resultingViews.
    """
    structureNode: BusinessObject = None
    resultingViews: List[BusinessObject] = ()
    csIdContextOccurrence: BusinessObject = None
    clonestableId: List[str] = ()


"""
Generic map of one business object to another.
"""
BoToBoMap = Dict[BusinessObject, BusinessObject]


"""
Generic map of boolean names to values (string, bool). Commonly used to contain selected options from a client.
"""
BoolMap = Dict[str, bool]
