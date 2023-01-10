from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, RevisionRule, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ItemElementLineInfo(TcBaseObj):
    """
    This contains Item element Input structure for addOrUpdateChildrenToParentLine operation.
    
    :var clientId: Identifier that helps the client to track the object created. This is an optional parameter.
    :var itemElement: Refers to the Item element object.
    :var occType: The occurrence type used for the child BOMLine creation objects.
    :var itemElementline: Refers to BOMLine object which represents itemElement for modification of properties (Used in
    case of update).
    :var itemElementLineProperties: Refers to the 'BomLineProperties' struct.
    """
    clientId: str = ''
    itemElement: BusinessObject = None
    occType: str = ''
    itemElementline: BOMLine = None
    itemElementLineProperties: BomLineProperties = None


@dataclass
class ItemLineInfo(TcBaseObj):
    """
    Refers to Item input structure for addOrUpdateChildrenToParentLine operation.
    
    :var clientId: Identifier that helps the client to track the object created. This is an optional parameter.
    :var item: Refers to Item object.(used in case of precise structure)
    :var itemRev: Refers to the ItemRevision object (used in case of imprecise structure)
    :var occType: Refers to occurrence type used for the child BOMLine (occurrence) creation.
    :var bomline: Refers to BOMLine for modification of its properties (Used in case of update when clientId is empty).
    :var itemLineProperties: Refers 'BomLineProperties'  struct which represents to property name/value pairs for
    additional properties.
    """
    clientId: str = ''
    item: BusinessObject = None
    itemRev: BusinessObject = None
    occType: str = ''
    bomline: BOMLine = None
    itemLineProperties: BomLineProperties = None


@dataclass
class BOMLinesOutput(TcBaseObj):
    """
    This represents output structure for addOrUpdateChildrenToParentLine operation.
    
    :var clientId: Identifier that helps the client to track the object created.
    :var bomline: The refers to BOMLine object.
    """
    clientId: str = ''
    bomline: BOMLine = None


@dataclass
class RemoveChildrenFromParentLineResponse(TcBaseObj):
    """
    Return structure for removeChildrenFromParentLine operation
    
    :var serviceData: The ServiceData structure is used to return the updated parent BOMLine business objects whose
    children have been removed and can contain partial errors if the operations fails to create bom window. It also
    holds services exceptions.
    """
    serviceData: ServiceData = None


@dataclass
class BaselineInput(TcBaseObj):
    """
    Input structure that holds information to create a new Baseline ItemRevision
    
    :var dryrun: To be set as 'true' if dryrun is to be performed, false if not. This is an optional element and the
    default value is false. Dry run option helps users to know of any possible errors without performing the actual
    baseline action. Choosing this option generates a report and can be accessed from the 'BaselineResponse'.
    :var clientID:  Identifier that helps the client to track the object(s) created
    :var itemRev: Input ItemRevision object, that is to be baselined
    :var viewType: View type name. To be provided if input ItemRevision has BOMViewRevision
    :var revRule: RevisionRule object. To be provided if input ItemRevision has BOMViewRevision.
    :var precise: Creates a precise baseline if set to true. If set to false, creates an imprecise baseline. Default
    value is false.
    :var releaseProcess: Name of the workflow process template to be used for baselining.
    :var description: Description for baseline ItemRevision, optional
    :var baselineJobName: Name to identify the job initiated during baseline. Operation will fail if a job name is not
    provided. In general job name is a combination of ItemId, Revision Id and ItemRevision Name property values.
    :var baselineJobDescription: Description for baseline job, optional
    """
    dryrun: bool = False
    clientID: str = ''
    itemRev: ItemRevision = None
    viewType: str = ''
    revRule: RevisionRule = None
    precise: bool = False
    releaseProcess: str = ''
    description: str = ''
    baselineJobName: str = ''
    baselineJobDescription: str = ''


@dataclass
class BaselineOutput(TcBaseObj):
    """
    Refers to the output structure for baseline create operation.
    
    :var dryrun: BaselineOutput structure contains following elements
    dryrun - Dry run indicates that the operation will not create a baseline but it will only do the required
    validation. Boolean variable indicating if dry option was used.
    
    :var clientID: Client Identifier
    :var baselineItemRev: Created baseline ItemRevision object.
    :var dryrunLogTicket: FMS ticket for dryrun log. Contains path to dry run report if dryrun flag is set to true.
    """
    dryrun: bool = False
    clientID: str = ''
    baselineItemRev: ItemRevision = None
    dryrunLogTicket: str = ''


@dataclass
class BaselineResponse(TcBaseObj):
    """
    Output structure containing list of 'BaselineOutput' structures and 'ServiceData' with list of errors encountered
    during the Operation
    
    :var output: List of 'BaselineOutput' structures
    :var serviceData: structure containing error codes and messages
    """
    output: List[BaselineOutput] = ()
    serviceData: ServiceData = None


@dataclass
class AddOrUpdateChildrenToParentLineInfo(TcBaseObj):
    """
    Input structure for addOrUpdateChildrenToParentLine operation
    
    :var parentLine: Parent BOMLine business object under which item or item element occurrences are added or modified.
    :var viewType: View Type string used for creating BOMView for parent BOMLine if it does not exist (NULL implies use
    default view type).
    :var items: Array of ItemLineInfo input structure.
    :var itemElements: Array of ItemElementLineInfo input structure
    """
    parentLine: BOMLine = None
    viewType: str = ''
    items: List[ItemLineInfo] = ()
    itemElements: List[ItemElementLineInfo] = ()


@dataclass
class AddOrUpdateChildrenToParentLineResponse(TcBaseObj):
    """
    Return structure for addOrUpdateChildrenToParentLine operation
    
    :var itemLines: Array of Output itemLines
    :var itemelementLines: Array of Output itemElementLines
    :var serviceData: This is a common data strucuture used to return sets of
    Teamcenter Data Model object from a service request. This also
    holds services exceptions.
    """
    itemLines: List[BOMLinesOutput] = ()
    itemelementLines: List[BOMLinesOutput] = ()
    serviceData: ServiceData = None


"""
Refers to a map of BOMLine object property as key and BOMLine object property value as value pair.
"""
BomLineProperties = Dict[str, str]
