from __future__ import annotations

from tcsoa.gen.BusinessObjects import IncrementalChangeElement, MECfgLine, POM_object, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ICEAttributes(TcBaseObj):
    """
    The attibutes from a single IncrementaChangeElement structure
    
    :var attributeName: Attribute name.
    :var attributeValue: Attribute value.
    :var absOccRootLine: String representing the absolute occurrence root line (al_absocc_rootline_string)
    :var bomViewRevision: Related BOMView Revision from the absolute occurrence data.
    """
    attributeName: str = ''
    attributeValue: str = ''
    absOccRootLine: str = ''
    bomViewRevision: POM_object = None


@dataclass
class AttachmentChangeResponse(TcBaseObj):
    """
    A list of output for each passed in CfgAttachmentLine and the 'ServiceData'.
    
    
    :var response: A list of output for each passed in CfgAttachmentLine
    :var serviceData: Service data.
    """
    response: List[AttachmentInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AttachmentICEInfo(TcBaseObj):
    """
    Contains the attachment line, the absolute occurrence root line,  and the IncrementalChangeElement objects
    associated with it.
    
    :var line: The attachment line
    :var absOccRootLine: The absolute occurrence root line.
    :var childEditIces: A list of edit IncrementalChangeElement objects which includes the type of
    IncrementalChangeElement, incremental change revision, the IncrementalChangeElement and how it is configured.
    :var relationIces: A list of relation IncrementalChangeElement objects which includes the type of
    IncrementalChangeElement, incremental change revision, the IncrementalChangeElement and how it is configured.
    """
    line: MECfgLine = None
    absOccRootLine: str = ''
    childEditIces: List[BaseICEInfo] = ()
    relationIces: List[BaseICEInfo] = ()


@dataclass
class AttachmentInfo(TcBaseObj):
    """
    A list of 'AttachmentICEInfo' objects each of which contain the attachment line and the IncrementalChangeElement
    objects associated with it.
    
    :var listOfAttachments: A list of 'AttachmentICEInfo' objects each of which contain the attachment line and the
    IncrementalChangeElement objects associated with it.
    """
    listOfAttachments: List[AttachmentICEInfo] = ()


@dataclass
class AttributeChangeResponse(TcBaseObj):
    """
    The response from the 'getAttributeChanges' SOA function
    
    :var response: A list of attribute outputs for the passed in BOMLine objects.
    :var serviceData: The SOA Service data.  Any error will be populated here.
    """
    response: List[AttributeInfoOutput] = ()
    serviceData: ServiceData = None


@dataclass
class AttributeICEInfo(TcBaseObj):
    """
    Structure passed back from the 'getAttributeChanges' SOA call
    
    :var baseICEInfo: Basic IncrementalChangeElement object information for all IncrementalChangeElement object types.
    :var attributes: Attribute information for this IncrementalChangeElement object.
    """
    baseICEInfo: BaseICEInfo = None
    attributes: ICEAttributes = None


@dataclass
class AttributeInfoOutput(TcBaseObj):
    """
    The output from the 'getAttributeChanges' SOA function.
    
    :var attributeInfo: The acutal attribute information
    """
    attributeInfo: List[AttributeICEInfo] = ()


@dataclass
class ParentAndChildComponentsResponse(TcBaseObj):
    """
    Response from the 'getParentAndChildComponents' SOA API call
    
    :var parentAndChildInfoResponse: The output response for the 'getParentAndChildComponents' call.
    :var serviceData: The service data.
    """
    parentAndChildInfoResponse: ParentAndChildInfos = None
    serviceData: ServiceData = None


@dataclass
class ParentAndChildInfos(TcBaseObj):
    """
    The output of the 'getParentAndChildComponents' SOA API call
    
    :var parentChildInfos: A list of 'ParentInfo' structures describing the parent and child components of the passed
    in IncrementalChangeElement objects.
    """
    parentChildInfos: List[ParentChildInfo] = ()


@dataclass
class ParentChildInfo(TcBaseObj):
    """
    Parent and child information for the given IncrementalChangeElement.
    
    :var context: The context
    :var parent: The parent component object.
    :var child: The child component object.
    :var ice: The IncrementalChangeElement object for the given parent and child components.
    """
    context: str = ''
    parent: POM_object = None
    child: POM_object = None
    ice: IncrementalChangeElement = None


@dataclass
class PredecessorChangeInfo(TcBaseObj):
    """
    The output that comes from the 'getPredecessorChanges' SOA function
    
    :var baseICEInfo: Basic information for IncrementalChangeElement objects.
    :var listOfPredecessors: List of predecessor information.
    """
    baseICEInfo: List[BaseICEInfo] = ()
    listOfPredecessors: List[PredecessorICEInfo] = ()


@dataclass
class PredecessorChangeResponse(TcBaseObj):
    """
    The response to the 'getPredecessorChanges' SOA function
    
    :var serviceData: The service data
    :var response: List of predecessor information with the IncrementalChangeElement objects for each.
    """
    serviceData: ServiceData = None
    response: List[PredecessorChangeInfo] = ()


@dataclass
class PredecessorICEInfo(TcBaseObj):
    """
    The predecessors to the given IncrementalChangeElement object.
    
    :var predecessorName: Name of the predecessor.
    :var sequenceNumber: The sequence numbert for this predecessor.
    """
    predecessorName: str = ''
    sequenceNumber: str = ''


@dataclass
class BaseICEInfo(TcBaseObj):
    """
    Basic ICE information
    
    :var typeOfIce: 'Add', 'Delete'  
    'Add' means that a BOMLine has been added to the structure in the context of the incremental change.  'Delete'
    means that a BOMLine has been removed from the structure in the context of the incremental change.
    
    :var howConfigured: If the value of "ic_not_configure" is an empty string, it means that the incremental change is
    not configured therefore it will not show in the structure.
    :var icRev: A single incremental change item revision.
    :var ice: IncrementalChangeElement object
    """
    typeOfIce: int = 0
    howConfigured: str = ''
    icRev: ItemRevision = None
    ice: IncrementalChangeElement = None


@dataclass
class StructureChangeResponse(TcBaseObj):
    """
    A list of outputs per IncrementalChangeElement and the 'serviceDate' structure that consists of the incremental
    change revision and the IncrementalChangeElement object.
    
    
    :var response: A list of outputs per IncrementalChangeElement
    :var serviceData: The SOA service data structure
    It consists of the incremental change revision and the IncrementalChangeElement object.
    """
    response: List[StructureChangesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class StructureChangesOutput(TcBaseObj):
    """
    A list of 'BaseICEInfo' structures that contains any structure changes.
    
    :var baseInfo: A list of 'BaseICEInfo' structures that contains any structure changes.
    """
    baseInfo: List[BaseICEInfo] = ()
