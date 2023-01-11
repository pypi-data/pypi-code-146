from __future__ import annotations

from tcsoa.gen.BusinessObjects import Item, PSBOMViewRevision, PSViewType, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAllAvailableViewTypesInput(TcBaseObj):
    """
    The 'GetAllAvailableViewTypesInput' denotes input structure for getting available PSBOMView types.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var itemRevisionObj: Refers to ItemRevision object on which we find the available PSBOMView Types.
    :var itemObject: Refers to the Item object of itemRevisionObj.
    """
    clientId: str = ''
    itemRevisionObj: ItemRevision = None
    itemObject: Item = None


@dataclass
class GetAvailableViewTypesOutput(TcBaseObj):
    """
    This contains 'GetAvailableViewTypesOutput' struct which has a list of available PSBOMView types on given
    ItemRevision object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var viewTags: Refers to a list of PSBOMView types available for given ItemRevision object.
    """
    clientId: str = ''
    viewTags: List[PSViewType] = ()


@dataclass
class GetAvailableViewTypesResponse(TcBaseObj):
    """
    This contains 'GetAvailableViewTypesResponse' object which refers to the available PSBOMView types on given
    ItemRevision object.
    
    :var serviceData: SOA Framework class that holds model objects and partial errors.
    :var viewTypesOutputs: Refers to a list of 'GetAvailableViewTypesOutput' output structure, and has a list of
    PSBOMView types for given ItemRevision object.
    """
    serviceData: ServiceData = None
    viewTypesOutputs: List[GetAvailableViewTypesOutput] = ()


@dataclass
class CreateOrSaveAsPSBOMViewRevisionInput(TcBaseObj):
    """
    This contains inputs related to Item object and ItemRevision object on which we need to create the
    PSBOMViewRevision object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var itemObject: Item object associated with PSBOMViewRevision object. It is mandatory in case of create and Save
    As scenario.
    :var itemRevObj: Refers to ItemRevision object associated with PSBOMViewRrevision object. It is mandatory in Save
    As operation and optional in case of Create operation. In case of create if this do not present, then the latest
    ItemRevision of itemObject will be used.
    :var viewTypeTag: Refers to PSViewType object in case of save as operation.
    :var srcBvrTag: Refers to source PSBOMViewRevision object. If srcBvrTag is null object then Create operation will
    be performed. If srcBvrTag is not null object, it will be used for Save As operation.
    In case of Save As scenario if srcBvrTag object's PSBOMView and viewTypeTag are same then the new PSBOMViewRevision
    object created as revise operation on given Item object and ItemRevision object. If they are different then the new
    PSBOMViewRevision object created as copy operation on given itemObject and itemRevObj
    
    :var isPrecise: This indicates that PSBOMViewRevision to be created as precise or not in case of creating new
    PSBOMViewRevision for Create Operation. This parameter is not used in the Save As operation.
    """
    clientId: str = ''
    itemObject: Item = None
    itemRevObj: ItemRevision = None
    viewTypeTag: PSViewType = None
    srcBvrTag: PSBOMViewRevision = None
    isPrecise: bool = False


@dataclass
class CreateOrSaveAsPSBOMViewRevisionOutput(TcBaseObj):
    """
    The 'CreateOrSaveAsPSBOMViewRevisionOutput' is output data structure and it contains newly created
    PSBOMViewRevision object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var bvrTag: This has PSBOMViewRevision object created as a result of create or save as action.
    """
    clientId: str = ''
    bvrTag: PSBOMViewRevision = None


@dataclass
class CreateOrSaveAsPSBOMViewRevisionResponse(TcBaseObj):
    """
    The 'CreateOrSaveAsPSBOMViewRevisionResponse' is response structure for create or save as action for
    PSBOMViewRevision object.
    
    :var serviceData: SOA Framework class that holds model objects and partial errors.
    :var psBVROutputs: This has list of 'CreateOrSaveAsPSBOMViewRevisionOutput' struct output data which contains the
    newly created PSBOMViewRevision object.
    """
    serviceData: ServiceData = None
    psBVROutputs: List[CreateOrSaveAsPSBOMViewRevisionOutput] = ()
