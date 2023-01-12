from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, POM_object
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MetaDataStampInputInfo(TcBaseObj):
    """
    This structure holds information about the objects to stamp along with the stamping context within which the
    stamped objects reside.
    
    :var metaStampInfoId: Client supplied unique identifier string that helps the client map the input to the
    MetaDataStampOutput.
    :var stampingContext: A stamping context BusinessObject within which the stamped objects reside.  The root line
    occurrence object of a structure, or an ItemRevision object that owns a DirectModel dataset are two examples of
    expected inputs for this argument, but intended to be general (could be any business object).
    :var stampedObjects: A list of any POM_objects on which the metadatastamp file is to be generated. POM_objects like
    Fnd0ModelViewProxy and Datasets like SnapshotViewData are two examples of expected input for this argument, but
    intended to be general ( could be any POM_object ).
    """
    metaStampInfoId: str = ''
    stampingContext: BusinessObject = None
    stampedObjects: List[StampedObjectInfo] = ()


@dataclass
class MetaDataStampOutput(TcBaseObj):
    """
    This structure contains the list of StampedObjectTicketInfo structures.
    
    :var stampObjectTickets: A list of StampedObjectTicketInfo structures.
    """
    stampObjectTickets: List[StampedObjectTicketInfo] = ()


@dataclass
class MetaDataStampOutputResponse(TcBaseObj):
    """
    This structure is used to return information from the getMetaDataStampWithContext operation. This structure holds
    information about serviceData and MetaDataStampOutputMap. The serviceData may contain information relevant to error
    messages, which are then associated to metaStampInfoId identifier and added to the error stack. The map,
    MetaDataStampOutputMap, contains information mapping the metaStampInfoId identifier to the MetaDataStampOutput
    struct, containing information about the tickets of the stamped object.
    
    :var metaDataStampOutputInfo: A map (string/MetaDataStampOutput) associating the unique metaStampInfoId identifier
    with the correct MetaDataStampOutput structure, containing tickets for the stamped objects for the given context
    object.
    :var serviceData: Any failure will be returned with error messages in the serviceData list of partial errors.
    """
    metaDataStampOutputInfo: MetaDataStampOutputMap = None
    serviceData: ServiceData = None


@dataclass
class StampedObjectInfo(TcBaseObj):
    """
    This structure holds information of the stamped object along with its unique identifier.
    
    :var uniqueStampObjectId: Client supplied unique identifier string that helps the client map the returned ticket to
    the stamped object.
    :var stampedObject: Any POM_object on which the metadatastamp file is to be generated. POM_objects like
    Fnd0ModelViewProxy and Datasets like SnapshotViewData are two examples of expected input for this argument, but
    intended to be general ( could be any POM_object ).
    """
    uniqueStampObjectId: str = ''
    stampedObject: POM_object = None


@dataclass
class StampedObjectTicketInfo(TcBaseObj):
    """
    This structure holds information of the ticket generated for the stamped object. Failures to get ticket for the
    stamped object maybe recorded as partial errors in the error stack and associated to uniqueStampObjectId identifier.
    
    :var uniqueStampObjectId: Client supplied unique identifier string that helps the client map the ticket to the
    stamped object.
    :var mdsFileTicket: The FMS transient read ticket generated for the stamped object. The file will be placed in the
    transient file volume and the caller will need to download it from there with the ticket sent by the service.
    """
    uniqueStampObjectId: str = ''
    mdsFileTicket: str = ''


"""
This structure maps the metaStampInfoId of the input to the MetaDataStampOutput structure.
"""
MetaDataStampOutputMap = Dict[str, MetaDataStampOutput]
